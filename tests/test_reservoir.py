"""Unit tests for spintronic_qrc.reservoir."""

import numpy as np
import pytest

from spintronic_qrc.reservoir import (
    ReservoirConfig,
    reservoir_device,
    sample_disorder_field,
    xxz_chain_hamiltonian,
)


class TestDisorder:
    def test_shape(self):
        h = sample_disorder_field(5, W=1.0, seed=0)
        assert h.shape == (5,)

    def test_bounds(self):
        h = sample_disorder_field(100, W=0.5, seed=1)
        assert np.all(h >= -0.5)
        assert np.all(h <= 0.5)

    def test_reproducible(self):
        a = sample_disorder_field(8, seed=42)
        b = sample_disorder_field(8, seed=42)
        np.testing.assert_array_equal(a, b)


class TestXXZHamiltonian:
    def test_raises_for_single_site(self):
        with pytest.raises(ValueError, match=">= 2"):
            xxz_chain_hamiltonian(1)

    def test_has_terms(self, chain4):
        assert len(chain4.ops) > 0
        assert len(chain4.coeffs) == len(chain4.ops)

    def test_custom_disorder(self):
        h_field = np.array([0.1, -0.2, 0.3, 0.0])
        H = xxz_chain_hamiltonian(4, disorder_field=h_field)
        assert len(H.ops) > 0

    def test_config_defaults(self, reservoir_cfg):
        assert reservoir_cfg.n_sites == 6
        assert reservoir_cfg.J_xy == 1.0


class TestDevice:
    def test_wire_count(self):
        dev = reservoir_device(5)
        assert len(dev.wires) == 5
