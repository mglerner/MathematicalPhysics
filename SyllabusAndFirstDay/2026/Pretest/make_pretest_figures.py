#!/usr/bin/env python
"""Generate the three figures for the PHY 210 math pretest.

Recreations (not copies) of the figures from the S23/S26 pretest:
  - triangular_region.pdf : triangle (0,0)-(0,2)-(1,2); right edge is y=2x
  - plotting_derivative.pdf: f(x) with empty axes at right for sketching df/dx
  - cosine_plot.pdf        : x(t) = 3 cos(pi t / 2)

Run from this directory:  ../../../../.venv/bin/python make_pretest_figures.py
(or any python with matplotlib+numpy)
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE = "#4C72B0"
GRAY = "#666666"


def clean_axes(ax, xlabel, ylabel, xlim, ylim):
    """Center the spines through the origin, label the axis ends."""
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRAY)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.annotate(xlabel, xy=(xlim[1], 0), xytext=(4, -2), textcoords="offset points",
                fontsize=16, fontweight="bold", color=GRAY, va="center")
    ax.annotate(ylabel, xy=(0, ylim[1]), xytext=(2, 2), textcoords="offset points",
                fontsize=16, fontweight="bold", color=GRAY, ha="left")
    ax.tick_params(colors=GRAY, labelsize=14)


def triangular_region():
    fig, ax = plt.subplots(figsize=(3.2, 4.0))
    tri_x, tri_y = [0, 0, 1], [0, 2, 2]
    ax.fill(tri_x, tri_y, color=BLUE, alpha=0.75, edgecolor=BLUE, linewidth=2)
    clean_axes(ax, "x", "y", (-0.35, 1.7), (-0.55, 2.6))
    ax.set_xticks([1])
    ax.set_yticks([2])
    ax.set_aspect(1.4)
    fig.tight_layout()
    fig.savefig("triangular_region.pdf")
    plt.close(fig)


def plotting_derivative():
    # A cubic with a local min near x=-1.2 and a local max near x=+0.65,
    # crossing zero near x=1.6 (mimics the original figure's shape).
    # f'(x) = -c (x - 0.65)(x + 1.2)
    x = np.linspace(-2, 2, 400)
    c = 1.5
    f = -c * (x**3 / 3 + 0.275 * x**2 - 0.78 * x) + 0.6
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.2))
    ax1.plot(x, f, color=BLUE, lw=2.2)
    clean_axes(ax1, "x", "f(x)", (-2.3, 2.3), (-2.2, 2.2))
    ax1.set_xticks([-2, -1, 1, 2])
    ax1.set_yticks([])
    # Empty axes for the student's sketch
    clean_axes(ax2, "x", "f '(x)", (-2.3, 2.3), (-2.2, 2.2))
    ax2.set_xticks([-2, -1, 1, 2])
    ax2.set_yticks([])
    fig.tight_layout()
    fig.savefig("plotting_derivative.pdf")
    plt.close(fig)


def cosine_plot():
    t = np.linspace(-4, 4, 600)
    x = 3 * np.cos(np.pi * t / 2)
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    ax.plot(t, x, color=BLUE, lw=2.2)
    clean_axes(ax, "t", "x", (-4.6, 4.6), (-4.4, 4.4))
    ax.set_xticks([-4, -3, -2, -1, 1, 2, 3, 4])
    ax.set_yticks([-4, -2, 2, 4])
    fig.tight_layout()
    fig.savefig("cosine_plot.pdf")
    plt.close(fig)


if __name__ == "__main__":
    triangular_region()
    plotting_derivative()
    cosine_plot()
    print("wrote triangular_region.pdf, plotting_derivative.pdf, cosine_plot.pdf")
