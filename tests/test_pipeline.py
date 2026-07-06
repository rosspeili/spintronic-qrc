"""Unit tests for spintronic_qrc.pipeline."""

import numpy as np
import pytest

from spintronic_qrc.pipeline import QRCConfig, collect_features, run_qrc
from spintronic_qrc.readout import feature_dim
from spintronic_qrc.tasks import narma10


@pytest.fixture
def small_config() -> QRCConfig:
    """Fast QRC settings for unit tests (N=4, few Trotter steps)."""
    return QRCConfig(
        n_sites=4,
        evolution_time=0.5,
        n_trotter_steps=3,
        washout=5,
        seed=0,
    )


class TestCollectFeatures:
    def test_output_shape(self, small_config):
        inputs = np.linspace(0.1, 0.4, 20)
        X = collect_features(inputs, small_config)
        n_feat = feature_dim(
            small_config.n_sites,
            paulis=small_config.readout_paulis,
            sites=small_config.readout_sites,
        )
        assert X.shape == (len(inputs) - small_config.washout, n_feat)

    def test_features_finite(self, small_config):
        inputs = np.linspace(0.0, 0.5, 15)
        X = collect_features(inputs, small_config)
        assert np.all(np.isfinite(X))

    def test_washout_zero(self):
        config = QRCConfig(
            n_sites=4,
            evolution_time=0.3,
            n_trotter_steps=2,
            washout=0,
            seed=1,
        )
        inputs = np.array([0.2, 0.3, 0.4, 0.5])
        X = collect_features(inputs, config)
        assert X.shape[0] == len(inputs)

    def test_empty_when_sequence_too_short(self, small_config):
        inputs = np.ones(small_config.washout)
        X = collect_features(inputs, small_config)
        assert X.shape == (0, feature_dim(small_config.n_sites))

    def test_global_encoding(self):
        config = QRCConfig(
            n_sites=4,
            evolution_time=0.4,
            n_trotter_steps=2,
            encoding="global",
            washout=2,
            seed=2,
        )
        X = collect_features(np.linspace(0.1, 0.5, 10), config)
        assert X.shape == (8, feature_dim(4))
        assert np.all(np.isfinite(X))

    def test_invalid_encoding_site_raises(self):
        config = QRCConfig(n_sites=4, encoding_site=4)
        with pytest.raises(ValueError, match="encoding_site"):
            collect_features(np.ones(12), config)


class TestRunQRC:
    def test_narma10_end_to_end(self):
        u, y = narma10(length=50, seed=0)
        config = QRCConfig(
            n_sites=4,
            evolution_time=0.5,
            n_trotter_steps=3,
            washout=10,
            seed=0,
        )
        result = run_qrc(u, y, config, train_fraction=0.8, ridge_alpha=1e-2)
        assert result.X.shape[0] == len(u) - config.washout
        assert len(result.y) == result.X.shape[0]
        assert len(result.predictions) == len(result.X) - int(0.8 * len(result.X))
        assert np.isfinite(result.train_rmse)
        assert np.isfinite(result.test_rmse)

    def test_length_mismatch_raises(self, small_config):
        with pytest.raises(ValueError, match="same length"):
            run_qrc(np.ones(20), np.ones(15), small_config)

    def test_invalid_train_fraction_raises(self, small_config):
        with pytest.raises(ValueError, match="train_fraction"):
            run_qrc(np.ones(20), np.ones(20), small_config, train_fraction=1.0)
