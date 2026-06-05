# -*- coding: utf-8 -*-
"""Приклад до §2: граф із 3 компонентами зв'язності («архіпелаг островів»)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

from .palette import C_NODE_EDGE, A_DSU

# власна послідовність кольорів компонент (інший порядок, ніж COMP_PALETTE,
# щоб три острівці пофарбувались саме як у ноутбуці)
PALETTE = ["#A8D8EA", "#C9E4C5", "#FCE4A6", "#F6C9C9", "#D7C9EC"]


def connected_components_example():
    """Граф із трьох «острівців»: {A,B,C}, {D,E,F}, {G} — кожен своїм кольором."""
    G = nx.Graph()
    G.add_edges_from([("A", "B"), ("B", "C"), ("A", "C")])   # трикутник
    G.add_edges_from([("D", "E"), ("E", "F")])               # ланцюжок
    G.add_node("G")                                          # самотня вершина

    POS = {"A": (0, 2), "B": (1.1, 2.5), "C": (0.7, 1.2),
           "D": (3.4, 2.3), "E": (4.6, 2.6), "F": (4.2, 1.3),
           "G": (2.3, 0.1)}

    comps = list(nx.connected_components(G))
    comp_id = {n: ci for ci, cc in enumerate(comps) for n in cc}
    node_colors = [PALETTE[comp_id[n]] for n in G.nodes()]

    fig, ax = plt.subplots(figsize=(8, 4.2))
    nx.draw_networkx_nodes(G, POS, ax=ax, node_size=850, node_color=node_colors,
                           edgecolors=C_NODE_EDGE, linewidths=1.8)
    nx.draw_networkx_labels(G, POS, ax=ax, font_size=13, font_weight="bold", font_color="#15384A")
    nx.draw_networkx_edges(G, POS, ax=ax, width=2.4, edge_color=A_DSU)
    ax.set_title("Граф із 3 компонентами зв'язності (кожен колір — окрема компонента)", fontsize=12)
    ax.set_axis_off(); ax.margins(0.15)
    fig.tight_layout()
    return fig
