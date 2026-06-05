# -*- coding: utf-8 -*-
"""Компактний огляд: усі кроки Краскала на одній сітці панелей."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from ..core.palette import C_NODE, C_NODE_EDGE, C_MST, C_CONSIDER, C_REJECT
from ..core.graph_plot import draw_graph
from ...kruskal import kruskal_logged


def steps_grid(G, cols=3):
    """Побудувати фігуру-сітку з усіма кроками алгоритму до збирання дерева."""
    _, _, steps = kruskal_logged(G)
    complete_at = next(i for i, s in enumerate(steps)
                       if len(s["mst_after"]) == G.number_of_nodes() - 1)
    vis = steps[:complete_at + 1]

    rows = (len(vis) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4.3, rows * 3.6))
    axes = axes.ravel()

    for i, s in enumerate(vis):
        u, v, w = s["edge"]
        mst_set = {tuple(sorted((a, b))) for a, b, _ in s["mst_after"]}
        tag = "ДОДАНО" if s["accepted"] else "ВІДХИЛЕНО (цикл)"
        draw_graph(G, axes[i], mst_set=mst_set, consider=(u, v),
                   consider_ok=s["accepted"], comp=s["comp_after"],
                   title=f"Крок {i + 1}: {u}\u2013{v} (вага {w}) — {tag}")

    for j in range(len(vis), len(axes)):
        axes[j].set_axis_off()

    legend_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=C_NODE,
               markeredgecolor=C_NODE_EDGE, markersize=12, markeredgewidth=1.6,
               label="колір вершини = компонента зв'язності"),
        Line2D([0], [0], color=C_MST, lw=3.2, label="ребро у МОД"),
        Line2D([0], [0], color=C_CONSIDER, lw=3.2, label="щойно прийняте"),
        Line2D([0], [0], color=C_REJECT, lw=3.2, ls="--", label="відхилене (цикл)"),
    ]
    fig.legend(handles=legend_handles, loc="lower center", ncol=4, fontsize=10,
               frameon=False, bbox_to_anchor=(0.5, 0.005),
               handlelength=1.8, columnspacing=2.0, handletextpad=0.6)
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    return fig
