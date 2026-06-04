# -*- coding: utf-8 -*-
"""Покрокова DSU-версія у форматі трьох панелей: код | граф | структура DSU.

``build_steps(G)`` будує журнал кроків (ініціалізація, сортування, перебір ребер
до моменту збирання дерева). ``render_step(...)`` повертає одну фігуру matplotlib
для заданого кроку. ``step_figures(G)`` повертає всі фігури послідовності.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from .palette import HL_ACTIVE, HL_ADD, HL_SKIP
from .graph_plot import draw_graph
from .dsu_forest import draw_dsu_forest
from .code_panel import draw_code, draw_sorted_list, LEGEND_HANDLES
from ..dsu import DSU


def _root_of(parent, x):
    """Корінь у мапі ``parent`` без стиснення (щоб не псувати структуру)."""
    while parent[x] != x:
        x = parent[x]
    return x


def build_steps(G):
    """Зібрати покроковий журнал для тривопанельної схеми."""
    nodes = list(G.nodes())
    dsu = DSU(nodes)
    mst, steps = [], []
    need = len(nodes) - 1
    base_p = {n: n for n in nodes}
    base_r = {n: 0 for n in nodes}
    steps.append(dict(kind="init", hl={0: HL_ACTIVE, 1: HL_ACTIVE},
                      comp={n: n for n in nodes}, mst=[],
                      parent=dict(base_p), rank=dict(base_r)))
    sorted_edges = sorted(G.edges(data="weight"), key=lambda e: e[2])
    steps.append(dict(kind="sort", hl={3: HL_ACTIVE, 4: HL_ACTIVE},
                      comp={n: n for n in nodes}, mst=[],
                      parent=dict(base_p), rank=dict(base_r),
                      order=[(u, v, w) for u, v, w in sorted_edges]))
    for u, v, w in sorted_edges:
        pbefore = dict(dsu.parent)
        ru, rv = _root_of(pbefore, u), _root_of(pbefore, v)
        accepted = dsu.union(u, v)
        if accepted:
            mst.append((u, v, w))
        psnap, rsnap = dict(dsu.parent), dict(dsu.rank)
        new_link = None
        if accepted:                                   # який корінь підвісився під який
            new_link = (ru, psnap[ru]) if psnap[ru] != ru else (rv, psnap[rv])
        hl = {6: HL_ACTIVE, 7: HL_ACTIVE}
        hl.update({8: HL_ADD} if accepted else {9: HL_SKIP})
        steps.append(dict(kind="edge", hl=hl, comp={n: _root_of(psnap, n) for n in nodes},
                          mst=list(mst), parent=psnap, rank=rsnap,
                          u=u, v=v, w=w, accepted=accepted,
                          new_link=new_link, done=(len(mst) == need)))
        if len(mst) == need:                           # дерево готове
            break
    return steps


def render_step(step, k, G):
    """Побудувати й повернути фігуру matplotlib для одного кроку ``step`` (номер ``k``)."""
    if step["kind"] == "sort":                         # сортування — 2 панелі
        fig, (axc, axr) = plt.subplots(1, 2, figsize=(12, 3.9),
                                       gridspec_kw={"width_ratios": [1.15, 1]})
        draw_code(axc, step["hl"])
        draw_sorted_list(axr, step["order"])
        fig.suptitle("Крок 2 — сортування ребер за вагою", fontsize=13, fontweight="bold")
        fig.tight_layout(rect=[0, 0, 1, 0.95])
        return fig

    fig, (axc, axg, axd) = plt.subplots(1, 3, figsize=(15.6, 4.2),
                                        gridspec_kw={"width_ratios": [1.05, 0.95, 1.0]})
    draw_code(axc, step["hl"])
    if step["kind"] == "init":
        draw_graph(G, axg, comp=step["comp"])
        draw_dsu_forest(axd, step["parent"], step["rank"])
        title = "Крок 1 — ініціалізація: DSU + порожнє МОД"
        axg.set_title("Граф: 7 окремих компонент", fontsize=10, color="#333")
        axd.set_title("Структура DSU: 7 окремих коренів", fontsize=10, color="#333")
    else:
        mst_set = {tuple(sorted((a, b))) for a, b, _ in step["mst"]}
        draw_graph(G, axg, mst_set=mst_set, consider=(step["u"], step["v"]),
                   consider_ok=step["accepted"], comp=step["comp"])
        draw_dsu_forest(axd, step["parent"], step["rank"],
                        highlight={step["u"], step["v"]}, new_link=step["new_link"])
        verdict = ("ДОДАЄМО (union -> різні множини)" if step["accepted"]
                   else "ПРОПУСКАЄМО (union -> цикл)")
        title = f"Крок {k} — ребро {step['u']}\u2013{step['v']} (вага {step['w']}): {verdict}"
        axg.set_title(f"dsu.union('{step['u']}','{step['v']}') = {step['accepted']}",
                      fontsize=10, color="#333")
        axd.set_title("Структура DSU: підвішуємо корінь під корінь" if step["accepted"]
                      else "Структура DSU: u і v вже в одному дереві -> цикл",
                      fontsize=10, color="#333")
    fig.suptitle(title, fontsize=12.5, fontweight="bold")
    fig.tight_layout(rect=[0, 0.09, 1, 0.95])
    fig.legend(handles=LEGEND_HANDLES, loc="lower center", ncol=5, fontsize=8,
               frameon=False, handlelength=1.6, columnspacing=1.2, handletextpad=0.4)
    return fig


def step_figures(G):
    """Повернути список (підпис, фігура) для всієї послідовності кроків."""
    steps = build_steps(G)
    out = []
    for k, step in enumerate(steps, 1):
        out.append((f"step_{k:02d}_{step['kind']}", render_step(step, k, G)))
    return out
