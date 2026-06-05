# -*- coding: utf-8 -*-
"""Схема до §6: чому на кроці 8 ребро B–C утворило б цикл B → E → C → B."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx

from ..graph import POS
from .palette import C_NODE, C_NODE_EDGE, C_MST, C_REJECT, C_CONSIDER, C_PANEL_EDGE


def bc_cycle_step8(G, pos=POS):
    """Граф перед кроком 8: зелене — у МОД, помаранчеве — наявний шлях B→E→C, пунктир — відкинуте B–C."""
    forest = nx.Graph(); forest.add_nodes_from(G.nodes())
    for e in [("A", "D"), ("C", "E"), ("D", "F"), ("A", "B"), ("B", "E")]:
        forest.add_edge(*e)

    norm = lambda e: tuple(sorted(e))
    path = nx.shortest_path(forest, "B", "C")
    cyc = {norm((path[i], path[i + 1])) for i in range(len(path) - 1)}   # {B-E, C-E}

    mst_now = [norm(e) for e in [("A", "D"), ("C", "E"), ("D", "F"), ("A", "B"), ("B", "E")]]
    green = [e for e in mst_now if e not in cyc]
    reject = norm(("B", "C"))
    used = set(mst_now) | {reject}
    base = [(u, v) for u, v in G.edges() if norm((u, v)) not in used]

    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=820, node_color=C_NODE,
                           edgecolors=C_NODE_EDGE, linewidths=1.8)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight="bold", font_color="#15384A")
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=base, edge_color=C_PANEL_EDGE, width=1.5)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=green, edge_color=C_MST, width=3.0)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=list(cyc), edge_color=C_CONSIDER, width=4.0)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[reject], edge_color=C_REJECT, width=3.2, style="dashed")
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=nx.get_edge_attributes(G, "weight"),
                                 font_size=9, rotate=False,
                                 bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
    ax.set_title("Крок 8: ребро B–C замкнуло б цикл  B → E → C → B", fontsize=12)
    ax.set_axis_off(); ax.margins(0.13)
    ax.legend(handles=[
        Line2D([0], [0], color=C_MST, lw=3, label="вже у МОД"),
        Line2D([0], [0], color=C_CONSIDER, lw=4, label="наявний шлях B→E→C"),
        Line2D([0], [0], color=C_REJECT, lw=3, ls="--", label="B–C: замкнуло б цикл"),
    ], loc="lower right", fontsize=9, frameon=False)
    fig.tight_layout()
    return fig
