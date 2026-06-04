# -*- coding: utf-8 -*-
"""Порівняння на одному кроці (§10): ``nx.has_path`` (обхід графа) проти DSU (підняття до кореня).

``compare_has_path_vs_dsu(G)`` повертає фігуру з двома панелями поряд для кроку 8 (ребро B–C):
ліворуч — BFS, що крокує лісом-графом; праворуч — DSU, що звіряє корені вершин B і C.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

from ..graph import POS

# локальні кольори саме для цієї схеми
C_NODE = "#A8D8EA"; C_VISIT = "#FCD9A6"; C_PATH = "#F4A300"; C_ROOT = "#2E8B57"
C_EDGE = "#2C6E8F"; C_FOREST = "#444"; C_FAINT = "#E3E6E8"; C_ARROW = "#888"

# розкладка дерева DSU саме для правої панелі
DPOS = {"A": (1.6, 2.3), "B": (0.0, 1.1), "C": (1.0, 1.1), "D": (2.2, 1.1), "F": (3.2, 1.1),
        "E": (1.0, 0.0), "G": (4.2, 1.7)}


def compare_has_path_vs_dsu(G, pos=POS):
    """Дві панелі поряд: ліворуч BFS усередині has_path, праворуч підняття до кореня в DSU."""
    forest_edges = [("A", "D"), ("C", "E"), ("D", "F"), ("A", "B"), ("B", "E")]   # вже у МОД
    forest = nx.Graph(); forest.add_nodes_from(G.nodes()); forest.add_edges_from(forest_edges)
    norm = lambda e: tuple(sorted(e))

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.4))

    # ===== ЛІВОРУЧ: nx.has_path (обхід графа BFS) =====
    bfs_order = ["B", "A", "E", "D", "C"]                 # порядок відвідування, поки не знайдено C
    visit_num = {n: i + 1 for i, n in enumerate(bfs_order)}
    path = nx.shortest_path(forest, "B", "C")              # B-E-C
    path_edges = [norm((path[i], path[i + 1])) for i in range(len(path) - 1)]

    node_colors = [C_PATH if n in ("B", "C") else (C_VISIT if n in visit_num else C_NODE)
                   for n in G.nodes()]
    fset = {norm(e) for e in forest_edges}
    non_forest = [(u, v) for u, v in G.edges() if norm((u, v)) not in fset]
    forest_only = [(u, v) for u, v in G.edges() if norm((u, v)) in fset and norm((u, v)) not in set(path_edges)]
    nx.draw_networkx_edges(G, pos, ax=axL, edgelist=non_forest, edge_color=C_FAINT, width=1.2, style="dotted")
    nx.draw_networkx_edges(G, pos, ax=axL, edgelist=forest_only, edge_color=C_FOREST, width=2.2)
    nx.draw_networkx_edges(G, pos, ax=axL, edgelist=path_edges, edge_color=C_PATH, width=4.0)
    nx.draw_networkx_nodes(G, pos, ax=axL, node_size=900, node_color=node_colors,
                           edgecolors=C_EDGE, linewidths=1.8)
    nx.draw_networkx_labels(G, pos, ax=axL, font_size=12, font_weight="bold", font_color="#15384A")
    for n, num in visit_num.items():
        x, y = pos[n]
        axL.annotate(str(num), (x, y), xytext=(x + 0.28, y + 0.30), fontsize=11, fontweight="bold", color="#B5651D")
    axL.set_title("nx.has_path(B, C): обходить граф по ребрах", fontsize=12)
    axL.set_axis_off(); axL.margins(0.16)
    axL.text(0.5, -0.04,
             "BFS від B крокує по ребрах: B → A → E → D → C …\n"
             "відвідано 5 вузлів, поки знайдено C  →  шлях є  →  ЦИКЛ",
             transform=axL.transAxes, ha="center", va="top", fontsize=9.5, color="#333")

    # ===== ПРАВОРУЧ: DSU (підняття до кореня) =====
    parent = {"A": "A", "B": "A", "C": "A", "D": "A", "E": "C", "F": "A", "G": "G"}   # стан після 5 union
    D = nx.DiGraph(); D.add_nodes_from(parent)
    for ch, pa in parent.items():
        if ch != pa:
            D.add_edge(ch, pa)
    find_edges = [("B", "A"), ("C", "A")]
    other_edges = [e for e in D.edges() if e not in find_edges]
    dcolors = [C_ROOT if n == "A" else (C_PATH if n in ("B", "C") else C_NODE) for n in D.nodes()]
    nx.draw_networkx_nodes(D, DPOS, ax=axR, node_size=900, node_color=dcolors,
                           edgecolors=C_EDGE, linewidths=1.8)
    nx.draw_networkx_labels(D, DPOS, ax=axR, font_size=12, font_weight="bold", font_color="#15384A")
    nx.draw_networkx_edges(D, DPOS, ax=axR, edgelist=other_edges, edge_color=C_ARROW, width=1.8,
                           arrows=True, arrowstyle="-|>", arrowsize=18, node_size=900,
                           min_source_margin=16, min_target_margin=16)
    nx.draw_networkx_edges(D, DPOS, ax=axR, edgelist=find_edges, edge_color=C_PATH, width=3.4,
                           arrows=True, arrowstyle="-|>", arrowsize=22, node_size=900,
                           min_source_margin=16, min_target_margin=16)
    rx, ry = DPOS["A"]
    axR.annotate("корінь A", (rx, ry), xytext=(rx + 0.35, ry + 0.18), fontsize=10, color=C_ROOT, fontweight="bold")
    axR.set_title("DSU: find(B) == find(C)? — підняття до кореня", fontsize=12)
    axR.set_axis_off(); axR.margins(0.16)
    axR.text(0.5, -0.04,
             "find(B): B → A (1 стрибок);  find(C): C → A (1 стрибок)\n"
             "корені однакові (A == A)  →  ЦИКЛ",
             transform=axR.transAxes, ha="center", va="top", fontsize=9.5, color="#333")

    fig.suptitle("Перевірка «чи B і C вже з'єднані?» (крок 8, ребро B–C)",
                 fontsize=13, fontweight="bold", y=1.0)
    fig.subplots_adjust(top=0.9, bottom=0.14, wspace=0.05)
    return fig
