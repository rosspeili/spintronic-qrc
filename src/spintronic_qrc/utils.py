"""
utils.py
--------
Plotting helpers with a soft pastel palette consistent with the QONDRA program.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

# Soft pastel palette (QONDRA program style)
RESERVOIR_COLOR = "#7EB8D4"
READOUT_COLOR = "#E8A598"
BASELINE_COLOR = "#B0B0B0"
ACCENT_SAGE = "#A8D8B0"
ACCENT_LAVENDER = "#B8B8E8"

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "#FAFAFA",
        "axes.edgecolor": "#CCCCCC",
        "axes.labelcolor": "#444444",
        "xtick.color": "#666666",
        "ytick.color": "#666666",
        "font.size": 11,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.color": "#DDDDDD",
    }
)
