# -*- coding: utf-8 -*-
"""Генерує соц-зображення 1280×640 (у палітрі проєкту) для GitHub та LinkedIn:

* ``social_preview.png``       — банер для GitHub Social Preview (граф + назва/стек);
* ``dsu_path_compression.png`` — кадр «до → після» стиснення шляху в DSU.

Запуск:  python scripts/make_banner.py   (кладе обидва файли в images/)
Працює без встановлення пакета — додає ``src/`` у шлях самостійно.
"""

from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")            # без вікон, лише запис у файл
import matplotlib.pyplot as plt
import networkx as nx

# дозволяємо імпорт пакета з src/ без встановлення
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
plt.rcParams["font.family"] = "DejaVu Sans"

from kruskal_mst import build_graph, kruskal_mst, POS                # noqa: E402
from kruskal_mst.viz import (                                        # noqa: E402
    C_NODE, C_NODE_EDGE, C_MST, C_BASE_EDGE, A_DSU, ROOT_BORDER,
)
from kruskal_mst.viz.core.palette import A_HI                        # noqa: E402

BG, DARK, ACC = "#F6FAFB", "#15384A", "#2C6E8F"


def make_banner(path: str) -> None:
    """Зібрати банер 1280×640 і зберегти у ``path``."""
    G = build_graph()
    mst, _ = kruskal_mst(G)
    mst_set = {tuple(sorted((u, v))) for u, v, _ in mst}
    norm = lambda e: tuple(sorted(e))

    fig = plt.figure(figsize=(12.8, 6.4), dpi=100)
    fig.patch.set_facecolor(BG)

    # ── ліворуч: текст ──
    axt = fig.add_axes([0.045, 0, 0.50, 1.0]); axt.axis("off")
    axt.set_xlim(0, 1); axt.set_ylim(0, 1)
    axt.text(0, 0.80, "Алгоритм Краскала", fontsize=38, fontweight="bold", color=DARK, va="center")
    axt.text(0, 0.685, "Мінімальне остовне дерево  ·  MST", fontsize=19, color=ACC, va="center")
    axt.plot([0.005, 0.46], [0.625, 0.625], color=C_MST, lw=3, solid_capstyle="round")
    for i, f in enumerate(["Union-Find (DSU)  vs  наївний варіант",
                           "доведення коректності  +  бенчмарк O(E log E)",
                           "покрокові візуалізації та анімації"]):
        axt.text(0.01, 0.54 - i * 0.082, "•   " + f, fontsize=15.5, color="#2f2f2f", va="center")
    axt.text(0, 0.165, "Python  ·  NetworkX  ·  Matplotlib", fontsize=15,
             color=DARK, fontweight="bold", va="center")
    axt.text(0, 0.075, "github.com/MarynaShavlak/algo-krustal-mst", fontsize=13.5, color=ACC, va="center")

    # ── праворуч: граф із зеленим МОД ──
    axg = fig.add_axes([0.55, 0.05, 0.43, 0.90]); axg.axis("off")
    base = [(u, v) for u, v in G.edges() if norm((u, v)) not in mst_set]
    mste = [(u, v) for u, v in G.edges() if norm((u, v)) in mst_set]
    nx.draw_networkx_edges(G, POS, ax=axg, edgelist=base, edge_color=C_BASE_EDGE, width=2.0)
    nx.draw_networkx_edges(G, POS, ax=axg, edgelist=mste, edge_color=C_MST, width=5.0)
    nx.draw_networkx_nodes(G, POS, ax=axg, node_size=900, node_color=C_NODE,
                           edgecolors=C_NODE_EDGE, linewidths=2.4)
    nx.draw_networkx_labels(G, POS, ax=axg, font_size=14, font_weight="bold", font_color=DARK)
    axg.margins(0.13)

    # без bbox_inches="tight" => збереже рівно 1280×640
    fig.savefig(path, dpi=100, facecolor=BG)
    plt.close(fig)


def make_path_compression(path: str) -> None:
    """Кадр «до → після» стиснення шляху в DSU (1280×640) — для соцмедіа."""
    def draw_tree(ax, parent, pos, hi_edges, hi_color):
        D = nx.DiGraph(); D.add_nodes_from(parent)
        for ch, pa in parent.items():
            if ch != pa:
                D.add_edge(ch, pa)
        nodes = list(parent)
        normal = [e for e in D.edges() if e not in hi_edges]
        nx.draw_networkx_edges(D, pos, ax=ax, edgelist=normal, edge_color=A_DSU, width=2.2,
                               arrows=True, arrowstyle="-|>", arrowsize=22, node_size=1500,
                               min_source_margin=18, min_target_margin=20)
        nx.draw_networkx_edges(D, pos, ax=ax, edgelist=list(hi_edges), edge_color=hi_color, width=5.0,
                               arrows=True, arrowstyle="-|>", arrowsize=28, node_size=1500,
                               min_source_margin=18, min_target_margin=20)
        edge = [ROOT_BORDER if n == "A" else C_NODE_EDGE for n in nodes]
        lw = [3.2 if n == "A" else 2.0 for n in nodes]
        nx.draw_networkx_nodes(D, pos, ax=ax, nodelist=nodes, node_size=1500,
                               node_color=C_NODE, edgecolors=edge, linewidths=lw)
        nx.draw_networkx_labels(D, pos, ax=ax, font_size=18, font_weight="bold", font_color=DARK)
        ax.annotate("корінь · ранг 2", pos["A"], xytext=(pos["A"][0], pos["A"][1] + 0.55),
                    ha="center", fontsize=11.5, fontweight="bold", color="#B5651D")
        ax.set_xlim(-0.6, 4.4); ax.set_ylim(-0.1, 4.1); ax.set_axis_off()

    fig = plt.figure(figsize=(12.8, 6.4), dpi=100)
    fig.patch.set_facecolor(BG)
    fig.text(0.5, 0.93, "Стиснення шляху у Union-Find (DSU)", ha="center",
             fontsize=27, fontweight="bold", color=DARK)
    fig.text(0.5, 0.85, "чому find лишається швидким", ha="center", fontsize=16, color=ACC)

    # ── ДО:  D → C → A ──
    axL = fig.add_axes([0.01, 0.08, 0.44, 0.70])
    posL = {"A": (2.0, 3.3), "B": (0.5, 1.9), "C": (2.0, 1.9), "E": (3.5, 1.9), "D": (2.0, 0.6)}
    draw_tree(axL, {"A": "A", "B": "A", "C": "A", "E": "A", "D": "C"}, posL,
              {("D", "C"), ("C", "A")}, A_HI)
    axL.set_title("ДО:  find(D) йде  D → C → A   (2 стрибки)", fontsize=15,
                  color=DARK, fontweight="bold", pad=2)

    fig.text(0.495, 0.42, "→", ha="center", va="center", fontsize=64, color=C_MST, fontweight="bold")

    # ── ПІСЛЯ:  D → A ──
    axR = fig.add_axes([0.55, 0.08, 0.44, 0.70])
    posR = {"A": (2.0, 3.3), "B": (0.5, 1.9), "C": (1.4, 1.9), "D": (2.6, 1.9), "E": (3.6, 1.9)}
    draw_tree(axR, {"A": "A", "B": "A", "C": "A", "D": "A", "E": "A"}, posR,
              {("D", "A")}, C_MST)
    axR.set_title("ПІСЛЯ:  D чіпляється прямо до A   (1 стрибок)", fontsize=15,
                  color=DARK, fontweight="bold", pad=2)

    fig.text(0.5, 0.035, "find/union ≈ O(α(n)) — практично константа", ha="center",
             fontsize=13.5, color="#555", style="italic")
    fig.savefig(path, dpi=100, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    img = os.path.join(ROOT, "images")
    make_banner(os.path.join(img, "social_preview.png"))
    make_path_compression(os.path.join(img, "dsu_path_compression.png"))
    print("-> images/social_preview.png (1280x640)")
    print("-> images/dsu_path_compression.png (1280x640)")
