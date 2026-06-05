# -*- coding: utf-8 -*-
"""Схема до §7: вироджений ланцюг проти плаского дерева (навіщо потрібні оптимізації DSU)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

from ..core.palette import C_NODE, C_NODE_EDGE, C_MST

C_ARROW = "#777"   # стрілки вказівників (темно-сірі саме для цієї схеми)


def _draw_forest(ax, parent, pos, root, title):
    D = nx.DiGraph(); D.add_nodes_from(parent.keys())
    for child, par in parent.items():
        if child != par:
            D.add_edge(child, par)               # стрілка: дитина -> батько
    colors = [C_MST if n == root else C_NODE for n in D.nodes()]
    nx.draw_networkx_nodes(D, pos, ax=ax, node_size=900, node_color=colors,
                           edgecolors=C_NODE_EDGE, linewidths=2.0)
    nx.draw_networkx_labels(D, pos, ax=ax, font_size=13, font_weight="bold", font_color="#15384A")
    nx.draw_networkx_edges(D, pos, ax=ax, edge_color=C_ARROW, width=2.0,
                           arrows=True, arrowstyle="-|>", arrowsize=22,
                           node_size=900, min_source_margin=18, min_target_margin=18)
    rx, ry = pos[root]
    ax.annotate("корінь", (rx, ry), xytext=(rx + 0.55, ry + 0.15),
                fontsize=10, color=C_MST, fontweight="bold")
    # явні межі (вузли ланцюга всі при x=0 → інакше bbox «tight» розпливається)
    xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
    ax.set_xlim(min(xs) - 0.7, max(xs) + 1.3)   # запас праворуч під підпис «корінь»
    ax.set_ylim(min(ys) - 0.6, max(ys) + 0.8)
    ax.set_title(title, fontsize=12); ax.set_axis_off()


def chain_vs_flat():
    """Ліворуч вироджений ланцюг (find(5) = 4 кроки), праворуч пласке дерево (find(5) = 1 крок)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))

    # Ліворуч: вироджений ланцюг (без оптимізацій)
    _draw_forest(ax1, {1: 1, 2: 1, 3: 2, 4: 3, 5: 4},
                 {1: (0, 4), 2: (0, 3), 3: (0, 2), 4: (0, 1), 5: (0, 0)}, 1,
                 "Без оптимізацій: ланцюг\nfind(5) = 4 кроки до кореня")

    # Праворуч: пласке дерево (після стиснення шляху / union by rank)
    _draw_forest(ax2, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1},
                 {1: (1.5, 2), 2: (0, 0.4), 3: (1, 0.4), 4: (2, 0.4), 5: (3, 0.4)}, 1,
                 "Зі стисненням шляху: пласко\nfind(5) = 1 крок до кореня")

    fig.subplots_adjust(top=0.84, wspace=0.08)
    return fig
