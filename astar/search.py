"""
search.py - Bộ máy tìm kiếm trên lưới.

Cài đặt TỔNG QUÁT cho các biến thể cùng họ "tìm kiếm có thông tin / chi phí":

    | mode        | hàm ưu tiên f(n)            | tối ưu? | ghi chú                    |
    |-------------|-----------------------------|---------|----------------------------|
    | A*          | f = g + w·h                 | có*     | * nếu h khả dụng và w = 1  |
    | UCS/Dijkstra| f = g                       | có      | h = 0                      |
    | Greedy      | f = h                       | không   | nhanh nhưng dễ kẹt cục bộ  |
    | BFS         | FIFO, mọi bước = 1          | chỉ khi mọi trọng số bằng nhau |

Mọi thuật toán đều phát ra các SỰ KIỆN (event) dưới dạng generator, nhờ đó
giao diện có thể vẽ quá trình tìm kiếm theo từng bước (animation).
"""

from __future__ import annotations

import heapq
import itertools
import math
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Iterator

from . import heuristics as H
from .grid import Grid, INF, Node

MODE_ASTAR = "A*"
MODE_UCS = "UCS (Dijkstra)"
MODE_GREEDY = "Greedy Best-First"
MODE_BFS = "BFS"

ALL_MODES = (MODE_ASTAR, MODE_UCS, MODE_GREEDY, MODE_BFS)
EPS = 1e-9


# ---------------------------------------------------------------------- #
# Kết quả
# ---------------------------------------------------------------------- #
@dataclass
class SearchResult:
    """Toàn bộ số liệu đo được của một lần chạy tìm kiếm."""

    algorithm: str = ""
    heuristic: str = "-"
    weight: float = 1.0
    diagonal: bool = False
    allow_reopen: bool = True
    found: bool = False
    path: tuple[Node, ...] = ()
    cost: float = INF
    expanded: int = 0        # số đỉnh đã lấy ra khỏi OPEN và duyệt (đóng)
    generated: int = 0       # số lần sinh đỉnh mới vào OPEN
    relaxations: int = 0     # số lần cập nhật g(n) tốt hơn
    reused: int = 0          # số lần mở lại một đỉnh đã đóng
    iterations: int = 0      # số vòng lặp chính
    max_open: int = 0        # kích thước lớn nhất của tập OPEN (bộ nhớ đỉnh cao)
    max_depth: int = 0       # độ sâu lớn nhất của cây tìm kiếm
    time_ms: float = 0.0
    closed: set[Node] = field(default_factory=set, repr=False)
    open_left: set[Node] = field(default_factory=set, repr=False)

    @property
    def path_len(self) -> int:
        """Số ô trên đường đi (bao gồm cả điểm đầu và điểm cuối)."""
        return len(self.path)

    @property
    def steps(self) -> int:
        """Số bước đi (số cạnh trên đường đi)."""
        return max(0, len(self.path) - 1)

    def summary(self) -> str:
        if not self.found:
            return (
                f"{self.algorithm:>16} | {self.heuristic:<9} | KHÔNG tìm thấy đường | "
                f"duyệt={self.expanded:<6} sinh={self.generated:<6} "
                f"open_max={self.max_open:<5} thời gian={self.time_ms:8.3f} ms"
            )
        return (
            f"{self.algorithm:>16} | {self.heuristic:<9} | "
            f"cost={self.cost:8.3f} | ô={self.path_len:<4} duyệt={self.expanded:<6} "
            f"sinh={self.generated:<6} open_max={self.max_open:<5} "
            f"độ sâu={self.max_depth:<4} thời gian={self.time_ms:8.3f} ms"
        )

    def as_dict(self) -> dict[str, object]:
        """Dạng phẳng để ghi CSV / báo cáo."""
        return {
            "thuat_toan": self.algorithm,
            "heuristic": self.heuristic,
            "trong_so_w": self.weight,
            "8_huong": int(self.diagonal),
            "tim_thay": int(self.found),
            "chi_phi_duong_di": round(self.cost, 4) if self.found else "",
            "so_o_tren_duong": self.path_len,
            "so_buoc": self.steps,
            "so_dinh_duyet": self.expanded,
            "so_dinh_sinh": self.generated,
            "so_lan_cap_nhat_g": self.relaxations,
            "so_lan_mo_lai": self.reused,
            "open_lon_nhat": self.max_open,
            "do_sau_lon_nhat": self.max_depth,
            "thoi_gian_ms": round(self.time_ms, 4),
        }


# ---------------------------------------------------------------------- #
# Bộ máy chính
# ---------------------------------------------------------------------- #
def search_steps(
    grid: Grid,
    start: Node,
    goal: Node,
    mode: str = MODE_ASTAR,
    heuristic: str = H.DEFAULT_NAME,
    weight: float = 1.0,
    tie_break: bool = True,
    keep_sets: bool = False,
    allow_reopen: bool = True,
) -> Iterator[tuple]:
    """Chạy tìm kiếm và phát ra sự kiện.

    allow_reopen:
        True  - cho phép "mở lại" đỉnh đã đóng khi tìm được g(n) nhỏ hơn
                (cần thiết khi h(n) không nhất quán; trung thực về mặt lý thuyết).
        False - khoá tập CLOSED. Chạy nhanh hơn, nhưng với h(n) không khả dụng
                (ví dụ weighted A* với w > 1) có thể cho đường DƯỚI tối ưu.

    Sự kiện:

    Sự kiện:
        ("expand",  node, g)             - đỉnh vừa được lấy ra khỏi OPEN
        ("frontier", node, g)            - đỉnh mới/cập nhật trong OPEN
        ("reuse",   node, g)             - đỉnh đã đóng được mở lại
        ("done",    SearchResult)        - kết thúc (luôn là sự kiện cuối)
    """
    if heuristic == "dijkstra":
        heuristic = "zero"
    h_fn = H.get(heuristic)

    result = SearchResult(
        algorithm=mode, heuristic=heuristic if mode != MODE_UCS else "-",
        weight=float(weight), diagonal=grid.diagonal, allow_reopen=bool(allow_reopen),
    )
    t0 = time.perf_counter()

    # --- Kiểm tra đầu vào -------------------------------------------------
    if grid.is_blocked(start) or grid.is_blocked(goal):
        result.time_ms = (time.perf_counter() - t0) * 1000.0
        if keep_sets:
            result.closed, result.open_left = set(), set()
        yield ("done", result)
        return

    if start == goal:
        result.found, result.path, result.cost = True, (start,), 0.0
        result.time_ms = (time.perf_counter() - t0) * 1000.0
        yield ("expand", start, 0.0)
        if keep_sets:
            result.closed, result.open_left = {start}, set()
        yield ("done", result)
        return

    # --- BFS: hàng đợi FIFO, mọi bước tính bằng 1 (bỏ qua trọng số) -------
    if mode == MODE_BFS:
        yield from _bfs_steps(grid, start, goal, result, t0, keep_sets)
        return

    # --- Các thuật toán có chi phí ---------------------------------------
    gscore: dict[Node, float] = {start: 0.0}
    parent: dict[Node, Node | None] = {start: None}
    depth: dict[Node, int] = {start: 0}
    closed: set[Node] = set()
    heap: list[tuple[float, float, int, Node]] = []
    counter = itertools.count()
    scale = grid.min_step_cost

    def priority(node: Node, g: float) -> tuple[float, float]:
        if mode == MODE_GREEDY:
            h = h_fn(node, goal) * scale
            return h, h
        h = h_fn(node, goal) * scale if h_fn is not H.zero else 0.0
        return g + weight * h, (h if tie_break else 0.0)

    def push(node: Node, g: float) -> None:
        f, tie = priority(node, g)
        heapq.heappush(heap, (f, tie, next(counter), node))

    push(start, 0.0)
    result.generated = 1

    while heap:
        f, _, _, node = heapq.heappop(heap)
        if node in closed:
            continue                      # bản ghi cũ, đã duyệt rồi

        closed.add(node)
        gnode = gscore[node]
        result.expanded += 1
        result.iterations += 1
        result.max_open = max(result.max_open, len(heap))
        result.max_depth = max(result.max_depth, depth[node])
        yield ("expand", node, gnode)

        if node == goal:
            path = _reconstruct(parent, goal)
            result.found = True
            result.path = path
            result.cost = _path_cost(grid, path)
            result.time_ms = (time.perf_counter() - t0) * 1000.0
            if keep_sets:
                result.closed = closed
                result.open_left = {n for _, _, _, n in heap if n not in closed}
            yield ("done", result)
            return

        for nb, step in grid.neighbors(node):
            ng = gnode + step
            if ng >= gscore.get(nb, INF) - EPS:
                continue
            is_reopen = nb in closed
            if is_reopen:
                if mode == MODE_GREEDY or not allow_reopen:
                    continue              # GBFS cổ điển / chế độ khoá CLOSED
                closed.discard(nb)
                result.reused += 1
                yield ("reuse", nb, ng)
            # cập nhật
            gscore[nb] = ng
            parent[nb] = node
            depth[nb] = depth[node] + 1
            result.relaxations += 1
            result.generated += 1
            push(nb, ng)
            yield ("frontier", nb, ng)

    # OPEN rỗng -> không có đường đi
    result.time_ms = (time.perf_counter() - t0) * 1000.0
    if keep_sets:
        result.closed = closed
        result.open_left = set()
    yield ("done", result)


def _bfs_steps(
    grid: Grid,
    start: Node,
    goal: Node,
    result: SearchResult,
    t0: float,
    keep_sets: bool,
) -> Iterator[tuple]:
    """BFS trên lưới (mọi bước có chi phí 1, không xét địa hình trọng số)."""
    came: dict[Node, Node | None] = {start: None}
    depth: dict[Node, int] = {start: 0}
    closed: set[Node] = set()
    queue = deque([start])
    result.generated = 1

    while queue:
        node = queue.popleft()
        if node in closed:
            continue
        closed.add(node)
        result.expanded += 1
        result.iterations += 1
        result.max_open = max(result.max_open, len(queue))
        result.max_depth = max(result.max_depth, depth[node])
        yield ("expand", node, float(depth[node]))

        if node == goal:
            path: list[Node] = []
            cur: Node | None = goal
            while cur is not None:
                path.append(cur)
                cur = came[cur]
            path.reverse()
            result.found = True
            result.path = tuple(path)
            result.cost = float(len(path) - 1)
            result.heuristic = "-"
            result.time_ms = (time.perf_counter() - t0) * 1000.0
            if keep_sets:
                result.closed, result.open_left = closed, set(queue)
            yield ("done", result)
            return

        for nb, _step in grid.neighbors(node):
            if nb in came and nb in closed:
                continue
            if nb in came:
                continue
            came[nb] = node
            depth[nb] = depth[node] + 1
            result.generated += 1
            queue.append(nb)
            yield ("frontier", nb, float(depth[nb]))

    result.time_ms = (time.perf_counter() - t0) * 1000.0
    result.heuristic = "-"
    if keep_sets:
        result.closed, result.open_left = closed, set()
    yield ("done", result)


# ---------------------------------------------------------------------- #
# Hàm tiện dụng
# ---------------------------------------------------------------------- #
def _reconstruct(parent: dict[Node, Node | None], goal: Node) -> tuple[Node, ...]:
    path: list[Node] = []
    cur: Node | None = goal
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()
    return tuple(path)


def _path_cost(grid: Grid, path: tuple[Node, ...]) -> float:
    total = 0.0
    for a, b in zip(path, path[1:]):
        dr = abs(a[0] - b[0])
        dc = abs(a[1] - b[1])
        base = math.sqrt(2.0) if (dr and dc) else 1.0
        total += base * grid.weight(b)
    return total


def search(
    grid: Grid,
    start: Node,
    goal: Node,
    mode: str = MODE_ASTAR,
    heuristic: str = H.DEFAULT_NAME,
    weight: float = 1.0,
    keep_sets: bool = False,
    allow_reopen: bool = True,
) -> SearchResult:
    """Chạy tìm kiếm đến khi xong và trả về SearchResult."""
    for event in search_steps(
        grid, start, goal, mode=mode, heuristic=heuristic,
        weight=weight, keep_sets=keep_sets, allow_reopen=allow_reopen,
    ):
        if event[0] == "done":
            return event[1]
    raise RuntimeError("Bộ máy tìm kiếm không trả về kết quả")  # pragma: no cover


def astar(
    grid: Grid,
    start: Node,
    goal: Node,
    heuristic: str = H.DEFAULT_NAME,
    weight: float = 1.0,
    keep_sets: bool = False,
) -> SearchResult:
    """Gọi tắt A*."""
    return search(grid, start, goal, MODE_ASTAR, heuristic, weight, keep_sets)


def dijkstra(grid: Grid, start: Node, goal: Node, **kw) -> SearchResult:
    """UCS / Dijkstra: A* với h(n) = 0."""
    return search(grid, start, goal, MODE_UCS, "zero", **kw)


def greedy(grid: Grid, start: Node, goal: Node, heuristic: str = "octile", **kw) -> SearchResult:
    return search(grid, start, goal, MODE_GREEDY, heuristic, **kw)


def bfs(grid: Grid, start: Node, goal: Node, **kw) -> SearchResult:
    return search(grid, start, goal, MODE_BFS, **kw)


def path_cost(grid: Grid, path: tuple[Node, ...] | list[Node]) -> float:
    """Chi phí THỰC của một đường đi (có xét trọng số địa hình).

    Dùng để so sánh công bằng: BFS/Greedy có thể cho đường ít bước nhưng
    chi phí thực (qua cát/bùn) lại đắt.
    """
    return _path_cost(grid, tuple(path))


def validate_path(grid: Grid, start: Node, goal: Node,
                  path: tuple[Node, ...] | list[Node]) -> tuple[bool, str]:
    """Kiểm tra tính hợp lệ của đường đi: liền kề, không xuyên tường, đúng đầu-cuối."""
    if not path:
        return False, "đường rỗng"
    if path[0] != start:
        return False, "điểm đầu sai"
    if path[-1] != goal:
        return False, "điểm cuối sai"
    if len(set(path)) != len(path):
        return False, "đường đi lặp ô (có chu trình)"
    for a, b in zip(path, path[1:]):
        if abs(a[0] - b[0]) > 1 or abs(a[1] - b[1]) > 1:
            return False, f"bước nhảy không liền kề: {a} -> {b}"
        allowed = {n for n, _ in grid.neighbors(a)}
        if b not in allowed:
            return False, f"bước đi xuyên tường / bị chặn: {a} -> {b}"
    return True, "hợp lệ"
