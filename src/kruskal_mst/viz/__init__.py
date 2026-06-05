# -*- coding: utf-8 -*-
"""Підпакет візуалізацій: усі схеми будуються тут і повертаються як фігури matplotlib.

Внутрішньо поділено на підпапки за роллю — ``core`` (примітиви), ``steps`` (покрокові
розбори), ``figures`` (окремі схеми), ``proofs`` (доведення), ``anim`` (анімації), —
але публічний API лишається пласким: імпортуй усе прямо з ``kruskal_mst.viz``.
"""

from .core.palette import (
    C_NODE, C_NODE_EDGE, C_BASE_EDGE, C_MST, C_REJECT, C_CONSIDER, COMP_PALETTE,
    HL_ACTIVE, HL_ADD, HL_SKIP, ROOT_BORDER, A_DSU, CHIP,
)
from .core.graph_plot import draw_graph
from .core.dsu_forest import draw_dsu_forest
from .core.code_panel import CODE, draw_code, draw_sorted_list, LEGEND_HANDLES
from .steps.dsu_steps import build_steps, render_step, step_figures, dsu_steps_grid
from .steps.grid import steps_grid
from .steps.has_path_steps import has_path_steps_grid
from .proofs.cut import cut_property
from .proofs.exchange import exchange_argument
from .benchmark import run_benchmark, plot_benchmark
from .figures.compare import compare_has_path_vs_dsu
from .figures.tree_example import spanning_tree_example
from .figures.components_example import connected_components_example
from .figures.bc_cycle import bc_cycle_step8
from .figures.chain_vs_flat import chain_vs_flat
from .anim.dsu_anim import build_dsu_build_animation
from .anim.bfs_anim import build_bfs_found_animation, build_bfs_notfound_animation
from .anim.dsu_step8_anim import build_dsu_step8_animation

__all__ = [
    "draw_graph", "draw_dsu_forest",
    "CODE", "draw_code", "draw_sorted_list", "LEGEND_HANDLES",
    "build_steps", "render_step", "step_figures", "dsu_steps_grid",
    "steps_grid", "cut_property", "exchange_argument",
    "run_benchmark", "plot_benchmark", "compare_has_path_vs_dsu",
    "spanning_tree_example", "connected_components_example", "bc_cycle_step8",
    "chain_vs_flat", "has_path_steps_grid",
    "build_dsu_build_animation", "build_bfs_found_animation",
    "build_bfs_notfound_animation", "build_dsu_step8_animation",
]
