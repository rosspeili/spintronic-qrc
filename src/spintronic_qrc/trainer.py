"""
trainer.py
----------
Classical output layer for quantum reservoir computing.

The reservoir produces a feature matrix ``X``; a Ridge regressor maps features
to target outputs. This is the only trained component in the QRC pipeline.

References
----------
- Jaeger (2001) GMD Report 148 — Echo State Networks (classical baseline)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass
class TrainResult:
    """Container for fitted QRC output-layer results."""

    model: Pipeline
    train_rmse: float


def train_ridge(
    X: np.ndarray,
    y: np.ndarray,
    alpha: float = 1e-3,
) -> TrainResult:
    """
    Fit a standardized Ridge regressor on reservoir features.

    Parameters
    ----------
    X : array, shape (n_samples, n_features)
        Reservoir feature matrix.
    y : array, shape (n_samples,) or (n_samples, n_targets)
        Target values.
    alpha : float
        Ridge regularization strength.

    Returns
    -------
    TrainResult
        Fitted pipeline and in-sample RMSE.
    """
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    if X.ndim != 2:
        raise ValueError(f"X must be 2-D, got shape {X.shape}")
    if len(X) != len(y):
        raise ValueError(f"X and y length mismatch: {len(X)} vs {len(y)}")

    model = Pipeline(
        [
            ("scale", StandardScaler()),
            ("ridge", Ridge(alpha=alpha)),
        ]
    )
    model.fit(X, y)
    pred = model.predict(X)
    rmse = float(np.sqrt(np.mean((pred - y) ** 2)))
    return TrainResult(model=model, train_rmse=rmse)


def predict(model: Pipeline, X: np.ndarray) -> np.ndarray:
    """Predict targets from reservoir features using a fitted pipeline."""
    return model.predict(np.asarray(X, dtype=float))
