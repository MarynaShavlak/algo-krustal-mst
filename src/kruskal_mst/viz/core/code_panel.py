# -*- coding: utf-8 -*-
"""Ліва панель схеми: код DSU-версії з підсвічуванням + список ребер + легенда."""

from __future__ import annotations

from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

from .palette import (
    C_BASE_EDGE, C_MST, C_CONSIDER, C_REJECT, C_NODE, ROOT_BORDER,
)

#: Код DSU-версії Краскала, який показуємо ліворуч на покрокових схемах.
CODE = [
    "dsu = DSU(graph.nodes())",                           # 0
    "mst = []",                                           # 1
    "",                                                   # 2
    "sorted_edges = sorted(graph.edges(data='weight'),",  # 3
    "                      key=lambda e: e[2])",          # 4
    "",                                                   # 5
    "for u, v, w in sorted_edges:",                       # 6
    "    if dsu.union(u, v):          # різні множини?",   # 7
    "        mst.append((u, v, w))",                      # 8
    "    # else: вже разом -> цикл -> пропуск",            # 9
]

#: Код варіанту через has_path (forest) для покрокової схеми §6.
CODE_HAS_PATH = [
    "forest = nx.Graph()",
    "for node in graph.nodes():",
    "    forest.add_node(node)",
    "",
    "sorted_edges = sorted(graph.edges(data=True),",
    "                      key=lambda t: t[2]['weight'])",
    "",
    "for u, v, attr in sorted_edges:",
    "    if not nx.has_path(forest, u, v):",
    "        forest.add_edge(u, v)",
    "        mst.add_edge(u, v, weight=attr['weight'])",
    "    # else: u,v вже з'єднані -> цикл -> пропустити",
]


def draw_code(ax, highlights, code=CODE):
    """Намалювати код ``code`` з підсвіченими рядками (``highlights`` = {індекс: колір})."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    line_h = 1.0 / len(code)
    for i, line in enumerate(code):
        y = 1.0 - (i + 0.5) * line_h
        if i in highlights:
            ax.add_patch(Rectangle((0, y - line_h * 0.45), 1, line_h * 0.9,
                                   facecolor=highlights[i], edgecolor="none", zorder=0))
        ax.text(0.015, y, line, family="monospace", fontsize=10,
                va="center", ha="left", color="#1b1b1b", zorder=2)


def draw_sorted_list(ax, order):
    """Намалювати вертикальний список відсортованих ребер ``order`` = [(u, v, w), ...]."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.0, 0.99, "Відсортовані ребра (за зростанням ваги):",
            fontsize=10.5, fontweight="bold", va="top", color="#15384A")
    n = len(order)
    top, bottom = 0.86, 0.06
    line_h = (top - bottom) / (n - 1)
    for i, (u, v, w) in enumerate(order):
        y = top - i * line_h
        ax.text(0.04, y, f"{i + 1:>2}.", family="monospace", fontsize=10, va="center", color="#888")
        ax.text(0.16, y, f"{u}\u2013{v}", family="monospace", fontsize=10.5, va="center",
                fontweight="bold", color="#1b1b1b")
        ax.text(0.40, y, f"вага {w}", family="monospace", fontsize=10, va="center", color="#444")
    ax.text(0.0, -0.02, "Далі перебираємо зверху вниз \u2192", fontsize=8.5,
            style="italic", va="top", color="#666")


#: Підписи для легенди покрокових схем (граф + структура DSU).
LEGEND_HANDLES = [
    Line2D([0], [0], color=C_BASE_EDGE, lw=2.4, label="ребро графа (кандидат)"),
    Line2D([0], [0], color=C_MST, lw=3.0, label="обране (у МОД)"),
    Line2D([0], [0], color=C_CONSIDER, lw=3.0, label="щойно додане / нова зв'язка DSU"),
    Line2D([0], [0], color=C_REJECT, lw=3.0, ls="--", label="відкинуте (цикл)"),
    Line2D([0], [0], marker="o", color="none", markerfacecolor=C_NODE,
           markeredgecolor=ROOT_BORDER, markeredgewidth=2, markersize=11,
           label="корінь DSU (рN = ранг)"),
]
