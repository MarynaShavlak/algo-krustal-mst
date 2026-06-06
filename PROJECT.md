# 📦 Структура проєкту, встановлення та запуск

*Технічна довідка до репозиторію. Навчальний розбір самого алгоритму Краскала — в основному [**README.md**](README.md).*

---

## Структура репозиторію

```
algo-krustal-mst/
├── README.md                    # навчальний розбір алгоритму, UA (§1–§18)
├── README.en.md                 # English version of the walkthrough
├── PROJECT.md                   # структура, встановлення, запуск (цей файл)
├── pyproject.toml
├── LICENSE
├── requirements.txt
├── images/                       # згенеровані схеми для README
│   ├── graph.png
│   ├── spanning_tree_example.png # приклад до §1: граф із циклами + остовне дерево
│   ├── components_example.png   # §2: граф із 3 компонентами зв'язності
│   ├── has_path_steps.png       # §6: 13 панелей [код | граф] (варіант через has_path)
│   ├── bc_cycle_step8.png       # §6: ребро B–C замкнуло б цикл B→E→C→B
│   ├── chain_vs_flat.png        # §7: ланцюг vs пласке дерево DSU
│   ├── steps_grid.png          # §16: компактний огляд усіх кроків (лише графи)
│   ├── dsu_steps.png           # §15: усі кроки [код|граф|структура DSU] + підсумок
│   ├── dsu_step8.png
│   ├── mst_result.png
│   ├── cut_property.png
│   ├── exchange_argument.png
│   ├── benchmark.png
│   ├── compare_step8.png     # порівняння has_path vs DSU на кроці 8 (§10)
│   ├── dsu_build.gif         # анімація §7 (GIF; поряд може лежати .mp4 для відео)
│   ├── bfs_found.gif         # анімація §11 (BFS B→C)
│   ├── bfs_notfound.gif      # анімація §12 (BFS E→G)
│   ├── dsu_step8_build.gif   # анімація §13 (побудова DSU перед кроком 8)
│   ├── social_preview.png    # банер 1280×640 для GitHub Social Preview
│   ├── dsu_path_compression.png  # кадр «до → після» стиснення шляху DSU (для LinkedIn)
│   └── bfs_cycle_check.png   # коли ребро дає цикл (B–C), а коли безпечне (E–G)
├── notebooks/
│   └── kruskal_mst_idea.ipynb    # повний навчальний ноутбук з анімаціями
├── scripts/
│   ├── generate_images.py        # регенерує всі зображення в images/
│   └── make_banner.py            # генерує соц-зображення (банер + кадр стиснення шляху)
└── src/
    └── kruskal_mst/
        ├── __init__.py
        ├── dsu.py                # клас DSU (Union-Find)
        ├── graph.py              # прикладовий граф, координати + генератор випадкових графів
        ├── kruskal.py            # реалізації Краскала (3 варіанти + журнал)
        └── viz/                          # підпакет візуалізацій (публічний API — плаский)
            ├── __init__.py               #   re-export усіх схем
            ├── benchmark.py              #   бенчмарк і графік масштабування (§18)
            ├── core/                     # базові примітиви малювання
            │   ├── palette.py            #     палітра кольорів (єдине джерело)
            │   ├── graph_plot.py         #     малювальник графа
            │   ├── dsu_forest.py         #     дерево вказівників DSU
            │   └── code_panel.py         #     панель коду + список ребер + легенда
            ├── steps/                    # покрокові розбори
            │   ├── dsu_steps.py          #     «код | граф | структура DSU» (§15)
            │   ├── grid.py               #     компактний огляд усіх кроків (§16)
            │   └── has_path_steps.py     #     13 панелей через has_path (§6)
            ├── figures/                  # окремі статичні схеми
            │   ├── tree_example.py       #     граф із циклами + остовне дерево (§1)
            │   ├── components_example.py #     граф із 3 компонентами (§2)
            │   ├── bc_cycle.py           #     ребро B–C замкнуло б цикл (§6)
            │   ├── chain_vs_flat.py      #     ланцюг vs пласке дерево DSU (§7)
            │   └── compare.py            #     has_path vs DSU на одному кроці (§10)
            ├── proofs/                   # доведення коректності (§17)
            │   ├── cut.py                #     схема розрізу
            │   └── exchange.py           #     схема аргументу обміну
            └── anim/                     # анімації GIF/MP4
                ├── dsu_anim.py           #     як DSU будується зсередини (§7)
                ├── bfs_anim.py           #     BFS усередині has_path (§11, §12)
                └── dsu_step8_anim.py     #     структура DSU перед кроком 8 (§13)
```

## Встановлення та запуск

```bash
# 1. Клонувати репозиторій
git clone https://github.com/MarynaShavlak/algo-krustal-mst.git
cd algo-krustal-mst

# 2. Встановити залежності (бажано у віртуальному середовищі)
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .

# 3. Регенерувати всі зображення для README (PNG + GIF-анімації)
python scripts/generate_images.py
```

### Відео анімацій (`.mp4`) — необов'язково

GIF-анімації генеруються завжди. Щоб додатково отримати `.mp4` (відео з контролерами
для GitHub), потрібен **ffmpeg**. Найпростіше — pip-пакет із вбудованим ffmpeg (без `sudo`):

```bash
pip install -e ".[video]"          # ставить imageio-ffmpeg
python scripts/generate_images.py  # тепер створює й images/*.mp4
```

> Альтернатива — системний ffmpeg: `sudo apt install ffmpeg` (Linux) /
> `brew install ffmpeg` (macOS) / `conda install -c conda-forge ffmpeg`. Скрипт сам
> підхопить будь-який доступний ffmpeg.

---

## Автор

**Maryna Shavlak** — shavlakmaryna@gmail.com

## Ліцензія

Проєкт поширюється за ліцензією MIT — див. файл [LICENSE](LICENSE).
