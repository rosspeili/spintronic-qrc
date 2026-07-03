"""
reservoir.py
------------
Disordered XXZ spin chain as a fixed quantum reservoir.

The reservoir Hamiltonian models antiferromagnetic spin-chain dynamics — the
same class of physics that governs frustrated spintronic materials such as
Mn₃Sn. Exchange parameters can be imported from ``spinq-vqe`` Kagome VQE results
when calibrating the reservoir Hamiltonian.

Hamiltonian
-----------
    H = J_xy Σ_i (σ_i^x σ_{i+1}^x + σ_i^y σ_{i+1}^y)
      + J_z  Σ_i  σ_i^z σ_{i+1}^z
      + Σ_i  h_i σ_i^z

Where ``h_i ~ Uniform[-W, W]`` breaks translational symmetry and enriches
reservoir dynamics (Fujii & Nakajima 2017).

References
----------
- Fujii & Nakajima (2017) Phys. Rev. Applied 8, 024030
- Dambre et al. (2012) IEEE TNN 24, 687
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pennylane as qp

# Default exchange couplings (dimensionless; set J_xy=1 as energy unit)
J_XY_DEFAULT: float = 1.0
J_Z_DEFAULT: float = 1.0
DISORDER_W_DEFAULT: float = 0.5


@dataclass(frozen=True)
class ReservoirConfig:
    """Physical and numerical settings for the spin-chain reservoir."""

    n_sites: int
    J_xy: float = J_XY_DEFAULT
    J_z: float = J_Z_DEFAULT
    disorder: float = DISORDER_W_DEFAULT
    seed: int | None = 42


def sample_disorder_field(
    n_sites: int,
    W: float = DISORDER_W_DEFAULT,
    seed: int | None = 42,
) -> np.ndarray:
    """
    Draw on-site disorder fields ``h_i ~ Uniform[-W, W]``.

    Parameters
    ----------
    n_sites : int
        Chain length.
    W : float
        Half-width of the uniform disorder distribution.
    seed : int or None
        RNG seed for reproducibility.

    Returns
    -------
    np.ndarray
        Shape ``(n_sites,)`` disorder fields.
    """
    rng = np.random.default_rng(seed)
    return rng.uniform(-W, W, size=n_sites)


def xxz_chain_hamiltonian(
    n_sites: int,
    J_xy: float = J_XY_DEFAULT,
    J_z: float = J_Z_DEFAULT,
    disorder_field: np.ndarray | None = None,
    W: float = DISORDER_W_DEFAULT,
    seed: int | None = 42,
) -> qp.Hamiltonian:
    """
    Build the open-boundary XXZ chain Hamiltonian as a PennyLane operator.

    Parameters
    ----------
    n_sites : int
        Number of spin-1/2 sites on the chain.
    J_xy : float
        In-plane exchange coupling (XX + YY terms).
    J_z : float
        Ising (ZZ) exchange coupling.
    disorder_field : array-like, optional
        On-site ``Z`` fields. If ``None``, sampled via ``sample_disorder_field``.
    W : float
        Disorder half-width used when ``disorder_field`` is ``None``.
    seed : int or None
        RNG seed for disorder sampling.

    Returns
    -------
    qp.Hamiltonian
        Sum of two-qubit and single-qubit Pauli terms.

    Examples
    --------
    >>> H = xxz_chain_hamiltonian(4, seed=0)
    >>> len(H.ops) > 0
    True
    """
    if n_sites < 2:
        raise ValueError("n_sites must be >= 2 for a chain reservoir")

    coeffs: list[float] = []
    ops: list[qp.operation.Operator] = []

    for i in range(n_sites - 1):
        coeffs.extend([J_xy, J_xy, J_z])
        ops.extend(
            [
                qp.PauliX(i) @ qp.PauliX(i + 1),
                qp.PauliY(i) @ qp.PauliY(i + 1),
                qp.PauliZ(i) @ qp.PauliZ(i + 1),
            ]
        )

    if disorder_field is None:
        disorder_field = sample_disorder_field(n_sites, W=W, seed=seed)
    else:
        disorder_field = np.asarray(disorder_field, dtype=float)
        if disorder_field.shape != (n_sites,):
            raise ValueError(
                f"disorder_field must have shape ({n_sites},), "
                f"got {disorder_field.shape}"
            )

    for i, h_i in enumerate(disorder_field):
        if h_i != 0.0:
            coeffs.append(float(h_i))
            ops.append(qp.PauliZ(i))

    return qp.Hamiltonian(coeffs, ops)


def reservoir_device(
    n_sites: int,
    shots: int | None = None,
) -> qp.Device:
    """
    Create a PennyLane simulator device for the reservoir.

    Parameters
    ----------
    n_sites : int
        Number of qubits / spin sites.
    shots : int or None
        If set, use shot-based sampling; otherwise exact simulation.

    Returns
    -------
    qp.Device
        ``default.qubit`` device with ``n_sites`` wires.
    """
    return qp.device("default.qubit", wires=n_sites, shots=shots)
