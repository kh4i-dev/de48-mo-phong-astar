"""
experiments.py - Kịch bản thực nghiệm cho Đề tài 48.

Chạy:  python main.py exp        (thêm --diagonal để đo trên lưới 8 hướng)

Kịch bản:
    TN1. So sánh A* với 4 hàm h(n) khác nhau trên 6 bộ dữ liệu mẫu.
    TN2. So sánh A* với UCS (Dijkstra), Greedy Best-First, BFS (đối chứng).
    TN3. Khảo sát weighted A*: w = 1.0, 1.5, 2.0, 3.0 (đánh đổi tốc độ/tối ưu).
    TN4. Kiểm chứng tính tối ưu: A* phải bằng chi phí của UCS.
    TN5. Ảnh hưởng của việc cho phép đi chéo (4 hướng vs 8 hướng).

Kết quả ghi ra thư mục results/:
    ket_qua_thuc_nghiem.csv         - toàn bộ số liệu (mở bằng Excel)
    bang_ket_qua.md                 - bảng Markdown để dán vào báo cáo
    bao_cao_thuc_nghiem.html        - báo cáo trực quan (biểu đồ SVG nhúng)
    duong_di_mau.txt                - trực quan hoá một lần chạy bằng ASCII
    ban_do_mau.json                 - lưới mẫu (tái sử dụng, không cần sinh lại)
"""

from __future__ import annotations

import csv
import html
import os
import statistics
import sys
from dataclasses import dataclass

from astar import heuristics as H
from astar.maps import SampleMap, from_json, sample_maps, to_json
from astar.search import (
    MODE_ASTAR,
    MODE_BFS,
    MODE_GREEDY,
    MODE_UCS,
    SearchResult,
    path_cost,
    search,
    validate_path,
)

RESULTS_DIR = "results"
DATA_DIR = "data"


# ---------------------------------------------------------------------- #
# Cấu trúc một dòng kết quả
# ---------------------------------------------------------------------- #
@dataclass
class Row:
    map_key: str
    map_name: str
    size: str
    walls: float
    algorithm: str
    heuristic: str
    weight: float
    reopen: bool
    diagonal: bool
    found: bool
    cost: float          # chi phí THỰC (đã xét trọng số địa hình)
    path_cells: int
    steps: int
    expanded: int
    generated: int
    max_open: int
    time_ms: float
    valid: bool
    optimal: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "ban_do": self.map_key,
            "ten_ban_do": self.map_name,
            "kich_thuoc": self.size,
            "ty_le_tuong": f"{self.walls:.1%}",
            "thuat_toan": self.algorithm,
            "heuristic": self.heuristic,
            "w": self.weight,
            "cho_mo_lai_dinh": int(self.reopen),
            "8_huong": int(self.diagonal),
            "tim_thay": int(self.found),
            "chi_phi_thuc": round(self.cost, 4) if self.found else "",
            "so_o": self.path_cells,
            "so_buoc": self.steps,
            "so_dinh_duyet": self.expanded,
            "so_dinh_sinh": self.generated,
            "open_lon_nhat": self.max_open,
            "thoi_gian_ms": round(self.time_ms, 4),
            "duong_di_hop_le": int(self.valid),
            "toi_uu": int(self.optimal),
        }


def _run_one(
    m: SampleMap,
    mode: str,
    heuristic: str,
    weight: float = 1.0,
    optimal_cost: float | None = None,
    allow_reopen: bool = True,
) -> Row:
    r: SearchResult = search(m.grid, m.start, m.goal, mode=mode,
                             heuristic=heuristic, weight=weight,
                             allow_reopen=allow_reopen)
    real_cost = path_cost(m.grid, r.path) if r.found else float("inf")
    valid = validate_path(m.grid, m.start, m.goal, r.path)[0] if r.found else False
    optimal = bool(
        r.found and optimal_cost is not None and abs(real_cost - optimal_cost) < 1e-6
    )
    return Row(
        map_key=m.key, map_name=m.name, size=m.size_text, walls=m.wall_ratio,
        algorithm=r.algorithm, heuristic=(r.heuristic if mode != MODE_BFS else "-"),
        weight=weight, reopen=allow_reopen, diagonal=m.grid.diagonal, found=r.found,
        cost=real_cost,
        path_cells=r.path_len, steps=r.steps, expanded=r.expanded,
        generated=r.generated, max_open=r.max_open, time_ms=r.time_ms,
        valid=valid, optimal=optimal,
    )


def _reference_cost(m: SampleMap) -> float:
    """Chi phí tối ưu tham chiếu = Dijkstra (UCS) từ start tới goal."""
    r = search(m.grid, m.start, m.goal, mode=MODE_UCS, heuristic="zero")
    return r.cost if r.found else float("inf")


# ---------------------------------------------------------------------- #
# Các thí nghiệm
# ---------------------------------------------------------------------- #
def exp_heuristics(m: SampleMap, ref: float) -> list[Row]:
    """TN1: A* với từng h(n) (và TN2: các thuật toán đối chứng)."""
    rows: list[Row] = []
    for hn in ("manhattan", "euclidean", "chebyshev", "octile"):
        rows.append(_run_one(m, MODE_ASTAR, hn, 1.0, ref))
    rows.append(_run_one(m, MODE_UCS, "zero", 1.0, ref))
    rows.append(_run_one(m, MODE_GREEDY, "octile" if m.grid.diagonal else "manhattan",
                         1.0, ref))
    rows.append(_run_one(m, MODE_BFS, "-", 1.0, ref))
    return rows


def exp_weighted(m: SampleMap, ref: float) -> list[Row]:
    """TN3: weighted A* với w > 1, ở cả hai chế độ mở lại / khoá tập CLOSED."""
    hn = "octile" if m.grid.diagonal else "manhattan"
    rows = [_run_one(m, MODE_ASTAR, hn, w, ref, allow_reopen=True)
            for w in (1.0, 1.5, 2.0, 3.0)]
    rows += [_run_one(m, MODE_ASTAR, hn, w, ref, allow_reopen=False)
             for w in (2.0, 3.0)]
    return rows


def collect(diagonal: bool = False) -> tuple[list[Row], list[Row]]:
    """Chạy toàn bộ thực nghiệm, trả về (bảng chính, bảng weighted)."""
    maps = sample_maps(diagonal=diagonal)
    main_rows: list[Row] = []
    weighted_rows: list[Row] = []
    for m in maps:
        ref = _reference_cost(m)
        main_rows.extend(exp_heuristics(m, ref))
        weighted_rows.extend(exp_weighted(m, ref))
    return main_rows, weighted_rows


def exp_4_vs_8(*maps: SampleMap) -> list[Row]:
    """TN5: so sánh lưới 4 hướng và 8 hướng trên cùng địa hình."""
    rows: list[Row] = []
    for m4 in maps:
        m8 = SampleMap(
            key=m4.key, name=m4.name, description=m4.description,
            grid=_to_diagonal(m4.grid), start=m4.start, goal=m4.goal,
        )
        for m in (m4, m8):
            ref = _reference_cost(m)
            rows.append(_run_one(m, MODE_ASTAR, "octile" if m.grid.diagonal else "manhattan",
                                 1.0, ref))
    return rows


def _to_diagonal(grid):
    from astar.grid import DIRS_8, Grid

    g = Grid(grid.width, grid.height, diagonal=True, name=grid.name)
    g.cost = [row[:] for row in grid.cost]
    g._dirs = DIRS_8
    return g


# ---------------------------------------------------------------------- #
# Kết xuất
# ---------------------------------------------------------------------- #
def write_csv(path: str, rows: list[Row]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fields = list(rows[0].as_dict().keys())
    with open(path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter=";")
        w.writeheader()
        for r in rows:
            w.writerow(r.as_dict())


def markdown_table(rows: list[Row]) -> str:
    head = ("| Bản đồ | Thuật toán | h(n) | w | Mở lại | Tìm thấy | Chi phí | Ô | Duyệt | "
            "Sinh | \\|OPEN\\|max | Thời gian (ms) | Hợp lệ | Tối ưu |")
    sep = "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"
    out = [head, sep]
    for r in rows:
        out.append(
            f"| {r.map_key} | {r.algorithm} | {r.heuristic} | {r.weight:g} | "
            f"{'✔' if r.reopen else '—'} | "
            f"{'✔' if r.found else '✘'} | "
            f"{(f'{r.cost:.3f}' if r.found else '—')} | {r.path_cells} | "
            f"{r.expanded} | {r.generated} | {r.max_open} | {r.time_ms:.3f} | "
            f"{'✔' if r.valid else '✘'} | {'✔' if r.optimal else '–'} |"
        )
    return "\n".join(out)


def print_table(rows: list[Row], title: str) -> None:
    print(f"\n=== {title} ===")
    head = (f"{'bản đồ':<14}{'thuật toán':<20}{'h(n)':<11}{'w':>4}{'chi phí':>10}"
            f"{'ô':>6}{'duyệt':>8}{'sinh':>8}{'open_max':>9}{'TG(ms)':>10}{'tối ưu':>8}")
    print(head)
    print("-" * len(head))
    for r in rows:
        cost = f"{r.cost:.3f}" if r.found else "—"
        print(f"{r.map_key:<14}{r.algorithm:<20}{r.heuristic:<11}{r.weight:>4g}"
              f"{cost:>10}{r.path_cells:>6}{r.expanded:>8}{r.generated:>8}"
              f"{r.max_open:>9}{r.time_ms:>10.3f}{('có' if r.optimal else 'không'):>8}")


def svg_hbars(title: str, items: list[tuple[str, float]], unit: str = "",
              fmt: str = "{:,.0f}") -> str:
    """Biểu đồ thanh ngang bằng SVG thuần (không cần thư viện ngoài)."""
    if not items:
        return ""
    w = 520
    row_h = 26
    pad_l, pad_r, pad_t = 210, 70, 34
    h = pad_t + row_h * len(items) + 16
    vmax = max(v for _, v in items) or 1.0
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="Segoe UI, Arial, sans-serif" font-size="12">',
        f'<text x="8" y="20" font-size="13" font-weight="600" fill="#1b2430">'
        f'{html.escape(title)}</text>',
    ]
    for i, (label, value) in enumerate(items):
        y = pad_t + i * row_h
        bar_w = max(1.0, (w - pad_l - pad_r) * (value / vmax))
        color = "#4da3ff" if i % 2 == 0 else "#7cc0ff"
        parts.append(f'<rect x="{pad_l}" y="{y + 4}" width="{bar_w}" height="{row_h - 10}" '
                     f'rx="3" fill="{color}"/>')
        parts.append(f'<text x="{pad_l - 8}" y="{y + 17}" text-anchor="end" '
                     f'fill="#22303f">{html.escape(label)}</text>')
        parts.append(f'<text x="{pad_l + bar_w + 6}" y="{y + 17}" fill="#22303f">'
                     f'{html.escape(fmt.format(value))}{html.escape(unit)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def write_html(path: str, main_rows: list[Row], weighted: list[Row],
               extra: list[Row], maps: list[SampleMap]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    body: list[str] = []
    body.append("<h1>Đề tài 48 — Mô phỏng thuật toán A* tìm đường trên lưới</h1>")
    body.append("<p class='sub'>Báo cáo thực nghiệm tự sinh bởi <code>python main.py exp</code>. "
                "Chi phí trong bảng là <b>chi phí thực</b> (đã tính trọng số địa hình). "
                "Cột <b>Tối ưu</b> so với chi phí chuẩn của Dijkstra.</p>")

    body.append("<h2>1. Bộ dữ liệu mẫu</h2>")
    body.append("<table><tr><th>Khoá</th><th>Tên</th><th>Kích thước</th>"
                "<th>Tỷ lệ tường</th><th>Xuất phát</th><th>Đích</th><th>Mô tả</th></tr>")
    for m in maps:
        body.append(f"<tr><td><code>{m.key}</code></td><td>{html.escape(m.name)}</td>"
                    f"<td>{m.size_text}</td><td>{m.wall_ratio:.1%}</td>"
                    f"<td>{m.start}</td><td>{m.goal}</td>"
                    f"<td>{html.escape(m.description)}</td></tr>")
    body.append("</table>")

    body.append("<h2>2. Số đỉnh đã duyệt — A* so với các thuật toán đối chứng</h2>")
    for m in maps:
        rows = [r for r in main_rows if r.map_key == m.key]
        items = [(r.algorithm + (f" · {r.heuristic}" if r.heuristic not in ("-",) else ""),
                  r.expanded) for r in rows]
        items = [(r.algorithm, r.expanded) for r in rows]
        chart = svg_hbars(f"{m.name} ({m.size_text}) — số đỉnh duyệt (càng ít càng tốt)",
                          items, unit=" đỉnh")
        body.append(chart)

    body.append("<h2>3. Đánh đổi của weighted A* (w &gt; 1)</h2>"
                "<p>Hai chế độ: <b>mở lại</b> (cho phép mở lại đỉnh đã đóng — đúng lý "
                "thuyết khi h không nhất quán) và <b>khoá</b> (khoá tập CLOSED — nhanh "
                "hơn nhưng có thể mất tối ưu).</p>")
    for m in maps:
        rows = [r for r in weighted if r.map_key == m.key]
        items = [(f"w = {r.weight:g}" + ("" if r.reopen else " (khoá CLOSED)"), r.expanded)
                 for r in rows]
        chart = svg_hbars(f"{m.name} — số đỉnh duyệt theo w", items, unit=" đỉnh")
        body.append(chart)
        costs = [(f"w = {r.weight:g}" + ("" if r.reopen else " (khoá CLOSED)"),
                  r.cost if r.found else 0.0) for r in rows]
        chart2 = svg_hbars(f"{m.name} — chi phí đường đi theo w", costs,
                           fmt="{:,.2f}")
        body.append(chart2)

    body.append("<h2>4. Lưới 4 hướng so với 8 hướng (cùng địa hình)</h2>")
    body.append(svg_hbars("Chi phí đường đi khi cho phép đi chéo (8 hướng)",
                          [(f"{r.map_key} · {'8 hướng' if r.diagonal else '4 hướng'}", r.cost)
                           for r in extra if r.found], fmt="{:,.2f}"))

    body.append("<h2>5. Bảng số liệu đầy đủ (TN1 + TN2)</h2>")
    body.append(_html_table(main_rows))
    body.append("<h2>6. Bảng số liệu weighted A* (TN3)</h2>")
    body.append(_html_table(weighted))

    # Kết luận tự động
    def ratio(map_key: str, algo: str, hn: str | None = None) -> float | None:
        a = [r for r in main_rows if r.map_key == map_key and r.algorithm == algo
             and (hn is None or r.heuristic == hn)]
        u = [r for r in main_rows if r.map_key == map_key and r.algorithm == MODE_UCS]
        if not a or not u or u[0].expanded == 0:
            return None
        return a[0].expanded / u[0].expanded

    ratios = [x for x in (ratio(m.key, MODE_ASTAR, "octile" if m.grid.diagonal else "manhattan")
                          for m in maps) if x is not None]
    greedy_bad = [r for r in main_rows if r.algorithm == MODE_GREEDY and not r.optimal]
    body.append("<h2>7. Kết luận rút ra</h2><ul>")
    if ratios:
        body.append(f"<li>A* (h khả dụng) duyệt trung bình <b>{statistics.mean(ratios):.1%}</b> "
                    f"số đỉnh so với Dijkstra/UCS, trong khi chi phí đường đi <b>không đổi</b> "
                    f"(vẫn tối ưu).</li>")
    if greedy_bad:
        names = ", ".join(sorted({r.map_key for r in greedy_bad}))
        body.append(f"<li>Greedy Best-First chạy nhanh nhưng cho đường <b>dưới tối ưu</b> trên: "
                    f"{names} — minh hoạ rõ việc bỏ qua g(n) sẽ mất tính tối ưu.</li>")
    body.append("<li>BFS chỉ tối ưu theo <b>số bước</b>; khi lưới có trọng số địa hình, "
                "đường của BFS có thể đắt hơn nhiều so với A*/UCS.</li>")
    body.append("<li>Trên hành lang xoắn ốc (chỉ một lối đi), mọi thuật toán đều phải duyệt "
                "gần như toàn bộ lưới: h(n) không giúp được gì khi cấu trúc bắt buộc.</li>")
    body.append("</ul>")

    doc = f"""<!DOCTYPE html>
<html lang="vi"><head><meta charset="utf-8">
<title>Đề tài 48 — Báo cáo thực nghiệm A*</title>
<style>
 body {{ font-family: "Segoe UI", Arial, sans-serif; color:#1b2430; margin:0; padding:28px 34px;
        background:#f7f9fc; line-height:1.5; }}
 h1 {{ font-size:22px; margin:0 0 6px; }}
 h2 {{ font-size:16px; margin:26px 0 10px; color:#0f4c81; border-bottom:1px solid #dbe4ef;
       padding-bottom:4px; }}
 p.sub {{ color:#4a5a6a; margin-top:0; }}
 table {{ border-collapse:collapse; width:100%; background:#fff; font-size:12.5px;
          box-shadow:0 1px 2px rgba(20,40,70,.08); margin-bottom:14px; }}
 th, td {{ border:1px solid #dde5ee; padding:5px 7px; text-align:left; }}
 th {{ background:#eaf1f9; font-weight:600; }}
 tr:nth-child(even) td {{ background:#fbfcfe; }}
 svg {{ background:#fff; border:1px solid #e3eaf3; border-radius:6px; margin:6px 0 14px;
        display:block; }}
 code {{ background:#eef3f8; padding:1px 4px; border-radius:3px; }}
 ul {{ margin-top:6px; }}
</style></head><body>
{chr(10).join(body)}
</body></html>"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(doc)


def _html_table(rows: list[Row]) -> str:
    head = ("<table><tr><th>Bản đồ</th><th>Thuật toán</th><th>h(n)</th><th>w</th>"
            "<th>Mở lại đỉnh</th><th>Chi phí thực</th><th>Ô</th><th>Bước</th>"
            "<th>Đỉnh duyệt</th><th>Đỉnh sinh</th><th>OPEN max</th><th>TG (ms)</th>"
            "<th>Hợp lệ</th><th>Tối ưu</th></tr>")
    out = [head]
    for r in rows:
        cost = f"{r.cost:.3f}" if r.found else "—"
        out.append(
            f"<tr><td><code>{r.map_key}</code></td><td>{html.escape(r.algorithm)}</td>"
            f"<td>{html.escape(r.heuristic)}</td><td>{r.weight:g}</td>"
            f"<td>{'✔' if r.reopen else '—'}</td><td>{cost}</td>"
            f"<td>{r.path_cells}</td><td>{r.steps}</td><td>{r.expanded}</td>"
            f"<td>{r.generated}</td><td>{r.max_open}</td><td>{r.time_ms:.3f}</td>"
            f"<td>{'✔' if r.valid else '✘'}</td><td>{'✔' if r.optimal else '–'}</td></tr>")
    out.append("</table>")
    return "".join(out)


def write_ascii_demo(path: str, m: SampleMap, heuristic: str = "manhattan") -> str:
    r = search(m.grid, m.start, m.goal, MODE_ASTAR, heuristic, keep_sets=True)
    art = (f"Ví dụ một lần chạy A* trên bản đồ {m.name} ({m.size_text}), h(n) = {heuristic}\n"
           f"Ký hiệu: # tường | . trống | : ~ = địa hình nặng | o đã duyệt | "
           f"- đang chờ | * đường đi | S/G đầu-cuối\n\n"
           + m.grid.to_text(start=m.start, goal=m.goal, path=r.path,
                            closed=r.closed, open_set=r.open_left)
           + "\n\n" + r.summary() + "\n")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(art)
    return art


# ---------------------------------------------------------------------- #
# Điểm vào
# ---------------------------------------------------------------------- #
def main(diagonal: bool = False, quiet: bool = False) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover
        pass

    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    maps = sample_maps(diagonal=diagonal)
    # Lưu dữ liệu mẫu để tái sử dụng
    to_json(maps, os.path.join(DATA_DIR, "ban_do_mau.json"))
    for m in maps:
        with open(os.path.join(DATA_DIR, f"{m.key}.txt"), "w", encoding="utf-8") as fh:
            fh.write(m.grid.to_text(start=m.start, goal=m.goal) + "\n")

    main_rows, weighted_rows = collect(diagonal=diagonal)
    extra = exp_4_vs_8(sample_maps(diagonal=False)[1],
                       sample_maps(diagonal=False)[5],   # vật cản + địa hình
                       sample_maps(diagonal=False)[2])   # mê cung

    write_csv(os.path.join(RESULTS_DIR, "ket_qua_thuc_nghiem.csv"), main_rows + weighted_rows)
    with open(os.path.join(RESULTS_DIR, "bang_ket_qua.md"), "w", encoding="utf-8") as fh:
        fh.write("# Đề tài 48 — Bảng kết quả thực nghiệm\n\n")
        fh.write("## TN1 + TN2: A* với các h(n) và thuật toán đối chứng\n\n")
        fh.write(markdown_table(main_rows) + "\n\n")
        fh.write("## TN3: Weighted A*\n\n")
        fh.write(markdown_table(weighted_rows) + "\n\n")
        fh.write("## TN5: 4 hướng so với 8 hướng\n\n")
        fh.write(markdown_table(extra) + "\n")
    write_html(os.path.join(RESULTS_DIR, "bao_cao_thuc_nghiem.html"),
               main_rows, weighted_rows, extra, maps)
    art = write_ascii_demo(os.path.join(RESULTS_DIR, "duong_di_mau.txt"),
                           maps[2], "manhattan")

    if not quiet:
        print_table(main_rows, "TN1 + TN2: A* với các h(n) và các thuật toán đối chứng")
        print_table(weighted_rows, "TN3: Weighted A* — đánh đổi tốc độ và tối ưu")
        print_table(extra, "TN5: lưới 4 hướng so với 8 hướng")
        print("\n" + art[:2000])

        # Tóm tắt so sánh
        print("\n=== TÓM TẮT ===")
        for m in maps:
            rows = [r for r in main_rows if r.map_key == m.key]
            ucs = next((r for r in rows if r.algorithm == MODE_UCS), None)
            ha = next((r for r in rows if r.algorithm == MODE_ASTAR
                       and r.heuristic == ("octile" if m.grid.diagonal else "manhattan")), None)
            gr = next((r for r in rows if r.algorithm == MODE_GREEDY), None)
            if not (ucs and ha and gr):
                continue
            red = (1 - ha.expanded / ucs.expanded) * 100 if ucs.expanded else 0.0
            print(f"  {m.key:<18} UCS={ucs.expanded:<6} A*={ha.expanded:<6} "
                  f"(giảm {red:5.1f}% đỉnh)  Greedy={gr.expanded:<5} "
                  f"chi phí Greedy={gr.cost:.2f} so với tối ưu {ucs.cost:.2f}")
    print(f"\nĐã ghi kết quả vào: {os.path.abspath(RESULTS_DIR)}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
