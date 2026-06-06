# -*- coding: utf-8 -*-
"""Анімації BFS усередині ``nx.has_path`` (обхід лісу перед кроком 8).

* ``build_bfs_found_animation()``    — BFS від B шукає C: шлях знайдено → ребро B–C дало б цикл (§11);
* ``build_bfs_notfound_animation()`` — BFS від E шукає G: ціль недосяжна → ребро E–G безпечно додати (§12).

Кожна повертає ``(fig, anim)`` — готовий ``FuncAnimation`` для збереження у GIF/MP4.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.animation import FuncAnimation
from ..core.i18n import t
import networkx as nx

from ...graph import build_graph, POS
from ..core.palette import (
    C_NODE, C_NODE_EDGE, C_MST, C_REJECT, C_CONSIDER, S_QUEUE, S_DONE, E_BASE, E_FAINT, A_HI,
)

# Спільний граф і ліс (ребра, вже додані до МОД перед кроком 8)
G = build_graph()
FOREST_EDGES = [("A", "D"), ("C", "E"), ("D", "F"), ("A", "B"), ("B", "E")]   # ребра, вже у МОД
norm = lambda e: tuple(sorted(e))
fset = {norm(e) for e in FOREST_EDGES}
non_forest = [(u, v) for u, v in G.edges() if norm((u, v)) not in fset]


def build_bfs_found_animation():
    """BFS від B шукає C — шлях знайдено (ребро B–C дало б цикл)."""
    # Кадри BFS від B у пошуках C
    frames = [
        dict(desc="Старт: кладемо стартову вершину B у чергу. Ціль — дістатися C.",
             state={"B": "queue"}, trav=set(), cons=[], queue=["B"]),
        dict(desc="Беремо з черги B (обробляємо). Дивимось її сусідів: A та E.",
             state={"B": "cur"}, trav=set(), cons=[("B", "A"), ("B", "E")], queue=[]),
        dict(desc="A і E ще не відвідані → кладемо їх у чергу. (A≠C, E≠C)",
             state={"B": "done", "A": "queue", "E": "queue"}, trav={norm(("A", "B")), norm(("B", "E"))},
             cons=[], queue=["A", "E"]),
        dict(desc="Беремо з черги A (обробляємо). Дивимось її сусідів: D та B.",
             state={"B": "done", "A": "cur", "E": "queue"}, trav={norm(("A", "B")), norm(("B", "E"))},
             cons=[("A", "D"), ("A", "B")], queue=["E"]),
        dict(desc="D нове → у чергу. B вже відвідане → пропускаємо. (D≠C)",
             state={"B": "done", "A": "done", "E": "queue", "D": "queue"},
             trav={norm(("A", "B")), norm(("B", "E")), norm(("A", "D"))}, cons=[], queue=["E", "D"]),
        dict(desc="Беремо з черги E (обробляємо). Дивимось її сусідів: C та B.",
             state={"B": "done", "A": "done", "E": "cur", "D": "queue"},
             trav={norm(("A", "B")), norm(("B", "E")), norm(("A", "D"))},
             cons=[("C", "E"), ("B", "E")], queue=["D"]),
        dict(desc="C — це наша ціль! ЗНАЙДЕНО. Маршрут: B → E → C.",
             state={"B": "done", "A": "done", "E": "done", "D": "queue", "C": "found"},
             trav={norm(("A", "B")), norm(("B", "E")), norm(("A", "D")), norm(("C", "E"))},
             cons=[], queue=["D"], path=[norm(("B", "E")), norm(("C", "E"))]),
        dict(desc="Шлях B → E → C існує → B і C в одній компоненті → ЦИКЛ. Ребро B–C пропускаємо.",
             state={"B": "done", "A": "done", "E": "done", "D": "queue", "C": "found"},
             trav={norm(("A", "B")), norm(("B", "E")), norm(("A", "D")), norm(("C", "E"))},
             cons=[], queue=[], path=[norm(("B", "E")), norm(("C", "E"))]),
    ]
    NODE_COL = {"new": C_NODE, "queue": S_QUEUE, "cur": C_CONSIDER, "done": S_DONE, "found": C_MST}

    def draw_frame(ax, i):
        ax.clear()
        fr = frames[i]
        state, trav = fr["state"], fr["trav"]
        cons = {norm(e) for e in fr["cons"]}
        path = {norm(e) for e in fr.get("path", [])}
        colors = [NODE_COL.get(state.get(n, "new")) for n in G.nodes()]

        nx.draw_networkx_edges(G, POS, ax=ax, edgelist=non_forest, edge_color=E_FAINT, width=1.0, style="dotted")
        base = [(u, v) for u, v in G.edges() if norm((u, v)) in fset and norm((u, v)) not in trav and norm((u, v)) not in cons]
        tr = [(u, v) for u, v in G.edges() if norm((u, v)) in trav and norm((u, v)) not in path]
        nx.draw_networkx_edges(G, POS, ax=ax, edgelist=base, edge_color=E_BASE, width=1.8)
        nx.draw_networkx_edges(G, POS, ax=ax, edgelist=tr, edge_color=A_HI, width=3.0)
        if path:
            pe = [(u, v) for u, v in G.edges() if norm((u, v)) in path]
            nx.draw_networkx_edges(G, POS, ax=ax, edgelist=pe, edge_color=A_HI, width=5.0)
        if cons:
            ce = [(u, v) for u, v in G.edges() if norm((u, v)) in cons]
            nx.draw_networkx_edges(G, POS, ax=ax, edgelist=ce, edge_color=C_REJECT, width=3.0, style="dashed")

        nx.draw_networkx_nodes(G, POS, ax=ax, node_size=900, node_color=colors,
                               edgecolors=C_NODE_EDGE, linewidths=1.8)
        nx.draw_networkx_labels(G, POS, ax=ax, font_size=12, font_weight="bold", font_color="#15384A")
        cx, cy = POS["C"]
        ax.annotate(t("ціль"), (cx, cy), xytext=(cx - 0.75, cy + 0.10), fontsize=9.5, color="#2E8B57", fontweight="bold")

        ax.set_title(f"{t('Крок')} {i + 1}/{len(frames)}:  {t(fr['desc'])}", fontsize=11)
        q = ", ".join(fr["queue"]) if fr["queue"] else "—"
        ax.text(0.5, -0.05, t("Черга (наступні до обробки): [ {q} ]").format(q=q),
                transform=ax.transAxes, ha="center", va="top", fontsize=10, color="#333")
        ax.set_axis_off(); ax.margins(0.14)
        handles = [Patch(facecolor=C_NODE, edgecolor=C_NODE_EDGE, label=t("ще не відвідано")),
                   Patch(facecolor=S_QUEUE, edgecolor=C_NODE_EDGE, label=t("у черзі")),
                   Patch(facecolor=C_CONSIDER, edgecolor=C_NODE_EDGE, label=t("обробляємо зараз")),
                   Patch(facecolor=S_DONE, edgecolor=C_NODE_EDGE, label=t("відвідано")),
                   Patch(facecolor=C_MST, edgecolor=C_NODE_EDGE, label=t("знайдено ціль"))]
        ax.legend(handles=handles, loc="upper left", fontsize=8.5, frameon=False, bbox_to_anchor=(-0.02, 1.02))

    fig, ax = plt.subplots(figsize=(7.5, 5.6))
    fig.subplots_adjust(top=0.9, bottom=0.1)
    anim = FuncAnimation(fig, lambda i: draw_frame(ax, i), frames=len(frames), interval=1800)
    return fig, anim


def build_bfs_notfound_animation():
    """BFS від E шукає G — ціль недосяжна (ребро E–G безпечно додати)."""
    EC, EB, BA, AD, DF = norm(("C", "E")), norm(("B", "E")), norm(("A", "B")), norm(("A", "D")), norm(("D", "F"))

    # Кадри BFS від E у пошуках G (якого немає в цій компоненті)
    frames = [
        dict(desc="Старт: кладемо стартову вершину E у чергу. Ціль — дістатися G.",
             state={"E": "queue"}, trav=set(), queue=["E"]),
        dict(desc="Обробляємо E. Сусіди C і B — нові → у чергу. (жодне ≠ G)",
             state={"E": "cur", "C": "queue", "B": "queue"}, trav={EC, EB}, queue=["C", "B"]),
        dict(desc="Обробляємо C. Єдиний сусід E вже відвіданий → пропуск. Нічого нового.",
             state={"E": "done", "C": "cur", "B": "queue"}, trav={EC, EB}, queue=["B"]),
        dict(desc="Обробляємо B. A — нове → у чергу; E вже відвідане → пропуск. (A ≠ G)",
             state={"E": "done", "C": "done", "B": "cur", "A": "queue"}, trav={EC, EB, BA}, queue=["A"]),
        dict(desc="Обробляємо A. D — нове → у чергу; B вже відвідане → пропуск. (D ≠ G)",
             state={"E": "done", "C": "done", "B": "done", "A": "cur", "D": "queue"}, trav={EC, EB, BA, AD}, queue=["D"]),
        dict(desc="Обробляємо D. F — нове → у чергу; A вже відвідане → пропуск. (F ≠ G)",
             state={"E": "done", "C": "done", "B": "done", "A": "done", "D": "cur", "F": "queue"}, trav={EC, EB, BA, AD, DF}, queue=["F"]),
        dict(desc="Обробляємо F. Сусід D вже відвіданий → пропуск.\nЧерга спорожніла!",
             state={"E": "done", "C": "done", "B": "done", "A": "done", "D": "done", "F": "cur"}, trav={EC, EB, BA, AD, DF}, queue=[]),
        dict(desc="Черга порожня, G так і не знайдено → шляху немає.\nРізні компоненти → ребро E–G ДОДАЄМО.",
             state={"E": "done", "C": "done", "B": "done", "A": "done", "D": "done", "F": "done"}, trav={EC, EB, BA, AD, DF}, queue=[], added=[("E", "G")]),
    ]
    NODE_COL = {"new": C_NODE, "queue": S_QUEUE, "cur": C_CONSIDER, "done": S_DONE}

    def draw_frame(ax, i):
        ax.clear()
        fr = frames[i]; state, trav = fr["state"], fr["trav"]
        added = {norm(e) for e in fr.get("added", [])}
        colors = [NODE_COL.get(state.get(n, "new")) for n in G.nodes()]

        nx.draw_networkx_edges(G, POS, ax=ax, edgelist=non_forest, edge_color=E_FAINT, width=1.0, style="dotted")
        base = [(u, v) for u, v in G.edges() if norm((u, v)) in fset and norm((u, v)) not in trav]
        tr = [(u, v) for u, v in G.edges() if norm((u, v)) in trav]
        nx.draw_networkx_edges(G, POS, ax=ax, edgelist=base, edge_color=E_BASE, width=1.8)
        nx.draw_networkx_edges(G, POS, ax=ax, edgelist=tr, edge_color=A_HI, width=3.0)
        if added:
            ae = [(u, v) for u, v in G.edges() if norm((u, v)) in added]
            nx.draw_networkx_edges(G, POS, ax=ax, edgelist=ae, edge_color=C_MST, width=4.5)

        nx.draw_networkx_nodes(G, POS, ax=ax, node_size=900, node_color=colors,
                               edgecolors=C_NODE_EDGE, linewidths=1.8)
        nx.draw_networkx_labels(G, POS, ax=ax, font_size=12, font_weight="bold", font_color="#15384A")
        gx, gy = POS["G"]
        ax.annotate(t("ціль"), (gx, gy), xytext=(gx - 0.05, gy - 0.55), fontsize=9.5, color="#B5651D", fontweight="bold")

        ax.set_title(f"{t('Крок')} {i + 1}/{len(frames)}:  {t(fr['desc'])}", fontsize=10.5)
        q = ", ".join(fr["queue"]) if fr["queue"] else t("—  (порожня)")
        ax.text(0.5, -0.05, t("Черга (наступні до обробки): [ {q} ]").format(q=q),
                transform=ax.transAxes, ha="center", va="top", fontsize=10, color="#333")
        ax.set_axis_off(); ax.margins(0.14)
        handles = [Patch(facecolor=C_NODE, edgecolor=C_NODE_EDGE, label=t("ще не відвідано")),
                   Patch(facecolor=S_QUEUE, edgecolor=C_NODE_EDGE, label=t("у черзі")),
                   Patch(facecolor=C_CONSIDER, edgecolor=C_NODE_EDGE, label=t("обробляємо зараз")),
                   Patch(facecolor=S_DONE, edgecolor=C_NODE_EDGE, label=t("відвідано"))]
        ax.legend(handles=handles, loc="upper left", fontsize=8.5, frameon=False, bbox_to_anchor=(-0.02, 1.02))

    fig, ax = plt.subplots(figsize=(7.5, 5.6))
    fig.subplots_adjust(top=0.88, bottom=0.1)
    anim = FuncAnimation(fig, lambda i: draw_frame(ax, i), frames=len(frames), interval=1800)
    return fig, anim
