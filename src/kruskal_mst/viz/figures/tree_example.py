# -*- coding: utf-8 -*-
"""Приклад до §1: граф G з циклами та одне з його остовних дерев T (4 вершини).

``spanning_tree_example()`` повертає фігуру з двома панелями: ліворуч повний граф G
(5 ребер, є цикли), праворуч остовне дерево T (ті самі 4 вершини, 3 ребра, без циклів;
відкинуті ребра — сірим пунктиром).
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

from ..core.palette import C_NODE, C_NODE_EDGE, C_BASE_EDGE, C_MST, A_DSU
from ..core.i18n import t


def spanning_tree_example():
    """Дві панелі: граф G (є цикли) і одне з його остовних дерев T."""
    # Граф-приклад: 4 міста і дороги між ними (є цикли)
    G = nx.Graph()
    G.add_edges_from([("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"), ("B", "D")])

    # Одне з остовних дерев цього графа (3 ребра, без циклів)
    tree_edges = [("A", "B"), ("A", "C"), ("C", "D")]
    T = nx.Graph(); T.add_nodes_from(G.nodes()); T.add_edges_from(tree_edges)

    POS = {"A": (0, 1), "B": (1.4, 1), "C": (0, 0), "D": (1.4, 0)}
    norm = lambda e: tuple(sorted(e))
    tree_set = {norm(e) for e in tree_edges}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6))

    # Ліворуч: повний граф (є цикли)
    nx.draw_networkx_nodes(G, POS, ax=ax1, node_size=900, node_color=C_NODE,
                           edgecolors=C_NODE_EDGE, linewidths=1.8)
    nx.draw_networkx_labels(G, POS, ax=ax1, font_size=14, font_weight="bold", font_color="#15384A")
    nx.draw_networkx_edges(G, POS, ax=ax1, width=2.2, edge_color=A_DSU)
    ax1.set_title(t("Граф G: 4 вершини, 5 ребер (є цикли)"), fontsize=12)
    ax1.set_axis_off(); ax1.margins(0.18)

    # Праворуч: остовне дерево (зелене), відкинуті ребра — сірим пунктиром
    nx.draw_networkx_nodes(T, POS, ax=ax2, node_size=900, node_color=C_NODE,
                           edgecolors=C_NODE_EDGE, linewidths=1.8)
    nx.draw_networkx_labels(T, POS, ax=ax2, font_size=14, font_weight="bold", font_color="#15384A")
    non_tree = [e for e in G.edges() if norm(e) not in tree_set]
    nx.draw_networkx_edges(G, POS, ax=ax2, edgelist=non_tree, width=1.8,
                           edge_color=C_BASE_EDGE, style="dashed")
    nx.draw_networkx_edges(T, POS, ax=ax2, edgelist=tree_edges, width=3.4, edge_color=C_MST)
    ax2.set_title(t("Остовне дерево T: ті самі 4 вершини, 3 ребра"), fontsize=12)
    ax2.set_axis_off(); ax2.margins(0.18)

    fig.tight_layout()
    return fig
