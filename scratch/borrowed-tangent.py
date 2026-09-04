#!/usr/bin/env python3
"""Borrowed tangent still and avatar crop."""

from __future__ import annotations

import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


BG = "#0b0c10"
INK = "#ece7d8"
MUTED = "#8d92a0"
STONE = "#a6a6a6"
GOLD = "#e5b84a"
CYAN = "#5fcbd3"
ROSE = "#e8788b"
GREEN = "#87d37c"
BLUE_ROOM = "#102d3a"
WARM_ROOM = "#3b2414"
VIOLET_ROOM = "#271b3d"


def draw_piece(path: str, *, avatar: bool = False) -> None:
    if avatar:
        fig = plt.figure(figsize=(6, 6), dpi=220, facecolor=BG)
        ax = fig.add_axes([0, 0, 1, 1])
    else:
        fig = plt.figure(figsize=(12, 7), dpi=180, facecolor=BG)
        ax = fig.add_axes([0.04, 0.08, 0.92, 0.82])

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")

    rooms = [
        (0.0, 0.33, WARM_ROOM),
        (0.33, 0.66, BLUE_ROOM),
        (0.66, 1.0, VIOLET_ROOM),
    ]
    for x0, x1, color in rooms:
        ax.add_patch(Rectangle((x0, 0), x1 - x0, 1, facecolor=color, edgecolor="none"))
    for x in (0.33, 0.66):
        ax.plot([x, x], [0, 1], color="#0f1117", lw=1.2, alpha=0.85)

    # The physical path is straight; only the surrounding basis bends the read.
    xs = [0.16, 0.34, 0.50, 0.66, 0.84]
    ys = [0.26, 0.39, 0.50, 0.61, 0.74]
    ax.plot(xs, ys, color=STONE, lw=7.0, solid_capstyle="round", alpha=0.95)
    ax.plot(xs, ys, color=INK, lw=0.8, alpha=0.55)

    for x, y in zip(xs, ys):
        ax.add_patch(Circle((x, y), 0.026, facecolor=STONE, edgecolor=INK, lw=0.7, zorder=4))

    tangent_points = [(0.29, 0.36, GOLD, -12), (0.50, 0.50, ROSE, 25), (0.71, 0.64, CYAN, -18)]
    for x, y, color, angle in tangent_points:
        dx = 0.12 * math.cos(math.radians(angle))
        dy = 0.12 * math.sin(math.radians(angle))
        arrow = FancyArrowPatch(
            (x - dx / 2, y - dy / 2),
            (x + dx / 2, y + dy / 2),
            arrowstyle="-|>",
            mutation_scale=14,
            lw=2.2,
            color=color,
            alpha=0.95,
        )
        ax.add_patch(arrow)

    # Folding the room away: the same gray object remains, now without borrowed color.
    ax.add_patch(Rectangle((0.21, 0.11), 0.58, 0.11, facecolor="#23262d", edgecolor=INK, lw=0.65))
    ax.plot([0.25, 0.75], [0.165, 0.165], color=STONE, lw=7.0, solid_capstyle="round")
    ax.add_patch(Circle((0.25, 0.165), 0.022, facecolor=STONE, edgecolor=INK, lw=0.6))
    ax.add_patch(Circle((0.75, 0.165), 0.022, facecolor=STONE, edgecolor=INK, lw=0.6))
    ax.plot([0.21, 0.79], [0.095, 0.095], color=GREEN, lw=1.7)

    if not avatar:
        fig.text(0.06, 0.94, "borrowed tangent", color=INK, fontsize=25, weight="bold")
        fig.text(
            0.06,
            0.895,
            "same object, changing rooms: the apparent turn is a coordinate debt",
            color=MUTED,
            fontsize=11,
        )
        ax.text(0.50, 0.055, "fold the room away; the stone has not moved", color=GREEN, fontsize=10, ha="center")
        ax.text(0.50, 0.86, "the difference is borrowed", color=INK, fontsize=12, ha="center")

    fig.savefig(path, facecolor=BG, bbox_inches="tight" if not avatar else None, pad_inches=0.08 if not avatar else 0)


if __name__ == "__main__":
    draw_piece("assets/borrowed-tangent.png")
    draw_piece("assets/vita-avatar-borrowed-tangent.png", avatar=True)
    print("wrote assets/borrowed-tangent.png")
    print("wrote assets/vita-avatar-borrowed-tangent.png")
