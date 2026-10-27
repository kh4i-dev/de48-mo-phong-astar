"""
make_figures.py - Sinh các HÌNH SỐ LIỆU cho báo cáo BTL (thang độ xám, in A4).

Mọi số liệu đều lấy từ chính bộ máy tìm kiếm của đề tài (không bịa số).
Đầu ra: docs/figures/*.png  (dpi 200, bề rộng ~15.5 cm để chèn vừa trang A4)

Chạy:  <python có matplotlib> tools/make_figures.py
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from astar import heuristics as H
from astar.grid import INF, Grid
from astar.maps import sample_maps
from astar.search import (
    MODE_ASTAR,
    MODE_BFS,
    MODE_GREEDY,
    MODE_UCS,
    path_cost,
    search,
    search_steps,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "figures")
os.makedirs(OUT, exist_ok=True)

# --- Bảng xám (zero-color) -------------------------------------------------
WALL = "#111111"
FREE = "#ffffff"
TERRAIN_2 = "#dcdcdc"
TERRAIN_4 = "#b3b3b3"
TERRAIN_6 = "#8c8c8c"
CLOSED = "#c3c3c3"
OPEN = "#efefef"
PATH = "#4d4d4d"
START = "#000000"
GOAL = "#000000"
GRIDLINE = "#c8c8c8"
HATCHES = ["", "//", "xx", "..", "\\\\", "++"]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9.5,
    "axes.titlesize": 10.5,
    "axes.labelsize": 9.5,
    "axes.edgecolor": "#333333",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 200,
})


def terrain_color(w: float) -> str:
    if w == INF:
        return WALL
    if w >= 6:
        return TERRAIN_6
    if w >= 4:
        return TERRAIN_4
    if w >= 2:
        return TERRAIN_2
    return FREE


def draw_grid(ax, grid: Grid, *, start=None, goal=None, path=(), closed=(),
              open_set=(), current=None, cell_texts=False, lw=0.6):
    """Vẽ lưới lên trục ax với 4 lớp màu: nền, CLOSED, OPEN, đường đi."""
    closed_s, open_s = set(closed), set(open_set)
    path_s = list(path)
    for r in range(grid.height):
        for c in range(grid.width):
            node = (r, c)
            color = terrain_color(grid.weight(node))
            if node in closed_s:
                color = CLOSED
            if node in open_s:
                color = OPEN
            ax.add_patch(mpatches.Rectangle((c, grid.height - 1 - r), 1, 1,
                                            facecolor=color, edgecolor=GRIDLINE,
                                            linewidth=lw))
            if cell_texts and grid.weight(node) not in (1.0, INF):
                ax.text(c + 0.5, grid.height - 1 - r + 0.5, f"{grid.weight(node):g}",
                        ha="center", va="center", fontsize=5.4, color="#555555")
    if path_s:
        xs = [c + 0.5 for _, c in path_s]
        ys = [grid.height - 1 - r + 0.5 for r, _ in path_s]
        ax.plot(xs, ys, color=PATH, linewidth=2.2, solid_capstyle="round", zorder=4)
        for r, c in path_s:
            ax.add_patch(mpatches.Rectangle((c + 0.08, grid.height - 1 - r + 0.08),
                                            0.84, 0.84, facecolor="none",
                                            edgecolor=PATH, linewidth=1.4, zorder=3))
    for node, tag in ((start, "S"), (goal, "G")):
        if node is None:
            continue
        r, c = node
        ax.add_patch(mpatches.Rectangle((c, grid.height - 1 - r), 1, 1, facecolor="white",
                                        edgecolor=WALL, linewidth=1.6, zorder=5))
        ax.text(c + 0.5, grid.height - 1 - r + 0.5, tag, ha="center", va="center",
                fontsize=7.5, fontweight="bold", color=WALL, zorder=6)
    if current is not None:
        r, c = current
        ax.add_patch(mpatches.Rectangle((c, grid.height - 1 - r), 1, 1, facecolor="none",
                                        edgecolor="#000000", linewidth=2.2, zorder=7))
    ax.set_xlim(0, grid.width)
    ax.set_ylim(0, grid.height)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#333333")


def legend_handles(*, path=True, closed=True, opened=True, terrain=False, current=False):
    hs = []
    if terrain:
        hs.append(mpatches.Patch(facecolor=TERRAIN_2, edgecolor=GRIDLINE, label="địa hình 2"))
        hs.append(mpatches.Patch(facecolor=TERRAIN_4, edgecolor=GRIDLINE, label="địa hình 4"))
        hs.append(mpatches.Patch(facecolor=TERRAIN_6, edgecolor=GRIDLINE, label="địa hình 6"))
    if opened:
        hs.append(mpatches.Patch(facecolor=OPEN, edgecolor=GRIDLINE, label="tập OPEN"))
    if closed:
        hs.append(mpatches.Patch(facecolor=CLOSED, edgecolor=GRIDLINE, label="tập CLOSED"))
    if path:
        hs.append(Line2D([0], [0], color=PATH, lw=2.2, label="đường đi tìm được"))
    if current:
        hs.append(mpatches.Patch(facecolor="none", edgecolor="black", lw=2.2,
                                 label="đỉnh đang xét"))
    hs.append(mpatches.Patch(facecolor=WALL, edgecolor=WALL, label="tường"))
    return hs


# ====================================================================== #
# Hình 2.3: minh hoạ g(n), h(n), f(n) trên lưới thật
# ====================================================================== #
def fig_g_h_f() -> None:
    text_map = [
        "S...##......",
        ".#.#.#.####.",
        ".#...#....#.",
        ".#.###.##.#.",
        ".#.....#..#.",
        ".##.##.#.##.",
        "......#.#...",
        "####.#..#.#.",
        ".....####..G",
    ]
    grid, start, goal = Grid.from_text(text_map, name="minh_hoa")
    gen = search_steps(grid, start, goal, MODE_ASTAR, "manhattan")
    closed, open_set = {}, {}
    current = None
    snap_g = snap_h = snap_f = 0.0
    for ev in gen:
        if ev[0] == "expand":
            node, g = ev[1], ev[2]
            open_set.pop(node, None)
            closed[node] = g
            current = node
            if len(closed) == 14:          # chụp lại đúng trạng thái bước 14
                snap_g = g
                snap_h = H.manhattan(node, goal) * grid.min_step_cost
                snap_f = snap_g + snap_h
                break
        elif ev[0] == "frontier":
            if ev[1] not in closed:
                open_set[ev[1]] = ev[2]

    path_to_current = _reconstruct_visible(grid, start, current)
    fig, ax = plt.subplots(figsize=(6.0, 4.5))
    draw_grid(ax, grid, start=start, goal=goal, path=path_to_current,
              closed=set(closed), open_set=set(open_set), current=current)
    ax.plot([current[1] + 0.5], [grid.height - 1 - current[0] + 0.5], marker="o",
            markersize=8, markerfacecolor="white", markeredgecolor="black",
            markeredgewidth=2, zorder=8)
    ax.annotate(f"n{f' = {current}'}",
                xy=(current[1] + 0.5, grid.height - 1 - current[0] + 0.5),
                xytext=(current[1] + 0.9, grid.height - 1 - current[0] + 2.4),
                arrowprops=dict(arrowstyle="->", color="#222222", lw=1.2),
                fontsize=9)
    ax.set_title("Minh hoạ các đại lượng g(n), h(n), f(n) tại một bước của A*", pad=8)
    ax.legend(handles=legend_handles(current=True), loc="upper center",
              bbox_to_anchor=(0.5, -0.02), ncol=3, frameon=False, fontsize=8.5)
    fig.text(0.5, -0.10,
             f"g(n) = {snap_g:.0f}   |   h(n) = {snap_h:.0f} (khoảng cách Manhattan tới đích)"
             f"   |   f(n) = g(n) + h(n) = {snap_f:.0f}",
             ha="center", fontsize=9.5)
    fig.savefig(os.path.join(OUT, "hinh_2_3_g_h_f.png"), bbox_inches="tight")
    plt.close(fig)
    print(f"  hinh_2_3: g={snap_g:.0f} h={snap_h:.0f} f={snap_f:.0f} "
          f"(đỉnh {current}, duyệt {len(closed)})")


def _reconstruct_visible(grid: Grid, start, target):
    """Đường đi ngắn nhất start -> target (dùng UCS) để tô rõ phần đã đi."""
    r = search(grid, start, target, MODE_UCS, "zero")
    return r.path if r.found else ()


# ====================================================================== #
# Hình 4.1: sáu bộ dữ liệu mẫu
# ====================================================================== #
def fig_sample_maps() -> None:
    maps = sample_maps()
    fig, axes = plt.subplots(2, 3, figsize=(6.4, 4.6))
    for ax, m in zip(axes.ravel(), maps):
        # Không in số trọng số ở panel nhỏ (sẽ nhỏ hơn 9pt khi in); hình 4.4 sẽ thấy rõ số
        draw_grid(ax, m.grid, start=m.start, goal=m.goal, lw=0.35)
        ax.set_title(f"{m.name}\n{m.size_text}, tường {m.wall_ratio:.0%}", fontsize=9)
    handles = legend_handles(path=False, closed=False, opened=False, terrain=True)
    fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, fontsize=8.5)
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(os.path.join(OUT, "hinh_4_1_sau_bo_du_lieu_mau.png"), bbox_inches="tight")
    plt.close(fig)
    print("  hinh_4_1: 6 bộ dữ liệu mẫu")


# ====================================================================== #
# Hình 4.2: diễn biến quá trình tìm kiếm trên lưới vật cản ngẫu nhiên
# ====================================================================== #
def fig_astar_progress() -> None:
    m = [x for x in sample_maps() if x.key == "vat_can_ngau_nhien"][0]
    grid, start, goal = m.grid, m.start, m.goal
    total = search(grid, start, goal, MODE_ASTAR, "manhattan").expanded
    stops = sorted({max(1, total // 4), max(2, total // 2), max(3, (3 * total) // 4)})
    snapshots = []
    closed, open_set = {}, {}
    path = ()
    for ev in search_steps(grid, start, goal, MODE_ASTAR, "manhattan"):
        if ev[0] == "expand":
            node, g = ev[1], ev[2]
            open_set.pop(node, None)
            closed[node] = g
            if len(closed) in stops:
                snapshots.append((len(closed), dict(closed), dict(open_set)))
        elif ev[0] == "frontier":
            if ev[1] not in closed:
                open_set[ev[1]] = ev[2]
        elif ev[0] == "done":
            path = tuple(ev[1].path)
    fig, axes = plt.subplots(2, 2, figsize=(6.4, 5.0))
    for ax, (n, c, o) in zip(axes.ravel()[:3], snapshots):
        draw_grid(ax, grid, start=start, goal=goal, closed=c, open_set=o, lw=0.3)
        ax.set_title(f"sau khi duyệt {n} đỉnh", fontsize=9.5)
    ax = axes.ravel()[3]
    r = search(grid, start, goal, MODE_ASTAR, "manhattan")
    draw_grid(ax, grid, start=start, goal=goal, path=path, lw=0.3)
    ax.set_title(f"kết thúc: {r.path_len} ô, chi phí {r.cost:.0f}", fontsize=9.5)
    handles = legend_handles(current=False)
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=8.5)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(os.path.join(OUT, "hinh_4_2_qua_trinh_astar.png"), bbox_inches="tight")
    plt.close(fig)
    print(f"  hinh_4_2: các mốc {stops}, đường đi {len(path)} ô")


# ====================================================================== #
# Bảng số liệu dùng chung cho các biểu đồ
# ====================================================================== #
def collect_numbers():
    maps = sample_maps()
    rows = {}
    for m in maps:
        hk = "octile" if m.grid.diagonal else "manhattan"
        rows[m.key] = {
            "name": m.name,
            "A*": search(m.grid, m.start, m.goal, MODE_ASTAR, hk),
            "UCS": search(m.grid, m.start, m.goal, MODE_UCS, "zero"),
            "Greedy": search(m.grid, m.start, m.goal, MODE_GREEDY, hk),
            "BFS": search(m.grid, m.start, m.goal, MODE_BFS, "-"),
            "map": m,
        }
        for key in ("Greedy", "BFS"):
            r = rows[m.key][key]
            r.cost = path_cost(m.grid, r.path) if r.found else INF
    return maps, rows


FACE = ["#ffffff", "#c9c9c9", "#8f8f8f", "#4a4a4a", "#1a1a1a"]


def hbar_group(ax, labels, series: dict[str, list[float]], unit="", annotate=True,
               orient="v", tick_fontsize=8.5, rot=90):
    """Biểu đồ cột nhóm (thang độ xám + hoa văn) theo chiều dọc hoặc ngang."""
    n = len(labels)
    k = len(series)
    width = 0.8 / max(1, k)
    for i, (name, vals) in enumerate(series.items()):
        offset = -0.4 + width * (i + 0.5)
        style = dict(label=name, facecolor=FACE[i % len(FACE)], edgecolor="#222222",
                     linewidth=0.7, hatch=HATCHES[i % len(HATCHES)])
        if orient == "h":
            pos = [y + offset for y in range(n)]
            ax.barh(pos, vals, height=width, **style)
            if annotate:
                for y, v in zip(pos, vals):
                    ax.text(v + max(vals) * 0.015, y, f"{v:,.0f}", va="center",
                            ha="left", fontsize=7.2)
        else:
            pos = [x + offset for x in range(n)]
            ax.bar(pos, vals, width=width, **style)
            if annotate:
                for x, v in zip(pos, vals):
                    ax.text(x, v * 1.02, f"{v:,.0f}", ha="center", va="bottom",
                            fontsize=7.2, rotation=rot)
    if orient == "h":
        ax.set_yticks(range(n))
        ax.set_yticklabels(labels, fontsize=tick_fontsize)
        ax.invert_yaxis()
        ax.grid(axis="x", color="#dddddd", linewidth=0.6)
        if unit:
            ax.set_xlabel(unit)
    else:
        ax.set_xticks(range(n))
        ax.set_xticklabels(labels, fontsize=tick_fontsize)
        ax.grid(axis="y", color="#dddddd", linewidth=0.6)
        if unit:
            ax.set_ylabel(unit)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


# ====================================================================== #
# Hình 4.3: số đỉnh đã duyệt của 4 thuật toán
# ====================================================================== #
SHORT = {
    "trong": "Lưới trống",
    "vat_can_ngau_nhien": "Vật cản 25%",
    "me_cung": "Mê cung",
    "phong_hanh_lang": "Phòng",
    "xoan_oc": "Xoắn ốc",
    "dia_hinh": "Địa hình 2/4/6",
}


def fig_expanded(rows) -> None:
    keys = list(rows)
    labels = [SHORT.get(k, k) for k in keys]
    series = {
        "A*": [rows[k]["A*"].expanded for k in keys],
        "UCS (Dijkstra)": [rows[k]["UCS"].expanded for k in keys],
        "Greedy": [rows[k]["Greedy"].expanded for k in keys],
        "BFS": [rows[k]["BFS"].expanded for k in keys],
    }
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    # Không ghi số trên cột: số liệu chính xác đã có trong bảng của báo cáo
    hbar_group(ax, labels, series, unit="số đỉnh đã duyệt", orient="h", annotate=False)
    ax.set_title("Số đỉnh đã duyệt của bốn thuật toán trên sáu bộ dữ liệu mẫu", pad=26)
    ax.legend(frameon=False, fontsize=8.5, ncol=4, loc="lower left",
              bbox_to_anchor=(0.0, 1.005))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "hinh_4_3_dinh_duyet.png"), bbox_inches="tight")
    plt.close(fig)
    print("  hinh_4_3:", {k: {a: rows[k][a].expanded for a in ('A*', 'UCS')} for k in keys})


# ====================================================================== #
# Hình 4.4: ảnh hưởng của hàm h(n)
# ====================================================================== #
def fig_heuristics(rows) -> None:
    keys = ["trong", "vat_can_ngau_nhien", "phong_hanh_lang", "dia_hinh"]
    hn = ["manhattan", "euclidean", "chebyshev", "octile"]
    series = {h: [] for h in hn}
    for k in keys:
        m = rows[k]["map"]
        for h in hn:
            r = search(m.grid, m.start, m.goal, MODE_ASTAR, h)
            series[h].append(r.expanded)
    labels = [SHORT.get(k, k) for k in keys]
    fig, ax = plt.subplots(figsize=(6.4, 2.6))
    hbar_group(ax, labels, series, unit="số đỉnh đã duyệt", orient="h", annotate=False)
    ax.set_title("Số đỉnh A* phải duyệt theo từng hàm h(n), lưới 4 hướng", pad=8)
    handles = [mpatches.Patch(facecolor=FACE[i], edgecolor="#222222", hatch=HATCHES[i],
                              label=f"h(n) = {hn[i]}") for i in range(len(hn))]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=8.5)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(os.path.join(OUT, "hinh_4_4_anh_huong_heuristic.png"), bbox_inches="tight")
    plt.close(fig)
    print("  hinh_4_4:", {h: series[h] for h in hn})


# ====================================================================== #
# Hình 4.5: đánh đổi của weighted A* (w > 1)
# ====================================================================== #
def fig_weighted(rows) -> None:
    m = rows["dia_hinh"]["map"]
    ws = [1.0, 1.5, 2.0, 3.0]
    exp_reopen, exp_lock, cost_reopen, cost_lock = [], [], [], []
    for w in ws:
        a = search(m.grid, m.start, m.goal, MODE_ASTAR, "manhattan", weight=w)
        b = search(m.grid, m.start, m.goal, MODE_ASTAR, "manhattan", weight=w,
                   allow_reopen=False)
        exp_reopen.append(a.expanded)
        cost_reopen.append(path_cost(m.grid, a.path))
        exp_lock.append(b.expanded)
        cost_lock.append(path_cost(m.grid, b.path))
    optimal = rows["dia_hinh"]["UCS"].cost

    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.0))
    ax = axes[0]
    hbar_group(ax, [f"w = {w:g}" for w in ws],
               {"có mở lại đỉnh": exp_reopen, "khoá tập CLOSED": exp_lock},
               unit="số đỉnh đã duyệt", orient="h", tick_fontsize=8.5)
    ax.set_title("Số đỉnh đã duyệt", fontsize=9.5, pad=6)
    ax = axes[1]
    hbar_group(ax, [f"w = {w:g}" for w in ws],
               {"có mở lại đỉnh": cost_reopen, "khoá tập CLOSED": cost_lock},
               unit="chi phí đường đi", orient="h", tick_fontsize=8.5)
    ax.axvline(optimal, color="#222222", linestyle="--", linewidth=1.1)
    ax.text(0.03, 1.03, f"nét đứt: chi phí tối ưu = {optimal:.0f}",
            transform=ax.transAxes, fontsize=7.8, color="#222222")
    ax.set_title("Chi phí đường đi", fontsize=9.5, pad=14)
    handles = [mpatches.Patch(facecolor=FACE[0], edgecolor="#222222", hatch=HATCHES[0],
                              label="có mở lại đỉnh"),
               mpatches.Patch(facecolor=FACE[1], edgecolor="#222222", hatch=HATCHES[1],
                              label="khoá tập CLOSED")]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, fontsize=8.5)
    fig.suptitle("Weighted A* trên lưới địa hình trọng số: đánh đổi tốc độ và chất lượng",
                 fontsize=10, y=1.0)
    fig.tight_layout(rect=(0, 0.07, 1, 0.95))
    fig.savefig(os.path.join(OUT, "hinh_4_5_weighted_astar.png"), bbox_inches="tight")
    plt.close(fig)
    print(f"  hinh_4_5: exp_reopen={exp_reopen} exp_lock={exp_lock} "
          f"cost_reopen={[round(c) for c in cost_reopen]} "
          f"cost_lock={[round(c) for c in cost_lock]} optimal={optimal:.0f}")


# ====================================================================== #
# Hình 4.6: lưới 4 hướng so với 8 hướng
# ====================================================================== #
def fig_4_vs_8(rows) -> None:
    from astar.grid import DIRS_8

    keys = ["vat_can_ngau_nhien", "dia_hinh", "me_cung"]
    labels = [SHORT.get(k, k) for k in keys]
    cost4, cost8, steps4, steps8 = [], [], [], []
    for k in keys:
        m = rows[k]["map"]
        r4 = search(m.grid, m.start, m.goal, MODE_ASTAR, "manhattan")
        g8 = Grid(m.grid.width, m.grid.height, diagonal=True, name=m.grid.name)
        g8.cost = [row[:] for row in m.grid.cost]
        g8._dirs = DIRS_8
        r8 = search(g8, m.start, m.goal, MODE_ASTAR, "octile")
        cost4.append(r4.cost)
        cost8.append(r8.cost)
        steps4.append(r4.steps)
        steps8.append(r8.steps)

    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.0))
    hbar_group(axes[0], labels, {"4 hướng": cost4, "8 hướng": cost8},
               unit="chi phí đường đi", annotate=True, rot=0, tick_fontsize=8)
    axes[0].set_title("Chi phí đường đi", fontsize=9.5, pad=16)
    hbar_group(axes[1], labels, {"4 hướng": steps4, "8 hướng": steps8},
               unit="số bước đi", annotate=True, rot=0, tick_fontsize=8)
    axes[1].set_title("Số bước đi", fontsize=9.5, pad=16)
    handles = [mpatches.Patch(facecolor=FACE[0], edgecolor="#222222", hatch=HATCHES[0],
                              label="lưới 4 hướng"),
               mpatches.Patch(facecolor=FACE[1], edgecolor="#222222", hatch=HATCHES[1],
                              label="lưới 8 hướng (cho phép đi chéo)")]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, fontsize=8.5)
    fig.suptitle("Ảnh hưởng của việc cho phép đi chéo (8 hướng) tới đường đi của A*",
                 fontsize=10, y=1.0)
    fig.tight_layout(rect=(0, 0.08, 1, 0.94))
    fig.savefig(os.path.join(OUT, "hinh_4_6_4_huong_8_huong.png"), bbox_inches="tight")
    plt.close(fig)
    print(f"  hinh_4_6: cost4={[round(c,1) for c in cost4]} cost8={[round(c,1) for c in cost8]} "
          f"steps4={steps4} steps8={steps8}")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print("Sinh hình số liệu cho báo cáo ...")
    fig_g_h_f()
    fig_sample_maps()
    fig_astar_progress()
    maps, rows = collect_numbers()
    fig_expanded(rows)
    fig_heuristics(rows)
    fig_weighted(rows)
    fig_4_vs_8(rows)
    print("Hoàn tất ->", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
