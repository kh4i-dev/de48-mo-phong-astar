"""
heuristics.py - Các hàm ước lượng h(n) dùng cho A*.

Quy ước:
    - Mọi hàm ở đây trả về KHOẢNG CÁCH HÌNH HỌC (đơn vị: "số ô").
    - Bộ máy tìm kiếm sẽ tự nhân thêm `grid.min_step_cost` để giữ tính
      KHẢ DỤNG (admissible) khi lưới có địa hình trọng số > 1.

Ghi chú lý thuyết:
    * h(n) khả dụng (admissible)  : h(n) <= h*(n) với mọi n  -> A* tối ưu.
    * h(n) nhất quán (consistent): h(n) <= c(n,n') + h(n')   -> A* tối ưu
      và không cần mở lại đỉnh (không cần re-open).
    * h(n) = 0 với mọi n  <=>  Dijkstra (UCS).
    * h(n) quá lớn ("tham lam") -> mất tính tối ưu nhưng duyệt ít đỉnh hơn.
"""

from __future__ import annotations

import math
from typing import Callable

from .grid import Grid, Node

SQRT2 = math.sqrt(2.0)

DistanceFn = Callable[[Node, Node], float]


# ---------------------------------------------------------------------- #
# Các hàm khoảng cách cơ sở (nhận 2 toạ độ)
# ---------------------------------------------------------------------- #
def manhattan(a: Node, b: Node) -> float:
    """Khoảng cách L1 - khả dụng cho lưới 4 hướng."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a: Node, b: Node) -> float:
    """Khoảng cách L2 - khả dụng cho cả 4 và 8 hướng (luôn <= thực tế)."""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def chebyshev(a: Node, b: Node) -> float:
    """Khoảng cách L-inf (max) - khả dụng cho lưới 8 hướng khi bước chéo = 1."""
    return float(max(abs(a[0] - b[0]), abs(a[1] - b[1])))


def octile(a: Node, b: Node) -> float:
    """Khoảng cách octile - KHỚP chính xác chi phí lưới 8 hướng (chéo = sqrt2).

    Là heuristic tốt nhất (chặt nhất mà vẫn khả dụng) cho lưới 8 hướng.
    """
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return (dx + dy) + (SQRT2 - 2.0) * min(dx, dy)


def zero(a: Node, b: Node) -> float:
    """h(n) = 0 -> A* thoái hoá thành Dijkstra (UCS)."""
    return 0.0


# ---------------------------------------------------------------------- #
# Registry
# ---------------------------------------------------------------------- #
_HEURISTICS: dict[str, tuple[DistanceFn, str]] = {
    "manhattan": (manhattan, "L1 - tốt cho lưới 4 hướng"),
    "euclidean": (euclidean, "L2 - an toàn cho cả 4/8 hướng"),
    "chebyshev": (chebyshev, "L∞ - hợp với lưới 8 hướng, bước chéo = 1"),
    "octile": (octile, "Octile - khớp chính xác lưới 8 hướng (chéo = √2)"),
    "dijkstra": (zero, "h = 0 ⇔ Dijkstra / UCS"),
    "zero": (zero, "h = 0 ⇔ Dijkstra / UCS"),
}

NEUTRAL_NAME = "zero"    # heuristic trung tính cho UCS/Dijkstra
DEFAULT_NAME = "manhattan"


def names() -> list[str]:
    return ["manhattan", "euclidean", "chebyshev", "octile", "zero"]


def describe(name: str) -> str:
    fn = _HEURISTICS.get(name)
    return fn[1] if fn else "không rõ"


def get(name: str) -> DistanceFn:
    """Lấy hàm khoảng cách theo tên. '-' / '' / None được coi là h = 0."""
    if name in ("-", "", None):
        name = NEUTRAL_NAME
    entry = _HEURISTICS.get(name)
    if entry is None:
        raise KeyError(
            f"Heuristic không hợp lệ: {name!r}. Chọn một trong: {', '.join(sorted(_HEURISTICS))}"
        )
    return entry[0]


def is_admissible(name: str, diagonal: bool) -> bool:
    """Đánh giá (theo lý thuyết) heuristic có khả dụng trên lưới này không."""
    if name in ("zero", "dijkstra"):
        return True
    if name == "manhattan":
        return not diagonal          # 8 hướng: Manhattan có thể vượt h*(n)
    # euclidean / chebyshev (khi chéo = sqrt2, Chebyshev vẫn khả dụng) / octile
    return True


def scale_by_grid(fn: DistanceFn, grid: Grid) -> DistanceFn:
    """Nhân heuristic với chi phí bước nhỏ nhất để giữ tính khả dụng."""
    m = grid.min_step_cost

    def wrapped(a: Node, b: Node) -> float:
        return fn(a, b) * m

    return wrapped
