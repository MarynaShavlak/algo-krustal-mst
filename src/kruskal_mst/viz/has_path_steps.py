# -*- coding: utf-8 -*-
"""Покрокова візуалізація лекційного варіанту (forest + has_path) для §6.

``has_path_steps_grid(G)`` рендерить усі 13 панелей (ініціалізація, сортування і по
одній на кожне з 11 ребер) в ОДНЕ зображення: кожен рядок — ``[код | граф]``, де ліворуч
підсвічено активні рядки коду, праворуч — стан графа (компоненти кольором, прийняте/
відкинуте ребро). Це грід-аналог окремих панелей з ноутбука.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import networkx as nx

from ..graph import POS

# ---------- Палітра ----------
C_NODE_EDGE = "#2C6E8F"; C_BASE_EDGE = "#DADDE0"
C_MST = "#2E8B57"; C_REJECT = "#E63946"; C_CONSIDER = "#F4A300"
COMP_PALETTE = ["#A8D8EA", "#F6C9C9", "#C9E4C5", "#FCE4A6",
                "#D7C9EC", "#F8C8DC", "#C9E9E9", "#E8D5B7"]
HL_ACTIVE = "#FFF1A8"   # рядок виконується зараз
HL_ADD = "#C7E9C0"      # гілка "додати ребро"
HL_SKIP = "#F7C5C5"     # гілка "пропустити (цикл)"

LEGEND_HANDLES = [
    Line2D([0], [0], color=C_BASE_EDGE, lw=2.4, label="ребро графа (кандидат, не в МОД)"),
    Line2D([0], [0], color=C_MST, lw=3.0, label="обране (у МОД)"),
    Line2D([0], [0], color=C_CONSIDER, lw=3.0, label="щойно додане"),
    Line2D([0], [0], color=C_REJECT, lw=3.0, ls="--", label="відкинуте (цикл)"),
]

# Рядки коду, які підсвічуємо
CODE = [
    "forest = nx.Graph()",
    "for node in graph.nodes():",
    "    forest.add_node(node)",
    "",
    "sorted_edges = sorted(graph.edges(data=True),",
    "                      key=lambda t: t[2]['weight'])",
    "",
    "for u, v, attr in sorted_edges:",
    "    if not nx.has_path(forest, u, v):",
    "        forest.add_edge(u, v)",
    "        mst.add_edge(u, v, weight=attr['weight'])",
    "    # else: u,v вже з'єднані -> цикл -> пропустити",
]


def _draw_code(ax, highlights):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    line_h = 1.0 / len(CODE)
    for i, line in enumerate(CODE):
        y = 1.0 - (i + 0.5) * line_h
        if i in highlights:
            ax.add_patch(Rectangle((0, y - line_h * 0.45), 1, line_h * 0.9,
                                   facecolor=highlights[i], edgecolor="none", zorder=0))
        ax.text(0.015, y, line, family="monospace", fontsize=10,
                va="center", ha="left", color="#1b1b1b", zorder=2)


def _draw_state(ax, G, pos, comp, mst_edges, consider=None, added=None, faint_only=False):
    mst_set = {tuple(sorted((a, b))) for a, b, *_ in mst_edges}
    roots = sorted(set(comp.values()))
    cmap = {r: COMP_PALETTE[i % len(COMP_PALETTE)] for i, r in enumerate(roots)}
    node_colors = [cmap[comp[n]] for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=720, node_color=node_colors,
                           edgecolors=C_NODE_EDGE, linewidths=1.7)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=11, font_weight="bold", font_color="#15384A")
    norm = lambda e: tuple(sorted(e))
    base, mst_e, con_e, rej_e = [], [], [], []
    for a, b in G.edges():
        e = norm((a, b))
        if consider is not None and e == norm(consider):
            (con_e if added else rej_e).append((a, b))
        elif e in mst_set:
            mst_e.append((a, b))
        else:
            base.append((a, b))
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=base, edge_color=C_BASE_EDGE, width=1.4)
    if not faint_only:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=mst_e, edge_color=C_MST, width=3.0)
        if con_e:
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=con_e, edge_color=C_CONSIDER, width=3.6)
        if rej_e:
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=rej_e, edge_color=C_REJECT,
                                   width=3.0, style="dashed")
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=nx.get_edge_attributes(G, "weight"),
                                 font_size=9, rotate=False,
                                 bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8))
    ax.set_axis_off(); ax.margins(0.13)


def _draw_sorted_list(ax, order):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.0, 0.99, "Відсортовані ребра (за зростанням ваги):",
            fontsize=10.5, fontweight="bold", va="top", color="#15384A")
    n = len(order)
    top, bottom = 0.86, 0.06
    line_h = (top - bottom) / (n - 1)
    for i, (u, v, w) in enumerate(order):
        y = top - i * line_h
        ax.text(0.04, y, f"{i + 1:>2}.", family="monospace", fontsize=10, va="center", color="#888")
        ax.text(0.16, y, f"{u}–{v}", family="monospace", fontsize=10.5, va="center",
                fontweight="bold", color="#1b1b1b")
        ax.text(0.40, y, f"вага {w}", family="monospace", fontsize=10, va="center", color="#444")
    ax.text(0.0, -0.02, "Далі перебираємо зверху вниз →", fontsize=8.5, style="italic",
            va="top", color="#666")


def _comps_of(forest):
    comp = {}
    for ci, cc in enumerate(nx.connected_components(forest)):
        for n in cc:
            comp[n] = ci
    return comp


def _build_steps(G):
    forest = nx.Graph(); forest.add_nodes_from(G.nodes())
    sorted_edges = sorted(G.edges(data=True), key=lambda t: t[2]["weight"])
    steps = [dict(kind="init", hl={0: HL_ACTIVE, 1: HL_ACTIVE, 2: HL_ACTIVE},
                  comp=_comps_of(forest), mst=[]),
             dict(kind="sort", hl={4: HL_ACTIVE, 5: HL_ACTIVE},
                  comp=_comps_of(forest), mst=[],
                  order=[(u, v, d["weight"]) for u, v, d in sorted_edges])]
    mst = []
    for u, v, d in sorted_edges:
        w = d["weight"]
        connected = nx.has_path(forest, u, v)   # чи u,v вже в одній компоненті?
        added = not connected
        if added:
            forest.add_edge(u, v); mst.append((u, v, w))
        hl = {7: HL_ACTIVE, 8: HL_ACTIVE}
        hl.update({9: HL_ADD, 10: HL_ADD} if added else {11: HL_SKIP})
        steps.append(dict(kind="edge", hl=hl, comp=_comps_of(forest), mst=list(mst),
                          u=u, v=v, w=w, connected=connected, added=added,
                          done=(len(mst) == G.number_of_nodes() - 1)))
    return steps


def has_path_steps_grid(G, pos=POS):
    """Усі 13 панелей лекційного варіанту в одному зображенні: рядок = [код | граф]."""
    steps = _build_steps(G)
    n = len(steps)
    need = G.number_of_nodes() - 1
    fig, axes = plt.subplots(n, 2, figsize=(12, 3.0 * n),
                             gridspec_kw={"width_ratios": [1.15, 1]})
    for i, step in enumerate(steps):
        axc, axr = axes[i]
        _draw_code(axc, step["hl"])
        if step["kind"] == "init":
            _draw_state(axr, G, pos, step["comp"], step["mst"], faint_only=True)
            axc.set_title("Крок 1 — ініціалізація лісу", fontsize=11, fontweight="bold", loc="left")
            axr.set_title("Ліс = 7 окремих компонент (вершини ще не з'єднані).\n"
                          "Сірим — ребра вхідного графа, серед яких обиратимемо.",
                          fontsize=9.5, color="#333")
        elif step["kind"] == "sort":
            _draw_sorted_list(axr, step["order"])
            axc.set_title("Крок 2 — сортування ребер за вагою", fontsize=11, fontweight="bold", loc="left")
        else:
            _draw_state(axr, G, pos, step["comp"], step["mst"],
                        consider=(step["u"], step["v"]), added=step["added"])
            verdict = "ДОДАЄМО (різні компоненти)" if step["added"] else "ПРОПУСКАЄМО (цикл)"
            axc.set_title(f"Крок {i + 1} — ребро {step['u']}–{step['v']} (вага {step['w']})",
                          fontsize=11, fontweight="bold", loc="left")
            sub = f"has_path(forest, '{step['u']}', '{step['v']}') = {step['connected']}  →  {verdict}"
            if step["added"] and step["done"]:
                sub += f"   |  дерево готове: {need} ребер"
            axr.set_title(sub, fontsize=9.5, color="#333")

    fig.suptitle("Покроково: код (підсвічено активні рядки) | граф (компоненти кольором)",
                 fontsize=14, fontweight="bold")
    fig.legend(handles=LEGEND_HANDLES, loc="lower center", ncol=4, fontsize=9, frameon=False,
               handlelength=1.8, columnspacing=1.6, handletextpad=0.5)
    fig.tight_layout(rect=[0, 0.012, 1, 0.99])
    return fig
