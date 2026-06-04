# -*- coding: utf-8 -*-
"""Система неперетинних множин (Union-Find / DSU).

Зберігає розбиття елементів на неперетинні множини й уміє швидко:
* ``find(x)``  — повернути представника (корінь) множини елемента ``x``;
* ``union(a, b)`` — злити множини, що містять ``a`` і ``b``.

Дві оптимізації — об'єднання за рангом і стиснення шляху — тримають дерева
пласкими, тож амортизована складність операції становить ``O(alpha(n))`` ≈ ``O(1)``.
"""

from __future__ import annotations

from typing import Hashable, Iterable


class DSU:
    """Disjoint Set Union з об'єднанням за рангом і стисненням шляху."""

    def __init__(self, vertices: Iterable[Hashable]) -> None:
        self.parent = {v: v for v in vertices}   # кожен елемент спочатку сам собі корінь
        self.rank = {v: 0 for v in vertices}     # наближена «висота» дерева

    def find(self, x: Hashable) -> Hashable:
        """Повернути корінь множини елемента ``x`` (зі стисненням шляху)."""
        # 1) піднімаємось до кореня
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        # 2) стиснення шляху: усіх на шляху чіпляємо одразу до кореня
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: Hashable, b: Hashable) -> bool:
        """Злити множини елементів ``a`` і ``b``.

        Повертає ``True``, якщо множини реально злилися (були різними), і
        ``False``, якщо ``a`` і ``b`` вже були в одній множині (тобто ребро
        ``a-b`` утворило б цикл).
        """
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                          # вже в одній множині — нічого не робимо
        # менший за рангом корінь підвішуємо під більший
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True                               # множини реально злилися

    def connected(self, a: Hashable, b: Hashable) -> bool:
        """Чи лежать ``a`` і ``b`` в одній множині."""
        return self.find(a) == self.find(b)
