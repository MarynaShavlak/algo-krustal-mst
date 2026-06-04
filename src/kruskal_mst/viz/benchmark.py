# -*- coding: utf-8 -*-
"""Емпіричний бенчмарк: час Краскала через DSU проти наївного ``nx.has_path``."""

from __future__ import annotations

import time

import matplotlib.pyplot as plt

from ..kruskal import kruskal_dsu, kruskal_naive, random_connected

from .palette import C_MST, C_REJECT


def run_benchmark(sizes=(50, 100, 200, 400, 600), seed=123, check=True):
    """Поміряти час обох реалізацій на зв'язних графах розмірів ``sizes``.

    Якщо ``check`` — спершу звіряє ваги МОД на кількох випадкових графах.
    Повертає словник зі списками: sizes, edges, dsu_ms, naive_ms.
    """
    if check:
        for s in range(5):
            g = random_connected(40, s)
            assert kruskal_dsu(g) == kruskal_naive(g)

    data = {"sizes": [], "edges": [], "dsu_ms": [], "naive_ms": []}
    for n in sizes:
        g = random_connected(n, seed)
        t0 = time.perf_counter(); kruskal_dsu(g);   td = (time.perf_counter() - t0) * 1000
        t0 = time.perf_counter(); kruskal_naive(g); tn = (time.perf_counter() - t0) * 1000
        data["sizes"].append(n)
        data["edges"].append(g.number_of_edges())
        data["dsu_ms"].append(td)
        data["naive_ms"].append(tn)
    return data


def plot_benchmark(data):
    """Побудувати графік масштабування часу (вісь часу — логарифмічна)."""
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.plot(data["sizes"], data["dsu_ms"], "o-", color=C_MST, lw=2.2,
            markersize=6, label="DSU (Union-Find)")
    ax.plot(data["sizes"], data["naive_ms"], "s--", color=C_REJECT, lw=2.2,
            markersize=6, label="наївний (nx.has_path)")
    ax.set_yscale("log")
    ax.set_xlabel("Кількість вершин")
    ax.set_ylabel("Час, мс (логарифмічна шкала)")
    ax.set_title("Масштабування часу: DSU проти nx.has_path")
    ax.grid(True, which="both", ls=":", alpha=0.5)
    ax.legend()
    fig.tight_layout()
    return fig
