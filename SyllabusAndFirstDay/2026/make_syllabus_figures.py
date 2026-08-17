#!/usr/bin/env python
"""Margin figures for the F2026 PHY 210 syllabus (tufte-handout).

  coupled_oscillators.pdf : two coupled SHOs trading energy (beats);
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
    # Equal masses/outer springs with weak coupling: x1(0)=1, x2(0)=0,
    # released from rest -> energy slowly trades between the two masses.
    w1, w2 = 9.0, 10.0
    t = np.linspace(0, 12.5, 2000)
    x1 = 0.5 * (np.cos(w1 * t) + np.cos(w2 * t))
    x2 = 0.5 * (np.cos(w1 * t) - np.cos(w2 * t))
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(2.1, 1.5), sharex=True)
    for ax, x, lab in ((ax1, x1, "$x_1$"), (ax2, x2, "$x_2$")):
        ax.plot(t, x, color="black", lw=0.6)
        ax.set_ylim(-1.25, 1.25)
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ("top", "right", "left", "bottom"):
            ax.spines[s].set_visible(False)
        ax.text(-0.4, 0, lab, ha="right", va="center", fontsize=9)
    ax2.annotate("time", xy=(0.85, -0.12), xycoords="axes fraction",
                 fontsize=7, color="#555555")
    fig.subplots_adjust(left=0.12, right=0.99, top=0.98, bottom=0.08,
                        hspace=0.25)
    fig.savefig("coupled_oscillators.pdf")
    plt.close(fig)


def heat_equation():
    # Uniformly hot bar, ends held cold: T(x,0)=1 on (0,1), T=0 at ends.
    # T(x,t) = sum over odd n of (4/(n pi)) sin(n pi x) exp(-(n pi)^2 t).
    x = np.linspace(0, 1, 400)
    times = [0.0005, 0.003, 0.01, 0.03, 0.09]
    grays = ["0.0", "0.25", "0.45", "0.62", "0.78"]
    fig, ax = plt.subplots(figsize=(2.1, 1.35))
    for t, g in zip(times, grays):
        T = np.zeros_like(x)
        for n in range(1, 80, 2):
            T += (4 / (n * np.pi)) * np.sin(n * np.pi * x) * np.exp(
                -((n * np.pi) ** 2) * t)
        ax.plot(x, T, color=g, lw=0.7)
    ax.set_ylim(0, 1.15)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.5)
    ax.annotate("", xy=(0.62, 0.28), xytext=(0.55, 0.78),
                arrowprops=dict(arrowstyle="->", lw=0.5, color="#555555"))
    ax.text(0.63, 0.5, "time", fontsize=7, color="#555555")
    fig.subplots_adjust(left=0.03, right=0.99, top=0.97, bottom=0.06)
    fig.savefig("heat_equation.pdf")
    plt.close(fig)


if __name__ == "__main__":
    coupled_oscillators()
    heat_equation()
    print("wrote coupled_oscillators.pdf, heat_equation.pdf")
