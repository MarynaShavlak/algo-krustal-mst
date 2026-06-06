# -*- coding: utf-8 -*-
"""Генерує банер 1280×640 для GitHub Social Preview (Settings → General → Social preview).

Граф із підсвіченим мінімальним остовним деревом + назва/опис/стек проєкту,
у тій самій палітрі, що й решта схем.

Запуск:  python scripts/make_banner.py   (кладе images/social_preview.png)
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
from kruskal_mst.viz import C_NODE, C_NODE_EDGE, C_MST, C_BASE_EDGE  # noqa: E402

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


if __name__ == "__main__":
    out = os.path.join(ROOT, "images", "social_preview.png")
    make_banner(out)
    print("-> images/social_preview.png (1280x640)")
