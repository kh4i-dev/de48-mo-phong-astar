"""
grid.py - Biểu diễn bài toán tìm đường trên lưới (grid pathfinding).

Mỗi ô (cell) có một "trọng số" (weight) là chi phí để đi VÀO ô đó:

    - Ô trống            : weight = 1.0
    - Ô địa hình nặng    : weight > 1.0  (cát, nước, đồi dốc, ...)
    - Ô tường / vật cản  : weight = math.inf  (không đi vào được)

Lưới hỗ trợ 4 hướng (N/S/E/W) hoặc 8 hướng (thêm 4 hướng chéo với
chi phí sqrt(2) cho mỗi bước chéo, đúng như khoảng cách Euclid thực tế).
"""

from __future__ import annotations

import math
from typing import Iterator

INF = math.inf

# Kiểu dữ liệu của một đỉnh (ô) trên lưới: (row, col)
Node = tuple[int, int]

# Bộ hướng di chuyển: (delta_row, delta_col, hệ số nhân chi phí)
DIRS_4: tuple[tuple[int, int, float], ...] = (
    (-1, 0, 1.0),  # lên
    (1, 0, 1.0),   # xuống
    (0, -1, 1.0),  # trái
    (0, 1, 1.0),   # phải
)
DIRS_8: tuple[tuple[int, int, float], ...] = DIRS_4 + (
    (-1, -1, math.sqrt(2.0)),  # chéo trên-trái
    (-1, 1, math.sqrt(2.0)),   # chéo trên-phải
    (1, -1, math.sqrt(2.0)),   # chéo dưới-trái
    (1, 1, math.sqrt(2.0)),    # chéo dưới-phải
)

# Ký tự dùng trong biểu diễn lưới dạng văn bản (xem Grid.from_text)
TERRAIN_COST: dict[str, float] = {
    "#": INF,   # tường
    " ": 1.0,
    ".": 1.0,   # đường thường
    ":": 2.0,   # cỏ / đường mòn
    "~": 4.0,   # cát lún / nước nông
    "=": 6.0,   # bùn lầy / dốc đứng
}


class Grid:
    """Lưới chi phí có vật cản, hỗ trợ 4/8 hướng di chuyển."""

    def __init__(
        self,
        width: int,
        height: int,
        walls: set[Node] | None = None,
        diagonal: bool = False,
        allow_corner_cutting: bool = False,
        name: str = "grid",
    ) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("Kích thước lưới phải là số nguyên dương")
        self.width = int(width)
        self.height = int(height)
        self.name = name
        self.diagonal = bool(diagonal)
        self.allow_corner_cutting = bool(allow_corner_cutting)

        # Ma trận chi phí đi vào từng ô
        self.cost: list[list[float]] = [
            [1.0] * self.width for _ in range(self.height)
        ]
        for r, c in walls or ():
            if self.inside((r, c)):
                self.cost[r][c] = INF

        self._dirs = DIRS_8 if self.diagonal else DIRS_4
        self._neighbors_cache: dict[Node, tuple[tuple[Node, float], ...]] = {}

    # ------------------------------------------------------------------ #
    # Thuộc tính cơ bản
    # ------------------------------------------------------------------ #
    @property
    def cells(self) -> int:
        return self.width * self.height

    @property
    def walls(self) -> set[Node]:
        return {
            (r, c)
            for r in range(self.height)
            for c in range(self.width)
            if self.cost[r][c] == INF
        }

    @property
    def min_step_cost(self) -> float:
        """Chi phí nhỏ nhất để đi từ một ô sang ô kề (dùng cho tính khả dụng heuristic)."""
        best = INF
        for row in self.cost:
            for w in row:
                if w < best:
                    best = w
        if best == INF:  # lưới bị chặn hoàn toàn
            return 1.0
        return best

    @property
    def max_step_cost(self) -> float:
        best = 1.0
        for row in self.cost:
            for w in row:
                if w != INF and w > best:
                    best = w
        return best

    def inside(self, node: Node) -> bool:
        r, c = node
        return 0 <= r < self.height and 0 <= c < self.width

    def is_blocked(self, node: Node) -> bool:
        r, c = node
        return not self.inside(node) or self.cost[r][c] == INF

    def is_free(self, node: Node) -> bool:
        return not self.is_blocked(node)

    def weight(self, node: Node) -> float:
        r, c = node
        return self.cost[r][c]

    def set_wall(self, node: Node, blocked: bool = True) -> None:
        r, c = node
        if not self.inside(node):
            return
        self.cost[r][c] = INF if blocked else 1.0
        self._neighbors_cache.clear()

    def set_weight(self, node: Node, weight: float) -> None:
        r, c = node
        if not self.inside(node):
            return
        self.cost[r][c] = max(1.0, float(weight))
        self._neighbors_cache.clear()

    def clear(self, weight: float = 1.0) -> None:
        self.cost = [[weight] * self.width for _ in range(self.height)]
        self._neighbors_cache.clear()

    # ------------------------------------------------------------------ #
    # Sinh lân cận (neighbor generation)
    # ------------------------------------------------------------------ #
    def neighbors(self, node: Node) -> tuple[tuple[Node, float], ...]:
        """Trả về tuple các cặp (ô kề, chi phí bước đi). Có cache để chạy nhanh."""
        cached = self._neighbors_cache.get(node)
        if cached is not None:
            return cached

        r, c = node
        cost = self.cost
        out: list[tuple[Node, float]] = []
        for dr, dc, base in self._dirs:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < self.height and 0 <= nc < self.width):
                continue
            cw = cost[nr][nc]
            if cw == INF:
                continue
            if dr and dc and not self.allow_corner_cutting:
                # Không cho "cắt góc" xuyên qua khe hở giữa hai tường
                if cost[r][nc] == INF or cost[nr][c] == INF:
                    continue
            out.append(((nr, nc), base * cw))

        result = tuple(out)
        self._neighbors_cache[node] = result
        return result

    def iter_free_cells(self) -> Iterator[Node]:
        for r in range(self.height):
            row = self.cost[r]
            for c in range(self.width):
                if row[c] != INF:
                    yield (r, c)

    # ------------------------------------------------------------------ #
    # Nhập / xuất dạng văn bản
    # ------------------------------------------------------------------ #
    @classmethod
    def from_text(
        cls,
        lines: list[str],
        diagonal: bool = False,
        name: str = "grid",
    ) -> tuple["Grid", Node | None, Node | None]:
        """Dựng lưới từ khung ký tự. '#'=tường, '.'=trống, '~',':','='=địa hình,
        'S'/'s'=xuất phát, 'G'/'g'=đích."""
        rows = [ln.rstrip("\n") for ln in lines if ln.strip("\n") != ""]
        if not rows:
            raise ValueError("Dữ liệu lưới rỗng")
        height = len(rows)
        width = max(len(r) for r in rows)
        grid = cls(width, height, name=name, diagonal=diagonal)

        start: Node | None = None
        goal: Node | None = None
        for r, line in enumerate(rows):
            for c in range(width):
                ch = line[c] if c < len(line) else "#"
                if ch in ("S", "s"):
                    start = (r, c)
                    grid.cost[r][c] = 1.0
                elif ch in ("G", "g"):
                    goal = (r, c)
                    grid.cost[r][c] = 1.0
                elif ch == "o":  # cách viết khác cho ô trống
                    grid.cost[r][c] = 1.0
                else:
                    grid.cost[r][c] = TERRAIN_COST.get(ch, 1.0)
        return grid, start, goal

    def to_text(self, start: Node | None = None, goal: Node | None = None,
                path: list[Node] | tuple[Node, ...] | None = None,
                closed: set[Node] | None = None,
                open_set: set[Node] | None = None) -> str:
        """Kết xuất lưới ra văn bản để in ra console (trực quan hoá)."""
        path_set = set(path or ())
        closed = closed or set()
        open_set = open_set or set()
        lines: list[str] = []
        for r in range(self.height):
            row: list[str] = []
            for c in range(self.width):
                node = (r, c)
                w = self.cost[r][c]
                if node == start:
                    ch = "S"
                elif node == goal:
                    ch = "G"
                elif w == INF:
                    ch = "#"
                elif node in path_set:
                    ch = "*"
                elif node in closed:
                    ch = "o"   # đã duyệt xong (đóng)
                elif node in open_set:
                    ch = "-"   # đang chờ trong tập mở
                elif w >= 6.0:
                    ch = "="
                elif w >= 4.0:
                    ch = "~"
                elif w >= 2.0:
                    ch = ":"
                else:
                    ch = "."
                row.append(ch)
            lines.append("".join(row))
        return "\n".join(lines)

    def copy(self) -> "Grid":
        g = Grid(self.width, self.height, diagonal=self.diagonal,
                 allow_corner_cutting=self.allow_corner_cutting, name=self.name)
        g.cost = [row[:] for row in self.cost]
        return g

    def __repr__(self) -> str:  # pragma: no cover
        return f"Grid({self.name!r}, {self.width}x{self.height}, diagonal={self.diagonal})"


def manhattan_grid(width: int, height: int) -> Grid:
    """Lưới trống kích thước cho trước."""
    return Grid(width, height, name=f"trong_{width}x{height}")


def parse_map_file(path: str, diagonal: bool = False) -> tuple[Grid, Node | None, Node | None]:
    """Đọc lưới từ file .txt (mỗi dòng một hàng ký tự)."""
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    return Grid.from_text(lines, diagonal=diagonal, name=path)


def save_map_file(path: str, grid: Grid, start: Node | None = None,
                  goal: Node | None = None) -> None:
    """Ghi lưới ra file .txt dạng ký tự."""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(grid.to_text(start=start, goal=goal) + "\n")
