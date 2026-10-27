"""
main.py - Điểm vào (entry point) của Đề tài 48:
          "Mô phỏng thuật toán A* trong bài toán tìm đường trên lưới".

Cách dùng:
    python main.py            # mở giao diện đồ hoạ (GUI)
    python main.py gui        # giống trên
    python main.py demo       # chạy 1 ví dụ, in đường đi ra console (ASCII)
    python main.py exp        # chạy toàn bộ thực nghiệm, xuất results/
    python main.py test       # chạy bộ kiểm thử đơn vị
    python main.py info       # in thông tin môi trường & danh sách dữ liệu mẫu
"""

from __future__ import annotations

import argparse
import os
import sys


def _fix_console() -> None:
    """Đảm bảo console Windows in được tiếng Việt."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except Exception:  # pragma: no cover
            pass


def cmd_gui(_args: argparse.Namespace) -> int:
    from gui import main as gui_main
    gui_main()
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    from astar import heuristics as H
    from astar.maps import sample_maps
    from astar.search import MODE_ASTAR, search, validate_path

    maps = {m.key: m for m in sample_maps()}
    key = args.map or "vat_can_ngau_nhien"
    if key not in maps:
        print(f"Không có bản đồ {key!r}. Các lựa chọn: {', '.join(maps)}")
        return 2
    m = maps[key]
    hn = args.heuristic or ("octile" if m.grid.diagonal else "manhattan")
    print(f"=== BẢN ĐỒ: {m.name} ({m.size_text}) ===")
    print(f"   {m.description}")
    print(f"   S = {m.start}   G = {m.goal}   h(n) = {hn}\n")

    r = search(m.grid, m.start, m.goal, MODE_ASTAR, hn, weight=args.weight,
               keep_sets=True)
    print(r.summary())
    if r.found:
        ok, msg = validate_path(m.grid, m.start, m.goal, r.path)
        print(f"   kiểm tra đường đi: {msg}\n")
        print("LƯỚI SAU KHI TÌM KIẾM")
        print("  ký hiệu: # tường | . trống | : ~ = địa hình nặng | "
              "o đã duyệt | - đang chờ | * đường đi | S/G đầu-cuối\n")
        print(m.grid.to_text(start=m.start, goal=m.goal, path=r.path,
                             closed=r.closed, open_set=r.open_left))
        print("\nĐƯỜNG ĐI (danh sách ô):")
        print("  " + " -> ".join(f"({a},{b})" for a, b in r.path[:40])
              + (" ..." if r.path_len > 40 else ""))
        print(f"\n  Tổng: {r.path_len} ô, {r.steps} bước, chi phí {r.cost:.3f}, "
              f"duyệt {r.expanded} đỉnh, {r.time_ms:.3f} ms")
        print(f"  (gợi ý heuristic: {H.describe(hn)})")
    else:
        print("Không có đường đi từ S tới G.")
    return 0


def cmd_exp(args: argparse.Namespace) -> int:
    import experiments
    return experiments.main(diagonal=args.diagonal, quiet=args.quiet)


def cmd_test(_args: argparse.Namespace) -> int:
    import unittest

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


def cmd_info(_args: argparse.Namespace) -> int:
    import platform
    from astar import __version__, heuristics as H
    from astar.maps import sample_maps

    print(f"Đề tài 48 - Mô phỏng A* tìm đường trên lưới  (v{__version__})")
    print(f"Python  : {platform.python_version()} ({platform.system()} {platform.machine()})")
    print(f"Thư viện: chỉ dùng thư viện chuẩn (tkinter cho GUI)")
    print(f"Heuristic hỗ trợ: {', '.join(H.names())}")
    print("\nBộ dữ liệu mẫu:")
    for m in sample_maps():
        print(f"  - {m.key:18} {m.name:26} {m.size_text:8} "
              f"tường={m.wall_ratio:5.1%}  S={m.start} G={m.goal}")
    print("\nCấu trúc thư mục:")
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
        level = root.count(os.sep)
        print("   " + "  " * level + os.path.basename(root) + "/")
        for f in sorted(files):
            if f.endswith((".py", ".md", ".txt", ".json", ".csv", ".html")):
                print("   " + "  " * (level + 1) + f)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="main.py",
        description="Đề tài 48 - Mô phỏng thuật toán A* tìm đường trên lưới",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="command")

    sp = sub.add_parser("gui", help="mở giao diện đồ hoạ (mặc định)")
    sp.set_defaults(func=cmd_gui)

    sp = sub.add_parser("demo", help="chạy 1 ví dụ và in lưới ra console")
    sp.add_argument("-m", "--map", help="khoá bản đồ mẫu (mặc định vat_can_ngau_nhien)")
    sp.add_argument("-H", "--heuristic", help="hàm h(n): manhattan|euclidean|chebyshev|octile")
    sp.add_argument("-w", "--weight", type=float, default=1.0, help="trọng số w của weighted A*")
    sp.set_defaults(func=cmd_demo)

    sp = sub.add_parser("exp", help="chạy thực nghiệm và xuất báo cáo")
    sp.add_argument("--diagonal", action="store_true", help="dùng lưới 8 hướng")
    sp.add_argument("--quiet", action="store_true", help="không in bảng ra console")
    sp.set_defaults(func=cmd_exp)

    sp = sub.add_parser("test", help="chạy kiểm thử đơn vị")
    sp.set_defaults(func=cmd_test)

    sp = sub.add_parser("info", help="in thông tin môi trường và dữ liệu mẫu")
    sp.set_defaults(func=cmd_info)
    return p


def main(argv: list[str] | None = None) -> int:
    _fix_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        return cmd_gui(args)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
