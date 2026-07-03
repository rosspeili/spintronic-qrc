"""
readout.py
----------
Extract reservoir state features via Pauli expectation values.

The readout layer maps the post-evolution quantum state to a classical feature
vector. Only a linear output layer is trained downstream (see ``trainer``).

References
----------
- Dambre et al. (2012) IEEE TNN 24, 687
"""

from __future__ import annotations

from itertools import product

import pennylane as qp


def readout_observables(
    n_sites: int,
    paulis: tuple[str, ...] = ("X", "Y", "Z"),
    sites: list[int] | None = None,
) -> list[qp.operation.Operator]:
    """
    Build the list of single-site Pauli observables for readout.

    Parameters
    ----------
    n_sites : int
        Chain length.
    paulis : tuple of str
        Which Pauli axes to measure per site.
    sites : list of int, optional
        Subset of sites. Defaults to all sites.

    Returns
    -------
    list
        PennyLane observables (``PauliX``, ``PauliY``, ``PauliZ``).
    """
    if sites is None:
        sites = list(range(n_sites))

    pauli_ops = {"X": qp.PauliX, "Y": qp.PauliY, "Z": qp.PauliZ}
    unknown = set(paulis) - pauli_ops.keys()
    if unknown:
        raise ValueError(f"Unknown Pauli labels: {unknown}")

    obs: list[qp.operation.Operator] = []
    for site, label in product(sites, paulis):
        obs.append(pauli_ops[label](site))
    return obs


def feature_dim(
    n_sites: int,
    paulis: tuple[str, ...] = ("X", "Y", "Z"),
    sites: list[int] | None = None,
) -> int:
    """Return the number of readout features for the given configuration."""
    if sites is None:
        sites = list(range(n_sites))
    return len(sites) * len(paulis)
