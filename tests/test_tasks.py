"""Unit tests for spintronic_qrc.tasks."""

import numpy as np

from spintronic_qrc.tasks import mackey_glass, narma10


class TestNARMA10:
    def test_output_shapes(self, narma10_small):
        u, y = narma10_small
        assert u.shape == y.shape
        assert len(u) == 50

    def test_reproducible(self):
        u1, y1 = narma10(30, seed=7)
        u2, y2 = narma10(30, seed=7)
        np.testing.assert_array_equal(u1, u2)
        np.testing.assert_array_equal(y1, y2)

    def test_not_constant(self, narma10_small):
        _, y = narma10_small
        assert np.std(y) > 0


class TestMackeyGlass:
    def test_length(self):
        x = mackey_glass(200)
        assert x.shape == (200,)

    def test_non_constant(self):
        x = mackey_glass(500, tau=17)
        assert np.std(x) > 0
