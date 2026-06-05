# -*- coding: utf-8 -*-
"""Алгоритм Краскала (мінімальне остовне дерево) з покроковими візуалізаціями.

Пакет містить:
* ``DSU`` — систему неперетинних множин (Union-Find);
* реалізації Краскала (``kruskal_mst``, ``kruskal_dsu``, ``kruskal_naive``, ``kruskal_logged``);
* прикладовий граф (``build_graph``, ``POS``);
* підпакет ``viz`` з усіма схемами (граф, покрокова сітка, дерево DSU, розріз, обмін, бенчмарк).
"""

from .dsu import DSU
from .graph import build_graph, random_connected, EDGES, POS, POS_DSU, POS_CUT, POS_EX
from .kruskal import kruskal_mst, kruskal_dsu, kruskal_naive, kruskal_logged

__version__ = "1.0.0"

__all__ = [
    "DSU",
    "build_graph", "EDGES", "POS", "POS_DSU", "POS_CUT", "POS_EX",
    "kruskal_mst", "kruskal_dsu", "kruskal_naive", "kruskal_logged", "random_connected",
]
