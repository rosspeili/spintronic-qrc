# spintronic-qrc — Documentation

> ARPA Quantum Logical Systems (QONDRA) &nbsp;·&nbsp; [qondra@arpacorp.net](mailto:qondra@arpacorp.net)

---

## Contents

| Document | What it covers |
|----------|---------------|
| [Research overview](../OVERVIEW.md) | Narrative, research threads, literature context |
| [Physics background](physics.md) | XXZ spin chains, QRC pipeline, spintronic gate mapping |
| [API reference](api.md) | Module-level reference for `spintronic_qrc` |
| [Notebook guide](notebooks.md) | What each notebook does and how to run it |
| [Testing guide](testing.md) | Running tests, coverage map |

---

## Quick orientation

**The physics:** A disordered XXZ spin chain is a natural quantum reservoir — entangled,
sensitive to inputs, nonlinear in its evolution. This is the same *class* of Hamiltonian
as frustrated antiferromagnets such as Mn₃Sn, which
[`spinq-vqe`](https://github.com/ARPAQLS/spinq-vqe) simulates on a Kagome lattice.

**The stack:** PennyLane + JAX for the reservoir. scikit-learn for the Ridge output layer.
NumPy/SciPy for benchmark tasks. Optional: Optuna (tuning), QuTiP (open systems),
Qiskit+Aer (dynamics cross-validation), Plotly (interactive plots).

**The pipeline:** Input `u(t)` → encode into local fields → evolve under `H` for time τ
→ measure Pauli expectations → train Ridge → predict `ŷ(t)`.

**Install:** from `Spintronics/`: `pip install -e "./spintronic-qrc[dev]"`. See
[`README.md`](../README.md) for optional extras.

---

*Part of the ARPA Spintronics QML Research Program*
