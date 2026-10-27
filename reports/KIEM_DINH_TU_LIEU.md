# Biên bản kiểm định tư liệu hình ảnh và báo cáo

Tài liệu này ghi lại bằng chứng kiểm định của toàn bộ tư liệu hình ảnh dùng trong báo cáo
Bài tập lớn Đề tài 48, cùng các lỗi đã phát hiện và cách khắc phục. Mọi kết luận ở đây đều
dựa trên việc **mở trực tiếp tệp PNG để quan sát**, không dựa trên nhật ký chạy script.

## 1. Sơ đồ UML (`docs/diagrams/`)

Kiểm định tự động bằng script của skill `diagram-auditor`:

```text
node audit-diagrams.mjs docs/diagrams --top-level-only
=> 5/5 SVG đạt các lỗi chặn cứng (không đè chữ, không cắt nét, đủ cặp SVG + PNG +
   tệp nguồn .puml, không vi phạm zero-color, cỡ chữ >= 9pt, tỉ lệ khung 0.5-2.4)
=> 2 cảnh báo vàng về mật độ nhãn (hinh_3_2, hinh_3_3) - đã soi mắt phân xử: đọc được
```

| Sơ đồ | Kích thước | Tỉ lệ | Cỡ chữ khi in 15,5 cm | Nhãn đọc được nguyên văn từ ảnh PNG | Lỗi đã phát hiện và sửa |
|---|---|---|---|---|---|
| hinh_2_1_vong_doi_dinh | 385x421 | 0,91 | 16,0 pt | "CHƯA BIẾT g(n) = ∞", "TRONG TẬP MỞ (OPEN) chờ xét", "ĐÃ DUYỆT (CLOSED) g(n) đã chốt", "TÌM THẤY ĐÍCH" | Bản đầu có 2 nhãn chuyển trạng thái đè lên nhau và đè hộp OPEN; đã giảm số nhánh từ 8 xuống 6 và rút ngắn nhãn, render lại và soi lại: sạch |
| hinh_2_2_giai_thuat_astar | 583x632 | 0,92 | 10,5 pt | "Khởi tạo: OPEN = {start}, g(start) = 0", "Lấy n có f(n) nhỏ nhất", "bước mới < g(m)?", "Cập nhật g(m), cha(m); đưa m vào OPEN" | Bản đầu rộng 930 px (chữ chỉ đạt 6,6 pt khi in A4); đã bỏ hộp chú thích và rút gọn nhãn, còn 583 px (10,5 pt) |
| hinh_3_1_kien_truc_module | 615x323 | 1,90 | 10,0 pt | "Tầng trình bày (Presentation)", "Tầng xử lý (Business Logic)", "Tầng dữ liệu và kiểm chứng", "gọi từng bước theo sự kiện" | Bản đầu là sơ đồ thành phần với mũi tên cắt xuyên khung package; đã chuyển sang kiến trúc phân tầng 3 lớp (đúng mẫu báo cáo TNUT) |
| hinh_3_2_so_do_lop | 618x434 | 1,42 | 9,9 pt | "astar_search() (generator phát sự kiện)", "Grid", "SearchResult", "manhattan(a, b)" | Script phát hiện 1 điểm đè chữ giữa nhãn bội số "1" và "*"; đã bỏ nhãn bội số trên quan hệ chứa |
| hinh_3_3_luu_do_mo_phong | 613x572 | 1,07 | 10,0 pt | "Người dùng", "gui.py (AStarApp)", "search_steps() generator", "Grid (lưới + chi phí)", "next()", "done (SearchResult)" | Cảnh báo dồn cục 13 cụm nhãn; đã rút ngắn các thông điệp tự gửi ("tô màu", "vẽ đường đi"), soi lại: đọc được |

Ghi chú về sơ đồ: mọi sơ đồ đều dùng `skinparam monochrome true` nên chỉ có thang độ xám,
phù hợp yêu cầu in ấn học thuật. Tệp nguồn `.puml` nằm cùng thư mục với ảnh xuất.

## 2. Biểu đồ và hình số liệu (`docs/figures/`)

Mọi biểu đồ được sinh từ chính bộ máy tìm kiếm của đề tài (không có số liệu nhập tay),
thang độ xám kèm hoa văn phân biệt chuỗi số liệu.

| Hình | Kích thước | Lỗi đã phát hiện khi soi ảnh | Cách sửa |
|---|---|---|---|
| hinh_2_3_g_h_f | 1125x974 | Không lỗi; đọc được "tập OPEN", "tập CLOSED", "đỉnh đang xét", và dòng g(n) = 11, h(n) = 8, f(n) = 19 | Đã bỏ số trọng số quá nhỏ ở panel bản đồ mẫu (nhỏ hơn 9 pt khi in) |
| hinh_4_1_sau_bo_du_lieu_mau | 1261x910 | Số chi phí địa hình in ở 5,4 pt, không đọc được khi in A4 | Bỏ số trong panel nhỏ (số chi phí đã thể hiện rõ ở Hình 4.6) |
| hinh_4_2_qua_trinh_astar | 1260x997 | **Một panel trống** vì mốc chụp thứ ba (160 đỉnh) vượt quá số đỉnh thực tế (127) | Chọn mốc động theo 25%, 50%, 75% số đỉnh thực tế; cả 4 panel đều có dữ liệu |
| hinh_4_3_dinh_duyet | 1261x619 | Nhãn số trên cột trùng nhau khi hai giá trị bằng nhau; tiêu đề đè lên chú giải; nhãn trục hoành chồng nhau | Chuyển sang cột ngang, rút ngắn tên bộ dữ liệu, đưa chú giải ra ngoài, bỏ nhãn số (số chính xác đã có ở Bảng 4.6 và 4.7) |
| hinh_4_4_anh_huong_heuristic | 1261x501 | Tiêu đề chồng lên chú giải; nhãn trục bị chồng | Cột ngang, chú giải đặt dưới hình, tên bộ dữ liệu viết ngắn |
| hinh_4_5_weighted_astar | 1284x628 | Chú giải và nhãn giá trị chồng lên nhau; nhãn "1.364" chạm tiêu đề; dòng "chi phí tối ưu" đè thanh dữ liệu | Chuyển sang cột ngang, chú giải đặt dưới hình, nhãn đường tối ưu đưa lên trên trục |
| hinh_4_6_4_huong_8_huong | 1263x613 | Nhãn giá trị xoay 90 độ chạm tiêu đề; nhãn trục hoành chồng nhau | Nhãn giá trị nằm ngang, tên bộ dữ liệu viết ngắn, chú giải đặt dưới hình |

## 3. Ảnh chụp màn hình (`docs/screenshots/`)

Ảnh chụp được lấy từ cửa sổ thật của chương trình bằng cách chụp toàn màn hình rồi cắt
theo khung cửa sổ, sau đó kiểm tra chất lượng bằng mắt.

| Ảnh | Kích thước | Nội dung đọc được từ ảnh | Lỗi đã phát hiện và sửa |
|---|---|---|---|
| 01_tong_quan_giao_dien | 2639x1623 | "Đề tài 48 - Mô phỏng thuật toán A* tìm đường trên lưới", bảng số liệu "số đỉnh đã duyệt 111", "chi phí đường đi 104.000", thanh trạng thái "Tìm thấy đường đi! chi phí = 104.000" | Bản đầu chỉ chụp được 57% cửa sổ (màn hình đặt tỉ lệ 175%), thiếu toàn bộ bảng điều khiển bên phải; đã sửa bằng cách quy đổi theo tỉ lệ thật rồi cắt lại |
| 02_dang_mo_phong_open_closed | 2639x1623 | "đỉnh đang xét (16, 15)", "g(n) / h(n) / f(n) 29 / 40.00 / 69.00", "số đỉnh đã duyệt 64", "|OPEN| / |CLOSED| 15 / 64" | Bản đầu chụp sau khi tìm xong (không phải trạng thái giữa chừng); đã chuyển sang tiến từng bước cố định và dừng đúng lúc để hiển thị đủ hai tập OPEN, CLOSED |
| 03_so_sanh_4_thuat_toan | 1361x493 | "Thuật toán", "Chi phí", "Duyệt", "Sinh", "OPEN max", "TG(ms)", nhãn "tối ưu" | Bảng trong hộp thoại bị bó hẹp làm chữ xuống dòng; đã mở rộng hộp thoại và tắt tự động ngắt dòng |
| 04_dia_hinh_trong_so | 2639x1623 | Số chi phí địa hình 2, 4, 6 trên các ô, "h(n): octile", "chi phí đường đi 108.841" | Số thời gian hiển thị ban đầu gồm cả thời gian vẽ; đã tách riêng thời gian tìm kiếm thuần |
| 05_huong_dan_va_chu_thich | 2639x1623 | "CHÚ THÍCH MÀU", "tập OPEN - đang chờ xét", "tập CLOSED - đã duyệt", "PHÍM TẮT" | Không lỗi |

## 4. Kiểm định báo cáo Word sau khi render

Báo cáo được render ra 57 trang (3 trang bìa + 54 trang thân) rồi soi từng trang mẫu.

| Trang | Nội dung kiểm tra | Kết quả |
|---|---|---|
| 1 (bìa chính) | Khung viền đôi, logo TNUT hiển thị đúng, tiêu đề, ngành, hệ, đề tài, "THÁI NGUYÊN - 2026" | Đạt. Bản đầu logo bị lỗi khi ghép bìa bằng công cụ ngoài; đã tự dựng bìa trong cùng tài liệu nên logo hiển thị đúng ở 3,2 cm |
| 2 (bìa lót) | Bổ sung bộ môn, năm học, giáo viên hướng dẫn, sinh viên, lớp, MSSV | Đạt |
| 3 (nhiệm vụ BTL) | Sáu mục nhiệm vụ, ngày giao và ngày hoàn thành, dòng ký | Đạt |
| 4 (LỜI NÓI ĐẦU) | Heading 1 ngắt trang đúng, văn xuôi Times New Roman 13 pt căn đều, thụt đầu dòng 1 cm, số trang hiển thị "1" | Đạt |
| 4 đến 7 (mục lục và danh mục) | Mục lục phân cấp hai mức, đường dẫn chấm tới số trang, danh mục 17 hình và 16 bảng có đủ số trang | Đạt. Bản đầu danh mục hình mất chữ "Hình"; đã khôi phục |
| 22 (công thức 2.3 và Hình 2.3) | Số công thức nằm sát lề phải trên cùng dòng, hình căn giữa, chú thích chữ nghiêng căn giữa ngay dưới hình | Đạt sau khi sửa tab dừng căn phải (bản đầu số "2.3" bị đẩy xuống dòng dưới) |
| 40 (Bảng 4.6) | Nền trắng hoàn toàn, hàng tiêu đề in đậm căn trái, lặp tiêu đề khi sang trang, chống gãy hàng, chú thích dưới bảng | Đạt sau hai lần sửa: lần đầu cột "Chi phí" hẹp làm số "166.000" bị bẻ; lần sau ba cột "Duyệt", "Ô", "TG (ms)" vẫn bẻ chữ; đã dùng tên ngắn, cỡ chữ 10 pt và cân lại độ rộng |
| 54 (Phụ lục A) | Mã nguồn trong khung Consolas 9,5 pt, giữ thụt lề | Đạt sau khi thay khoảng trắng đầu dòng bằng khoảng trắng không ngắt |
| Toàn bộ thân bài | Không còn khung viền bìa lọt sang trang thân | Đạt sau khi xoá `pgBorders` ở section thân (python-docx tự sao thuộc tính section cũ) |

## 5. Giới hạn đã biết

- Mục lục và danh mục trong tệp `.docx` là danh mục tĩnh có số trang thật, được dò từ bản
  render PDF. Nếu người dùng sửa nội dung làm thay đổi số trang thì cần chạy lại
  `tools/build_report.py` để cập nhật, không phải bấm cập nhật trường trong Word.
- Ảnh chụp màn hình phụ thuộc tỉ lệ hiển thị của Windows; kịch bản chụp đã tự quy đổi theo
  tỉ lệ thật nhưng vẫn nên chạy lại nếu thay đổi cấu hình màn hình.
- Sơ đồ UML được render qua dịch vụ Kroki nên cần kết nối mạng; tệp `.svg` và `.png` đã
  được lưu sẵn trong kho mã nguồn để không phải render lại khi chỉ xem tài liệu.
