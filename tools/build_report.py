"""
build_report.py - Dựng báo cáo BTL (.docx) cho Đề tài 48.

Quy trình:
  1. Nạp số liệu thực nghiệm từ results/ket_qua_thuc_nghiem.csv (do chính chương
     trình sinh ra) để dựng các bảng ở Chương 4.
  2. Gom toàn bộ khối nội dung và lập danh sách các mục sẽ đưa vào Mục lục,
     Danh mục bảng, Danh mục hình theo đúng thứ tự tài liệu.
  3. Dựng tệp .docx, render ra PDF, dò số trang thật của từng mục, rồi dựng lại
     với số trang đúng (lặp cho tới khi số trang ổn định).
  4. Ghi kết quả vào reports/ (không gian tài liệu học thuật của dự án).

Chạy:  <python có python-docx + pymupdf> tools/build_report.py
"""

from __future__ import annotations

import csv
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from docx.shared import Cm, Pt

import report_content_a as CA
import report_content_b as CB
import report_style as S
from astar.maps import sample_maps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")
RESULTS = os.path.join(ROOT, "results")
BUILD = os.path.join(REPORTS, "build")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"


# ---------------------------------------------------------------------- #
# 1. Số liệu thực nghiệm
# ---------------------------------------------------------------------- #
def load_rows() -> list[dict]:
    path = os.path.join(RESULTS, "ket_qua_thuc_nghiem.csv")
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=";"))


def _f(v, digits=3):
    try:
        return f"{float(v):.{digits}f}"
    except (TypeError, ValueError):
        return "-"


def _i(v):
    try:
        return str(int(float(v)))
    except (TypeError, ValueError):
        return "-"


SHORT_NAME = {
    "trong": "Lưới trống",
    "vat_can_ngau_nhien": "Vật cản 25%",
    "me_cung": "Mê cung",
    "phong_hanh_lang": "Phòng",
    "xoan_oc": "Xoắn ốc",
    "dia_hinh": "Địa hình",
}

SHORT_H = {
    "manhattan": "manh.",
    "euclidean": "eucl.",
    "chebyshev": "cheb.",
    "octile": "octile",
    "-": "-",
}


def build_ctx(rows: list[dict]) -> dict:
    ctx: dict = {}
    maps = sample_maps()
    by_key = {m.key: m for m in maps}

    # --- Bảng 4.2: thông số bộ dữ liệu
    ds_rows = []
    for m in maps:
        free = sum(1 for w in (m.grid.cost[r][c] for r in range(m.grid.height)
                               for c in range(m.grid.width)) if w != float("inf"))
        ds_rows.append([m.name, m.size_text, f"{m.wall_ratio:.0%}",
                        f"({m.start[0]}, {m.start[1]})", f"({m.goal[0]}, {m.goal[1]})",
                        f"{free}"])
    ctx["tbl_datasets"] = ("Bảng 4.2: Thông số của sáu bộ dữ liệu mẫu",
                           ["Bộ dữ liệu", "Kích thước", "Tỉ lệ tường", "Xuất phát", "Đích",
                            "Số ô đi được"], ds_rows,
                           [4.2, 2.2, 2.1, 2.2, 2.2, 2.6], (1, 2, 3, 4, 5))

    # --- Bảng 4.6: A* (manhattan) đối chiếu UCS, Greedy, BFS
    keep = {"A*": "manhattan", "UCS (Dijkstra)": "-", "Greedy Best-First": "manhattan",
            "BFS": "-"}
    tn12 = []
    for m in maps:
        for algo, h in keep.items():
            match = [r for r in rows if r["ban_do"] == m.key and r["thuat_toan"] == algo
                     and str(r["heuristic"]) == h and float(r["w"]) == 1.0
                     and int(r["cho_mo_lai_dinh"]) == 1]
            if not match:
                continue
            r = match[0]
            tn12.append([SHORT_NAME.get(m.key, m.name), algo, SHORT_H.get(h, h),
                         _f(r["chi_phi_thuc"]), _i(r["so_o"]), _i(r["so_dinh_duyet"]),
                         _i(r["so_dinh_sinh"]), _i(r["open_lon_nhat"]),
                         _f(r["thoi_gian_ms"]), "có" if _i(r["toi_uu"]) == "1" else "không"])
    ctx["tbl_tn12"] = ("Bảng 4.6: Kết quả thí nghiệm 1 và 2 trên sáu bộ dữ liệu mẫu",
                       ["Bộ dữ liệu", "Thuật toán", "h(n)", "Chi phí", "Ô", "Duyệt", "Sinh",
                        "OPEN", "TG (ms)", "Tối ưu"], tn12,
                       [1.8, 2.2, 1.5, 1.7, 1.0, 1.4, 1.3, 1.4, 1.5, 1.5],
                       (3, 4, 5, 6, 7, 8, 9), 10.0)

    # --- Bảng 4.7: mức giảm so với UCS
    summ = []
    for m in maps:
        a = next((r for r in rows if r["ban_do"] == m.key and r["thuat_toan"] == "A*"
                  and str(r["heuristic"]) == "manhattan" and float(r["w"]) == 1.0
                  and int(r["cho_mo_lai_dinh"]) == 1), None)
        u = next((r for r in rows if r["ban_do"] == m.key
                  and r["thuat_toan"] == "UCS (Dijkstra)"), None)
        if not (a and u):
            continue
        ea, eu = int(float(a["so_dinh_duyet"])), int(float(u["so_dinh_duyet"]))
        gain = (1 - ea / eu) * 100 if eu else 0.0
        summ.append([SHORT_NAME.get(m.key, m.name), f"{ea}", f"{eu}", f"{gain:.1f}%",
                     _f(a["chi_phi_thuc"]), _f(u["chi_phi_thuc"])])
    ctx["tbl_summary"] = ("Bảng 4.7: Mức giảm số đỉnh duyệt của A* so với tìm kiếm theo chi "
                          "phí đều",
                          ["Bộ dữ liệu", "A*", "Chi phí đều", "Mức giảm", "Chi phí A*",
                           "Chi phí đều"], summ, [3.6, 1.6, 2.6, 2.0, 2.5, 2.5],
                          (1, 2, 3, 4, 5))

    # --- Bảng 4.8: ảnh hưởng h(n)
    h_rows = []
    for key in ("trong", "vat_can_ngau_nhien", "phong_hanh_lang", "dia_hinh"):
        m = by_key[key]
        cells = [SHORT_NAME.get(m.key, m.name)]
        for h in ("manhattan", "euclidean", "chebyshev", "octile"):
            r = next((x for x in rows if x["ban_do"] == key and x["thuat_toan"] == "A*"
                      and str(x["heuristic"]) == h and float(x["w"]) == 1.0
                      and int(x["cho_mo_lai_dinh"]) == 1), None)
            cells.append(_i(r["so_dinh_duyet"]) if r else "-")
        h_rows.append(cells)
    ctx["tbl_tn_h"] = ("Bảng 4.8: Số đỉnh A* phải duyệt theo từng hàm ước lượng",
                       ["Bộ dữ liệu", "Manhattan", "Euclid", "Chebyshev", "Octile"], h_rows,
                       [4.0, 3.0, 3.0, 3.0, 3.0], (1, 2, 3, 4))

    # --- Bảng 4.9: weighted A*
    w_rows = []
    for r in rows:
        if r["ban_do"] != "dia_hinh" or r["thuat_toan"] != "A*":
            continue
        if not (float(r["w"]) == 1.0 or float(r["w"]) > 1.0):
            continue
        if float(r["w"]) == 1.0 and int(r["cho_mo_lai_dinh"]) != 1:
            continue
        w_rows.append([SHORT_NAME["dia_hinh"], f"{float(r['w']):g}",
                       "có" if int(r["cho_mo_lai_dinh"]) == 1 else "không",
                       _f(r["chi_phi_thuc"]), _i(r["so_o"]), _i(r["so_dinh_duyet"]),
                       _i(r["so_dinh_sinh"]), _i(r["open_lon_nhat"]),
                       _f(r["thoi_gian_ms"]), "có" if _i(r["toi_uu"]) == "1" else "không"])
    ctx["tbl_tn_w"] = ("Bảng 4.9: Kết quả khảo sát biến thể A* có trọng số",
                       ["Bộ dữ liệu", "w", "Mở lại", "Chi phí", "Ô", "Duyệt", "Sinh",
                        "OPEN", "TG (ms)", "Tối ưu"], w_rows,
                       [1.8, 1.0, 1.4, 1.7, 1.0, 1.4, 1.3, 1.4, 1.5, 1.5],
                       (1, 2, 3, 4, 5, 6, 7, 8, 9), 10.0)

    # --- Bảng 4.10: 4 hướng và 8 hướng (đọc từ tệp kết quả TN5 nếu có)
    tn8 = _load_tn8()
    ctx["tbl_tn_8"] = ("Bảng 4.10: Kết quả so sánh cấu hình bốn hướng và tám hướng",
                       ["Bộ dữ liệu", "Cấu hình", "h(n)", "Chi phí", "Ô", "Bước", "Duyệt",
                        "Sinh", "TG (ms)", "Tối ưu"], tn8,
                       [1.8, 1.6, 1.4, 1.7, 1.0, 1.3, 1.4, 1.3, 1.5, 1.5],
                       (1, 2, 3, 4, 5, 6, 7, 8, 9), 10.0)

    # --- Bảng kiểm thử
    ctx["tbl_tests"] = ("Bảng 4.4: Kịch bản kiểm thử tiêu biểu",
                        ["Mã", "Kịch bản kiểm thử", "Kết quả mong đợi"],
                        [
                            ["TC-01", "Đỉnh xuất phát trùng đỉnh đích",
                             "Đường đi gồm một ô, chi phí bằng 0"],
                            ["TC-02", "Đích bị bốn tường bao kín",
                             "Kết luận không tồn tại đường đi"],
                            ["TC-03", "Đỉnh xuất phát hoặc đích nằm trên tường",
                             "Không tìm thấy đường đi, không báo lỗi"],
                            ["TC-04", "Tường chắn giữa hai đỉnh, buộc phải đi vòng",
                             "Đường đi hợp lệ và có chi phí nhỏ nhất"],
                            ["TC-05", "Lưới trống có trọng số bằng 1",
                             "Chi phí đúng bằng khoảng cách Manhattan"],
                            ["TC-06", "Đường đi chéo trên lưới tám hướng",
                             "Tổng chi phí bằng ba lần căn bậc hai của hai"],
                            ["TC-07", "Lưới địa hình trọng số, so với chi phí đều",
                             "Chi phí của A* bằng chi phí tối ưu"],
                            ["TC-08", "Tìm kiếm theo chiều rộng trên lưới có trọng số",
                             "Chi phí thực của đường đi không nhỏ hơn mức tối ưu"],
                            ["TC-09", "Kiểm tra đường đi không xuyên qua tường",
                             "Mọi cặp ô liên tiếp đều kề nhau và hợp lệ"],
                            ["TC-10", "Hàm ước lượng tại đích",
                             "Giá trị bằng 0 với cả bốn hàm"],
                            ["TC-11", "Kiểm tra số sự kiện trùng với số đỉnh đã duyệt",
                             "Hai giá trị bằng nhau"],
                            ["TC-12", "Ghi lưới ra văn bản rồi đọc lại",
                             "Lưới, xuất phát và đích giữ nguyên"],
                        ],
                        [1.6, 6.6, 7.3], (0,))
    ctx["tbl_test_result"] = ("Bảng 4.5: Tổng hợp kết quả kiểm thử theo nhóm",
                              ["Nhóm kiểm thử", "Số ca", "Kết quả"],
                              [
                                  ["Nhóm 1: trường hợp cơ bản và biên", "6", "Đạt 6/6"],
                                  ["Nhóm 2: tính tối ưu so với chi phí đều", "5", "Đạt 5/5"],
                                  ["Nhóm 3: tính hợp lệ của đường đi", "2", "Đạt 2/2"],
                                  ["Nhóm 4: tính khả dụng của hàm ước lượng", "4", "Đạt 4/4"],
                                  ["Nhóm 5: thuật toán đối chứng", "4", "Đạt 4/4"],
                                  ["Nhóm 6: dòng sự kiện của bộ máy tìm kiếm", "2", "Đạt 2/2"],
                                  ["Nhóm 7: cấu trúc dữ liệu lưới", "5", "Đạt 5/5"],
                                  ["Tổng cộng", "28", "Đạt 28/28"],
                              ], [8.0, 2.5, 5.0], (1, 2))

    # --- Số liệu dùng cho phần diễn giải
    def exp(key, algo, h, w=1.0, reopen=1):
        r = next((x for x in rows if x["ban_do"] == key and x["thuat_toan"] == algo
                  and str(x["heuristic"]) == h and float(x["w"]) == w
                  and int(x["cho_mo_lai_dinh"]) == reopen), None)
        return int(float(r["so_dinh_duyet"])) if r else 0

    def cost(key, algo, h, w=1.0, reopen=1):
        r = next((x for x in rows if x["ban_do"] == key and x["thuat_toan"] == algo
                  and str(x["heuristic"]) == h and float(x["w"]) == w
                  and int(x["cho_mo_lai_dinh"]) == reopen), None)
        return float(r["chi_phi_thuc"]) if r and r["chi_phi_thuc"] else float("inf")

    shares = []
    shares_no_spiral = []
    for m in maps:
        a, u = exp(m.key, "A*", "manhattan"), exp(m.key, "UCS (Dijkstra)", "-")
        if u:
            shares.append(a / u)
            if m.key != "xoan_oc":
                shares_no_spiral.append(a / u)
    ctx["nums"] = {
        "trong_a": exp("trong", "A*", "manhattan"),
        "trong_ucs": exp("trong", "UCS (Dijkstra)", "-"),
        "vc_a": exp("vat_can_ngau_nhien", "A*", "manhattan"),
        "vc_ucs": exp("vat_can_ngau_nhien", "UCS (Dijkstra)", "-"),
        "ph_a": exp("phong_hanh_lang", "A*", "manhattan"),
        "ph_ucs": exp("phong_hanh_lang", "UCS (Dijkstra)", "-"),
        "ph_greedy_exp": exp("phong_hanh_lang", "Greedy Best-First", "manhattan"),
        "ph_greedy_cost": round(cost("phong_hanh_lang", "Greedy Best-First", "manhattan")),
        "ph_ucs_cost": round(cost("phong_hanh_lang", "UCS (Dijkstra)", "-")),
        "xo_a": exp("xoan_oc", "A*", "manhattan"),
        "dh_greedy_cost": round(cost("dia_hinh", "Greedy Best-First", "manhattan")),
        "dh_ucs_cost": round(cost("dia_hinh", "UCS (Dijkstra)", "-")),
        "dh_bfs_cost": round(cost("dia_hinh", "BFS", "-")),
        "share_pct": round(100 * sum(shares) / len(shares)) if shares else 0,
        "share_pct_no_spiral": (round(100 * sum(shares_no_spiral) / len(shares_no_spiral))
                                if shares_no_spiral else 0),
    }
    return ctx


def _load_tn8() -> list[list[str]]:
    """Đọc kết quả thí nghiệm 4 hướng so với 8 hướng (sinh lại nếu chưa có)."""
    from astar.grid import DIRS_8, Grid
    from astar.maps import sample_maps as sm
    from astar.search import MODE_ASTAR, path_cost, search, validate_path

    out: list[list[str]] = []
    for key in ("vat_can_ngau_nhien", "dia_hinh", "me_cung"):
        m = next(x for x in sm() if x.key == key)
        g8 = Grid(m.grid.width, m.grid.height, diagonal=True, name=m.grid.name)
        g8.cost = [row[:] for row in m.grid.cost]
        g8._dirs = DIRS_8
        for cfg, grid, hn in (("4 hướng", m.grid, "manhattan"), ("8 hướng", g8, "octile")):
            r = search(grid, m.start, m.goal, MODE_ASTAR, hn)
            c = path_cost(grid, r.path) if r.found else float("inf")
            ucs = search(grid, m.start, m.goal, "UCS (Dijkstra)", "zero")
            out.append([SHORT_NAME.get(m.key, m.name), cfg, SHORT_H.get(hn, hn), f"{c:.3f}", str(r.path_len), str(r.steps),
                        str(r.expanded), str(r.generated), f"{r.time_ms:.3f}",
                        "có" if abs(c - ucs.cost) < 1e-6 else "không"])
    return out


# ---------------------------------------------------------------------- #
# 2. Gom khối nội dung + danh sách mục
# ---------------------------------------------------------------------- #
def collect_blocks(ctx: dict) -> list[tuple]:
    blocks: list[tuple] = []
    blocks += CA.front_matter(ctx)
    blocks += CA.chapter1(ctx)
    blocks += CA.chapter2(ctx)
    blocks += CB.chapter3(ctx)
    blocks += CB.chapter4(ctx)
    blocks += CB.chapter5(ctx)
    blocks += CB.references(ctx)
    blocks += CB.appendix(ctx)
    return blocks


def collect_entries(blocks: list[tuple]) -> list[dict]:
    """Danh sách mục cho Mục lục, Danh mục bảng, Danh mục hình (theo thứ tự tài liệu)."""
    entries: list[dict] = []
    for b in blocks:
        kind = b[0]
        if kind in ("h1", "h2"):
            entries.append({"kind": "toc", "level": 1 if kind == "h1" else 2, "text": b[1]})
        elif kind == "figure":
            entries.append({"kind": "tof", "level": 1, "text": b[2]})
        elif kind == "table":
            entries.append({"kind": "tot", "level": 1, "text": b[1]})
        elif kind == "table_obj":
            entries.append({"kind": "tot", "level": 1, "text": b[1][0]})
    return entries


# ---------------------------------------------------------------------- #
# 3. Dựng tài liệu
# ---------------------------------------------------------------------- #
def code_source(name: str) -> str:
    if name == "astar/search.py":
        path = os.path.join(ROOT, "astar", "search.py")
        txt = open(path, encoding="utf-8").read()
        start = txt.index("def search_steps(")
        end = txt.index("def _bfs_steps(")
        head = ('# Trích astar/search.py: bộ máy A*, UCS, Greedy (rút gọn phần khai báo)\n'
                'def search_steps(grid, start, goal, mode=MODE_ASTAR,\n'
                '                 heuristic=H.DEFAULT_NAME, weight=1.0,\n'
                '                 tie_break=True, keep_sets=False, allow_reopen=True):\n')
        body = txt[start:end]
        body = body[body.index("\n") + 1:]
        extra = ("\n\n    # ... (xem toàn bộ mã nguồn tại de48/astar/search.py)\n")
        return head + body.rstrip() + extra
    if name == "gui_excerpt":
        path = os.path.join(ROOT, "gui.py")
        txt = open(path, encoding="utf-8").read()
        start = txt.index("    def _advance(")
        end = txt.index("    def _finish(")
        return txt[start:end].rstrip() + "\n\n    # ... (xem toàn bộ mã nguồn tại de48/gui.py)"
    return ""


COVER_INFO = {
    "truong": "TRƯỜNG ĐẠI HỌC KỸ THUẬT CÔNG NGHIỆP",
    "khoa": "KHOA ĐIỆN TỬ",
    "bo_mon": "Công nghệ thông tin",
    "mon_hoc": "KĨ THUẬT LẬP TRÌNH NÂNG CAO",
    "nam_hoc": "2025-2026",
    "nganh": "KỸ THUẬT MÁY TÍNH",
    "he": "ĐẠI HỌC CHÍNH QUY",
    "de_tai": "MÔ PHỎNG THUẬT TOÁN A* TRONG BÀI TOÁN TÌM ĐƯỜNG TRÊN LƯỚI (ĐỀ TÀI 48)",
    "gvhd": "GV. Nghiêm Văn Tính",
    "sv": "Trần Văn Khải",
    "lop": "K59.KTP",
    "mssv": "K235480106035",
    "nam": "2026",
    "logo": os.path.join(REPORTS, "assets", "tnut-logo.png"),
    "ngay_giao": "20/09/2026",
    "ngay_ht": "27/10/2026",
}


def build_doc(ctx: dict, blocks: list[tuple], entries: list[dict],
              pages: dict[int, int] | None = None):
    import cover_build

    doc = S.new_document()
    cover_build.add_cover(doc, COVER_INFO)
    cover_build.add_body_section(doc)
    pages = pages or {}
    counter = {"toc": 0, "tof": 0, "tot": 0}

    def list_block(kind: str) -> None:
        """Sinh Mục lục / Danh mục bảng / Danh mục hình với số trang thật."""
        for idx, e in enumerate(entries):
            if e["kind"] != kind:
                continue
            pg = pages.get(idx, "")
            p = doc.add_paragraph()
            pf = p.paragraph_format
            pf.first_line_indent = Cm(0)
            tab_leader(p)          # tab phải, đường dẫn chấm tới số trang
            pf.space_after = Pt(1)
            pf.line_spacing = 1.15
            if kind == "toc" and e["level"] == 2:
                pf.left_indent = Cm(0.8)
            run = p.add_run(f"{e['text']}\t{pg}")
            run.font.name = S.FONT
            run.font.size = Pt(11.5)

    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    def tab_leader(p) -> None:
        ppr = p._p.get_or_add_pPr()
        tabs = OxmlElement("w:tabs")
        tab = OxmlElement("w:tab")
        tab.set(qn("w:val"), "right")
        tab.set(qn("w:leader"), "dot")
        tab.set(qn("w:pos"), str(int(15.5 * 567)))
        tabs.append(tab)
        ppr.append(tabs)

    for b in blocks:
        kind = b[0]
        if kind == "h1":
            S.heading(doc, b[1], 1)
        elif kind == "h2":
            S.heading(doc, b[1], 2)
        elif kind == "p":
            S.para(doc, b[1])
        elif kind == "bullets":
            S.bullets(doc, b[1])
        elif kind == "formula":
            S.formula(doc, b[1], b[2] if len(b) > 2 else "")
        elif kind == "ref":
            S.para(doc, b[1], indent=False)
        elif kind == "figure":
            S.figure(doc, os.path.join(ROOT, b[1]), b[2], b[3] if len(b) > 3 else 15.5)
        elif kind == "table":
            S.table(doc, b[1], b[2], b[3], b[4])
        elif kind == "table_obj":
            spec = b[1]
            cap, headers, rows, widths, centers = spec[:5]
            font_size = spec[5] if len(spec) > 5 else S.TABLE_SIZE
            S.table(doc, cap, headers, rows, widths, font_size=font_size,
                    center_cols=tuple(centers))
        elif kind == "code_file":
            S.code_block(doc, code_source(b[1]), max_lines=110)
        elif kind == "code_text":
            S.code_block(doc, b[1])
        elif kind == "toc":
            list_block("toc")
        elif kind == "tot":
            list_block("tot")
        elif kind == "tof":
            list_block("tof")
        else:  # pragma: no cover
            raise ValueError(f"Khối không hỗ trợ: {kind}")
    # Chỉ đánh số trang cho section thân báo cáo (bìa không đánh số)
    S.add_page_numbers(doc, sections=[doc.sections[-1]])
    return doc


# ---------------------------------------------------------------------- #
# 4. Render và dò số trang
# ---------------------------------------------------------------------- #
def render_pdf(docx_path: str, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    subprocess.run([SOFFICE, "--headless", "--convert-to", "pdf", "--outdir", out_dir,
                    docx_path], check=True, capture_output=True, timeout=600)
    pdf = os.path.join(out_dir, os.path.splitext(os.path.basename(docx_path))[0] + ".pdf")
    if not os.path.exists(pdf):
        raise RuntimeError("Không render được PDF: " + pdf)
    return pdf


def detect_pages(pdf_path: str, entries: list[dict]) -> dict[int, int]:
    import pymupdf

    doc = pymupdf.open(pdf_path)
    page_text = []
    for page in doc:
        t = re.sub(r"\s+", " ", page.get_text())
        page_text.append(t)
    cursor = 0
    pages: dict[int, int] = {}
    for idx, e in enumerate(entries):
        needle = re.sub(r"\s+", " ", e["text"])[:44]
        found = None
        for pi in range(cursor, len(page_text)):
            if needle in page_text[pi]:
                found = pi + 1
                cursor = pi
                break
        if found is None:
            for pi in range(0, len(page_text)):
                if needle in page_text[pi]:
                    found = pi + 1
                    break
        pages[idx] = found or ""
    return pages


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    os.makedirs(REPORTS, exist_ok=True)
    os.makedirs(BUILD, exist_ok=True)

    rows = load_rows()
    ctx = build_ctx(rows)
    blocks = collect_blocks(ctx)
    entries = collect_entries(blocks)
    print(f"Số khối nội dung: {len(blocks)} | mục lục: "
          f"{sum(1 for e in entries if e['kind'] == 'toc')} | "
          f"danh mục hình: {sum(1 for e in entries if e['kind'] == 'tof')} | "
          f"danh mục bảng: {sum(1 for e in entries if e['kind'] == 'tot')}")

    pages: dict[int, int] = {}
    docx_path = os.path.join(BUILD, "BaoCao_BTL_DeTai48.docx")
    for attempt in range(1, 4):
        doc = build_doc(ctx, blocks, entries, pages)
        S.save(doc, docx_path)
        pdf = render_pdf(docx_path, BUILD)
        new_pages = detect_pages(pdf, entries)
        # Ảnh render tính theo trang vật lý; bìa đứng trước nên phải trừ đi phần bìa
        first = new_pages.get(0)          # số trang vật lý của mục "LỜI NÓI ĐẦU" (hiện số 1)
        if isinstance(first, int) and first > 1:
            offset = first - 1
            new_pages = {k: (v - offset if isinstance(v, int) else v)
                         for k, v in new_pages.items()}
        words = S.word_count(doc)
        import pymupdf
        n_pages = pymupdf.open(pdf).page_count
        changed = sum(1 for k, v in new_pages.items() if pages.get(k) != v)
        print(f"  lượt {attempt}: {words:,} từ, {n_pages} trang, "
              f"{changed} mục thay đổi số trang")
        if changed == 0 and attempt > 1:
            break
        pages = new_pages

    print(f"Xong. Bản nháp: {docx_path}")
    print(f"PDF kiểm tra: {pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



