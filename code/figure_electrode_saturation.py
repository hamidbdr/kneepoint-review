#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script illustrates early models of electrode saturation.

1. Reproduces Figure 17 of Dubarry et al.:
https://doi.org/10.1016/j.jpowsour.2012.07.016

The .mat file was obtained from Matthieu.

2. Reproduces Figure 1 of Smith et al.:
https://doi.org/10.23919/ACC.2017.7963578
    
The code was generated by Paul
"""

from pathlib import Path

import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt

import config

path = Path().cwd() / "data"
data = sio.loadmat(path / "dubarry_synthesize_2012_fig17.mat")

# Kandler Smith figure spaghetti code
t = np.arange(365 * 30)
N = t*0.2
b1 = 1e-3
b2 = 1e-4
p = 1.5
qLi = 1.06 - b1 * t ** 0.5
qPos = 1 + 0.02 * (1 - np.exp(- t / 150))
qNeg = (1.1 ** (1 + p) - b2 * 1.1 ** p * (1 + p) * N) ** (1 / (1 + p))
qCell = np.min(np.array([qLi, qNeg, qPos]).T, axis=1)

# Generate figure handles
fig, ax = plt.subplots(figsize=(config.FIG_WIDTH, 2 * config.FIG_HEIGHT),
                       nrows=2, ncols=1)

# Plots
ax[0].plot(
    data["x2"].flatten(),
    data["y2"].flatten(),
    "--",
    color="tab:blue",
    label="Loss of lithium inventory"
)

ax[0].plot(
    data["x3"].flatten(),
    data["y3"].flatten(),
    ":",
    color="tab:red",
    label="Loss of delithiated cathode active material"
)

ax[0].plot(
    data["x1"].flatten(),
    data["y1"].flatten(),
    color="k",
    label="Calculated capacity loss"
)


ax[1].plot(t / 1000, qLi, color="tab:purple", label="Lithium inventory, $Q_{Li}$")
ax[1].plot(t / 1000, qNeg, color="tab:blue", label="Negative electrode capacity, $Q_{neg}$")
ax[1].plot(t / 1000, qPos, color="tab:green", label="Positive electrode capacity, $Q_{pos}$")
ax[1].plot(t / 1000, qCell, "--k", label="Cell capacity = min($Q_{Li}$, $Q_{neg}$, $Q_{pos}$)")


# Set axes labels
ax[0].set_xlabel("Cycle number")
ax[0].set_ylabel("Degradation or capacity loss (%)")
ax[1].set_xlabel("Time (arbitrary)")
ax[1].set_ylabel("Relative capacity")

# Add axes limits
ax[0].set_xlim([0, 400])
ax[1].set_xlim([0, 11.5])
ax[0].set_ylim([0, 100])

# Add legends
ax[0].legend()
ax[1].legend()

ax[0].set_title("a", loc="left", weight="bold")
ax[1].set_title("b", loc="left", weight="bold")

# Save figure as both .PNG and .EPS
fig.tight_layout()
fig.savefig(config.FIG_PATH / "electrode_saturation.png", format="png", dpi=300)
fig.savefig(config.FIG_PATH / "electrode_saturation.eps", format="eps")