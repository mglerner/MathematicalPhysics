#!/usr/bin/env python
"""Margin figures for the F2026 PHY 210 syllabus (tufte-handout).

  coupled_oscillators.pdf : the Felder Sec 6.9 worked example (p. 337);
                            the week 7-9 eigenvector/normal-mode payoff.
  heat_equation.pdf       : heat-equation relaxation of a hot bar;
                            the week 15 PDE finale.

Tufte-ish: black/gray, thin lines, no boxes, minimal axes.
Run from this directory: ../../../.venv/bin/python make_syllabus_figures.py
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 8,
    "axes.linewidth": 0.5,
})


def coupled_oscillators():
    # The worked example on p. 337 (Felder & Felder Sec 6.9): the
    # coupled system xddot1 = -3x1 - 2x2, xddot2 = -x1 - 2x2 with
    # x1(0)=3, x2(0)=-9, released from rest. Normal modes (1, 1/2) at
    # omega=2 and (1, -1) at omega=1.
    t = np.linspace(0, 4 * np.pi, 2000)
    x1 = -4 * np.cos(2 * t) + 7 * np.cos(t)
    x2 = -2 * np.cos(2 * t) - 7 * np.cos(t)
    # Colors validated (dataviz six-checks, light surface): CVD-safe pair.
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(2.1, 1.5), sharex=True)
    for ax, x, lab, c in ((ax1, x1, "$x_1$", "#4C72B0"),
                          (ax2, x2, "$x_2$", "#C44E52")):
        ax.plot(t, x, color=c, lw=0.7)
        ax.set_ylim(-11.5, 11.5)
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ("top", "right", "left", "bottom"):
            ax.spines[s].set_visible(False)
        ax.text(-0.4, 0, lab, ha="right", va="center", fontsize=9)
        # (labels stay in ink; the trace carries the color)
    ax2.annotate("time", xy=(0.85, -0.12), xycoords="axes fraction",
                 fontsize=7, color="#555555")
    fig.subplots_adjust(left=0.12, right=0.99, top=0.98, bottom=0.08,
                        hspace=0.25)
    fig.savefig("coupled_oscillators.pdf")
    plt.close(fig)


def heat_equation():
    # Uniformly hot bar, ends held cold: T(x,0)=1 on (0,1), T=0 at ends.
    # T(x,t) = sum over odd n of (4/(n pi)) sin(n pi x) exp(-(n pi)^2 t).
    # Each curve is colored by its LOCAL temperature (blue = cold,
    # red = hot; matplotlib coolwarm, a proper diverging map), so the
    # early hot profiles read red and the late ones fade toward blue.
    from matplotlib.collections import LineCollection
    from matplotlib.colors import Normalize

    x = np.linspace(0, 1, 400)
    times = [0.0005, 0.003, 0.01, 0.03, 0.09]
    cmap = plt.get_cmap("coolwarm")
    norm = Normalize(0.0, 1.05)
    fig, ax = plt.subplots(figsize=(2.1, 1.35))
    for t in times:
        T = np.zeros_like(x)
        for n in range(1, 80, 2):
            T += (4 / (n * np.pi)) * np.sin(n * np.pi * x) * np.exp(
                -((n * np.pi) ** 2) * t)
        pts = np.array([x, T]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        mid = 0.5 * (T[:-1] + T[1:])
        lc = LineCollection(segs, colors=cmap(norm(mid)), linewidth=0.9)
        ax.add_collection(lc)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.15)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.5)
    ax.text(-0.03, 0.55, "temperature", fontsize=7, color="#555555",
            rotation=90, va="center", ha="right")
    ax.annotate("", xy=(0.62, 0.28), xytext=(0.55, 0.78),
                arrowprops=dict(arrowstyle="->", lw=0.5, color="#555555"))
    ax.text(0.63, 0.5, "time", fontsize=7, color="#555555")
    fig.subplots_adjust(left=0.10, right=0.99, top=0.97, bottom=0.06)
    fig.savefig("heat_equation.pdf")
    plt.close(fig)


if __name__ == "__main__":
    coupled_oscillators()
    heat_equation()
    print("wrote coupled_oscillators.pdf, heat_equation.pdf")
