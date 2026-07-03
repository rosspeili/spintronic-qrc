"""Unit tests for spintronic_qrc.trainer and readout."""

import numpy as np

from spintronic_qrc.readout import feature_dim, readout_observables
from spintronic_qrc.trainer import predict, train_ridge


class TestReadout:
    def test_observable_count(self):
        obs = readout_observables(4, paulis=("X", "Z"))
        assert len(obs) == 8

    def test_feature_dim(self):
        assert feature_dim(5, paulis=("Z",)) == 5


class TestTrainer:
    def test_ridge_fit(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(40, 6))
        y = X @ np.array([1.0, -0.5, 0.2, 0.0, 0.1, -0.3])
        result = train_ridge(X, y, alpha=1e-2)
        assert result.train_rmse < 0.5
        pred = predict(result.model, X[:5])
        assert pred.shape == (5,)
