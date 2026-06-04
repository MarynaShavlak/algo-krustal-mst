# -*- coding: utf-8 -*-
"""Малювальник дерева вказівників DSU (ліс «вказівник на батька»)."""

from __future__ import annotations

import networkx as nx

from ..graph import POS_DSU
from .palette import C_NODE, C_NODE_EDGE, C_CONSIDER, ROOT_BORDER, A_DSU


def draw_dsu_forest(ax, parent, rank, highlight=None, new_link=None, pos=POS_DSU):
    """Намалювати ліс вказівників DSU за станом ``parent``/``rank``.

    Параметри:
        parent     — мапа {вузол: батько}; корінь показує сам на себе;
        rank        — мапа {вузол: ранг} (підписується біля коренів);
        highlight   — множина вузлів, які підсвітити помаранчевим;
        new_link    — щойно додана зв'язка (child, parent) — помаранчева стрілка.
    """
    highlight = set(highlight or [])
    D = nx.DiGraph()
    D.add_nodes_from(parent.keys())
    for ch, pa in parent.items():
        if ch != pa:
            D.add_edge(ch, pa)

    face, edge, lw = [], [], []
    for n in D.nodes():
        is_root = parent[n] == n
        if n in highlight:
            face.append(C_CONSIDER); edge.append(C_NODE_EDGE); lw.append(2.2)
        else:
            face.append(C_NODE)
            edge.append(ROOT_BORDER if is_root else C_NODE_EDGE)
            lw.append(2.6 if is_root else 1.5)

    normal = [e for e in D.edges() if e != new_link]
    nx.draw_networkx_edges(D, pos, ax=ax, edgelist=normal, edge_color=A_DSU, width=1.7,
                           arrows=True, arrowstyle="-|>", arrowsize=15, node_size=640,
                           min_source_margin=12, min_target_margin=14)
    if new_link and new_link in D.edges():
        nx.draw_networkx_edges(D, pos, ax=ax, edgelist=[new_link], edge_color=C_CONSIDER,
                               width=3.2, arrows=True, arrowstyle="-|>", arrowsize=20,
                               node_size=640, min_source_margin=12, min_target_margin=14)
    nx.draw_networkx_nodes(D, pos, ax=ax, node_size=640, node_color=face,
                           edgecolors=edge, linewidths=lw)
    nx.draw_networkx_labels(D, pos, ax=ax, font_size=10, font_weight="bold",
                            font_color="#15384A")
    for n in D.nodes():
        if parent[n] == n:
            x, y = pos[n]
            ax.annotate(f"р{rank[n]}", (x, y), xytext=(x, y + 0.40), ha="center",
                        fontsize=7.5, color="#B5651D", fontweight="bold")
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(0.2, 4.0)
    ax.set_axis_off()
