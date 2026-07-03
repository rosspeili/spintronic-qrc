# Changelog

All notable changes to this project can be documented in this file.

The format follows the spirit of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses semantic versioning through the package version in
`pyproject.toml`.

## [Unreleased]

### Changed

- Expanded `REFERENCES.md` with Crossref-verified bibliography (corrected DOIs for Dambre,
  Mujal, Nakajima JPSJ, Domingo, Chen, Heyl; added QRC, spin-chain, and software cites).
- README badges: replaced version badge with QRC-specific readout badge (Ridge / sklearn).

### Removed

- Internal researcher draft files (`refresults1.md`, `refresults2.md`, `suggestedref.md`)
  after merging verified references.


### Added

- Initial release of `spintronic-qrc`: Python package, documentation, tests, and
  notebook directory structure.
- Core modules: `reservoir`, `encoder`, `readout`, `trainer`, `gates`, `tasks`, `utils`.
- XXZ spin-chain Hamiltonian builder (PennyLane) with on-site disorder sampling.
- NARMA-10 and Mackey-Glass benchmark task generators.
- Ridge regression output layer (`trainer`) and Pauli readout helpers.
- Spintronic-inspired gate set metadata and basic Larmor/exchange gates.
- `REFERENCES.md` bibliography, `docs/` guides, and `CITATION.cff`.
- QRC-specific dependency tiers in `pyproject.toml`: `[tuning]`, `[open]`,
  `[crossval]`, `[viz]`, `[notebooks]`, `[all]`.
- QONDRA splash logo (`docs/qondra_spintronic_qrc_splash.png`).

### Tests

- 16 unit tests covering reservoir, tasks, readout, and trainer (`pytest tests/ -v`).
