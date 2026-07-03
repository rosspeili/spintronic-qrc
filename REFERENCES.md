# spintronic-qrc — References

> Curated references for the `spintronic-qrc` repository.
> Covers QRC foundations, benchmark tasks, spin-chain physics, and frameworks.

---

## Quantum Reservoir Computing (Core)

| # | Reference | URL / DOI |
|---|-----------|-----------|
| Q1 | Fujii, K., Nakajima, T. (2017) — *Harnessing disorder to enhance transport properties: An exploration on the impacts of random potentials in quantum reservoir computing.* Phys. Rev. Applied 8, 024030 | https://doi.org/10.1103/PhysRevApplied.8.024030 |
| Q2 | Mujal, P. et al. (2021) — *Opportunities in quantum reservoir computing and related quantum machine learning.* APL Quantum 1, 010101 | https://doi.org/10.1063/5.0050235 |
| Q3 | Nakajima, K. (2021) — *Physical reservoir computing — an introductory perspective.* J. Phys. Soc. Jpn. 90, 101001 | https://doi.org/10.7566/JPSJ.90.101001 |
| Q4 | Chen, J. et al. (2020) — *Quantum advantage in learning from experiments.* Science 376, 1182 | https://doi.org/10.1126/science.abn0493 |
| Q5 | Domingo, L. et al. (2023) — *Taking advantage of noise in quantum reservoir computing.* Scientific Reports 13, 8790 | https://doi.org/10.1038/s41598-023-36167-w |

---

## Memory Capacity & Benchmark Tasks

| # | Reference | URL / DOI |
|---|-----------|-----------|
| M1 | Dambre, J. et al. (2012) — *Information processing capacity of dynamical systems.* IEEE Trans. Neural Netw. 24, 687 | https://doi.org/10.1109/TNNLS.2012.2236570 |
| M2 | Jaeger, H. (2001) — *The "echo state" approach to analysing and training recurrent neural networks.* GMD Report 148 | https://www.researchgate.net/publication/215385037 |
| M3 | Mackey, M. C., Glass, L. (1977) — *Oscillation and chaos in physiological control systems.* Science 197, 287 | https://doi.org/10.1126/science.267326 |
| M4 | Atiya, A. F., Parlos, A. G. (2000) — *New results on recurrent network training.* Neurocomputing 35, 159 | https://doi.org/10.1016/S0925-2312(00)00211-9 |

---

## Spin Chains & Spintronic Physics

| # | Reference | URL / DOI |
|---|-----------|-----------|
| P1 | Sachdev, S. (1992) — *Kagome- and triangular-lattice Heisenberg antiferromagnets.* Phys. Rev. B 45, 12377 | https://doi.org/10.1103/PhysRevB.45.12377 |
| P2 | Heyl, M. et al. (2019) — *Quantum many-body physics in NISQ era.* Rep. Prog. Phys. 82, 124401 | https://doi.org/10.1088/1361-6633/ab3c67 |
| P3 | Nakatsuji, S., Ishizuka, H. (2022) — *Topological and magnetic phases with strong spin-orbit coupling in the Mn₃X family.* Ann. Phys. 447, 169146 | https://doi.org/10.1016/j.aop.2022.169146 |
| P4 | Sinova, J. et al. (2015) — *Spin Hall effects.* Rev. Mod. Phys. 87, 1213 | https://doi.org/10.1103/RevModPhys.87.1214 |

---

## Related Software & Experiments

| # | Reference | URL |
|---|-----------|-----|
| R1 | **spinq-vqe** — Kagome AFM VQE; source for calibrated exchange parameters | https://github.com/ARPAQLS/spinq-vqe |
| R2 | Nakatsuji et al. (2026) — Mn₃Sn SOT switching at 40 ps | https://www.science.org/doi/10.1126/science.adt3136 |

---

## Frameworks

| # | Resource | Install extra | URL |
|---|----------|---------------|-----|
| F1 | **PennyLane** — QRC circuits, time evolution | core | https://pennylane.ai |
| F2 | PennyLane `ApproxTimeEvolution` | core | https://docs.pennylane.ai/en/stable/code/api/pennylane.ApproxTimeEvolution.html |
| F3 | **scikit-learn** — Ridge output layer | core | https://scikit-learn.org |
| F4 | **Optuna** — hyperparameter sweeps | `[tuning]` | https://optuna.org |
| F5 | **QuTiP** — open-system / Lindblad validation | `[open]` | https://qutip.org |
| F6 | **Qiskit + Aer** — dynamics cross-validation | `[crossval]` | https://docs.quantum.ibm.com |
| F7 | **Plotly** — interactive notebook plots | `[viz]` | https://plotly.com/python |

---

## Classical Baselines

| # | Reference | URL / DOI |
|---|-----------|-----------|
| B1 | Jaeger, H. (2001) — Echo State Networks | see M2 |
| B2 | Lukoševičius, M., Jaeger, H. (2009) — *Reservoir computing approaches to recurrent neural network training.* Comput. Sci. Rev. 3, 127 | https://doi.org/10.1016/j.cosrev.2009.03.005 |

---

*Last updated: 2026-07-03*
