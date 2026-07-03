# Notebook Guide

| # | File | Goal | Key outputs |
|---|------|------|-------------|
| 01 | `01_xxz_dynamics.ipynb` | Visualize XXZ chain evolution | `figures/xxz_dynamics.png` |
| 02 | `02_qrc_narma10.ipynb` | End-to-end QRC on NARMA-10 | `figures/qrc_narma10.png`, `data/narma10_results.csv` |
| 03 | `03_qrc_mackey_glass.ipynb` | Mackey-Glass prediction | `figures/qrc_mackey_glass.png` |
| 04 | `04_memory_capacity.ipynb` | Memory capacity vs chain params | `figures/memory_capacity.png` |
| 05 | `05_spintronic_gate_set.ipynb` | Gate set depth benchmarks | `figures/gate_depth_comparison.png` |
| 06 | `06_open_system_qrc.ipynb` | Dissipation via QuTiP | `figures/open_system_qrc.png` |

## Run order

1. **01** — confirm Hamiltonian and time evolution.
2. **02** — first full ML result on NARMA-10.
3. **03–04** — extend benchmarks and memory-capacity analysis.
4. **05–06** — gate set and open-system extensions.

## Kagome parameters from spinq-vqe

Notebook 01 may import exchange couplings from
[`spinq-vqe`](https://github.com/ARPAQLS/spinq-vqe) when calibrating the reservoir.
Default XXZ couplings (`J_xy=1`, `J_z=1`, `W=0.5`) work for initial development.
