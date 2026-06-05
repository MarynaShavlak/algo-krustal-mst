# -*- coding: utf-8 -*-
"""Схема розрізу (cut property): дві групи вершин і ребра, що їх з'єднують."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx

from ...graph import POS_CUT
from ..core.palette import C_NODE, C_NODE_EDGE, CHIP

# локальні кольори саме для цієї схеми
C_S = "#A8D8EA"          # група A (над розрізом)
C_T = "#FCD9A6"          # група B (під розрізом)
C_FAINT = "#D9D9D9"      # ребра всередині груп
C_CROSS = "#9C6ADE"      # ребра, що перетинають розріз
C_LIGHT = "#2E8B57"      # найлегше з них
CUT = "#555"             # лінія розрізу


def cut_property(G, S=("A", "B", "C", "D", "E"), pos=POS_CUT):
    """Побудувати фігуру з розрізом графа й виділеним найлегшим перетинним ребром."""
    S = set(S)
    norm = lambda e: tuple(sorted(e))
    crossing = [(u, v) for u, v in G.edges() if (u in S) != (v in S)]
    lightest = min(crossing, key=lambda e: G[e[0]][e[1]]["weight"])
    cross_other = [e for e in crossing if norm(e) != norm(lightest)]
    inside = [(u, v) for u, v in G.edges() if (u in S) == (v in S)]

    fig, ax = plt.subplots(figsize=(8.0, 5.8))
    cut_y = 1.1
    ax.axhspan(cut_y, 4.4, facecolor=C_S, alpha=0.07, zorder=0)
    ax.axhspan(-0.7, cut_y, facecolor=C_T, alpha=0.11, zorder=0)
    ax.axhline(cut_y, ls="--", color=CUT, lw=2.0, zorder=1)
    ax.annotate("РОЗРІЗ", (5.0, cut_y), xytext=(4.5, cut_y + 0.18),
                fontsize=10, color=CUT, fontweight="bold")

    ei = nx.draw_networkx_edges(G, pos, ax=ax, edgelist=inside, edge_color=C_FAINT, width=1.6)
    if ei is not None:
        ei.set_zorder(2)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=cross_other,
                           edge_color=C_CROSS, width=3.0).set_zorder(2)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[lightest],
                           edge_color=C_LIGHT, width=4.5).set_zorder(2)

    nd = nx.draw_networkx_nodes(G, pos, ax=ax, node_size=850,
                                node_color=[C_S if n in S else C_T for n in G.nodes()],
                                edgecolors=C_NODE_EDGE, linewidths=1.8)
    nd.set_zorder(3)
    for t in nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight="bold",
                                     font_color="#15384A").values():
        t.set_zorder(5)

    # ваги всередині груп — по центру, у плашці
    lab_in = {(u, v): G[u][v]["weight"] for u, v in inside}
    for t in nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=lab_in,
                                          font_size=9.5, rotate=False, bbox=CHIP).values():
        t.set_zorder(4)
    # ваги перетинних ребер — ближче до верхньої вершини, геть від лінії розрізу
    for u, v in crossing:
        top = u if u in S else v
        bot = v if u in S else u
        px = pos[top][0] + 0.34 * (pos[bot][0] - pos[top][0])
        py = pos[top][1] + 0.34 * (pos[bot][1] - pos[top][1])
        ax.text(px, py, str(G[u][v]["weight"]), fontsize=9.5,
                ha="center", va="center", zorder=4, bbox=CHIP)

    ax.text(4.3, 3.9, "Група A", fontsize=11.5, color="#15384A", fontweight="bold")
    ax.text(-0.7, -0.45, "Група B = {F, G}", fontsize=11.5, color="#7a5b1e", fontweight="bold")

    lx = (pos[lightest[0]][0] + pos[lightest[1]][0]) / 2
    ly = (pos[lightest[0]][1] + pos[lightest[1]][1]) / 2
    w_light = G[lightest[0]][lightest[1]]["weight"]
    ax.annotate("найлегше ребро\nчерез розріз ->\nбезпечно в МОД", (lx, ly), xytext=(4.55, 2.15),
                fontsize=9.5, color=C_LIGHT, fontweight="bold", ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color=C_LIGHT, lw=1.6))

    ax.legend(handles=[
        Line2D([0], [0], color=C_CROSS, lw=3, label="ребра, що перетинають розріз"),
        Line2D([0], [0], color=C_LIGHT, lw=4,
               label=f"найлегше з них ({lightest[0]}\u2013{lightest[1]}, вага {w_light})"),
        Line2D([0], [0], color=C_FAINT, lw=2.4, label="ребра всередині груп"),
    ], loc="upper left", fontsize=9, frameon=False)
    ax.set_title("Розріз: вершини поділено на дві групи; кольорові ребра їх з'єднують", fontsize=12)
    ax.set_xlim(-0.9, 5.6)
    ax.set_ylim(-0.7, 4.35)
    ax.set_axis_off()
    fig.tight_layout()
    return fig
