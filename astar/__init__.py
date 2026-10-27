"""
astar - Thư viện mô phỏng thuật toán A* tìm đường trên lưới.

Đề tài 48: "Mô phỏng thuật toán A* trong bài toán tìm đường trên lưới"

Gói này gồm:
    grid        - biểu diễn lưới, vật cản, chi phí địa hình
    heuristics  - các hàm h(n): Manhattan, Euclidean, Chebyshev, Octile, h=0
    search      - bộ máy A* / UCS / Greedy / BFS (phát sự kiện để mô phỏng)
    maps        - sinh dữ liệu mẫu (mê cung, phòng, xoắn ốc, địa hình...)
"""

from .grid import Grid, Node, INF, parse_map_file, save_map_file
from .search import (
    ALL_MODES,
    MODE_ASTAR,
    MODE_BFS,
    MODE_GREEDY,
    MODE_UCS,
    SearchResult,
    astar,
    bfs,
    dijkstra,
    greedy,
    path_cost,
    search,
    search_steps,
    validate_path,
)
from .maps import SampleMap, sample_maps, to_json, from_json
from . import heuristics

__all__ = [
    "Grid", "Node", "INF", "parse_map_file", "save_map_file",
    "SearchResult", "search", "search_steps", "astar", "dijkstra", "greedy", "bfs",
    "validate_path", "path_cost", "ALL_MODES",
    "MODE_ASTAR", "MODE_UCS", "MODE_GREEDY", "MODE_BFS",
    "SampleMap", "sample_maps", "to_json", "from_json", "heuristics",
]

__version__ = "1.0.0"
