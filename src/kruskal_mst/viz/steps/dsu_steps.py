# -*- coding: utf-8 -*-
"""Покрокова DSU-версія у форматі трьох панелей: код | граф | структура DSU.

``build_steps(G)`` будує журнал кроків (ініціалізація, сортування, перебір ребер
до моменту збирання дерева). ``render_step(...)`` повертає одну фігуру matplotlib
для заданого кроку. ``step_figures(G)`` повертає всі фігури послідовності.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from ..core.palette import HL_ACTIVE, HL_ADD, HL_SKIP, C_MST
from ..core.graph_plot import draw_graph
from ..core.dsu_forest import draw_dsu_forest
from ..core.code_panel import draw_code, draw_sorted_list, LEGEND_HANDLES
from ..core.i18n import t
from ...dsu import DSU


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
        fig.suptitle(t("Крок 2 — сортування ребер за вагою"), fontsize=13, fontweight="bold")
        fig.tight_layout(rect=[0, 0, 1, 0.95])
        return fig

    fig, (axc, axg, axd) = plt.subplots(1, 3, figsize=(15.6, 4.2),
                                        gridspec_kw={"width_ratios": [1.05, 0.95, 1.0]})
    draw_code(axc, step["hl"])
    if step["kind"] == "init":
        draw_graph(G, axg, comp=step["comp"])
        draw_dsu_forest(axd, step["parent"], step["rank"])
        title = t("Крок 1 — ініціалізація: DSU + порожнє МОД")
        axg.set_title(t("Граф: 7 окремих компонент"), fontsize=10, color="#333")
        axd.set_title(t("Структура DSU: 7 окремих коренів"), fontsize=10, color="#333")
    else:
        mst_set = {tuple(sorted((a, b))) for a, b, _ in step["mst"]}
        draw_graph(G, axg, mst_set=mst_set, consider=(step["u"], step["v"]),
                   consider_ok=step["accepted"], comp=step["comp"])
        draw_dsu_forest(axd, step["parent"], step["rank"],
                        highlight={step["u"], step["v"]}, new_link=step["new_link"])
        verdict = (t("ДОДАЄМО (union -> різні множини)") if step["accepted"]
                   else t("ПРОПУСКАЄМО (union -> цикл)"))
        title = t("Крок {k} — ребро {u}\u2013{v} (вага {w}): {verdict}").format(k=k, u=step['u'], v=step['v'], w=step['w'], verdict=verdict)
        axg.set_title(f"dsu.union('{step['u']}','{step['v']}') = {step['accepted']}",
                      fontsize=10, color="#333")
        axd.set_title(t("Структура DSU: підвішуємо корінь під корінь") if step["accepted"]
                      else t("Структура DSU: u і v вже в одному дереві -> цикл"),
                      fontsize=10, color="#333")
    fig.suptitle(title, fontsize=12.5, fontweight="bold")
    fig.tight_layout(rect=[0, 0.09, 1, 0.95])
    fig.legend(handles=LEGEND_HANDLES, labels=[t(h.get_label()) for h in LEGEND_HANDLES], loc="lower center", ncol=5, fontsize=8,
               frameon=False, handlelength=1.6, columnspacing=1.2, handletextpad=0.4)
    return fig


def step_figures(G):
    """Повернути список (підпис, фігура) для всієї послідовності кроків."""
    steps = build_steps(G)
    out = []
    for k, step in enumerate(steps, 1):
        out.append((f"step_{k:02d}_{step['kind']}", render_step(step, k, G)))
    return out


def _draw_result_list(ax, mst, total):
    """Список ребер готового МОД + сумарна вага (для підсумкового рядка гріда)."""
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.0, 0.99, t("Ребра мінімального остовного дерева:"), fontsize=10.5,
            fontweight="bold", va="top", color="#15384A")
    n = len(mst)
    top, bottom = 0.84, 0.24
    line_h = (top - bottom) / (n - 1) if n > 1 else 0
    for i, (u, v, w) in enumerate(mst):
        y = top - i * line_h
        ax.text(0.06, y, f"{u}–{v}", family="monospace", fontsize=11, va="center",
                fontweight="bold", color=C_MST)
        ax.text(0.30, y, f"{t('вага')} {w}", family="monospace", fontsize=10.5, va="center", color="#444")
    ax.text(0.06, 0.10, t("Разом: {n} ребер,  сумарна вага = {total}").format(n=n, total=total),
            fontsize=10.5, fontweight="bold", va="center", color="#15384A")


def dsu_steps_grid(G):
    """Усі кроки DSU-версії + підсумок в одному зображенні: рядок = [код | граф | структура DSU].

    Грід-аналог окремих панелей ``render_step`` (як ``has_path_steps_grid`` для §6), з легендою
    під кожним кроком і підсумковим рядком ``[список ребер МОД | готове дерево]``.
    """
    steps = build_steps(G)
    nrow = len(steps) + 1   # кроки + підсумковий рядок
    fig, axes = plt.subplots(nrow, 3, figsize=(15.6, 4.3 * nrow),
                             gridspec_kw={"width_ratios": [1.05, 0.95, 1.0]})

    def row_legend(ax):
        ax.legend(handles=LEGEND_HANDLES, labels=[t(h.get_label()) for h in LEGEND_HANDLES], loc="upper center", bbox_to_anchor=(0.5, -0.04),
                  ncol=3, fontsize=8, frameon=False,
                  handlelength=1.5, columnspacing=1.1, handletextpad=0.4)

    for i, step in enumerate(steps):
        axc, axg, axd = axes[i]
        draw_code(axc, step["hl"])
        if step["kind"] == "sort":
            draw_sorted_list(axg, step["order"])
            axd.set_axis_off()
            axc.set_title(t("Крок 2 — сортування ребер за вагою"), fontsize=11, fontweight="bold", loc="left")
            continue
        if step["kind"] == "init":
            draw_graph(G, axg, comp=step["comp"])
            draw_dsu_forest(axd, step["parent"], step["rank"])
            axc.set_title(t("Крок 1 — ініціалізація: DSU + порожнє МОД"), fontsize=11, fontweight="bold", loc="left")
            axg.set_title(t("Граф: 7 окремих компонент"), fontsize=10, color="#333")
            axd.set_title(t("Структура DSU: 7 окремих коренів"), fontsize=10, color="#333")
        else:
            mst_set = {tuple(sorted((a, b))) for a, b, _ in step["mst"]}
            draw_graph(G, axg, mst_set=mst_set, consider=(step["u"], step["v"]),
                       consider_ok=step["accepted"], comp=step["comp"])
            draw_dsu_forest(axd, step["parent"], step["rank"],
                            highlight={step["u"], step["v"]}, new_link=step["new_link"])
            verdict = (t("ДОДАЄМО (union → різні множини)") if step["accepted"]
                       else t("ПРОПУСКАЄМО (union → цикл)"))
            axc.set_title(t("Крок {k} — ребро {u}–{v} (вага {w}): {verdict}").format(k=i + 1, u=step['u'], v=step['v'], w=step['w'], verdict=verdict),
                          fontsize=10.5, fontweight="bold", loc="left")
            axg.set_title(f"dsu.union('{step['u']}','{step['v']}') = {step['accepted']}",
                          fontsize=10, color="#333")
            axd.set_title(t("Структура DSU: підвішуємо корінь під корінь") if step["accepted"]
                          else t("Структура DSU: u і v вже в одному дереві → цикл"),
                          fontsize=10, color="#333")
        row_legend(axg)

    # підсумковий рядок: список ребер МОД | готове дерево
    axl, axt, axe = axes[-1]
    final = steps[-1]["mst"]
    total = sum(w for _, _, w in final)
    _draw_result_list(axl, final, total)
    draw_graph(G, axt, mst_set={tuple(sorted((a, b))) for a, b, _ in final}, comp=steps[-1]["comp"])
    axe.set_axis_off()
    axl.set_title(t("Підсумок"), fontsize=11, fontweight="bold", loc="left")
    axt.set_title(t("Готове МОД (сумарна вага = {total})").format(total=total), fontsize=10, color="#333")
    row_legend(axt)

    fig.suptitle(t("Покроково DSU-версія: код | граф | структура DSU"), fontsize=14, fontweight="bold", y=0.997)
    fig.tight_layout(rect=[0, 0.005, 1, 0.985], h_pad=6.0)
    return fig
