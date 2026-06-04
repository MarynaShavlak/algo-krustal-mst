# -*- coding: utf-8 -*-
"""Підпакет візуалізацій: усі схеми будуються тут і повертаються як фігури matplotlib."""

from .palette import (
    C_NODE, C_NODE_EDGE, C_BASE_EDGE, C_MST, C_REJECT, C_CONSIDER, COMP_PALETTE,
    HL_ACTIVE, HL_ADD, HL_SKIP, ROOT_BORDER, A_DSU, CHIP,
)
from .graph_plot import draw_graph
from .dsu_forest import draw_dsu_forest
from .code_panel import CODE, draw_code, draw_sorted_list, LEGEND_HANDLES
from .steps import build_steps, render_step, step_figures
from .grid import steps_grid
from .cut import cut_property
from .exchange import exchange_argument
from .benchmark import run_benchmark, plot_benchmark
from .compare import compare_has_path_vs_dsu
from .dsu_anim import build_dsu_build_animation
from .bfs_anim import build_bfs_found_animation, build_bfs_notfound_animation
from .dsu_step8_anim import build_dsu_step8_animation

__all__ = [
    "draw_graph", "draw_dsu_forest",
    "CODE", "draw_code", "draw_sorted_list", "LEGEND_HANDLES",
    "build_steps", "render_step", "step_figures",
    "steps_grid", "cut_property", "exchange_argument",
    "run_benchmark", "plot_benchmark", "compare_has_path_vs_dsu",
    "build_dsu_build_animation", "build_bfs_found_animation",
    "build_bfs_notfound_animation", "build_dsu_step8_animation",
]
