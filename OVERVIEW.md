# spintronic-qrc — Research Overview

**Quantum Reservoir Computing with Spin Chain Dynamics**

Part of [ARPA Quantum Logical Systems — QONDRA](https://github.com/arpaqls) · [qondra@arpacorp.net](mailto:qondra@arpacorp.net)

---

## Status

| Field | Value |
|-------|-------|
| **Version** | 0.1.0 (scaffold) |
| **Clusters** | B3 (QRC on spin chains) + C1 (Spintronic-inspired gate set) |
| **Priority** | Next in program execution order — builds on `spinq-vqe` Hamiltonian baseline |
| **Shipped** | Package skeleton, XXZ Hamiltonian builder, NARMA-10 / Mackey-Glass tasks, Ridge trainer, tests |
| **Next** | Notebook 01 (XXZ dynamics) → Notebook 02 (NARMA-10 QRC loop) |

---

## Motivation

Quantum Reservoir Computing (QRC) exploits a **fixed quantum system** — the "reservoir" —
to perform temporal information processing. Only the output layer is trained classically.

The key insight: **antiferromagnetic spin chains are natural quantum reservoirs.** They are:
- Highly entangled (rich dynamics)
- Sensitive to initial conditions (good memory)
- Non-linear in their evolution (computational expressiveness)

This is the **same physics** that UTokyo's Mn₃Sn device exploits — spin-spin interactions,
exchange coupling, frustrated geometry. We are not simulating the device; we are using the
same *class* of Hamiltonian as a computational substrate for machine learning.

This is the most conceptually direct bridge between spintronics and QML in the entire program.

---

## Core Workstreams

### Workstream B3 — Quantum Reservoir Computing Pipeline

The QRC framework:

```
Input signal u(t)
      │
      ▼
[Encoding: inject u(t) into spin chain via local fields]
      │
      ▼
[Reservoir: XXZ spin chain evolves under H for time τ]
      │
      ▼
[Readout: measure Pauli expectation values <σ_i^α>]
      │
      ▼
[Classical output layer: linear regression / sklearn]
      │
      ▼
Prediction ŷ(t)
```

**Reservoir Hamiltonian (XXZ spin chain):**
```
H = J_xy Σ_i (σ_i^x σ_{i+1}^x + σ_i^y σ_{i+1}^y)
  + J_z  Σ_i  σ_i^z σ_{i+1}^z
  + h    Σ_i  σ_i^z            (disorder field, site-dependent)
```

Where the disorder `h_i ~ Uniform[-W, W]` is crucial — it breaks translational symmetry
and is the primary source of the reservoir's computational richness.

**Tasks:**
- Implement XXZ chain in PennyLane (time evolution via `qml.ApproxTimeEvolution`)
- Implement input encoding schemes: single-site, global field, partial injection
- Implement readout: local Pauli measurements → feature matrix X
- Train output layer: `sklearn.linear_model.Ridge`
- Benchmark on canonical tasks:
  - **NARMA-10**: Nonlinear Autoregressive Moving Average (memory + non-linearity test)
  - **Mackey-Glass**: Chaotic attractor short-term prediction
  - **Sine wave recall**: Memory capacity benchmark
- Sweep hyperparameters: chain length N, evolution time τ, disorder W, Jz/Jxy ratio
- Compute **quantum memory capacity** (Dambre et al. 2012 metric)

### Workstream C1 — Spintronic-Inspired Gate Set

Define a custom PennyLane gate library that maps to physical spintronic operations:

| Physical operation | Spintronic mechanism | Quantum gate analog |
|-------------------|---------------------|---------------------|
| Larmor precession | External field B | `qml.RZ(θ)` (exact) |
| Exchange coupling | RKKY interaction | `qml.IsingXX(φ)` |
| Spin-orbit torque | SOC, Rashba/Dresselhaus | `qml.Rot(φ, θ, ω)` |
| Damping (Gilbert) | Magnetization dissipation | Lindblad channel |
| Spin Hall injection | Interface SOC | Custom entangling gate |

Tasks:
- Implement `SpintronicGateSet` as PennyLane custom operations
- Show that circuits built from this gate set have lower depth for spin Hamiltonian
  simulation than universal gate sets (RZ + CNOT)
- Visualize gate set completeness using the Weyl chamber representation
- Benchmark: spin chain time evolution depth with spintronic gate set vs standard

---

## Stack

Dependencies are **QRC-specific** — not a copy of `spinq-vqe` (no NetworkX, QuSpin,
Materials Project, OpenFermion, etc.).

| Component | Library | Role | When needed |
|-----------|---------|------|-------------|
| Primary QML | PennyLane ≥ 0.39 | QRC circuits, `ApproxTimeEvolution`, Hamiltonians | **Core** — always |
| Simulator | PennyLane-Lightning + JAX | Fast statevector simulation | **Core** — always |
| Classical ML | scikit-learn | Ridge output layer | **Core** — always |
| Time series | NumPy, SciPy | NARMA-10, Mackey-Glass, memory capacity | **Core** — always |
| Visualization | Matplotlib | Publication figures | **Core** — always |
| Hyperparameter tuning | Optuna | Sweep N, τ, W, Jz/Jxy | Notebooks 02–04 (`[tuning]`) |
| Interactive plots | Plotly | Notebook dashboards | Optional (`[viz]`) |
| Open systems | QuTiP | Lindblad damping validation | Notebook 06 (`[open]`) |
| Alt framework | Qiskit + Aer | Cross-validate unitary dynamics | Validation (`[crossval]`) |
| Notebooks | Jupyter | Demos | Development (`[dev]`) |

Install tiers: `pip install -e ".[dev]"` for tests · `[notebooks]` for NB01–05 ·
`[all]` when open-system and cross-validation work begins.

---

## Deliverables

- [x] `src/spintronic_qrc/` — Python package: reservoir, encoder, readout, trainer, tasks
- [x] `src/spintronic_qrc/gates.py` — Spintronic gate set metadata + basic gates (stub)
- [x] `tests/` — Unit tests for reservoir, tasks, trainer
- [x] `docs/` — Physics, API, notebook plan, testing guide
- [x] `REFERENCES.md` — Seed bibliography
- [ ] `notebooks/01_xxz_dynamics.ipynb` — Spin chain time evolution visualization
- [ ] `notebooks/02_qrc_narma10.ipynb` — Full QRC pipeline on NARMA-10 task
- [ ] `notebooks/03_qrc_mackey_glass.ipynb` — Chaotic attractor prediction
- [ ] `notebooks/04_memory_capacity.ipynb` — Quantum memory capacity vs chain params
- [ ] `notebooks/05_spintronic_gate_set.ipynb` — Custom gate library + circuit depth benchmarks
- [ ] `notebooks/06_open_system_qrc.ipynb` — QRC with dissipation (QuTiP + PennyLane)
- [ ] `benchmarks/` — Reproducible benchmark scripts vs classical ESN (Echo State Network)
- [ ] `paper/` — LaTeX draft targeting npj Quantum Information or PRL

---

## Paper Angle

**Title (draft):** *Quantum Reservoir Computing on Antiferromagnetic Spin Chains:
Connecting Spintronic Physics to Temporal Machine Learning*

**Novelty:**
1. First systematic study of QRC using **frustrated** XXZ chains (Kagome-inspired disorder)
   rather than the Ising chains used in prior QRC literature
2. Spintronic gate set enables native circuit implementation closer to physical hardware
3. Direct comparison of quantum memory capacity vs classical Echo State Networks on
   identical tasks — clear, reproducible benchmark

**Target Journals:** npj Quantum Information, Physical Review Research, Quantum

**arXiv sections:** `quant-ph`, `cond-mat.dis-nn` (disordered systems)

---

## Unique Selling Point

> This repo uses **the same class of spin Hamiltonian** that defines the Mn₃Sn material
> as a *machine learning computational substrate* — no approximation, no analogy.
> The spintronics IS the computing. This is the most direct conceptual bridge in the program.

---

## Cross-Repo Dependencies

```
spintronic-qrc (this repo)
    │
    ├── uses:  spinq-vqe       [Kagome Hamiltonian parameters as reservoir H]
    ├── uses:  mtj-quantum-noise [noise channels applied to reservoir — future]
    └── feeds: spinmat-qnn     [QRC features as input to QNN — future]
```

---

## Research Context & Key References

1. **Fujii & Nakajima (2017)** — Harnessing disorder in quantum reservoir computing
   (Physical Review Applied) — *the* foundational QRC paper
2. **Mujal et al. (2021)** — Opportunities in quantum reservoir computing (APL Quantum)
3. **Dambre et al. (2012)** — Information processing capacity of dynamical systems
4. **Jaeger (2001)** — Echo State Network (classical baseline)
5. **Heyl et al. (2019)** — Quantum many-body physics in NISQ era
6. **Nakajima (2021)** — Physical reservoir computing review

Full bibliography: [`REFERENCES.md`](REFERENCES.md)

---

## Getting Started

Use the program workspace venv (`Spintronics/.venv`):

```bash
cd ..                              # Spintronics/ root
.venv\Scripts\activate             # Windows
pip install -e "./spintronic-qrc[dev]"
pytest spintronic-qrc/tests/ -v
```

First notebook to implement: `notebooks/01_xxz_dynamics.ipynb`

---

## Open Questions / Design Decisions

- [ ] Input encoding: single-site field injection vs global rotation — which preserves
      more of the reservoir's intrinsic dynamics?
- [ ] Measurement strategy: full Pauli set {X,Y,Z} on all sites, or subset?
- [ ] Disorder: quenched (fixed per run) vs annealed (resampled each step)?
- [ ] Open system extension: add Gilbert damping as Lindblad operator via QuTiP
- [ ] Gate set completeness: is the spintronic gate set universal?

---

*Last updated: 2026-07-03 · Part of the ARPA Spintronics QML Research Program*
