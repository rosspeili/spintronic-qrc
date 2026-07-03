"""
encoder.py
----------
Map classical input signals into the spin-chain reservoir.

Input encoding injects time-varying local fields (or global rotations) before
each reservoir evolution step. Only the classical output layer is trained;
the reservoir and encoder mapping remain fixed after design.

References
----------
- Fujii & Nakajima (2017) Phys. Rev. Applied 8, 024030
- Nakajima (2021) J. Phys. Soc. Jpn. 90, 101001
"""

from __future__ import annotations

import numpy as np
import pennylane as qp


def input_scale(u: float, scale: float = np.pi / 2) -> float:
    """
    Map a scalar input ``u ∈ [0, 1]`` to a rotation angle.

    Parameters
    ----------
    u : float
        Normalized input sample.
    scale : float
        Maximum rotation amplitude.

    Returns
    -------
    float
        Rotation angle in radians.
    """
    return float(np.clip(u, 0.0, 1.0) * scale)


def encode_local_field(
    u: float,
    site: int,
    n_sites: int,
    scale: float = np.pi / 2,
) -> qp.operation.Operation:
    """
    Encode input as a local ``RZ`` rotation on one site.

    Parameters
    ----------
    u : float
        Input sample (typically in ``[0, 1]``).
    site : int
        Target site index.
    n_sites : int
        Total chain length (wire count).
    scale : float
        Rotation scale factor.

    Returns
    -------
    qp.RZ
        Local encoding gate.
    """
    if not 0 <= site < n_sites:
        raise ValueError(f"site must be in [0, {n_sites}), got {site}")
    return qp.RZ(input_scale(u, scale=scale), wires=site)


def encode_global_rotation(
    u: float,
    n_sites: int,
    scale: float = np.pi / 4,
) -> list[qp.operation.Operation]:
    """
    Encode input as identical ``RX`` rotations on all sites.

    Parameters
    ----------
    u : float
        Input sample.
    n_sites : int
        Chain length.
    scale : float
        Rotation scale factor.

    Returns
    -------
    list of qp.RX
        One gate per site.
    """
    angle = input_scale(u, scale=scale)
    return [qp.RX(angle, wires=i) for i in range(n_sites)]
