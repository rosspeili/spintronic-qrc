"""
gates.py
--------
Spintronic-inspired custom gate set for PennyLane circuits.

Maps physical spintronic operations to quantum gates:

| Physical operation   | Gate analog        |
|---------------------|--------------------|
| Larmor precession   | ``RZ(θ)``          |
| Exchange coupling   | ``IsingXX(φ)``     |
| Spin-orbit torque   | ``Rot(φ, θ, ω)``   |
| Gilbert damping     | Lindblad channel   |

Full custom operations and depth benchmarks are planned for notebook 05.

References
----------
- Fujii & Nakajima (2017) Phys. Rev. Applied 8, 024030
"""

from __future__ import annotations

from dataclasses import dataclass

import pennylane as qp


@dataclass(frozen=True)
class SpintronicGateSpec:
    """Metadata for one entry in the spintronic native gate set."""

    name: str
    physical_op: str
    pennylane_op: str


SPINTRONIC_GATE_SET: tuple[SpintronicGateSpec, ...] = (
    SpintronicGateSpec("larmor", "External field B", "RZ"),
    SpintronicGateSpec("exchange", "RKKY interaction", "IsingXX"),
    SpintronicGateSpec("sot", "Spin-orbit torque", "Rot"),
    SpintronicGateSpec("damping", "Gilbert dissipation", "Lindblad"),
)


def larmor_gate(theta: float, wire: int) -> qp.RZ:
    """Larmor precession → ``RZ(θ)`` on ``wire``."""
    return qp.RZ(theta, wires=wire)


def exchange_gate(phi: float, i: int, j: int, n_sites: int) -> qp.IsingXX:
    """RKKY exchange → ``IsingXX(φ)`` between sites ``i`` and ``j``."""
    return qp.IsingXX(phi, wires=[i, j])
