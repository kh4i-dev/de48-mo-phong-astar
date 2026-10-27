"""
maps.py - Sinh và nạp các bộ dữ liệu mẫu (bản đồ lưới) cho thực nghiệm.

Gồm 6 nhóm dữ liệu đại diện cho các tình huống khác nhau:
    1. trong          - lưới trống (đường đi là đường chéo/đường thẳng lý tưởng)
    2. vat_can_ngau_nhien - vật cản ngẫu nhiên (kiểm thử khả năng vòng tránh)
    3. me_cung         - mê cung ngẫu nhiên (hành lang quanh co)
    4. phong_hanh_lang - nhiều phòng thông nhau bằng cửa hẹp
    5. xoan_oc         - hành lang xoắn ốc (kiểm thử khả năng "thoát kẹt")
    6. dia_hinh        - lưới có trọng số địa hình (A* phải cân nhắc chi phí)
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import Iterable

from .grid import Grid, INF, Node

random.seed(12345)


@dataclass
class SampleMap:
    """Một bộ dữ liệu mẫu hoàn chỉnh."""

    key: str
    name: str
    description: str
    grid: Grid
    start: Node
    goal: Node

    @property
    def size_text(self) -> str:
        return f"{self.grid.width}x{self.grid.height}"

    @property
    def wall_ratio(self) -> float:
        walls = sum(1 for row in self.grid.cost for w in row if w == INF)
        return walls / self.grid.cells


# ---------------------------------------------------------------------- #
# Công cụ phụ trợ
# ---------------------------------------------------------------------- #
def _is_reachable(grid: Grid, start: Node, goal: Node) -> bool:
    """BFS kiểm tra nhanh xem đích có tới được không."""
    seen = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        if node == goal:
            return True
        for nb, _ in grid.neighbors(node):
            if nb not in seen:
                seen.add(nb)
                stack.append(nb)
    return False


# ---------------------------------------------------------------------- #
# 1. Lưới trống
# ---------------------------------------------------------------------- #
def open_map(width: int = 30, height: int = 20, diagonal: bool = False) -> SampleMap:
    grid = Grid(width, height, diagonal=diagonal, name="trong")
    start, goal = (height - 1, 0), (0, width - 1)
    return SampleMap(
        key="trong", name="Lưới trống",
        description="Không có vật cản - quan sát A* đi thẳng/chéo về đích.",
        grid=grid, start=start, goal=goal,
    )


# ---------------------------------------------------------------------- #
# 2. Vật cản ngẫu nhiên
# ---------------------------------------------------------------------- #
def random_obstacles_map(
    width: int = 40,
    height: int = 25,
    density: float = 0.25,
    seed: int = 7,
    diagonal: bool = False,
) -> SampleMap:
    rng = random.Random(seed)
    start, goal = (height - 1, 0), (0, width - 1)
    for _ in range(200):
        walls = {
            (r, c)
            for r in range(height)
            for c in range(width)
            if rng.random() < density
        }
        walls.discard(start)
        walls.discard(goal)
        grid = Grid(width, height, walls=walls, diagonal=diagonal, name="vat_can")
        if _is_reachable(grid, start, goal):
            return SampleMap(
                key="vat_can_ngau_nhien",
                name=f"Vật cản ngẫu nhiên ({density:.0%})",
                description="Vật cản rải rác - kiểm thử khả năng vòng tránh và tối ưu chi phí.",
                grid=grid, start=start, goal=goal,
            )
    raise RuntimeError("Không sinh được bản đồ ngẫu nhiên liên thông")  # pragma: no cover


# ---------------------------------------------------------------------- #
# 3. Mê cung ngẫu nhiên (thuật toán đào lùi - recursive backtracker)
# ---------------------------------------------------------------------- #
def maze_map(width: int = 41, height: int = 25, seed: int = 42,
             diagonal: bool = False) -> SampleMap:
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1
    rng = random.Random(seed)
    grid = Grid(width, height, diagonal=diagonal, name="me_cung")

    # Ban đầu tất cả là tường
    for r in range(height):
        for c in range(width):
            grid.cost[r][c] = INF

    def carve(node: Node) -> None:
        grid.cost[node[0]][node[1]] = 1.0

    start = (1, 1)
    carve(start)
    stack = [start]
    visited = {start}
    while stack:
        r, c = stack[-1]
        neighbors = [
            (r - 2, c), (r + 2, c), (r, c - 2), (r, c + 2)
        ]
        rng.shuffle(neighbors)
        moved = False
        for nr, nc in neighbors:
            if 1 <= nr < height - 1 and 1 <= nc < width - 1 and (nr, nc) not in visited:
                carve(((r + nr) // 2, (c + nc) // 2))   # đục vách giữa
                carve((nr, nc))
                visited.add((nr, nc))
                stack.append((nr, nc))
                moved = True
                break
        if not moved:
            stack.pop()

    goal = (height - 2, width - 2)
    carve(goal)
    # Nối đích vào mê cung nếu bị tách rời
    if not _is_reachable(grid, start, goal):
        for dc in range(width - 2, 0, -1):
            if grid.cost[goal[0]][dc] == INF:
                grid.cost[goal[0]][dc] = 1.0
            else:
                break
    return SampleMap(
        key="me_cung", name="Mê cung ngẫu nhiên",
        description="Hành lang quan co, đúng 1 đường duy nhất - A* bộc lộ rõ sức mạnh dẫn hướng.",
        grid=grid, start=start, goal=goal,
    )


# ---------------------------------------------------------------------- #
# 4. Phòng và hành lang
# ---------------------------------------------------------------------- #
def rooms_map(width: int = 60, height: int = 30, rooms: int = 10,
              seed: int = 2024, diagonal: bool = False) -> SampleMap:
    rng = random.Random(seed)
    grid = Grid(width, height, diagonal=diagonal, name="phong")
    # Bao tường quanh biên
    for r in range(height):
        for c in range(width):
            if r in (0, height - 1) or c in (0, width - 1):
                grid.cost[r][c] = INF

    centers: list[Node] = []
    for _ in range(rooms * 12):
        if len(centers) >= rooms:
            break
        w = rng.randint(5, 12)
        h = rng.randint(4, 8)
        r0 = rng.randint(1, max(1, height - h - 2))
        c0 = rng.randint(1, max(1, width - w - 2))
        r1, c1 = min(height - 2, r0 + h), min(width - 2, c0 + w)
        ok = all(
            abs((r0 + r1) // 2 - cr) + abs((c0 + c1) // 2 - cc) > 6
            for cr, cc in centers
        )
        if not ok:
            continue
        centers.append(((r0 + r1) // 2, (c0 + c1) // 2))
        # đào phòng
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                grid.cost[r][c] = 1.0
                if r in (r0, r1) or c in (c0, c1):
                    grid.cost[r][c] = INF
        # cửa
        for _ in range(2):
            if rng.random() < 0.5:
                r = rng.choice([r0, r1])
                c = rng.randint(c0 + 1, c1 - 1)
            else:
                c = rng.choice([c0, c1])
                r = rng.randint(r0 + 1, r1 - 1)
            grid.cost[r][c] = 1.0

    # nối các phòng bằng hành lang chữ L
    centers.sort()
    for (r1, c1), (r2, c2) in zip(centers, centers[1:]):
        for c in range(min(c1, c2), max(c1, c2) + 1):
            if 0 < c < width - 1:
                grid.cost[r1][c] = 1.0
        for r in range(min(r1, r2), max(r1, r2) + 1):
            if 0 < r < height - 1:
                grid.cost[r][c2] = 1.0

    start = centers[0] if centers else (1, 1)
    goal = centers[-1] if centers else (height - 2, width - 2)
    for node in (start, goal):
        grid.cost[node[0]][node[1]] = 1.0
    if not _is_reachable(grid, start, goal):
        # đảm bảo liên thông bằng cách đục một hành lang ngang
        for r in range(1, height - 1):
            grid.cost[r][width // 2] = 1.0
    return SampleMap(
        key="phong_hanh_lang", name="Phòng & hành lang",
        description="Cấu trúc phòng lớn nối bằng cửa hẹp - giống bản đồ nhà máy/toà nhà.",
        grid=grid, start=start, goal=goal,
    )


# ---------------------------------------------------------------------- #
# 5. Hành lang xoắn ốc
# ---------------------------------------------------------------------- #
def spiral_map(size: int = 25, diagonal: bool = False) -> SampleMap:
    """Sinh hành lang xoắn ốc: mô phỏng con rắn đi vòng vào tâm.

    Mỗi vòng cách nhau đúng 1 ô tường, và TOÀN BỘ hành lang chỉ có MỘT lối đi
    duy nhất -> bản đồ "xấu nhất" cho tìm kiếm có thông tin.
    """
    if size % 2 == 0:
        size += 1
    size = max(9, size)
    grid = Grid(size, size, diagonal=diagonal, name="xoan_oc")
    for r in range(size):
        for c in range(size):
            grid.cost[r][c] = INF

    start = (1, 1)
    r, c = start
    path: list[Node] = [start]
    top, bottom, left, right = 1, size - 2, 1, size - 2

    while True:
        while c < right:                      # sang phải
            c += 1
            path.append((r, c))
        top += 2
        if top > bottom:
            break
        while r < bottom:                     # xuống
            r += 1
            path.append((r, c))
        right -= 2
        if left > right:
            break
        while c > left:                       # sang trái
            c -= 1
            path.append((r, c))
        bottom -= 2
        if top > bottom:
            break
        while r > top:                        # lên
            r -= 1
            path.append((r, c))
        left += 2
        if left > right:
            break

    for node in path:
        grid.cost[node[0]][node[1]] = 1.0
    return SampleMap(
        key="xoan_oc", name="Hành lang xoắn ốc",
        description="Một hành lang duy nhất xoắn vào tâm - thử thách nặng nhất cho tính dẫn hướng của h(n).",
        grid=grid, start=start, goal=path[-1],
    )


# ---------------------------------------------------------------------- #
# 6. Lưới có trọng số địa hình
# ---------------------------------------------------------------------- #
def terrain_map(width: int = 45, height: int = 28, seed: int = 99,
                diagonal: bool = False) -> SampleMap:
    rng = random.Random(seed)
    grid = Grid(width, height, diagonal=diagonal, name="dia_hinh")
    levels = [(2.0, 1), (4.0, 2), (6.0, 1)]
    for _ in range(14):
        weight, count = rng.choice(levels)
        r0 = rng.randint(0, height - 1)
        c0 = rng.randint(0, width - 1)
        rw = rng.randint(3, 8)
        rh = rng.randint(3, 8)
        for r in range(max(0, r0 - rh), min(height, r0 + rh + 1)):
            for c in range(max(0, c0 - rw), min(width, c0 + rw + 1)):
                if rng.random() < 0.75:
                    grid.cost[r][c] = weight
    for _ in range(6):  # thêm vài bức tường ngắn (rào chắn cục bộ)
        r = rng.randint(1, height - 2)
        c = rng.randint(1, width - 2)
        for dr in range(-2, 3):
            grid.cost[min(height - 1, max(0, r + dr))][c] = INF

    start, goal = (height - 1, 0), (0, width - 1)
    grid.cost[start[0]][start[1]] = 1.0
    grid.cost[goal[0]][goal[1]] = 1.0
    if not _is_reachable(grid, start, goal):
        for r in range(1, height - 1):
            grid.cost[r][width // 2] = 1.0
    return SampleMap(
        key="dia_hinh", name="Địa hình trọng số",
        description="Vùng cát/bùn/nước có chi phí 2, 4, 6 - đường ngắn nhất chưa chắc rẻ nhất.",
        grid=grid, start=start, goal=goal,
    )


# ---------------------------------------------------------------------- #
# Registry + nhập/xuất JSON
# ---------------------------------------------------------------------- #
def sample_maps(diagonal: bool = False, size_scale: float = 1.0) -> list[SampleMap]:
    """Trả về danh sách bộ dữ liệu mẫu đã chuẩn hoá kích thước."""
    def s(v: int) -> int:
        return max(7, int(round(v * size_scale)))

    spiral_n = s(25)
    if spiral_n % 2 == 0:
        spiral_n += 1
    return [
        open_map(s(30), s(20), diagonal=diagonal),
        random_obstacles_map(s(40), s(25), 0.25, seed=7, diagonal=diagonal),
        maze_map(s(41), s(25), seed=42, diagonal=diagonal),
        rooms_map(s(60), s(30), rooms=10, seed=2024, diagonal=diagonal),
        spiral_map(spiral_n, diagonal=diagonal),
        terrain_map(s(45), s(28), seed=99, diagonal=diagonal),
    ]


def to_json(maps: Iterable[SampleMap], path: str) -> None:
    """Lưu các bản đồ mẫu ra file JSON để tái sử dụng."""
    payload = []
    for m in maps:
        payload.append({
            "key": m.key,
            "name": m.name,
            "description": m.description,
            "width": m.grid.width,
            "height": m.grid.height,
            "start": list(m.start),
            "goal": list(m.goal),
            "cost": [
                ["inf" if w == INF else round(w, 3) for w in row]
                for row in m.grid.cost
            ],
        })
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)


def from_json(path: str, diagonal: bool = False) -> list[SampleMap]:
    """Đọc bản đồ mẫu từ file JSON."""
    with open(path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    out: list[SampleMap] = []
    for item in payload:
        grid = Grid(item["width"], item["height"], diagonal=diagonal, name=item["key"])
        for r, row in enumerate(item["cost"]):
            for c, w in enumerate(row):
                grid.cost[r][c] = INF if w == "inf" else float(w)
        out.append(SampleMap(
            key=item["key"], name=item["name"], description=item["description"],
            grid=grid, start=tuple(item["start"]), goal=tuple(item["goal"]),
        ))
    return out
