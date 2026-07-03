"""Shared pytest fixtures for the spintronic_qrc test suite."""

import numpy as np
import pytest

from spintronic_qrc.reservoir import ReservoirConfig, xxz_chain_hamiltonian


@pytest.fixture(scope="session")
def chain4():
    """4-site XXZ chain Hamiltonian with fixed disorder seed."""
    return xxz_chain_hamiltonian(4, seed=0)


@pytest.fixture(scope="session")
def reservoir_cfg():
    """Default 6-site reservoir configuration."""
    return ReservoirConfig(n_sites=6, seed=0)


@pytest.fixture
def narma10_small():
    """Short NARMA-10 series for fast tests."""
    from spintronic_qrc.tasks import narma10

    return narma10(length=50, seed=0)
