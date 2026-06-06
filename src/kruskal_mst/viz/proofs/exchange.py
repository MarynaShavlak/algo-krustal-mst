# -*- coding: utf-8 -*-
"""Схема аргументу обміну: важче ребро циклу міняємо на легше ребро Краскала."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx

from ...graph import POS_EX
from ..core.palette import C_NODE, C_NODE_EDGE, CHIP
from ..core.i18n import t

C_FAINT = "#DBDBDB"
C_TREE = "#2E8B57"       # ребро дерева
C_ADD = "#F4A300"        # додаємо (легше ребро Краскала)
C_REMOVE = "#E63946"     # прибираємо (важче ребро з циклу)


def exchange_argument(G, pos=POS_EX):
    """Побудувати двопанельну фігуру: інше дерево T* з циклом -> після обміну = дерево Краскала."""
    norm = lambda e: tuple(sorted(e))
    W = lambda e: G[e[0]][e[1]]["weight"]

    def panel(ax, green, red=None, dashed=None, title="", wlabels=None):
        special = (set(map(norm, green))
                   | ({norm(red)} if red else set())
                   | ({norm(dashed)} if dashed else set()))
        base = [(u, v) for u, v in G.edges() if norm((u, v)) not in special]
        eb = nx.draw_networkx_edges(G, pos, ax=ax, edgelist=base, edge_color=C_FAINT, width=1.4)
        if eb is not None:
            eb.set_zorder(1)
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=green, edge_color=C_TREE, width=3.2).set_zorder(2)
        if red:
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[red], edge_color=C_REMOVE, width=3.6).set_zorder(2)
        if dashed:
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[dashed], edge_color=C_ADD,
                                   width=3.6, style="dashed").set_zorder(2)
        nd = nx.draw_networkx_nodes(G, pos, ax=ax, node_size=780, node_color=C_NODE,
                                    edgecolors=C_NODE_EDGE, linewidths=1.7)
        nd.set_zorder(3)
        for txt in nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight="bold",
                                         font_color="#15384A").values():
            txt.set_zorder(5)
        for e in (wlabels or []):
            x = (pos[e[0]][0] + pos[e[1]][0]) / 2
            y = (pos[e[0]][1] + pos[e[1]][1]) / 2
            ax.text(x, y, str(W(e)), fontsize=9.5, ha="center", va="center", bbox=CHIP).set_zorder(4)
        ax.set_title(title, fontsize=11.5)
        ax.set_axis_off()
        ax.margins(0.13)

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.6))

    # T* = {A-B, B-D, C-E, B-E, D-F, E-G}; додаємо A-D -> цикл A-B-D; прибираємо B-D
    panel(axL, green=[("A", "B"), ("C", "E"), ("B", "E"), ("D", "F"), ("E", "G")],
          red=("B", "D"), dashed=("A", "D"),
          title=t("Інше дерево T* (вага 43): додаємо A\u2013D -> цикл A\u2013B\u2013D"),
          wlabels=[("A", "B"), ("B", "D"), ("A", "D")])
    axL.annotate(t("цикл A\u2013B\u2013D"), (2.4, 3.0), fontsize=10, color="#444", style="italic")
    axL.annotate(t("+ A\u2013D (5): легше,\nКраскал обрав його"), (pos["A"][0], pos["A"][1]),
                 xytext=(4.3, 4.0), fontsize=9.5, color=C_ADD, fontweight="bold", ha="left")
    axL.annotate(t("B\u2013D (9): найважче в циклі\n-> прибираємо"), (pos["B"][0] + 1.5, 2.8),
                 xytext=(0.2, 1.7), fontsize=9.5, color=C_REMOVE, fontweight="bold", ha="left",
                 arrowprops=dict(arrowstyle="->", color=C_REMOVE, lw=1.5))

    # T = {A-D, A-B, C-E, B-E, D-F, E-G}, вага 39
    panel(axR, green=[("A", "D"), ("A", "B"), ("C", "E"), ("B", "E"), ("D", "F"), ("E", "G")],
          title=t("Після обміну (B\u2013D -> A\u2013D) = дерево Краскала T (вага 39)"),
          wlabels=[("A", "D"), ("A", "B")])
    axR.annotate(t("B\u2013D більше немає"), (2.4, 2.85), xytext=(0.2, 1.6), fontsize=9.5,
                 color="#888", ha="left", arrowprops=dict(arrowstyle="->", color="#bbb", lw=1.3))

    fig.legend(handles=[
        Line2D([0], [0], color=C_TREE, lw=3.2, label=t("ребро дерева")),
        Line2D([0], [0], color=C_ADD, lw=3.2, ls="--", label=t("додаємо (e = A\u2013D, легше)")),
        Line2D([0], [0], color=C_REMOVE, lw=3.2, label=t("прибираємо (f = B\u2013D, важче)")),
        Line2D([0], [0], color=C_FAINT, lw=2.2, label=t("інші ребра графа")),
    ], loc="lower center", ncol=4, fontsize=9, frameon=False, bbox_to_anchor=(0.5, 0.0))
    fig.suptitle(t("Аргумент обміну: важче ребро B\u2013D міняємо на легше A\u2013D — вага падає 43 -> 39"),
                 fontsize=12.5, fontweight="bold")
    fig.tight_layout(rect=[0, 0.06, 1, 0.95])
    return fig
