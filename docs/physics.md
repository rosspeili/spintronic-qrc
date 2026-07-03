# Physics Background

## Quantum Reservoir Computing

Quantum Reservoir Computing (QRC) uses a **fixed** quantum system to transform input signals into a high-dimensional feature space. Only a classical linear output layer is trained. The reservoir's natural dynamics provide nonlinearity and memory.

Standard pipeline:

```
u(t) → [encode] → [evolve under H for τ] → [Pauli readout] → [Ridge] → ŷ(t)
```

## XXZ Spin Chain Reservoir

Open-boundary chain Hamiltonian:

```
H = J_xy Σ_i (σ_i^x σ_{i+1}^x + σ_i^y σ_{i+1}^y)
  + J_z  Σ_i  σ_i^z σ_{i+1}^z
  + Σ_i  h_i σ_i^z
```

On-site disorder `h_i ~ Uniform[-W, W]` breaks translational symmetry and increases computational richness (Fujii & Nakajima 2017).

## Connection to Spintronic Materials

Mn₃Sn and related antiferromagnets are governed by frustrated spin-exchange physics. The XXZ / Heisenberg chain is not an arbitrary ansatz — it is the same mathematical family used in the QONDRA program's Kagome VQE work (`spinq-vqe`).

## Spintronic-inspired gate set

| Physical operation | Spintronic mechanism | Quantum gate |
|-------------------|---------------------|--------------|
| Larmor precession | External field B | `RZ(θ)` |
| Exchange coupling | RKKY interaction | `IsingXX(φ)` |
| Spin-orbit torque | SOC | `Rot(φ, θ, ω)` |
| Gilbert damping | Dissipation | Lindblad channel |

## Benchmark Tasks

- **NARMA-10:** Tests memory and nonlinearity (standard QRC benchmark).
- **Mackey-Glass:** Chaotic short-term prediction.
- **Memory capacity:** Dambre et al. (2012) metric — planned in notebook 04.

See [`REFERENCES.md`](../REFERENCES.md) for full citations.
