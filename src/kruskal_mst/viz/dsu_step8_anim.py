# -*- coding: utf-8 -*-
"""Анімація: звідки взялася структура DSU на кроці 8.

Показує, як 5 ребер МОД (A–D, C–E, D–F, A–B, B–E) через ``union`` за рангом
будують структуру DSU, а потім — перевірку B–C (``find(B) == find(C)`` → цикл).
``build_dsu_step8_animation()`` повертає ``(fig, anim)`` для збереження у GIF/MP4.
"""

from __future__ import annotations

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.animation import FuncAnimation

S_NODE = "#A8D8EA"; S_CUR = "#F4A300"; S_FOUND = "#2E8B57"
ROOT_BORDER = "#C8860D"; NODE_BORDER = "#2C6E8F"; FOUND_BORDER = "#1E5E3A"
A_NORMAL = "#9AA0A6"; A_HI = "#F08A00"

NODES = ["A", "B", "C", "D", "E", "F", "G"]
POS = {"A": (2.5, 3.3), "B": (0.7, 2.0), "C": (2.0, 2.0), "D": (3.3, 2.0), "F": (4.5, 2.0),
       "E": (2.0, 0.7), "G": (5.5, 1.2)}
P_FINAL = {"A": "A", "B": "A", "C": "A", "D": "A", "E": "C", "F": "A", "G": "G"}   # структура перед кроком 8
R_FINAL = {"A": 2, "B": 0, "C": 1, "D": 0, "E": 0, "F": 0, "G": 0}

STATES = [
    dict(parent={n: n for n in NODES}, rank={n: 0 for n in NODES},
         desc="Старт DSU: усі 7 вершин — окремі корені (ранг 0). Ребер ще не додано."),
    dict(parent={"A": "A", "D": "A", "B": "B", "C": "C", "E": "E", "F": "F", "G": "G"},
         rank={"A": 1, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0},
         desc="Ребро A–D додано до МОД → union(A, D). Ранги рівні (0 = 0) → D під A; ранг A → 1.", new=("D", "A")),
    dict(parent={"A": "A", "D": "A", "C": "C", "E": "C", "B": "B", "F": "F", "G": "G"},
         rank={"A": 1, "B": 0, "C": 1, "D": 0, "E": 0, "F": 0, "G": 0},
         desc="Ребро C–E → union(C, E). Ранги рівні (0 = 0) → E під C; ранг C → 1.", new=("E", "C")),
    dict(parent={"A": "A", "D": "A", "F": "A", "C": "C", "E": "C", "B": "B", "G": "G"},
         rank={"A": 1, "B": 0, "C": 1, "D": 0, "E": 0, "F": 0, "G": 0},
         desc="Ребро D–F → union(D, F). Корінь D — це A. Ранг A (1) > ранг F (0) → F під A.", new=("F", "A")),
    dict(parent={"A": "A", "D": "A", "F": "A", "B": "A", "C": "C", "E": "C", "G": "G"},
         rank={"A": 1, "B": 0, "C": 1, "D": 0, "E": 0, "F": 0, "G": 0},
         desc="Ребро A–B → union(A, B). Ранг A (1) > ранг B (0) → B під A.", new=("B", "A")),
    dict(parent=dict(P_FINAL), rank=dict(R_FINAL),
         desc="Ребро B–E → union(B, E). Корінь B — A, корінь E — C; ранги рівні (1 = 1) → C під A; ранг A → 2.\nОсь і вся структура DSU перед кроком 8.", new=("C", "A")),
    dict(parent=dict(P_FINAL), rank=dict(R_FINAL),
         desc="Крок 8 — перевіряємо ребро B–C. find(B): B → A (1 стрибок).", current="B", climb=("B", "A")),
    dict(parent=dict(P_FINAL), rank=dict(R_FINAL),
         desc="find(C): C → A (1 стрибок).", current="C", climb=("C", "A")),
    dict(parent=dict(P_FINAL), rank=dict(R_FINAL),
         desc="Корені однакові: find(B) = find(C) = A → B і C вже в одній множині → ЦИКЛ.\nРебро B–C пропускаємо.",
         found="A", check_nodes=["B", "C"], check_edges=[("B", "A"), ("C", "A")]),
]


def _draw_state(ax, i):
    ax.clear()
    st = STATES[i]; parent, rank = st["parent"], st["rank"]
    D = nx.DiGraph(); D.add_nodes_from(NODES)
    for ch, pa in parent.items():
        if ch != pa:
            D.add_edge(ch, pa)
    cur_set = set(st.get("check_nodes", []))
    if st.get("current"):
        cur_set.add(st["current"])

    face, edge, lw = [], [], []
    for n in NODES:
        is_root = parent[n] == n
        if st.get("found") == n:
            face.append(S_FOUND); edge.append(FOUND_BORDER); lw.append(2.6)
        elif n in cur_set:
            face.append(S_CUR); edge.append(NODE_BORDER); lw.append(2.2)
        else:
            face.append(S_NODE); edge.append(ROOT_BORDER if is_root else NODE_BORDER)
            lw.append(2.6 if is_root else 1.6)

    hi = set()
    if st.get("new"):
        hi.add(st["new"])
    if st.get("climb"):
        hi.add(st["climb"])
    for e in st.get("check_edges", []):
        hi.add(e)
    normal = [e for e in D.edges() if e not in hi]
    nx.draw_networkx_edges(D, POS, ax=ax, edgelist=normal, edge_color=A_NORMAL, width=1.8,
                           arrows=True, arrowstyle="-|>", arrowsize=18, node_size=1000,
                           min_source_margin=15, min_target_margin=17)
    hi_present = [e for e in hi if e in D.edges()]
    if hi_present:
        nx.draw_networkx_edges(D, POS, ax=ax, edgelist=hi_present, edge_color=A_HI, width=3.4,
                               arrows=True, arrowstyle="-|>", arrowsize=22, node_size=1000,
                               min_source_margin=15, min_target_margin=17)

    nx.draw_networkx_nodes(D, POS, ax=ax, node_size=1000, node_color=face,
                           edgecolors=edge, linewidths=lw)
    nx.draw_networkx_labels(D, POS, ax=ax, font_size=13, font_weight="bold", font_color="#15384A")
    for n in NODES:
        if parent[n] == n:
            x, y = POS[n]
            tag = "КОРІНЬ" if st.get("found") == n else "корінь"
            ax.annotate(f"{tag} р={rank[n]}", (x, y), xytext=(x, y + 0.40), ha="center",
                        fontsize=8, fontweight="bold",
                        color=FOUND_BORDER if st.get("found") == n else "#B5651D")

    ax.set_title(f"Крок {i + 1}/{len(STATES)}:  {st['desc']}", fontsize=10)
    ax.set_xlim(-0.3, 6.3); ax.set_ylim(0.2, 4.0); ax.set_axis_off()
    handles = [Patch(facecolor=S_NODE, edgecolor=ROOT_BORDER, linewidth=2, label="корінь"),
               Patch(facecolor=S_NODE, edgecolor=NODE_BORDER, label="звичайний вузол"),
               Patch(facecolor=S_CUR, edgecolor=NODE_BORDER, label="де ми зараз (find)"),
               Patch(facecolor=S_FOUND, edgecolor=FOUND_BORDER, label="знайдений корінь")]
    ax.legend(handles=handles, loc="lower left", fontsize=8, frameon=False, bbox_to_anchor=(-0.02, -0.02), ncol=2)


def build_dsu_step8_animation():
    """Зібрати анімацію побудови структури DSU перед кроком 8. Повертає ``(fig, anim)``."""
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    fig.subplots_adjust(top=0.84, bottom=0.03)
    anim = FuncAnimation(fig, lambda i: _draw_state(ax, i), frames=len(STATES), interval=2000)
    return fig, anim
