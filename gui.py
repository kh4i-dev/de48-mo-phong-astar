"""
gui.py - Giao diện đồ hoạ mô phỏng A* (Tkinter, không cần thư viện ngoài).

Chạy:  python main.py            (hoặc  python gui.py)

Tính năng:
    * Vẽ tường / tô địa hình / đặt xuất phát - đích bằng chuột
    * Chọn thuật toán (A*, UCS/Dijkstra, Greedy, BFS) và hàm h(n)
    * Trọng số w cho A* có trọng số (weighted A*)
    * Mô phỏng từng bước: tô màu tập OPEN (đang chờ) và tập CLOSED (đã duyệt)
    * Bảng số liệu trực tiếp: g, h, f, số đỉnh duyệt, chi phí, thời gian
    * Nạp 6 bộ dữ liệu mẫu, sinh vật cản ngẫu nhiên, sinh mê cung
    * So sánh nhanh 4 thuật toán & xuất kết quả ra CSV
"""

from __future__ import annotations

import csv
import os
import random
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from astar import heuristics as H
from astar.grid import DIRS_4, DIRS_8, Grid, INF, Node
from astar.maps import SampleMap, maze_map, random_obstacles_map, sample_maps
from astar.search import (
    ALL_MODES,
    MODE_ASTAR,
    MODE_BFS,
    MODE_GREEDY,
    MODE_UCS,
    SearchResult,
    path_cost,
    search,
    search_steps,
)
from astar.grid import parse_map_file, save_map_file

# ---------------------------------------------------------------------- #
# Bảng màu
# ---------------------------------------------------------------------- #
BG = "#1e2229"
PANEL_BG = "#272c35"
FG = "#e8eaf0"
ACCENT = "#4da3ff"

COLOR_WALL = "#11151b"
COLOR_FREE = "#f5f7fa"
COLOR_TERRAIN = {2.0: "#dfeed2", 4.0: "#f6e6c0", 6.0: "#e0c9a6"}
COLOR_CLOSED = "#9dbfe8"
COLOR_OPEN = "#bfe6b8"
COLOR_PATH = "#ffd54f"
COLOR_START = "#2e9e4f"
COLOR_GOAL = "#d64545"
COLOR_CURRENT = "#ff8a4c"
COLOR_GRID = "#c9ced8"

VIEW_MODES = (MODE_ASTAR, MODE_UCS, MODE_GREEDY, MODE_BFS)


def terrain_color(w: float) -> str:
    if w == INF:
        return COLOR_WALL
    for level, color in COLOR_TERRAIN.items():
        if w >= level:
            return color
    return COLOR_FREE


class AStarApp:
    """Ứng dụng mô phỏng."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Đề tài 48 - Mô phỏng thuật toán A* tìm đường trên lưới")
        root.configure(bg=BG)
        root.minsize(1080, 700)

        # ----- Trạng thái mô hình -------------------------------------
        self.grid = Grid(40, 25, name="tùy_chỉnh")
        self.start: Node = (self.grid.height - 1, 0)
        self.goal: Node = (0, self.grid.width - 1)
        self.cell = 22
        self.tool = tk.StringVar(value="wall")
        self.algorithm = tk.StringVar(value=MODE_ASTAR)
        self.heuristic = tk.StringVar(value=H.DEFAULT_NAME)
        self.weight = tk.DoubleVar(value=1.0)
        self.diagonal = tk.BooleanVar(value=False)
        self.speed = tk.IntVar(value=6)          # số sự kiện mỗi nhịp
        self.density = tk.IntVar(value=25)       # % vật cản

        # ----- Trạng thái mô phỏng ------------------------------------
        self.gen = None
        self.running = False
        self.finished = True
        self.open_g: dict[Node, float] = {}
        self.closed: dict[Node, float] = {}
        self.path: tuple[Node, ...] = ()
        self.current: Node | None = None
        self.result: SearchResult | None = None
        self.last_results: list[SearchResult] = []
        self.t0 = 0.0
        self.gen_time_ms = 0.0   # thời gian TÌM KIẾM thuần (không tính thời gian vẽ)

        self.items: dict[Node, int] = {}
        self.texts: dict[Node, int] = {}

        self._build_ui()
        self._load_sample(sample_maps()[0], keep_size=True)
        self._draw_all()

    # ================================================================== #
    # Giao diện
    # ================================================================== #
    def _build_ui(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:  # pragma: no cover
            pass
        style.configure("TFrame", background=PANEL_BG)
        style.configure("TLabel", background=PANEL_BG, foreground=FG)
        style.configure("TCheckbutton", background=PANEL_BG, foreground=FG)
        style.configure("TRadiobutton", background=PANEL_BG, foreground=FG)
        style.configure("TLabelframe", background=PANEL_BG, foreground=ACCENT)
        style.configure("TLabelframe.Label", background=PANEL_BG, foreground=ACCENT,
                        font=("Segoe UI", 10, "bold"))
        style.configure("TButton", font=("Segoe UI", 9))
        style.configure("Run.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TNotebook", background=PANEL_BG)
        style.configure("TNotebook.Tab", font=("Segoe UI", 9))

        outer = ttk.Frame(self.root, padding=8)
        outer.pack(fill="both", expand=True)

        # ---------------- Khung lưới (trái) --------------------------
        left = ttk.Frame(outer)
        left.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(left, bg="#eceff4", highlightthickness=1,
                                highlightbackground="#454b57", cursor="crosshair")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", lambda e: self._on_paint(e, erase=False))
        self.canvas.bind("<B1-Motion>", lambda e: self._on_paint(e, erase=False))
        self.canvas.bind("<Button-3>", lambda e: self._on_paint(e, erase=True))
        self.canvas.bind("<B3-Motion>", lambda e: self._on_paint(e, erase=True))
        self.canvas.bind("<Motion>", self._on_hover)

        self.status = tk.Label(left, text="", bg="#151920", fg=FG, anchor="w",
                               font=("Consolas", 9), padx=8, pady=3)
        self.status.pack(fill="x")

        # ---------------- Bảng điều khiển (phải) ---------------------
        right = ttk.Frame(outer, width=360, padding=(10, 0, 0, 0))
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        nb = ttk.Notebook(right)
        nb.pack(fill="both", expand=True)
        tab_run = ttk.Frame(nb, padding=8)
        tab_map = ttk.Frame(nb, padding=8)
        tab_info = ttk.Frame(nb, padding=8)
        nb.add(tab_run, text=" Chạy mô phỏng ")
        nb.add(tab_map, text=" Bản đồ ")
        nb.add(tab_info, text=" Hướng dẫn ")

        self._build_run_tab(tab_run)
        self._build_map_tab(tab_map)
        self._build_info_tab(tab_info)

    # ------------------------------------------------------------------ #
    def _build_run_tab(self, f: ttk.Frame) -> None:
        # --- Thuật toán
        box = ttk.Labelframe(f, text="1. Thuật toán", padding=6)
        box.pack(fill="x", pady=4)
        cb = ttk.Combobox(box, textvariable=self.algorithm, values=list(VIEW_MODES),
                          state="readonly")
        cb.pack(fill="x")
        cb.bind("<<ComboboxSelected>>", lambda e: self._on_algo_change())

        row = ttk.Frame(box)
        row.pack(fill="x", pady=(6, 0))
        ttk.Label(row, text="h(n):").pack(side="left")
        self.h_box = ttk.Combobox(row, textvariable=self.heuristic, values=H.names(),
                                  state="readonly", width=12)
        self.h_box.pack(side="left", padx=4)
        self.h_box.bind("<<ComboboxSelected>>", lambda e: self._on_algo_change())

        row2 = ttk.Frame(box)
        row2.pack(fill="x", pady=(6, 0))
        ttk.Label(row2, text="Trọng số w:").pack(side="left")
        ttk.Spinbox(row2, from_=0.5, to=5.0, increment=0.5, width=5,
                    textvariable=self.weight, command=self._on_weight).pack(side="left", padx=4)
        ttk.Checkbutton(box, text="Cho phép đi chéo (8 hướng)",
                        variable=self.diagonal, command=self._on_toggle_diagonal).pack(
            anchor="w", pady=(6, 0))
        self.h_note = ttk.Label(box, text="", foreground="#ffd166", wraplength=310,
                                font=("Segoe UI", 8))
        self.h_note.pack(anchor="w")

        # --- Điều khiển
        box2 = ttk.Labelframe(f, text="2. Điều khiển", padding=6)
        box2.pack(fill="x", pady=4)
        g = ttk.Frame(box2)
        g.pack(fill="x")
        ttk.Button(g, text="▶ Chạy", style="Run.TButton", width=9,
                   command=self.run).pack(side="left", padx=(0, 4))
        ttk.Button(g, text="⏸ Dừng", width=9, command=self.pause).pack(side="left", padx=2)
        ttk.Button(g, text="⏭ 1 bước", width=9, command=self.step_once).pack(side="left", padx=2)

        g2 = ttk.Frame(box2)
        g2.pack(fill="x", pady=(6, 0))
        ttk.Button(g2, text="⟲ Xoá kết quả", width=14, command=self.clear_search).pack(
            side="left", padx=(0, 4))
        ttk.Button(g2, text="⏹ Xong / Đặt lại", width=14, command=self.reset).pack(side="left")

        row = ttk.Frame(box2)
        row.pack(fill="x", pady=(8, 0))
        ttk.Label(row, text="Tốc độ:").pack(side="left")
        ttk.Scale(row, from_=1, to=200, variable=self.speed, orient="horizontal",
                  length=200).pack(side="left", padx=6, fill="x", expand=True)
        ttk.Label(row, textvariable=self.speed, width=4).pack(side="left")

        # --- Thống kê
        box3 = ttk.Labelframe(f, text="3. Số liệu mô phỏng", padding=6)
        box3.pack(fill="both", expand=True, pady=4)
        self.stats = {}
        fields = [
            ("thuật toán", "algorithm"), ("h(n)", "heuristic"),
            ("đỉnh đang xét", "current"), ("g(n) / h(n) / f(n)", "ghf"),
            ("số đỉnh đã duyệt", "expanded"), ("số đỉnh đã sinh", "generated"),
            ("|OPEN| / |CLOSED|", "sets"), ("độ sâu lớn nhất", "depth"),
            ("chi phí đường đi", "cost"), ("số ô / số bước", "pathlen"),
            ("thời gian (ms)", "time"), ("số vòng lặp", "iters"),
        ]
        for i, (label, key) in enumerate(fields):
            ttk.Label(box3, text=label + ":").grid(row=i, column=0, sticky="w", pady=1)
            lb = ttk.Label(box3, text="-", foreground=ACCENT, font=("Consolas", 9, "bold"))
            lb.grid(row=i, column=1, sticky="w", padx=(6, 0))
            self.stats[key] = lb

        row = ttk.Frame(f)
        row.pack(fill="x", pady=4)
        ttk.Button(row, text="⚖ So sánh 4 thuật toán", command=self.compare_all).pack(
            fill="x", pady=2)
        ttk.Button(row, text="💾 Xuất kết quả ra CSV", command=self.export_csv).pack(fill="x")

    # ------------------------------------------------------------------ #
    def _build_map_tab(self, f: ttk.Frame) -> None:
        box = ttk.Labelframe(f, text="Công cụ vẽ", padding=6)
        box.pack(fill="x", pady=4)
        for text, val in (("Tường / vật cản", "wall"),
                          ("Ô thường (xoá)", "erase"),
                          ("Địa hình nặng (cát)", "terrain"),
                          ("Đặt xuất phát (S)", "start"),
                          ("Đặt đích (G)", "goal")):
            ttk.Radiobutton(box, text=text, value=val, variable=self.tool).pack(anchor="w")
        ttk.Label(box, text="Chuột trái = vẽ • Chuột phải = xoá • Kéo để vẽ liên tục",
                  foreground="#9aa4b2", font=("Segoe UI", 8), wraplength=310).pack(anchor="w")

        box2 = ttk.Labelframe(f, text="Sinh bản đồ", padding=6)
        box2.pack(fill="x", pady=4)
        row = ttk.Frame(box2)
        row.pack(fill="x")
        ttk.Label(row, text="Mật độ vật cản %:").pack(side="left")
        ttk.Spinbox(row, from_=5, to=60, increment=5, width=5,
                    textvariable=self.density).pack(side="left", padx=4)
        ttk.Button(box2, text="🎲 Vật cản ngẫu nhiên", command=self.gen_random).pack(
            fill="x", pady=2)
        ttk.Button(box2, text="🌀 Sinh mê cung", command=self.gen_maze).pack(fill="x", pady=2)
        ttk.Button(box2, text="🧹 Xoá toàn bộ lưới", command=self.gen_empty).pack(fill="x")

        box3 = ttk.Labelframe(f, text="Bộ dữ liệu mẫu", padding=6)
        box3.pack(fill="x", pady=4)
        for m in sample_maps():
            ttk.Button(box3, text=f"{m.name} ({m.size_text})",
                       command=lambda mm=m: self._load_sample(mm)).pack(fill="x", pady=1)

        box4 = ttk.Labelframe(f, text="Tệp", padding=6)
        box4.pack(fill="x", pady=4)
        ttk.Button(box4, text="📂 Mở bản đồ (.txt)", command=self.open_map).pack(fill="x", pady=2)
        ttk.Button(box4, text="📁 Lưu bản đồ (.txt)", command=self.save_map).pack(fill="x")

        box5 = ttk.Labelframe(f, text="Hiển thị", padding=6)
        box5.pack(fill="x", pady=4)
        row = ttk.Frame(box5)
        row.pack(fill="x")
        ttk.Button(row, text="− Thu nhỏ", command=lambda: self.zoom(-2)).pack(side="left", expand=True)
        ttk.Button(row, text="+ Phóng to", command=lambda: self.zoom(2)).pack(side="left", expand=True)
        ttk.Button(box5, text="⤢ Vừa cửa sổ", command=self.fit_cells).pack(fill="x", pady=2)

    # ------------------------------------------------------------------ #
    def _build_info_tab(self, f: ttk.Frame) -> None:
        txt = tk.Text(f, bg="#151920", fg=FG, font=("Consolas", 9), wrap="word",
                      relief="flat", padx=6, pady=6)
        txt.pack(fill="both", expand=True)
        legend = (
            "CHÚ THÍCH MÀU\n"
            "  ■ nền sáng     : ô đi được (chi phí 1)\n"
            "  ■ xanh lá nhạt : tập OPEN - đang chờ xét\n"
            "  ■ xanh dương   : tập CLOSED - đã duyệt\n"
            "  ■ vàng         : đường đi tối ưu tìm được\n"
            "  ■ cam          : đỉnh đang xét\n"
            "  ■ xanh đậm/đỏ  : xuất phát / đích\n"
            "  ■ đen          : tường (không đi được)\n"
            "  ô có chữ số    : địa hình nặng, chi phí 2/4/6\n\n"
            "PHÍM TẮT\n"
            "  Space : chạy / dừng          C : xoá kết quả\n"
            "  S     : đặt xuất phát        G : đặt đích\n"
            "  R     : vật cản ngẫu nhiên   M : sinh mê cung\n"
            "  D     : bật/tắt đi chéo      1..4 : chọn thuật toán\n\n"
            "CÁC BƯỚC MÔ PHỎNG\n"
            "  1. Chọn bản đồ mẫu hoặc tự vẽ.\n"
            "  2. Chọn thuật toán & h(n); thử w > 1 (weighted A*).\n"
            "  3. Bấm Chạy để xem OPEN/CLOSED lan ra thế nào.\n"
            "  4. So sánh 4 thuật toán rồi xuất CSV.\n\n"
            "ĐỊNH NGHĨA\n"
            "  g(n): chi phí thực từ start tới n\n"
            "  h(n): ước lượng chi phí từ n tới goal\n"
            "  f(n) = g(n) + w·h(n)  ->  chọn đỉnh có f nhỏ nhất\n"
        )
        txt.insert("1.0", legend)
        txt.configure(state="disabled")

    # ================================================================== #
    # Vẽ lưới
    # ================================================================== #
    def _draw_all(self) -> None:
        self.canvas.delete("all")
        self.items.clear()
        self.texts.clear()
        c = self.cell
        w = self.grid.width * c
        h = self.grid.height * c
        for r in range(self.grid.height):
            for col in range(self.grid.width):
                node = (r, col)
                x0, y0 = col * c, r * c
                fill = terrain_color(self.grid.weight(node))
                item = self.canvas.create_rectangle(
                    x0, y0, x0 + c, y0 + c, fill=fill, outline=COLOR_GRID, width=1)
                self.items[node] = item
                if self.grid.weight(node) not in (1.0, INF) and c >= 16:
                    self.texts[node] = self.canvas.create_text(
                        x0 + c / 2, y0 + c / 2, text=str(int(self.grid.weight(node))),
                        fill="#7a6a52", font=("Segoe UI", max(7, c // 3)))
        self.canvas.configure(scrollregion=(0, 0, w, h), width=w, height=h)
        self._redraw_state()

    def _set_cell_color(self, node: Node, color: str) -> None:
        item = self.items.get(node)
        if item is not None:
            self.canvas.itemconfig(item, fill=color)

    def _base_color(self, node: Node) -> str:
        return terrain_color(self.grid.weight(node))

    def _redraw_state(self) -> None:
        """Tô lại toàn bộ màu theo trạng thái tìm kiếm hiện tại."""
        for node in self.items:
            self._set_cell_color(node, self._base_color(node))
        for node in self.closed:
            self._set_cell_color(node, COLOR_CLOSED)
        for node in self.open_g:
            self._set_cell_color(node, COLOR_OPEN)
        for node in self.path:
            self._set_cell_color(node, COLOR_PATH)
        self._paint_endpoints()

    def _paint_endpoints(self) -> None:
        for node, color, label in ((self.start, COLOR_START, "S"),
                                   (self.goal, COLOR_GOAL, "G")):
            if node in self.items:
                self._set_cell_color(node, color)
        if self.current is not None and self.current in self.items:
            item = self.items[self.current]
            self.canvas.itemconfig(item, fill=COLOR_CURRENT)
        self.canvas.delete("marker")
        c = self.cell
        for node, label, color in ((self.start, "S", "#ffffff"), (self.goal, "G", "#ffffff")):
            if node in self.items:
                self.canvas.create_text(
                    node[1] * c + c / 2, node[0] * c + c / 2, text=label,
                    fill=color, font=("Segoe UI", max(8, c // 2), "bold"), tags="marker")
        if self.path and len(self.path) > 1:
            self.canvas.delete("pathline")
            pts = [(n[1] * c + c / 2, n[0] * c + c / 2) for n in self.path]
            flat = [v for p in pts for v in p]
            self.canvas.create_line(*flat, fill="#c9a227", width=2, tags="pathline")
            self.canvas.tag_lower("pathline", "marker")

    def _refresh_cell(self, node: Node) -> None:
        self._set_cell_color(node, self._base_color(node))

    # ================================================================== #
    # Tương tác chuột
    # ================================================================== #
    def _node_at(self, event: tk.Event) -> Node | None:
        col = int(self.canvas.canvasx(event.x) // self.cell)
        row = int(self.canvas.canvasy(event.y) // self.cell)
        node = (row, col)
        return node if self.grid.inside(node) else None

    def _on_hover(self, event: tk.Event) -> None:
        node = self._node_at(event)
        if node is None:
            return
        w = self.grid.weight(node)
        wtxt = "tường" if w == INF else f"chi phí {w:g}"
        self.status.configure(
            text=f"Ô {node} • {wtxt} • |OPEN|={len(self.open_g)} |CLOSED|={len(self.closed)} "
                 f"• g={self.open_g.get(node) or self.closed.get(node, '-')}"
        )

    def _on_paint(self, event: tk.Event, erase: bool = False) -> None:
        node = self._node_at(event)
        if node is None:
            return
        tool = "erase" if erase else self.tool.get()
        if tool == "start":
            if node == self.goal or self.grid.is_blocked(node):
                return
            self.start = node
        elif tool == "goal":
            if node == self.start or self.grid.is_blocked(node):
                return
            self.goal = node
        elif tool == "wall":
            if node in (self.start, self.goal):
                return
            self.grid.set_wall(node, True)
        elif tool == "terrain":
            if node in (self.start, self.goal):
                return
            cur = self.grid.weight(node)
            if cur == INF:
                return
            nxt = {1.0: 2.0, 2.0: 4.0, 4.0: 6.0, 6.0: 1.0}.get(cur, 1.0)
            self.grid.set_weight(node, nxt)
        else:  # erase
            if node in (self.start, self.goal):
                return
            self.grid.set_wall(node, False)
        self._redraw_state()
        self._invalidate()

    # ================================================================== #
    # Nhóm điều khiển
    # ================================================================== #
    def _invalidate(self) -> None:
        """Huỷ kết quả đang hiển thị vì lưới/thuật toán đã thay đổi."""
        self._stop_loop()
        self.gen = None
        self.open_g.clear()
        self.closed.clear()
        self.path = ()
        self.current = None
        self.result = None
        self.finished = True
        self._clear_stats()

    def _stop_loop(self) -> None:
        self.running = False

    def _on_algo_change(self) -> None:
        algo = self.algorithm.get()
        if algo == MODE_UCS:
            self.heuristic.set("zero")
            self.h_box.configure(state="disabled")
        elif algo == MODE_BFS:
            self.heuristic.set("-")
            self.h_box.configure(state="disabled")
        else:
            self.h_box.configure(state="readonly")
            if self.heuristic.get() in ("zero", "-"):
                self.heuristic.set("manhattan" if not self.diagonal.get() else "octile")
        self._update_h_note()
        self._invalidate()
        self._redraw_state()

    def _on_weight(self) -> None:
        try:
            self.weight.get()
        except tk.TclError:
            return
        self._update_h_note()
        self._invalidate()

    def _on_toggle_diagonal(self) -> None:
        self.grid.diagonal = self.diagonal.get()
        self.grid._dirs = DIRS_8 if self.diagonal.get() else DIRS_4
        self.grid._neighbors_cache.clear()
        if self.heuristic.get() == "manhattan" and self.diagonal.get():
            self.heuristic.set("octile")
        if self.heuristic.get() == "octile" and not self.diagonal.get():
            self.heuristic.set("manhattan")
        self._update_h_note()
        self._invalidate()
        self._redraw_state()

    def _update_h_note(self) -> None:
        algo = self.algorithm.get()
        if algo == MODE_BFS:
            self.h_note.configure(text="BFS: không dùng h(n), mọi bước tính bằng 1 "
                                       "(bỏ qua trọng số địa hình).")
            return
        if algo == MODE_UCS:
            self.h_note.configure(text="UCS/Dijkstra: h(n) = 0, luôn tối ưu nhưng duyệt nhiều đỉnh.")
            return
        h = self.heuristic.get()
        ok = H.is_admissible(h, self.diagonal.get())
        w = self.weight.get()
        msg = f"{h}: {H.describe(h)}"
        if not ok:
            msg += "  ⚠ KHÔNG khả dụng trên lưới 8 hướng -> có thể mất tính tối ưu!"
        elif algo == MODE_GREEDY:
            msg += "  ⚠ Greedy: chỉ xét h(n) -> nhanh nhưng không đảm bảo tối ưu."
        elif w > 1.0:
            msg += f"  ⚠ w = {w:g} > 1 (weighted A*): nhanh hơn nhưng có thể dưới tối ưu."
        self.h_note.configure(text=msg)

    # ------------------------------------------------------------------ #
    def zoom(self, delta: int) -> None:
        self.cell = max(8, min(48, self.cell + delta))
        self._draw_all()

    def fit_cells(self) -> None:
        self.canvas.update_idletasks()
        cw = max(200, self.canvas.winfo_width() - 4)
        ch = max(200, self.canvas.winfo_height() - 4)
        self.cell = max(6, min(48, int(min(cw / self.grid.width, ch / self.grid.height))))
        self._draw_all()

    # ================================================================== #
    # Sinh / nạp bản đồ
    # ================================================================== #
    def _load_sample(self, m: SampleMap, keep_size: bool = False) -> None:
        self.diagonal.set(m.grid.diagonal)
        self.grid = m.grid.copy()
        self.start, self.goal = m.start, m.goal
        self._invalidate()
        self._on_toggle_diagonal_silent()
        self._draw_all()
        self.status.configure(text=f"Đã nạp bản đồ mẫu: {m.name} - {m.description}")

    def _on_toggle_diagonal_silent(self) -> None:
        self.grid.diagonal = self.diagonal.get()
        self.grid._dirs = DIRS_8 if self.diagonal.get() else DIRS_4
        self.grid._neighbors_cache.clear()

    def gen_random(self) -> None:
        m = random_obstacles_map(self.grid.width, self.grid.height,
                                 self.density.get() / 100.0,
                                 seed=random.randint(0, 10**6),
                                 diagonal=self.diagonal.get())
        self._load_sample(m)

    def gen_maze(self) -> None:
        m = maze_map(self.grid.width, self.grid.height, seed=random.randint(0, 10**6),
                     diagonal=self.diagonal.get())
        self._load_sample(m)

    def gen_empty(self) -> None:
        self.grid.clear()
        self._invalidate()
        self._redraw_state()

    def open_map(self) -> None:
        path = filedialog.askopenfilename(
            title="Mở bản đồ", filetypes=[("Bản đồ văn bản", "*.txt"), ("Tất cả", "*.*")])
        if not path:
            return
        try:
            grid, start, goal = parse_map_file(path, diagonal=self.diagonal.get())
        except Exception as exc:  # pragma: no cover
            messagebox.showerror("Lỗi", f"Không đọc được bản đồ:\n{exc}")
            return
        self.grid = grid
        if start:
            self.start = start
        if goal:
            self.goal = goal
        self._invalidate()
        self._draw_all()

    def save_map(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Lưu bản đồ", defaultextension=".txt",
            filetypes=[("Bản đồ văn bản", "*.txt")])
        if not path:
            return
        save_map_file(path, self.grid, self.start, self.goal)
        self.status.configure(text=f"Đã lưu bản đồ vào {path}")

    # ================================================================== #
    # Chạy mô phỏng
    # ================================================================== #
    def _start_generator(self) -> None:
        self.open_g = {self.start: 0.0}
        self.closed = {}
        self.path = ()
        self.current = None
        self.result = None
        self.finished = False
        self.gen_time_ms = 0.0
        self.gen = search_steps(
            self.grid, self.start, self.goal,
            mode=self.algorithm.get(), heuristic=self.heuristic.get(),
            weight=float(self.weight.get()),
        )
        self.t0 = time.perf_counter()

    def run(self) -> None:
        if self.running:
            return
        if self.gen is None:
            self._start_generator()
        self.running = True
        self.status.configure(text="Đang mô phỏng ... (Space để dừng)")
        self._tick()

    def pause(self) -> None:
        self.running = False
        self.status.configure(text="Đã dừng mô phỏng. Bấm Chạy để tiếp tục.")

    def step_once(self) -> None:
        if self.gen is None:
            self._start_generator()
        self.running = False
        self._advance(1)
        self._refresh_stats()
        if self.finished:
            self._finish()
        else:
            self._redraw_state()

    def reset(self) -> None:
        self._invalidate()
        self._redraw_state()
        self.status.configure(text="Đã đặt lại. Sẵn sàng chạy mô phỏng mới.")

    def clear_search(self) -> None:
        self.open_g = {self.start: 0.0}
        self.closed = {}
        self.path = ()
        self.current = None
        self.result = None
        self.gen = None
        self.finished = True
        self._stop_loop()
        self._clear_stats()
        self._redraw_state()
        self.status.configure(text="Đã xoá kết quả tìm kiếm (giữ nguyên bản đồ).")

    def _tick(self) -> None:
        if not self.running:
            return
        budget = max(1, self.speed.get())
        self._advance(budget)
        self._refresh_stats()
        if self.finished:
            self._finish()
            return
        self.root.after(1, self._tick)

    def _advance(self, budget: int) -> None:
        """Xử lý tối đa `budget` sự kiện từ generator (tô màu từng ô ngay lập tức)."""
        if self.gen is None:
            return
        prev = self.current
        for _ in range(budget):
            t_call = time.perf_counter()
            try:
                event = next(self.gen)
            except StopIteration:  # pragma: no cover
                self.finished = True
                return
            # Chỉ cộng thời gian bộ máy tìm kiếm thực sự chạy (bỏ thời gian vẽ/nghỉ)
            self.gen_time_ms += (time.perf_counter() - t_call) * 1000.0
            kind = event[0]
            if kind == "expand":
                node, g = event[1], event[2]
                self.open_g.pop(node, None)
                self.closed[node] = g
                self.current = node
                if prev is not None and prev != node:
                    self._set_cell_color(
                        prev,
                        COLOR_CLOSED if prev in self.closed
                        else COLOR_OPEN if prev in self.open_g
                        else self._base_color(prev),
                    )
                prev = node
                self._set_cell_color(node, COLOR_CURRENT)
            elif kind == "frontier":
                node, g = event[1], event[2]
                self.open_g[node] = g
                if node not in self.closed:
                    self._set_cell_color(node, COLOR_OPEN)
            elif kind == "reuse":
                node, g = event[1], event[2]
                self.closed.pop(node, None)
                self.open_g[node] = g
                self._set_cell_color(node, COLOR_OPEN)
            elif kind == "done":
                self.result = event[1]
                self.path = tuple(self.result.path)
                self.finished = True
                return

    def _finish(self) -> None:
        self.running = False
        self.current = None
        self._redraw_state()
        r = self.result
        if r is None:
            return
        if r.found:
            self.status.configure(
                text=f"✔ Tìm thấy đường đi! chi phí = {r.cost:.3f} • {r.path_len} ô • "
                     f"duyệt {r.expanded} đỉnh • {self.gen_time_ms:.3f} ms (thời gian tìm kiếm)")
        else:
            self.status.configure(text="✘ Không tồn tại đường đi từ S tới G.")
        self._refresh_stats()

    # ================================================================== #
    # Thống kê
    # ================================================================== #
    def _clear_stats(self) -> None:
        for lb in self.stats.values():
            lb.configure(text="-")

    def _refresh_stats(self) -> None:
        r = self.result
        self.stats["algorithm"].configure(text=self.algorithm.get())
        hn = self.heuristic.get()
        if self.algorithm.get() in (MODE_UCS, MODE_BFS):
            hn = "-"
        self.stats["heuristic"].configure(text=hn)
        node = self.current
        if node is None:
            self.stats["current"].configure(text="-")
            self.stats["ghf"].configure(text="-")
        else:
            g = self.closed.get(node, self.open_g.get(node, 0.0))
            h = H.get(hn)(node, self.goal) * self.grid.min_step_cost
            f = g + float(self.weight.get()) * h
            self.stats["current"].configure(text=f"{node}")
            self.stats["ghf"].configure(text=f"{g:g} / {h:.2f} / {f:.2f}")
        self.stats["expanded"].configure(text=str(len(self.closed)))
        self.stats["sets"].configure(text=f"{len(self.open_g)} / {len(self.closed)}")
        if r is not None:
            self.stats["generated"].configure(text=str(r.generated))
            self.stats["depth"].configure(text=str(r.max_depth))
            self.stats["cost"].configure(
                text=f"{r.cost:.3f}" if r.found else "không có đường")
            self.stats["pathlen"].configure(
                text=f"{r.path_len} / {r.steps}" if r.found else "-")
            self.stats["time"].configure(text=f"{self.gen_time_ms:.3f}")
            self.stats["iters"].configure(text=str(r.iterations))

    # ================================================================== #
    # So sánh & xuất
    # ================================================================== #
    def _run_all(self) -> list[SearchResult]:
        grid = self.grid
        base_h = self.heuristic.get()
        plan = [
            (MODE_ASTAR, base_h, float(self.weight.get())),
            (MODE_UCS, "zero", 1.0),
            (MODE_GREEDY, "octile" if grid.diagonal else "manhattan", 1.0),
            (MODE_BFS, "-", 1.0),
        ]
        results: list[SearchResult] = []
        for mode, hn, w in plan:
            r = search(grid, self.start, self.goal, mode=mode, heuristic=hn, weight=w)
            r.cost = path_cost(grid, r.path) if r.found else INF
            results.append(r)
        self.last_results = results
        best = min((r.cost for r in results if r.found), default=None)
        for r in results:
            r.best = (best is not None and r.found and abs(r.cost - best) < 1e-6)  # type: ignore[attr-defined]
        return results

    def compare_all(self) -> None:
        results = self._run_all()
        best_cost = min((r.cost for r in results if r.found), default=None)
        win = tk.Toplevel(self.root)
        win.title("So sánh 4 thuật toán trên bản đồ hiện tại")
        win.configure(bg=PANEL_BG)
        head = (f"{'Thuật toán':<20}{'h(n)':<11}{'Chi phí':>10}{'Ô':>6}"
                f"{'Duyệt':>8}{'Sinh':>8}{'|OPEN|max':>10}{'TG(ms)':>10}")
        txt = tk.Text(win, bg="#151920", fg=FG, font=("Consolas", 10), padx=10, pady=8,
                      width=104, height=13, relief="flat", wrap="none")
        txt.pack(fill="both", expand=True, padx=8, pady=8)
        txt.insert("end", head + "\n" + "-" * 92 + "\n")
        for r in sorted(results, key=lambda x: (not x.found, x.cost)):
            star = "  ← tối ưu" if getattr(r, "best", False) else ""
            cost = f"{r.cost:.3f}" if r.found else "không có"
            txt.insert("end", f"{r.algorithm:<20}{r.heuristic:<11}{cost:>10}"
                              f"{r.path_len:>6}{r.expanded:>8}{r.generated:>8}"
                              f"{r.max_open:>10}{r.time_ms:>10.3f}{star}\n")
        txt.insert("end", "\nChi phí ở đây là chi phí THỰC (đã xét trọng số địa hình).\n")
        if best_cost is not None:
            txt.insert("end", f"Chi phí tối ưu của bản đồ này: {best_cost:.3f}\n")
        txt.configure(state="disabled")
        ttk.Button(win, text="Đóng", command=win.destroy).pack(pady=(0, 10))
        self.status.configure(text="Đã so sánh 4 thuật toán (xem cửa sổ kết quả).")

    def export_csv(self) -> None:
        if not self.last_results:
            self._run_all()
        os.makedirs("results", exist_ok=True)
        path = os.path.join("results", "ket_qua_gui.csv")
        with open(path, "w", newline="", encoding="utf-8-sig") as fh:
            writer = csv.writer(fh, delimiter=";")
            writer.writerow(["ban_do", f"{self.grid.width}x{self.grid.height}",
                             f"S={self.start}", f"G={self.goal}",
                             f"8_huong={int(self.grid.diagonal)}"])
            fields = list(self.last_results[0].as_dict().keys())
            writer.writerow(["thuat_toan_thuc"] + fields)
            for r in self.last_results:
                row = ["Chi phi THUC"] + [r.as_dict()[k] for k in fields]
                writer.writerow(row)
        messagebox.showinfo("Đã xuất", f"Đã ghi kết quả vào:\n{os.path.abspath(path)}")
        self.status.configure(text=f"Đã xuất CSV: {path}")

    # ================================================================== #
    # Phím tắt
    # ================================================================== #
    def bind_keys(self) -> None:
        r = self.root
        r.bind("<space>", lambda e: self.pause() if self.running else self.run())
        r.bind("<Key-c>", lambda e: self.clear_search())
        r.bind("<Key-C>", lambda e: self.clear_search())
        r.bind("<Key-s>", lambda e: self.tool.set("start"))
        r.bind("<Key-S>", lambda e: self.tool.set("start"))
        r.bind("<Key-g>", lambda e: self.tool.set("goal"))
        r.bind("<Key-G>", lambda e: self.tool.set("goal"))
        r.bind("<Key-r>", lambda e: self.gen_random())
        r.bind("<Key-R>", lambda e: self.gen_random())
        r.bind("<Key-m>", lambda e: self.gen_maze())
        r.bind("<Key-M>", lambda e: self.gen_maze())
        r.bind("<Key-d>", lambda e: (self.diagonal.set(not self.diagonal.get()),
                                     self._on_toggle_diagonal()))
        r.bind("<Key-D>", lambda e: (self.diagonal.set(not self.diagonal.get()),
                                     self._on_toggle_diagonal()))
        r.bind("<Key-n>", lambda e: self.step_once())
        for i, mode in enumerate(VIEW_MODES, start=1):
            r.bind(f"<Key-{i}>", lambda e, m=mode: (self.algorithm.set(m),
                                                    self._on_algo_change()))


def main() -> None:
    root = tk.Tk()
    app = AStarApp(root)
    app.bind_keys()
    root.mainloop()


if __name__ == "__main__":  # pragma: no cover
    main()
