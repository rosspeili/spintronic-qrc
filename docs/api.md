# API Reference

Package: `spintronic_qrc` (install with `pip install -e ".[dev]"`).

## `reservoir`

| Function / class | Description |
|------------------|-------------|
| `ReservoirConfig` | Dataclass: `n_sites`, `J_xy`, `J_z`, `disorder`, `seed` |
| `sample_disorder_field(n_sites, W, seed)` | Draw `h_i ~ Uniform[-W, W]` |
| `xxz_chain_hamiltonian(n_sites, ...)` | Build PennyLane `Hamiltonian` |
| `reservoir_device(n_sites, shots)` | Create `default.qubit` device |

## `encoder`

| Function | Description |
|----------|-------------|
| `input_scale(u, scale)` | Map input to rotation angle |
| `encode_local_field(u, site, n_sites)` | Single-site `RZ` encoding |
| `encode_global_rotation(u, n_sites)` | Global `RX` on all sites |

## `readout`

| Function | Description |
|----------|-------------|
| `readout_observables(n_sites, paulis, sites)` | List of Pauli observables |
| `feature_dim(n_sites, paulis, sites)` | Feature vector length |

## `trainer`

| Function / class | Description |
|------------------|-------------|
| `TrainResult` | `model`, `train_rmse` |
| `train_ridge(X, y, alpha)` | Fit standardized Ridge regressor |
| `predict(model, X)` | Predict from features |

## `gates`

| Symbol | Description |
|--------|-------------|
| `SPINTRONIC_GATE_SET` | Tuple of gate metadata |
| `larmor_gate(theta, wire)` | `RZ` precession gate |
| `exchange_gate(phi, i, j, n_sites)` | `IsingXX` coupling gate |

## `tasks`

| Function | Description |
|----------|-------------|
| `narma10(length, u, seed)` | NARMA-10 input/target series |
| `mackey_glass(length, tau, dt, x0)` | Mackey-Glass chaotic series |

## `utils`

Matplotlib rcParams with QONDRA pastel palette constants.
