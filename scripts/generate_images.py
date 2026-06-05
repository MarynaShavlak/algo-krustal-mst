# -*- coding: utf-8 -*-
"""Регенерує всі зображення для README у папку ``images/``.

Запуск:  python scripts/generate_images.py
Працює без встановлення пакета — додає ``src/`` у шлях самостійно.
"""

from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")            # без вікон, лише запис у файли
import matplotlib.pyplot as plt

# дозволяємо імпорт пакета з src/ без встановлення
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
plt.rcParams["font.family"] = "DejaVu Sans"

# Для відео (.mp4) потрібен ffmpeg. Якщо системного ffmpeg немає — спробуємо взяти
# бінарник із pip-пакета imageio-ffmpeg (pip install imageio-ffmpeg), щоб не ставити
# нічого через apt/sudo. Якщо й цього немає — .mp4 пропустяться, GIF усе одно будуть.
try:
    from matplotlib.animation import FFMpegWriter                    # noqa: E402
    if not FFMpegWriter.isAvailable():
        import imageio_ffmpeg
        plt.rcParams["animation.ffmpeg_path"] = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    pass

from kruskal_mst import build_graph, kruskal_mst                      # noqa: E402
from kruskal_mst.viz import (                                         # noqa: E402
    draw_graph, draw_dsu_forest, build_steps, render_step,
    steps_grid, cut_property, exchange_argument, run_benchmark, plot_benchmark,
    compare_has_path_vs_dsu, spanning_tree_example,
    connected_components_example, bc_cycle_step8, chain_vs_flat, has_path_steps_grid,
    build_dsu_build_animation, build_bfs_found_animation,
    build_bfs_notfound_animation, build_dsu_step8_animation,
)

IMAGES = os.path.join(ROOT, "images")
os.makedirs(IMAGES, exist_ok=True)


def save(fig, name, dpi=110):
    path = os.path.join(IMAGES, name)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    print("  ->", os.path.relpath(path, ROOT))


def save_anim(fig, anim, basename, fps=0.5):
    """Зберегти анімацію як GIF (Pillow, завжди) і MP4 (ffmpeg, якщо є)."""
    gif = os.path.join(IMAGES, basename + ".gif")
    anim.save(gif, writer="pillow", fps=fps, dpi=110)        # fps=0.5 ≈ 2 с на кадр
    print("  ->", os.path.relpath(gif, ROOT))
    try:
        mp4 = os.path.join(IMAGES, basename + ".mp4")
        anim.save(mp4, writer="ffmpeg", fps=fps, dpi=130)
        print("  ->", os.path.relpath(mp4, ROOT))
    except Exception as exc:                                 # ffmpeg не встановлено — GIF усе одно є
        print(f"  ({basename}.mp4 пропущено — встанови ffmpeg, щоб мати відео):", exc)
    plt.close(fig)


def main():
    G = build_graph()
    print("Генерація зображень:")

    # 1) вихідний граф
    fig, ax = plt.subplots(figsize=(7, 5.2))
    draw_graph(G, ax, title="Вихідний зважений граф")
    fig.tight_layout()
    save(fig, "graph.png")

    # 1b) приклад до §1: граф із циклами + одне з його остовних дерев
    save(spanning_tree_example(), "spanning_tree_example.png")

    # 2) усі кроки на одній сітці
    save(steps_grid(G), "steps_grid.png")

    # 3) репрезентативний тривопанельний крок — цикл B–C
    steps = build_steps(G)
    cyc_k, cyc_step = next((k, s) for k, s in enumerate(steps, 1)
                           if s["kind"] == "edge" and not s["accepted"])
    save(render_step(cyc_step, cyc_k, G), "dsu_3panel_cycle.png")

    # 4) структура DSU перед кроком 8 (стан тієї ж комірки циклу)
    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    draw_dsu_forest(ax, cyc_step["parent"], cyc_step["rank"],
                    highlight={cyc_step["u"], cyc_step["v"]})
    ax.set_title("Структура DSU на кроці перевірки B\u2013C", fontsize=12)
    fig.tight_layout()
    save(fig, "dsu_step8.png")

    # 5) підсумкове МОД
    mst, total = kruskal_mst(G)
    mst_set = {tuple(sorted((u, v))) for u, v, _ in mst}
    fig, ax = plt.subplots(figsize=(7, 5.2))
    draw_graph(G, ax, mst_set=mst_set, title=f"Мінімальне остовне дерево (вага {total})")
    fig.tight_layout()
    save(fig, "mst_result.png")

    # 6) розріз (доведення коректності)
    save(cut_property(G), "cut_property.png")

    # 7) аргумент обміну
    save(exchange_argument(G), "exchange_argument.png")

    # 8) бенчмарк
    data = run_benchmark()
    save(plot_benchmark(data), "benchmark.png")

    # 8b) порівняння has_path vs DSU на одному кроці (§10)
    save(compare_has_path_vs_dsu(G), "compare_step8.png")

    # 8c) додаткові схеми з ноутбука
    save(connected_components_example(), "components_example.png")  # §2 — 3 компоненти
    save(has_path_steps_grid(G), "has_path_steps.png")             # §6 — 13 панелей [код|граф]
    save(bc_cycle_step8(G), "bc_cycle_step8.png")                  # §6 — цикл B→E→C→B
    save(chain_vs_flat(), "chain_vs_flat.png")                     # §7 — ланцюг vs пласке

    # 9) анімації — GIF (працюють усюди, без контролерів) + MP4 (відео з контролерами
    #    на GitHub; потрібен ffmpeg). Кожна — окремий файл images/<name>.{gif,mp4}.
    for builder, name in [
        (build_dsu_build_animation, "dsu_build"),         # §7  — як DSU будується зсередини
        (build_bfs_found_animation, "bfs_found"),         # §11 — BFS B→C: шлях знайдено (цикл)
        (build_bfs_notfound_animation, "bfs_notfound"),   # §12 — BFS E→G: ціль недосяжна (додаємо)
        (build_dsu_step8_animation, "dsu_step8_build"),   # §13 — побудова структури DSU перед кроком 8
    ]:
        fig, anim = builder()
        save_anim(fig, anim, name)

    print("Готово.")


if __name__ == "__main__":
    main()
