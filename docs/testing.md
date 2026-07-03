# Testing Guide

## Run tests

From the **program workspace venv** (`Spintronics/.venv`):

```bash
cd Spintronics
.venv\Scripts\activate          # Windows
pip install -e "./spintronic-qrc[dev]"
pytest spintronic-qrc/tests/ -v
```

Tests use small chain sizes and short NARMA-10 series for speed (< 30 s on CPU).

## Coverage map

| Module | Test file | What is tested |
|--------|-----------|----------------|
| `reservoir` | `test_reservoir.py` | Disorder sampling, Hamiltonian build, device |
| `tasks` | `test_tasks.py` | NARMA-10 shapes/reproducibility, Mackey-Glass |
| `trainer`, `readout` | `test_trainer.py` | Ridge fit, feature dimensions |

## Fixtures

See `tests/conftest.py`:

- `chain4` — 4-site Hamiltonian (session scope)
- `reservoir_cfg` — default 6-site config
- `narma10_small` — 50-step NARMA-10 series

## Lint

```bash
ruff check src/
```
