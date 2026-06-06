# -*- coding: utf-8 -*-
"""Двомовні підписи для схем (uk/en).

``t(s)`` повертає ``s`` для української (типово) або переклад для англійської.
Ключ — сам український рядок, тож UA-вивід лишається байт-у-байт незмінним:
коли ``LANG == "uk"``, функція повертає аргумент без змін.

generate_images.py перемикає мову через ``set_lang("en")`` й кладе схеми в images/en/.
Рядки з ``{плейсхолдерами}`` використовуються як ``t(шаблон).format(...)``.
"""

from __future__ import annotations

LANG = "uk"


def set_lang(lang: str) -> None:
    """Встановити мову підписів: ``"uk"`` (типово) або ``"en"``."""
    global LANG
    assert lang in ("uk", "en"), lang
    LANG = lang


#: Український рядок -> англійський переклад (лише те, що потрапляє у схеми).
_EN = {
    # ── core/code_panel ──
    "    if dsu.union(u, v):          # різні множини?":
        "    if dsu.union(u, v):          # different sets?",
    "    # else: вже разом -> цикл -> пропуск":
        "    # else: already together -> cycle -> skip",
    "    # else: u,v вже з'єднані -> цикл -> пропустити":
        "    # else: u,v already connected -> cycle -> skip",
    "Відсортовані ребра (за зростанням ваги):":
        "Sorted edges (by increasing weight):",
    "Далі перебираємо зверху вниз →":
        "Then we scan top to bottom →",
    "ребро графа (кандидат)": "graph edge (candidate)",
    "обране (у МОД)": "chosen (in MST)",
    "щойно додане / нова зв'язка DSU": "just added / new DSU link",
    "відкинуте (цикл)": "rejected (cycle)",
    "корінь DSU (рN = ранг)": "DSU root (rN = rank)",
    # ── core/dsu_forest ── (префікс рангу біля кореня: рN -> rN)
    "р": "r",
    # ── steps/has_path_steps ──
    "ребро графа (кандидат, не в МОД)": "graph edge (candidate, not in MST)",
    "щойно додане": "just added",
    "Крок 1 — ініціалізація лісу": "Step 1 — forest initialization",
    "Ліс = 7 окремих компонент (вершини ще не з'єднані).\n"
    "Сірим — ребра вхідного графа, серед яких обиратимемо.":
        "Forest = 7 separate components (vertices not connected yet).\n"
        "Gray — input-graph edges to choose among.",
    "Крок 2 — сортування ребер за вагою": "Step 2 — sorting edges by weight",
    "ДОДАЄМО (різні компоненти)": "ADD (different components)",
    "ПРОПУСКАЄМО (цикл)": "SKIP (cycle)",
    "Покроково: код (підсвічено активні рядки) | граф (компоненти кольором)":
        "Step by step: code (active lines highlighted) | graph (components colored)",
    # templated (use via t(...).format(...))
    "Крок {i} — ребро {u}–{v} (вага {w})": "Step {i} — edge {u}–{v} (weight {w})",
    "has_path(forest, '{u}', '{v}') = {connected}  →  {verdict}":
        "has_path(forest, '{u}', '{v}') = {connected}  →  {verdict}",
    "   |  дерево готове: {need} ребер": "   |  tree complete: {need} edges",
    # ── generate_images.py ──
    "Вихідний зважений граф": "Input weighted graph",
    "Структура DSU на кроці перевірки B–C": "DSU structure at the B–C check step",
    "Мінімальне остовне дерево (вага {total})": "Minimum spanning tree (weight {total})",
    # -- steps/dsu_steps + steps/grid --
    "Крок 1 — ініціалізація: DSU + порожнє МОД": "Step 1 — initialization: DSU + empty MST",
    "Граф: 7 окремих компонент": "Graph: 7 separate components",
    "Структура DSU: 7 окремих коренів": "DSU structure: 7 separate roots",
    "ДОДАЄМО (union -> різні множини)": "ADD (union -> different sets)",
    "ПРОПУСКАЄМО (union -> цикл)": "SKIP (union -> cycle)",
    "ДОДАЄМО (union → різні множини)": "ADD (union → different sets)",
    "ПРОПУСКАЄМО (union → цикл)": "SKIP (union → cycle)",
    "Структура DSU: підвішуємо корінь під корінь": "DSU structure: hang one root under the other",
    "Структура DSU: u і v вже в одному дереві -> цикл": "DSU structure: u and v already in one tree -> cycle",
    "Структура DSU: u і v вже в одному дереві → цикл": "DSU structure: u and v already in one tree → cycle",
    "Крок {k} — ребро {u}–{v} (вага {w}): {verdict}": "Step {k} — edge {u}–{v} (weight {w}): {verdict}",
    "Підсумок": "Summary",
    "Готове МОД (сумарна вага = {total})": "Final MST (total weight = {total})",
    "Покроково DSU-версія: код | граф | структура DSU": "Step by step, DSU version: code | graph | DSU structure",
    "Ребра мінімального остовного дерева:": "Edges of the minimum spanning tree:",
    "Разом: {n} ребер,  сумарна вага = {total}": "Total: {n} edges,  total weight = {total}",
    "ДОДАНО": "ADDED",
    "ВІДХИЛЕНО (цикл)": "REJECTED (cycle)",
    "Крок {i}: {u}–{v} (вага {w}) — {tag}": "Step {i}: {u}–{v} (weight {w}) — {tag}",
    "колір вершини = компонента зв'язності": "vertex color = connected component",
    "ребро у МОД": "edge in MST",
    "щойно прийняте": "just accepted",
    "відхилене (цикл)": "rejected (cycle)",
    # -- figures --
    "Граф G: 4 вершини, 5 ребер (є цикли)": "Graph G: 4 vertices, 5 edges (has cycles)",
    "Остовне дерево T: ті самі 4 вершини, 3 ребра": "Spanning tree T: the same 4 vertices, 3 edges",
    "Граф із 3 компонентами зв'язності (кожен колір — окрема компонента)": "A graph with 3 connected components (each color is a separate component)",
    "Крок 8: ребро B–C замкнуло б цикл  B → E → C → B": "Step 8: edge B–C would close the cycle  B → E → C → B",
    "вже у МОД": "already in MST",
    "наявний шлях B→E→C": "existing path B→E→C",
    "B–C: замкнуло б цикл": "B–C: would close a cycle",
    "корінь": "root",
    "Без оптимізацій: ланцюг\nfind(5) = 4 кроки до кореня": "Without optimizations: a chain\nfind(5) = 4 steps to the root",
    "Зі стисненням шляху: пласко\nfind(5) = 1 крок до кореня": "With path compression: flat\nfind(5) = 1 step to the root",
    "nx.has_path(B, C): обходить граф по ребрах": "nx.has_path(B, C): walks the graph along edges",
    "корінь A": "root A",
    "DSU: find(B) == find(C)? — підняття до кореня": "DSU: find(B) == find(C)? — climbing to the root",
    "Перевірка «чи B і C вже з'єднані?» (крок 8, ребро B–C)": "Check «are B and C already connected?» (step 8, edge B–C)",
    # -- benchmark --
    "наївний (nx.has_path)": "naive (nx.has_path)",
    "Кількість вершин": "Number of vertices",
    "Час, мс (логарифмічна шкала)": "Time, ms (log scale)",
    "Масштабування часу: DSU проти nx.has_path": "Time scaling: DSU vs nx.has_path",
    # -- proofs/cut --
    "РОЗРІЗ": "CUT",
    "Група A": "Group A",
    "Група B = {F, G}": "Group B = {F, G}",
    "найлегше ребро\nчерез розріз ->\nбезпечно в МОД": "lightest edge\nacross the cut ->\nsafe in MST",
    "ребра, що перетинають розріз": "edges crossing the cut",
    "найлегше з них ({u}–{v}, вага {w})": "lightest of them ({u}–{v}, weight {w})",
    "ребра всередині груп": "edges inside the groups",
    "Розріз: вершини поділено на дві групи; кольорові ребра їх з'єднують": "Cut: vertices split into two groups; colored edges connect them",
    # -- proofs/exchange --
    "Інше дерево T* (вага 43): додаємо A–D -> цикл A–B–D": "Another tree T* (weight 43): add A–D -> cycle A–B–D",
    "цикл A–B–D": "cycle A–B–D",
    "+ A–D (5): легше,\nКраскал обрав його": "+ A–D (5): lighter,\nKruskal chose it",
    "B–D (9): найважче в циклі\n-> прибираємо": "B–D (9): heaviest in the cycle\n-> remove it",
    "Після обміну (B–D -> A–D) = дерево Краскала T (вага 39)": "After the swap (B–D -> A–D) = Kruskal's tree T (weight 39)",
    "B–D більше немає": "B–D is gone",
    "ребро дерева": "tree edge",
    "додаємо (e = A–D, легше)": "add (e = A–D, lighter)",
    "прибираємо (f = B–D, важче)": "remove (f = B–D, heavier)",
    "інші ребра графа": "other graph edges",
    "Аргумент обміну: важче ребро B–D міняємо на легше A–D — вага падає 43 -> 39": "Exchange argument: swap the heavier edge B–D for the lighter A–D — weight drops 43 -> 39",
}


def t(s: str) -> str:
    """Повернути підпис мовою ``LANG`` (ключ — український рядок)."""
    if LANG == "uk":
        return s
    return _EN.get(s, s)
