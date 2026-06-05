# -*- coding: utf-8 -*-
"""Універсальний малювальник графа з підсвічуванням стану алгоритму."""

from __future__ import annotations

import networkx as nx

from ...graph import POS
from .palette import (
    C_NODE, C_NODE_EDGE, C_BASE_EDGE, C_MST, C_REJECT, C_CONSIDER, COMP_PALETTE,
)


def draw_graph(G, ax, mst_set=None, consider=None, consider_ok=None,
               comp=None, title=None, pos=POS):
    """Намалювати граф у заданих осях.

    Параметри:
        mst_set     — множина ребер (як відсортованих кортежів), що вже у МОД;
        consider    — ребро, яке зараз розглядається;
        consider_ok — True, якщо це ребро приймається (інакше малюється як цикл);
        comp        — словник {вершина: корінь компоненти} для розфарбування вершин;
        pos         — координати вершин (за замовчуванням — спільні POS).
    """
    mst_set = mst_set or set()
    norm = lambda e: tuple(sorted(e))

    # колір вершин — за компонентою зв'язності
    if comp is not None:
        roots = sorted(set(comp.values()))
        cmap = {r: COMP_PALETTE[i % len(COMP_PALETTE)] for i, r in enumerate(roots)}
        node_colors = [cmap[comp[n]] for n in G.nodes()]
    else:
        node_colors = C_NODE

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=820, node_color=node_colors,
                           edgecolors=C_NODE_EDGE, linewidths=1.8)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight="bold",
                            font_color="#15384A")

    base, mst_e, rej_e, con_e = [], [], [], []
    for u, v in G.edges():
        e = norm((u, v))
        if consider is not None and e == norm(consider):
            (con_e if consider_ok else rej_e).append((u, v))
        elif e in mst_set:
            mst_e.append((u, v))
        else:
            base.append((u, v))

    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=base, edge_color=C_BASE_EDGE, width=1.6)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=mst_e, edge_color=C_MST, width=3.2)
    if con_e:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=con_e, edge_color=C_CONSIDER, width=3.6)
    if rej_e:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=rej_e, edge_color=C_REJECT,
                               width=3.0, style="dashed")

    nx.draw_networkx_edge_labels(
        G, pos, ax=ax, edge_labels=nx.get_edge_attributes(G, "weight"),
        font_size=10, rotate=False,
        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))

    if title:
        ax.set_title(title, fontsize=11)
    ax.set_axis_off()
    ax.margins(0.12)
