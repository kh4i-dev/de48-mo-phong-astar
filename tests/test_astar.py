"""
test_astar.py - Kiểm thử đơn vị cho thư viện A* (chạy: python main.py test).

Các nhóm kiểm thử:
    1. Tính đúng đắn cơ bản (lưới trống, S = G, không có đường, có vật cản)
    2. Tính TỐI ƯU: A* phải bằng Dijkstra/UCS trên mọi bộ dữ liệu
    3. Tính hợp lệ của đường đi (liền kề, không xuyên tường, không lặp)
    4. Heuristic: khả dụng, không vượt quá chi phí tối ưu, h(goal) = 0
    5. So sánh đối chứng: BFS, Greedy, weighted A*
    6. Cấu trúc dữ liệu lưới: nhập/xuất văn bản, 4/8 hướng, cắt góc
    7. Sự kiện mô phỏng (search_steps) khớp với SearchResult
"""

from __future__ import annotations

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from astar import heuristics as H
from astar.grid import DIRS_8, Grid, INF
from astar.maps import maze_map, open_map, random_obstacles_map, sample_maps, spiral_map, terrain_map
from astar.search import (
    MODE_ASTAR,
    MODE_BFS,
    MODE_GREEDY,
    MODE_UCS,
    path_cost,
    search,
    search_steps,
    validate_path,
)


class TestBasic(unittest.TestCase):
    def test_start_equals_goal(self):
        g = Grid(5, 5)
        r = search(g, (2, 2), (2, 2), MODE_ASTAR, "manhattan")
        self.assertTrue(r.found)
        self.assertEqual(r.path, ((2, 2),))
        self.assertEqual(r.cost, 0.0)
        self.assertEqual(r.steps, 0)

    def test_unreachable_returns_not_found(self):
        # Bịt kín đích bằng 4 tường
        walls = {(1, 2), (2, 1), (2, 3), (3, 2)}
        g = Grid(5, 5, walls=walls)
        r = search(g, (0, 0), (2, 2), MODE_ASTAR, "manhattan")
        self.assertFalse(r.found)
        self.assertEqual(r.path, ())
        self.assertEqual(r.cost, math.inf)

    def test_blocked_endpoint(self):
        g = Grid(5, 5, walls={(2, 2)})
        r = search(g, (0, 0), (2, 2), MODE_ASTAR, "manhattan")
        self.assertFalse(r.found)

    def test_open_grid_optimal_cost_and_manhattan(self):
        m = open_map(20, 12)
        r = search(m.grid, m.start, m.goal, MODE_ASTAR, "manhattan")
        self.assertTrue(r.found)
        expected = abs(m.start[0] - m.goal[0]) + abs(m.start[1] - m.goal[1])
        self.assertAlmostEqual(r.cost, expected, places=6)
        self.assertEqual(r.steps, expected)

    def test_walls_force_detour(self):
        g = Grid(7, 5)
        for r in range(4):          # tường chắn từ trên xuống, chừa 1 lỗ ở dưới
            g.set_wall((r, 3), True)
        res = search(g, (0, 0), (4, 6), MODE_ASTAR, "manhattan")
        self.assertTrue(res.found)
        self.assertTrue(validate_path(g, (0, 0), (4, 6), res.path)[0])

    def test_diagonal_cost_is_sqrt2(self):
        g = Grid(4, 4, diagonal=True)
        r = search(g, (0, 0), (3, 3), MODE_ASTAR, "octile")
        self.assertTrue(r.found)
        self.assertAlmostEqual(r.cost, 3 * math.sqrt(2), places=6)
        self.assertAlmostEqual(r.cost, H.octile((0, 0), (3, 3)), places=6)


class TestOptimality(unittest.TestCase):
    """A* với h khả dụng phải cho cùng chi phí với Dijkstra (UCS)."""

    def _check(self, m, heuristic: str = "manhattan"):
        ucs = search(m.grid, m.start, m.goal, MODE_UCS, "zero")
        ast = search(m.grid, m.start, m.goal, MODE_ASTAR, heuristic)
        self.assertEqual(ucs.found, ast.found, msg=f"{m.key}: khác trạng thái tìm thấy")
        if ucs.found:
            self.assertAlmostEqual(
                ucs.cost, ast.cost, places=6,
                msg=f"{m.key}: A* ({ast.cost}) khác UCS ({ucs.cost}) -> mất tính tối ưu")
        return ucs, ast

    def test_samples_4_huong(self):
        for m in sample_maps(diagonal=False):
            with self.subTest(ban_do=m.key):
                self._check(m, "manhattan")

    def test_samples_8_huong_octile(self):
        for m in sample_maps(diagonal=True):
            with self.subTest(ban_do=m.key):
                self._check(m, "octile")

    def test_weighted_terrain_optimality(self):
        m = terrain_map(30, 18, seed=5)
        ucs = search(m.grid, m.start, m.goal, MODE_UCS, "zero")
        ast = search(m.grid, m.start, m.goal, MODE_ASTAR, "euclidean")
        self.assertAlmostEqual(ucs.cost, ast.cost, places=6)
        # Đường "ít bước" của BFS phải đắt hơn hoặc bằng chi phí tối ưu thực
        b = search(m.grid, m.start, m.goal, MODE_BFS)
        self.assertGreaterEqual(path_cost(m.grid, b.path) + 1e-9, ucs.cost)

    def test_astar_not_more_expanded_than_ucs_on_open_grid(self):
        m = open_map(40, 25)
        ucs = search(m.grid, m.start, m.goal, MODE_UCS, "zero")
        ast = search(m.grid, m.start, m.goal, MODE_ASTAR, "manhattan")
        self.assertLess(ast.expanded, ucs.expanded)


class TestPathValidity(unittest.TestCase):
    def test_all_sample_paths_valid(self):
        for m in sample_maps(diagonal=False) + sample_maps(diagonal=True):
            with self.subTest(ban_do=m.key, cheo=m.grid.diagonal):
                r = search(m.grid, m.start, m.goal, MODE_ASTAR,
                           "octile" if m.grid.diagonal else "manhattan")
                ok, msg = validate_path(m.grid, m.start, m.goal, r.path)
                self.assertTrue(ok, msg=f"{m.key}: {msg}")
                # Tổng chi phí các cạnh phải bằng r.cost
                self.assertAlmostEqual(path_cost(m.grid, r.path), r.cost, places=6)

    def test_no_path_through_walls(self):
        m = maze_map(21, 15, seed=3)
        r = search(m.grid, m.start, m.goal, MODE_ASTAR, "manhattan")
        self.assertTrue(r.found)
        for node in r.path:
            self.assertFalse(m.grid.is_blocked(node))


class TestHeuristics(unittest.TestCase):
    def test_goal_heuristic_is_zero(self):
        for name in H.names():
            fn = H.get(name)
            self.assertAlmostEqual(fn((3, 4), (3, 4)), 0.0, places=9)

    def test_admissible_heuristics_do_not_overestimate(self):
        """h(start) <= chi phí tối ưu thực tế trên mọi bộ dữ liệu."""
        for m in sample_maps(diagonal=False):
            ucs = search(m.grid, m.start, m.goal, MODE_UCS, "zero")
            if not ucs.found:
                continue
            for name in ("manhattan", "euclidean", "chebyshev", "octile"):
                with self.subTest(ban_do=m.key, h=name):
                    h_start = H.get(name)(m.start, m.goal) * m.grid.min_step_cost
                    self.assertLessEqual(h_start, ucs.cost + 1e-9)

    def test_manhattan_inadmissible_on_diagonal_grid(self):
        """Manhattan không khả dụng khi đi chéo -> A* có thể không tối ưu."""
        self.assertFalse(H.is_admissible("manhattan", diagonal=True))
        self.assertTrue(H.is_admissible("octile", diagonal=True))

    def test_octile_equals_true_diagonal_distance(self):
        self.assertAlmostEqual(H.octile((0, 0), (3, 4)), 3 + 4 + (math.sqrt(2) - 2) * 3)


class TestComparisons(unittest.TestCase):
    def test_greedy_faster_but_can_be_suboptimal(self):
        m = sample_maps()[3]  # phòng & hành lang: greedy thường dưới tối ưu
        ucs = search(m.grid, m.start, m.goal, MODE_UCS, "zero")
        gr = search(m.grid, m.start, m.goal, MODE_GREEDY, "manhattan")
        self.assertTrue(gr.found)
        self.assertGreaterEqual(gr.cost + 1e-9, ucs.cost)  # không bao giờ tốt hơn tối ưu
        ok, _ = validate_path(m.grid, m.start, m.goal, gr.path)
        self.assertTrue(ok)

    def test_bfs_minimizes_steps_on_unweighted_grid(self):
        m = random_obstacles_map(25, 18, 0.2, seed=11)
        b = search(m.grid, m.start, m.goal, MODE_BFS)
        a = search(m.grid, m.start, m.goal, MODE_ASTAR, "manhattan")
        self.assertTrue(b.found)
        self.assertEqual(b.steps, a.steps)   # lưới không trọng số: số bước bằng nhau

    def test_weighted_astar_unweighted_map_faster_than_ucs(self):
        """Lưới không trọng số: weighted A* (w>1) luôn duyệt ít hơn UCS."""
        m = sample_maps(diagonal=False)[1]   # vật cản ngẫu nhiên
        ucs = search(m.grid, m.start, m.goal, MODE_UCS, "zero")
        for w in (1.5, 2.0, 3.0):
            with self.subTest(w=w):
                r = search(m.grid, m.start, m.goal, MODE_ASTAR, "manhattan", weight=w)
                self.assertTrue(r.found)
                self.assertTrue(validate_path(m.grid, m.start, m.goal, r.path)[0])
                self.assertGreaterEqual(r.cost + 1e-9, ucs.cost)
                self.assertLessEqual(r.expanded, ucs.expanded)

    def test_weighted_astar_on_weighted_terrain(self):
        """Lưới có địa hình nặng: weighted A* vẫn hợp lệ nhưng có thể phải MỞ LẠI
        nhiều đỉnh (h không nhất quán) hoặc mất tối ưu nếu khoá tập CLOSED."""
        m = sample_maps(diagonal=False)[5]   # địa hình trọng số
        ucs = search(m.grid, m.start, m.goal, MODE_UCS, "zero")
        for w in (1.5, 2.0, 3.0):
            with self.subTest(w=w):
                r = search(m.grid, m.start, m.goal, MODE_ASTAR, "manhattan", weight=w)
                self.assertTrue(r.found)
                self.assertTrue(validate_path(m.grid, m.start, m.goal, r.path)[0])
                self.assertGreaterEqual(r.cost + 1e-9, ucs.cost)
                # Khoá tập CLOSED: không còn lần mở lại nào nhưng đường có thể dưới tối ưu
                lock = search(m.grid, m.start, m.goal, MODE_ASTAR, "manhattan",
                              weight=w, allow_reopen=False)
                self.assertEqual(lock.reused, 0)
                self.assertTrue(validate_path(m.grid, m.start, m.goal, lock.path)[0])
                self.assertGreaterEqual(lock.cost + 1e-9, ucs.cost)

    def test_spiral_corridor_forces_full_scan(self):
        m = spiral_map(15)
        self.assertTrue(m.grid.is_free(m.goal))
        r = search(m.grid, m.start, m.goal, MODE_ASTAR, "manhattan")
        self.assertTrue(r.found)
        self.assertTrue(validate_path(m.grid, m.start, m.goal, r.path)[0])


class TestEvents(unittest.TestCase):
    def test_events_match_result(self):
        m = sample_maps()[1]
        expanded = 0
        result = None
        for ev in search_steps(m.grid, m.start, m.goal, MODE_ASTAR, "manhattan"):
            if ev[0] == "expand":
                expanded += 1
            elif ev[0] == "done":
                result = ev[1]
        self.assertIsNotNone(result)
        self.assertEqual(expanded, result.expanded)

    def test_events_never_move_into_wall(self):
        m = maze_map(21, 15, seed=9)
        for ev in search_steps(m.grid, m.start, m.goal, MODE_ASTAR, "manhattan"):
            if ev[0] in ("expand", "frontier", "reuse"):
                self.assertFalse(m.grid.is_blocked(ev[1]))


class TestGridStructure(unittest.TestCase):
    def test_text_roundtrip(self):
        text = ["S..~.", ".##..", "..=..", "..#G."]
        g, s, goal = Grid.from_text(text)
        self.assertEqual(s, (0, 0))
        self.assertEqual(goal, (3, 3))
        self.assertEqual(g.weight((1, 1)), INF)
        self.assertEqual(g.weight((0, 3)), 4.0)
        self.assertEqual(g.weight((2, 2)), 6.0)
        out = g.to_text(start=s, goal=goal)
        self.assertEqual(out.splitlines()[3][3], "G")

    def test_four_vs_eight_neighbors(self):
        g4 = Grid(5, 5)
        g8 = Grid(5, 5, diagonal=True)
        self.assertEqual(len(g4.neighbors((2, 2))), 4)
        self.assertEqual(len(g8.neighbors((2, 2))), 8)

    def test_no_corner_cutting_by_default(self):
        walls = {(0, 1), (1, 0)}
        g = Grid(3, 3, walls=walls, diagonal=True)
        nbs = dict(g.neighbors((1, 1)))
        self.assertNotIn((0, 0), nbs)          # bị chặn vì cắt góc

    def test_corner_cutting_allowed_when_enabled(self):
        walls = {(0, 1), (1, 0)}
        g = Grid(3, 3, walls=walls, diagonal=True, allow_corner_cutting=True)
        nbs = dict(g.neighbors((1, 1)))
        self.assertIn((0, 0), nbs)

    def test_neighbor_cost_scales_with_terrain(self):
        g = Grid(3, 1)
        g.set_weight((0, 2), 5.0)
        nbs = dict(g.neighbors((0, 0)))
        self.assertAlmostEqual(nbs[(0, 1)], 1.0)
        nbs = dict(g.neighbors((0, 1)))
        self.assertAlmostEqual(nbs[(0, 2)], 5.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
