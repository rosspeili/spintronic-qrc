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

## `pipeline`

End-to-end QRC loop: encode → `ApproxTimeEvolution` → Pauli readout → Ridge (Fujii & Nakajima 2017).

| Function / class | Description |
|------------------|-------------|
| `QRCConfig` | Dataclass: `n_sites`, `evolution_time`, `n_trotter_steps`, exchange/disorder, `encoding`, `washout`, readout settings |
| `QRCResult` | `X`, `y`, `train_result`, `train_rmse`, `test_rmse`, `predictions`, `config` |
| `collect_features(inputs, config)` | Run reservoir over a 1-D series; returns `(n - washout, n_features)` |
| `run_qrc(inputs, targets, config, ...)` | Features + chronological Ridge train/test split |

```python
from spintronic_qrc.pipeline import QRCConfig, run_qrc
from spintronic_qrc.tasks import narma10

u, y = narma10(length=200, seed=42)
config = QRCConfig(n_sites=6, evolution_time=1.0, n_trotter_steps=10, washout=50)
result = run_qrc(u, y, config)
print(result.test_rmse)
```

State is carried forward across timesteps via ``StatePrep`` + ``qml.state()`` handoff
between per-step QNode calls (no reset to ``|0⟩^N`` between steps).

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
