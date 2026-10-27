# Đề tài 48 — Mô phỏng thuật toán A* trong bài toán tìm đường trên lưới

Báo cáo bài tập lớn học phần **Kĩ thuật lập trình nâng cao** (BTL), cài đặt bằng Python
chỉ với thư viện chuẩn, giao diện đồ hoạ dùng Tkinter.

## Chạy chương trình

```bash
python main.py            # mở giao diện mô phỏng (GUI)
python main.py demo       # chạy 1 ví dụ, in lưới và đường đi ra console
python main.py exp        # chạy toàn bộ thực nghiệm, ghi kết quả vào results/
python main.py test       # chạy 28 ca kiểm thử tự động
python main.py info       # in thông tin môi trường và danh sách dữ liệu mẫu
```

Không cần cài thêm gói nào: Tkinter có sẵn trong bản cài Python chuẩn.

## Cấu trúc dự án

```text
de48/
├── astar/                    # THƯ VIỆN TÌM KIẾM (không phụ thuộc giao diện)
│   ├── grid.py               #   lưới, vật cản, trọng số địa hình, 4/8 hướng
│   ├── heuristics.py         #   Manhattan, Euclid, Chebyshev, Octile, h = 0
│   ├── search.py             #   bộ máy A* / UCS / Greedy / BFS (phát sự kiện)
│   └── maps.py               #   sinh 6 bộ dữ liệu mẫu (xác định, tái lập được)
├── gui.py                    # GIAO DIỆN mô phỏng từng bước (Tkinter)
├── main.py                   # điểm vào: gui | demo | exp | test | info
├── experiments.py            # kịch bản thực nghiệm, xuất CSV / Markdown / HTML
├── tests/test_astar.py       # 28 ca kiểm thử (tối ưu, hợp lệ, biên, cấu trúc)
├── data/                     # 6 bản đồ mẫu (.txt) + ban_do_mau.json
├── results/                  # kết quả thực nghiệm (CSV, MD, HTML, ASCII)
├── docs/
│   ├── diagrams/             # sơ đồ UML: .puml + .svg + .png (cùng tên)
│   ├── figures/              # biểu đồ số liệu sinh từ chính chương trình
│   └── screenshots/          # ảnh chụp màn hình THẬT của giao diện
├── reports/                  # BÁO CÁO BTL (.docx + .pdf) và tư liệu kiểm định
│   ├── BaoCao_BTL_DeTai48.docx
│   ├── BaoCao_BTL_DeTai48.pdf
│   └── assets/tnut-logo.png
└── tools/                    # script sinh ảnh, chụp màn hình, dựng báo cáo
```

## Nội dung đã cài đặt

| Thành phần | Mô tả |
|---|---|
| Thuật toán | A*, UCS (Dijkstra), Greedy Best-First, BFS trên cùng một bộ máy |
| Hàm ước lượng | Manhattan, Euclid, Chebyshev, Octile, h = 0 (kèm cảnh báo khả dụng) |
| Biến thể | A* có trọng số w (0,5 đến 5), bật/tắt mở lại đỉnh, bẻ thế bằng theo h(n) |
| Lưới | 4 hướng / 8 hướng, chi phí bước chéo bằng căn hai của hai, chống cắt góc |
| Địa hình | Trọng số 1, 2, 4, 6 (đường, cỏ, cát, bùn) |
| Dữ liệu mẫu | Lưới trống, vật cản ngẫu nhiên, mê cung, phòng và hành lang, xoắn ốc, địa hình |
| Giao diện | Vẽ tường/tô địa hình/đặt xuất phát và đích, chạy, dừng, từng bước, tốc độ, phím tắt |
| Đo đạc | Bảng số liệu trực tiếp (g, h, f, số đỉnh duyệt, sinh, |OPEN|, thời gian), so sánh 4 thuật toán, xuất CSV |

## Kết quả thực nghiệm chính (sinh bởi `python main.py exp`)

Số liệu đầy đủ ở `results/ket_qua_thuc_nghiem.csv`; bảng Markdown ở
`results/bang_ket_qua.md`; báo cáo trực quan ở `results/bao_cao_thuc_nghiem.html`.

| Bộ dữ liệu | A* (đỉnh duyệt) | UCS | Mức giảm | Chi phí A* | Chi phí UCS |
|---|---|---|---|---|---|
| Lưới trống 30x20 | 49 | 600 | 91,8% | 48 | 48 |
| Vật cản ngẫu nhiên 40x25 | 127 | 693 | 81,7% | 69 | 69 |
| Mê cung 41x25 | 111 | 119 | 6,7% | 104 | 104 |
| Phòng và hành lang 60x30 | 70 | 1139 | 93,9% | 49 | 49 |
| Xoắn ốc 25x25 | 287 | 287 | 0,0% | 286 | 286 |
| Địa hình trọng số 45x28 | 1184 | 1218 | 2,8% | 128 | 128 |

Chi phí của A* luôn trùng khớp với chi phí tối ưu của Dijkstra trên cả sáu bộ dữ liệu,
tức là tính tối ưu đã được kiểm chứng bằng thực nghiệm chứ không chỉ bằng lý thuyết.

## Kiểm thử

`python main.py test` chạy 28 ca trong khoảng 0,2 giây. Các nhóm chính: trường hợp biên,
tính tối ưu so với Dijkstra (4 và 8 hướng), tính hợp lệ của đường đi, tính khả dụng của
hàm ước lượng, thuật toán đối chứng, dòng sự kiện và cấu trúc dữ liệu lưới.

## Sinh lại toàn bộ tư liệu báo cáo

```bash
# 1) sơ đồ UML (cần mạng để render qua Kroki) — nguồn .puml nằm trong docs/diagrams/
node <đường dẫn>/render-puml.mjs --in docs/diagrams/<ten>.puml --out docs/diagrams/<ten>

# 2) biểu đồ số liệu + ảnh chụp giao diện (cần matplotlib/Pillow)
python tools/make_figures.py
python tools/capture_gui.py
python tools/check_images.py

# 3) dựng báo cáo .docx (cần python-docx, PyMuPDF, LibreOffice)
python tools/build_report.py
```

`tools/build_report.py` nạp số liệu từ `results/ket_qua_thuc_nghiem.csv`, dựng tài liệu,
render ra PDF để dò số trang thật rồi dựng lại cho tới khi mục lục ổn định, và chỉ đánh
số trang cho phần thân (bìa không đánh số, thân bắt đầu lại từ 1).
