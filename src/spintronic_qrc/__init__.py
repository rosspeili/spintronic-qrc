"""
spintronic_qrc
==============
Quantum Reservoir Computing with Spin Chain Dynamics.

Part of the ARPA Quantum Logical Systems (QONDRA) research program.

Modules
-------
reservoir : Disordered XXZ spin chain Hamiltonian and time-evolution helpers
encoder   : Input signal injection into the reservoir
readout   : Pauli expectation-value feature extraction
trainer   : Classical Ridge regression output layer
gates     : Spintronic-inspired PennyLane custom gate set
tasks     : Benchmark time-series generators (NARMA-10, Mackey-Glass)
utils     : Plotting helpers with consistent pastel palette
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("spintronic-qrc")
except PackageNotFoundError:
    __version__ = "dev"

__author__ = "ARPA Quantum Logical Systems (QONDRA)"
__all__ = [
    "reservoir",
    "encoder",
    "readout",
    "trainer",
    "gates",
    "tasks",
    "utils",
]
