# -*- coding: utf-8 -*-
"""Анімація «як DSU будується зсередини» на 5 елементах.

Показує кілька ``union`` (із об'єднанням за рангом), а потім ``find(D)`` зі
стисненням шляху. ``build_dsu_build_animation()`` повертає ``(fig, anim)`` —
готовий ``FuncAnimation``, який можна зберегти у GIF (Pillow) чи MP4 (ffmpeg).
"""

from __future__ import annotations

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.animation import FuncAnimation

from ..core.palette import (
    C_NODE, C_NODE_EDGE, C_MST, C_CONSIDER, ROOT_BORDER, FOUND_BORDER, A_DSU, A_HI,
)

# Власна (5-вузлова) розкладка саме для цієї анімації
POS = {"A": (2.0, 3.0), "B": (0.5, 1.6), "C": (2.0, 1.6), "E": (3.5, 1.6), "D": (3.1, 0.4)}
NODES = ["A", "B", "C", "D", "E"]
P_BUILT = {"A": "A", "B": "A", "C": "A", "D": "C", "E": "A"}   # стан після всіх union (D→C→A)
R_BUILT = {"A": 2, "B": 0, "C": 1, "D": 0, "E": 0}

STATES = [
    dict(parent={n: n for n in NODES}, rank={n: 0 for n in NODES},
         desc="Старт: кожен елемент — сам собі корінь. 5 окремих дерев, усі ранги = 0."),
    dict(parent={"A": "A", "B": "A", "C": "C", "D": "D", "E": "E"}, rank={"A": 1, "B": 0, "C": 0, "D": 0, "E": 0},
         desc="union(A, B): ранги рівні (0 = 0) → B під A; ранг A → 1.", new=("B", "A")),
    dict(parent={"A": "A", "B": "A", "C": "C", "D": "C", "E": "E"}, rank={"A": 1, "B": 0, "C": 1, "D": 0, "E": 0},
         desc="union(C, D): ранги рівні (0 = 0) → D під C; ранг C → 1.", new=("D", "C")),
    dict(parent={"A": "A", "B": "A", "C": "A", "D": "C", "E": "E"}, rank={"A": 2, "B": 0, "C": 1, "D": 0, "E": 0},
         desc="union(A, C): корені A і C мають рівні ранги (1 = 1) → C під A; ранг A → 2.\nТепер D на глибині 2:  D → C → A.", new=("C", "A")),
    dict(parent=dict(P_BUILT), rank=dict(R_BUILT),
         desc="union(A, E): ранг A (2) більший за ранг E (0) → E під A. Ранг A не змінюється.", new=("E", "A")),
    dict(parent=dict(P_BUILT), rank=dict(R_BUILT),
         desc="find(D): старт у D. Його батько — C. Піднімаємось до C.", current="D", climb=("D", "C")),
    dict(parent=dict(P_BUILT), rank=dict(R_BUILT),
         desc="Ми в C. Його батько — A. Піднімаємось до A.", current="C", climb=("C", "A")),
    dict(parent=dict(P_BUILT), rank=dict(R_BUILT),
         desc="Ми в A. parent[A] = A — це КОРІНЬ. Отже find(D) = A.", found="A"),
    dict(parent={"A": "A", "B": "A", "C": "A", "D": "A", "E": "A"}, rank=dict(R_BUILT),
         desc="Стиснення шляху: пройдені вузли чіпляємо прямо до кореня.\nБуло D → C → A, стало D → A (на 1 стрибок).", found="A", comp=("D", "A")),
]


def _draw_state(ax, i):
    ax.clear()
    st = STATES[i]; parent, rank = st["parent"], st["rank"]
    D = nx.DiGraph(); D.add_nodes_from(NODES)
    for ch, pa in parent.items():
        if ch != pa:
            D.add_edge(ch, pa)

    face, edge, lw = [], [], []
    for n in NODES:
        is_root = parent[n] == n
        if st.get("found") == n:
            face.append(C_MST); edge.append(FOUND_BORDER); lw.append(2.6)
        elif st.get("current") == n:
            face.append(C_CONSIDER); edge.append(C_NODE_EDGE); lw.append(2.2)
        else:
            face.append(C_NODE); edge.append(ROOT_BORDER if is_root else C_NODE_EDGE)
            lw.append(2.6 if is_root else 1.6)

    special, scol = None, None
    if st.get("new"):   special, scol = st["new"], A_HI
    if st.get("climb"): special, scol = st["climb"], A_HI
    if st.get("comp"):  special, scol = st["comp"], C_MST
    normal = [e for e in D.edges() if e != special]
    nx.draw_networkx_edges(D, POS, ax=ax, edgelist=normal, edge_color=A_DSU, width=1.8,
                           arrows=True, arrowstyle="-|>", arrowsize=20, node_size=1100,
                           min_source_margin=16, min_target_margin=18)
    if special and special in D.edges():
        nx.draw_networkx_edges(D, POS, ax=ax, edgelist=[special], edge_color=scol, width=3.6,
                               arrows=True, arrowstyle="-|>", arrowsize=24, node_size=1100,
                               min_source_margin=16, min_target_margin=18)

    nx.draw_networkx_nodes(D, POS, ax=ax, node_size=1100, node_color=face,
                           edgecolors=edge, linewidths=lw)
    nx.draw_networkx_labels(D, POS, ax=ax, font_size=14, font_weight="bold", font_color="#15384A")
    for n in NODES:
        if parent[n] == n:
            x, y = POS[n]
            tag = "КОРІНЬ" if st.get("found") == n else "корінь"
            ax.annotate(f"{tag}, ранг {rank[n]}", (x, y), xytext=(x, y + 0.42), ha="center",
                        fontsize=8.5, fontweight="bold",
                        color=FOUND_BORDER if st.get("found") == n else "#B5651D")

    ax.set_title(f"Крок {i + 1}/{len(STATES)}:  {st['desc']}", fontsize=10.5)
    ax.set_xlim(-0.6, 4.4); ax.set_ylim(-0.4, 3.9); ax.set_axis_off()
    handles = [Patch(facecolor=C_NODE, edgecolor=ROOT_BORDER, linewidth=2, label="корінь (сам собі батько)"),
               Patch(facecolor=C_NODE, edgecolor=C_NODE_EDGE, label="звичайний вузол"),
               Patch(facecolor=C_CONSIDER, edgecolor=C_NODE_EDGE, label="де ми зараз (find)"),
               Patch(facecolor=C_MST, edgecolor=FOUND_BORDER, label="знайдений корінь")]
    ax.legend(handles=handles, loc="upper left", fontsize=8, frameon=False, bbox_to_anchor=(-0.02, 1.0))


def build_dsu_build_animation():
    """Зібрати анімацію побудови DSU. Повертає ``(fig, anim)`` (фігуру не закриває)."""
    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    fig.subplots_adjust(top=0.86, bottom=0.04)
    anim = FuncAnimation(fig, lambda i: _draw_state(ax, i), frames=len(STATES), interval=2000)
    return fig, anim
