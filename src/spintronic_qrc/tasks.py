"""
tasks.py
--------
Canonical benchmark time-series for reservoir computing evaluation.

Implemented
-----------
- NARMA-10: nonlinear autoregressive moving-average (memory + nonlinearity)
- Mackey-Glass: chaotic delay-differential attractor (discretized)

References
----------
- Jaeger (2001) — Echo State Networks
- Dambre et al. (2012) — memory capacity metric
- Mackey & Glass (1977) Science 197, 287
"""

from __future__ import annotations

import numpy as np


def narma10(
    length: int,
    u: np.ndarray | None = None,
    seed: int | None = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate the NARMA-10 time series.

    Parameters
    ----------
    length : int
        Number of output samples (requires ``length + 10`` warmup steps).
    u : array, optional
        Input sequence in ``[0, 0.5]``. Sampled uniformly if ``None``.
    seed : int or None
        RNG seed for default input.

    Returns
    -------
    u : np.ndarray, shape (length,)
        Input sequence.
    y : np.ndarray, shape (length,)
        Target sequence.
    """
    if length < 1:
        raise ValueError("length must be >= 1")

    total = length + 10
    if u is None:
        rng = np.random.default_rng(seed)
        u = rng.uniform(0.0, 0.5, size=total)
    else:
        u = np.asarray(u, dtype=float)
        if len(u) < total:
            raise ValueError(f"u must have length >= {total}, got {len(u)}")

    y = np.zeros(total)
    for t in range(9, total):
        y[t] = (
            0.3 * y[t - 1]
            + 0.05 * y[t - 1] * np.sum(y[t - 9 : t])
            + 1.5 * u[t - 9] * u[t]
            + 0.1
        )

    return u[10:], y[10:]


def mackey_glass(
    length: int,
    tau: int = 17,
    dt: float = 1.0,
    x0: float = 1.2,
) -> np.ndarray:
    """
    Discretized Mackey-Glass chaotic time series.

    Parameters
    ----------
    length : int
        Number of output samples.
    tau : int
        Delay (in steps).
    dt : float
        Integration step size.
    x0 : float
        Initial condition.

    Returns
    -------
    np.ndarray
        Shape ``(length,)`` time series.
    """
    if length < 1:
        raise ValueError("length must be >= 1")
    if tau < 1:
        raise ValueError("tau must be >= 1")

    history = np.full(tau + 1, x0, dtype=float)
    out = np.empty(length, dtype=float)

    for t in range(length):
        x_tau = history[0]
        x = history[-1]
        dx = 0.2 * x_tau / (1.0 + x_tau**10) - 0.1 * x
        x_next = x + dt * dx
        history = np.roll(history, -1)
        history[-1] = x_next
        out[t] = x_next

    return out
