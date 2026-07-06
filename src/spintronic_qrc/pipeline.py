"""
pipeline.py
-----------
End-to-end quantum reservoir computing loop for the disordered XXZ spin chain.

Pipeline (Fujii & Nakajima 2017)
--------------------------------
    u(t)  -->  encode  -->  evolve under H for time tau  -->  Pauli readout  -->  row of X

The reservoir state is carried forward across timesteps: each step encodes the
new input, evolves under the fixed Hamiltonian, and measures Pauli expectations.
Only the classical Ridge readout is trained (see ``trainer``).

State carry-forward uses explicit statevector handoff between timesteps
(``StatePrep`` + ``qml.state()``; approach B in the design notes).

References
----------
- Fujii & Nakajima (2017) Phys. Rev. Applied 8, 024030
- Dambre et al. (2012) IEEE TNN 24, 687
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pennylane as qp

from spintronic_qrc.encoder import encode_global_rotation, encode_local_field
from spintronic_qrc.readout import feature_dim, readout_observables
from spintronic_qrc.reservoir import (
    DISORDER_W_DEFAULT,
    J_XY_DEFAULT,
    J_Z_DEFAULT,
    reservoir_device,
    xxz_chain_hamiltonian,
)
from spintronic_qrc.trainer import TrainResult, predict, train_ridge


@dataclass(frozen=True)
class QRCConfig:
    """
    Configuration for the spin-chain QRC pipeline.

    Parameters
    ----------
    n_sites : int
        Number of spin-1/2 sites (qubits) on the open chain.
    evolution_time : float
        Duration ``tau`` passed to ``ApproxTimeEvolution`` per timestep.
    n_trotter_steps : int
        Trotter slices for ``ApproxTimeEvolution(H, tau, n_trotter_steps)``.
    J_xy, J_z, disorder, seed
        XXZ exchange couplings and on-site disorder (see ``reservoir``).
    encoding : {"local", "global"}
        ``"local"`` applies ``RZ`` on ``encoding_site``; ``"global"`` applies
        ``RX`` on all sites.
    encoding_site : int
        Target site for local encoding (default 0).
    readout_paulis, readout_sites
        Pauli axes and sites measured after each evolution step.
    washout : int
        Discard the first ``washout`` timesteps before collecting features.
    input_scale : float
        Rotation amplitude passed to the encoder (radians at ``u=1``).
    """

    n_sites: int
    evolution_time: float = 1.0
    n_trotter_steps: int = 10
    J_xy: float = J_XY_DEFAULT
    J_z: float = J_Z_DEFAULT
    disorder: float = DISORDER_W_DEFAULT
    seed: int | None = 42
    encoding: Literal["local", "global"] = "local"
    encoding_site: int = 0
    readout_paulis: tuple[str, ...] = ("X", "Y", "Z")
    readout_sites: list[int] | None = None
    washout: int = 10
    input_scale: float = np.pi / 2


@dataclass
class QRCResult:
    """End-to-end QRC run: features, fitted readout, and hold-out metrics."""

    X: np.ndarray
    y: np.ndarray
    train_result: TrainResult
    train_rmse: float
    test_rmse: float
    predictions: np.ndarray
    config: QRCConfig


def _validate_config(config: QRCConfig) -> None:
    if config.n_sites < 2:
        raise ValueError("n_sites must be >= 2 for a chain reservoir")
    if config.n_trotter_steps < 1:
        raise ValueError("n_trotter_steps must be >= 1")
    if config.evolution_time <= 0:
        raise ValueError("evolution_time must be > 0")
    if config.washout < 0:
        raise ValueError("washout must be >= 0")
    if config.encoding not in ("local", "global"):
        raise ValueError(f"Unknown encoding mode: {config.encoding!r}")
    if not 0 <= config.encoding_site < config.n_sites:
        raise ValueError(
            f"encoding_site must be in [0, {config.n_sites}), "
            f"got {config.encoding_site}"
        )


def _initial_state(n_sites: int) -> np.ndarray:
    """Return the |0...0> statevector as a complex numpy array."""
    state = np.zeros(2**n_sites, dtype=np.complex128)
    state[0] = 1.0
    return state


def _build_step_qnode(config: QRCConfig):
    """Return a QNode for one encode → evolve → measure timestep with state carry-forward."""
    _validate_config(config)

    hamiltonian = xxz_chain_hamiltonian(
        config.n_sites,
        J_xy=config.J_xy,
        J_z=config.J_z,
        W=config.disorder,
        seed=config.seed,
    )
    observables = readout_observables(
        config.n_sites,
        paulis=config.readout_paulis,
        sites=config.readout_sites,
    )
    device = reservoir_device(config.n_sites)
    wires = list(range(config.n_sites))

    @qp.qnode(device)
    def reservoir_step(input_scalar: float, prev_state: np.ndarray):
        qp.StatePrep(prev_state, wires=wires)
        if config.encoding == "local":
            encode_local_field(
                float(input_scalar),
                config.encoding_site,
                config.n_sites,
                scale=config.input_scale,
            )
        else:
            encode_global_rotation(
                float(input_scalar),
                config.n_sites,
                scale=config.input_scale,
            )
        qp.ApproxTimeEvolution(
            hamiltonian,
            config.evolution_time,
            config.n_trotter_steps,
        )
        features = tuple(qp.expval(obs) for obs in observables)
        return features, qp.state()

    return reservoir_step


def collect_features(
    inputs: np.ndarray,
    config: QRCConfig,
) -> np.ndarray:
    """
    Run the QRC pipeline over a 1-D input sequence.

    The quantum state after timestep ``t`` is the initial state for ``t+1``
    (continuous reservoir dynamics; Fujii & Nakajima 2017). State carry-forward
    uses explicit statevector handoff via ``StatePrep`` between timesteps.

    Parameters
    ----------
    inputs : np.ndarray, shape (n_timesteps,)
        Scalar input time series (typically in ``[0, 1]`` or task-specific range).
    config : QRCConfig
        Reservoir, encoder, evolution, and readout settings.

    Returns
    -------
    X : np.ndarray, shape (n_timesteps - washout, n_features)
        Reservoir feature matrix (one row per timestep after washout).
    """
    inputs = np.asarray(inputs, dtype=float).ravel()
    n_features = feature_dim(
        config.n_sites,
        paulis=config.readout_paulis,
        sites=config.readout_sites,
    )
    if len(inputs) <= config.washout:
        return np.zeros((0, n_features), dtype=float)

    qnode = _build_step_qnode(config)
    state = _initial_state(config.n_sites)
    rows: list[np.ndarray] = []
    for u in inputs:
        features, state = qnode(float(u), state)
        rows.append(np.asarray(features, dtype=float))

    features = np.vstack(rows)
    return features[config.washout :]


def run_qrc(
    inputs: np.ndarray,
    targets: np.ndarray,
    config: QRCConfig,
    *,
    train_fraction: float = 0.8,
    ridge_alpha: float = 1e-3,
) -> QRCResult:
    """
    Full QRC pipeline: collect features, train Ridge on a chronological split.

    Parameters
    ----------
    inputs : np.ndarray
        Input time series.
    targets : np.ndarray
        Target series aligned with ``inputs`` (same length).
    config : QRCConfig
    train_fraction : float
        Fraction of post-washout samples used for training (chronological split).
    ridge_alpha : float
        Ridge regularization strength.

    Returns
    -------
    QRCResult
    """
    if not 0.0 < train_fraction < 1.0:
        raise ValueError("train_fraction must be in (0, 1)")

    inputs = np.asarray(inputs, dtype=float).ravel()
    targets = np.asarray(targets, dtype=float).ravel()
    if len(inputs) != len(targets):
        raise ValueError(
            f"inputs and targets must have the same length, "
            f"got {len(inputs)} vs {len(targets)}"
        )

    X = collect_features(inputs, config)
    y = targets[config.washout :]
    if len(X) != len(y):
        raise RuntimeError(
            f"Feature/target length mismatch after washout: {len(X)} vs {len(y)}"
        )
    if len(X) < 2:
        raise ValueError(
            "Need at least two post-washout samples for train/test split; "
            f"got {len(X)} (increase sequence length or reduce washout)"
        )

    n_train = max(1, int(train_fraction * len(X)))
    if n_train >= len(X):
        n_train = len(X) - 1

    X_train, X_test = X[:n_train], X[n_train:]
    y_train, y_test = y[:n_train], y[n_train:]

    train_result = train_ridge(X_train, y_train, alpha=ridge_alpha)
    train_rmse = train_result.train_rmse

    predictions = predict(train_result.model, X_test)
    test_rmse = float(np.sqrt(np.mean((predictions - y_test) ** 2)))

    return QRCResult(
        X=X,
        y=y,
        train_result=train_result,
        train_rmse=train_rmse,
        test_rmse=test_rmse,
        predictions=predictions,
        config=config,
    )
