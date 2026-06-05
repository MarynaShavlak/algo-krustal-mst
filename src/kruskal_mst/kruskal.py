# -*- coding: utf-8 -*-
"""Реалізації алгоритму Краскала та допоміжні функції.

* ``kruskal_mst``    — основна реалізація через DSU; повертає ребра МОД і вагу.
* ``kruskal_dsu``    — те саме, але повертає лише вагу (для бенчмарку).
* ``kruskal_naive``  — варіант через ``nx.has_path`` (перевірка циклу обходом графа).
* ``kruskal_logged`` — як ``kruskal_mst``, але веде покроковий журнал для візуалізації.
* ``random_connected`` — генератор випадкових зв'язних зважених графів.
"""

from __future__ import annotations

import random
from typing import List, Tuple

import networkx as nx

from .dsu import DSU

Edge = Tuple[str, str, int]


def kruskal_mst(G: nx.Graph) -> Tuple[List[Edge], int]:
    """Побудувати МОД. Повертає (список ребер МОД, сумарна вага)."""
    dsu = DSU(G.nodes())
    mst_edges: List[Edge] = []
    total = 0
    need = G.number_of_nodes() - 1

    # 1) усі ребра за зростанням ваги
    for u, v, w in sorted(G.edges(data="weight"), key=lambda e: e[2]):
        # 2) union повертає True лише якщо ребро з'єднало різні компоненти
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            total += w
            if len(mst_edges) == need:   # дерево зібране — далі дивитись нема сенсу
                break
    return mst_edges, total


def kruskal_dsu(G: nx.Graph) -> int:
    """Швидка реалізація через Union-Find. Повертає лише вагу МОД (зручно для бенчмарку).

    Це той самий алгоритм, що й ``kruskal_mst``, тож просто беремо з нього сумарну вагу.
    """
    return kruskal_mst(G)[1]


def kruskal_naive(G: nx.Graph) -> int:
    """Варіант через ``nx.has_path``: перевірка циклу обходом графа. Повертає вагу МОД."""
    forest = nx.Graph()
    forest.add_nodes_from(G.nodes())
    total = 0
    for u, v, w in sorted(G.edges(data="weight"), key=lambda e: e[2]):
        if not nx.has_path(forest, u, v):     # немає шляху => ребро не дасть циклу
            forest.add_edge(u, v)
            total += w
    return total


def kruskal_logged(G: nx.Graph) -> Tuple[List[Edge], int, list]:
    """Як ``kruskal_mst``, але повертає ще й покроковий журнал.

    Журнал — список словників на кожне розглянуте ребро з полями:
    ``edge``, ``accepted``, ``reason`` ("merge"/"cycle"/"stop"),
    ``mst_after`` (ребра МОД після кроку), ``comp_after`` (мапа вершина -> корінь).
    """
    nodes = list(G.nodes())
    dsu = DSU(nodes)
    mst_edges: List[Edge] = []
    total = 0
    steps: list = []
    need = len(nodes) - 1

    for u, v, w in sorted(G.edges(data="weight"), key=lambda e: e[2]):
        if len(mst_edges) == need:
            decision = "stop"                      # дерево вже готове
            accepted = False
        else:
            accepted = dsu.union(u, v)
            decision = "merge" if accepted else "cycle"
            if accepted:
                mst_edges.append((u, v, w))
                total += w
        steps.append({
            "edge": (u, v, w),
            "accepted": accepted,
            "reason": decision,
            "mst_after": list(mst_edges),
            "comp_after": {n: dsu.find(n) for n in nodes},
        })
    return mst_edges, total, steps


def random_connected(n: int, seed: int) -> nx.Graph:
    """Випадковий зв'язний зважений граф: кістяк-дерево + ~n додаткових ребер."""
    rng = random.Random(seed)
    G = nx.random_labeled_tree(n, seed=seed)   # дерево => гарантована зв'язність
    nodes = list(G.nodes())
    added = 0
    while added < n:
        u, v = rng.sample(nodes, 2)
        if not G.has_edge(u, v):
            G.add_edge(u, v)
            added += 1
    for u, v in G.edges():
        G[u][v]["weight"] = rng.randint(1, 100)
    return G
