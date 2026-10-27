"""
report_content_b.py - Nội dung Chương 3, Chương 4, Chương 5, TÀI LIỆU THAM KHẢO
và PHỤ LỤC A của báo cáo BTL.

Các bảng số liệu trong Chương 4 được build_report.py nạp từ tệp CSV thực nghiệm
(do chính chương trình sinh ra) và truyền vào qua tham số ctx, nhờ đó số liệu in
trong báo cáo luôn khớp với lần chạy thật.
"""

from __future__ import annotations


# ====================================================================== #
# CHƯƠNG 3
# ====================================================================== #
def chapter3(ctx: dict) -> list[tuple]:
    return [
        ("h1", "CHƯƠNG 3: PHÂN TÍCH THIẾT KẾ CHƯƠNG TRÌNH"),

        ("h2", "3.1. Yêu cầu chức năng và yêu cầu phi chức năng"),
        ("p", "Từ mục tiêu đã xác định ở Chương 1, chương trình được thiết kế để đáp ứng "
              "một bộ yêu cầu chức năng rõ ràng. Về mặt mô phỏng, chương trình phải cài "
              "đặt được thuật toán A* cùng ba thuật toán đối chứng gồm tìm kiếm theo chi "
              "phí đều, tìm kiếm tham lam và tìm kiếm theo chiều rộng. Về mặt cấu hình, "
              "người dùng phải chọn được hàm ước lượng, chọn giữa lưới bốn hướng và tám "
              "hướng, và điều chỉnh được trọng số của biến thể A* có trọng số."),
        ("p", "Về mặt dữ liệu, chương trình phải cho phép chỉnh sửa lưới trực tiếp bằng "
              "chuột, sinh lưới mới theo mật độ vật cản, sinh mê cung ngẫu nhiên, nạp sáu "
              "bộ dữ liệu mẫu dựng sẵn, đọc và ghi lưới dưới dạng tệp văn bản. Về mặt quan "
              "sát, chương trình phải hiển thị theo thời gian thực tập đỉnh đang chờ, tập "
              "đỉnh đã duyệt, đỉnh đang xét và đường đi cuối cùng, kèm bảng số liệu gồm "
              "các giá trị g, h, f của đỉnh đang xét."),
        ("p", "Về mặt đo đạc, chương trình phải xuất được bảng so sánh bốn thuật toán trên "
              "bản đồ hiện hành và ghi kết quả ra tệp CSV để phục vụ việc viết báo cáo. "
              "Ngoài giao diện, đề tài còn có một kịch bản dòng lệnh chạy toàn bộ thực "
              "nghiệm trên sáu bộ dữ liệu mẫu và sinh ra báo cáo kết quả dưới dạng tệp "
              "Markdown, CSV và HTML. Yêu cầu phi chức năng gồm ba điểm: chương trình chỉ "
              "được dùng thư viện chuẩn của Python ngoài thư viện Tkinter có sẵn, mã nguồn "
              "phải được tổ chức thành các mô-đun tách biệt, và phải có bộ kiểm thử tự "
              "động kiểm chứng các bất biến quan trọng của thuật toán."),

        ("h2", "3.2. Kiến trúc phân tầng của chương trình"),
        ("p", "Chương trình được tổ chức theo kiến trúc phân tầng gồm ba tầng. Tầng trình "
              "bày chứa mô-đun giao diện, chịu trách nhiệm dựng cửa sổ, vẽ lưới, xử lý sự "
              "kiện chuột và bàn phím, và hiển thị số liệu. Tầng xử lý chứa thư viện tìm "
              "kiếm gồm bốn mô-đun con là bộ máy tìm kiếm, biểu diễn lưới, các hàm ước "
              "lượng và sinh dữ liệu mẫu. Tầng dữ liệu và kiểm chứng chứa bộ dữ liệu mẫu "
              "dưới dạng văn bản và JSON, bộ kiểm thử tự động và kịch bản thực nghiệm."),
        ("p", "Cách phân tầng này mang lại hai lợi ích cụ thể. Thứ nhất, tầng xử lý hoàn "
              "toàn không phụ thuộc vào Tkinter, do đó cùng một thư viện tìm kiếm có thể "
              "được dùng lại trong kịch bản dòng lệnh và trong bộ kiểm thử tự động mà "
              "không cần thay đổi mã nguồn. Thứ hai, việc đo đạc hiệu năng có thể thực "
              "hiện ở tầng xử lý nên không bị ảnh hưởng bởi thời gian vẽ của giao diện. "
              "Hình 3.1 mô tả ba tầng cùng chiều phụ thuộc giữa chúng."),
        ("figure", "docs/diagrams/hinh_3_1_kien_truc_module.png",
         "Hình 3.1: Kiến trúc phân tầng của chương trình mô phỏng thuật toán A*", 14.0),
        ("p", "Chiều phụ thuộc giữa các tầng là một chiều. Tầng trình bày gọi tầng xử lý "
              "theo từng bước thông qua bộ sinh sự kiện, tầng xử lý đọc dữ liệu lưới và "
              "trả về kết quả, tầng kiểm chứng chạy các thí nghiệm trên tầng xử lý và ghi "
              "kết quả ra tệp. Không có phụ thuộc ngược từ tầng xử lý lên tầng trình bày, "
              "điều này được kiểm chứng bằng việc bộ kiểm thử tự động chạy được mà không "
              "cần khởi tạo cửa sổ đồ hoạ."),

        ("h2", "3.3. Thiết kế lớp và các mô-đun chính"),
        ("p", "Thư viện tìm kiếm gồm bốn lớp và một nhóm hàm tự do. Lớp Grid biểu diễn "
              "lưới với ma trận chi phí, cờ cấu hình bốn hay tám hướng, và bộ đệm danh "
              "sách đỉnh kề. Lớp SampleMap gói một bộ dữ liệu mẫu gồm lưới, đỉnh xuất "
              "phát, đỉnh đích và phần mô tả. Lớp SearchResult lưu toàn bộ kết quả của một "
              "lần tìm kiếm gồm đường đi, tổng chi phí, số đỉnh đã duyệt, số đỉnh đã sinh, "
              "kích thước lớn nhất của tập OPEN, độ sâu lớn nhất và thời gian chạy. Nhóm "
              "hàm tự do chứa bốn hàm ước lượng và hàm khoảng cách tương ứng."),
        ("p", "Bộ máy tìm kiếm được cài đặt dưới dạng một hàm sinh sự kiện. Thay vì chạy "
              "trọn vẹn từ đầu đến cuối rồi mới trả về kết quả, hàm này lần lượt phát ra "
              "các sự kiện như đỉnh vừa được đưa vào tập OPEN, đỉnh vừa được lấy ra duyệt, "
              "đỉnh vừa được mở lại, và sự kiện kết thúc kèm đối tượng kết quả. Nhờ thiết "
              "kế này, giao diện có thể dừng giữa chừng, chạy từng bước hoặc chạy với tốc "
              "độ tuỳ chọn mà không cần viết lại thuật toán. Hình 3.2 mô tả quan hệ giữa "
              "các lớp và nhóm hàm này."),
        ("figure", "docs/diagrams/hinh_3_2_so_do_lop.png",
         "Hình 3.2: Sơ đồ lớp lõi của thư viện tìm kiếm và quan hệ giữa các thành phần", 13.0),
        ("p", "Bảng 3.1 đặc tả các hàm chính của tầng xử lý. Việc đặc tả rõ kiểu tham số "
              "và kiểu trả về giúp phần cài đặt giao diện và phần kiểm thử sử dụng thư "
              "viện theo cùng một cách hiểu, đồng thời là cơ sở để mở rộng thêm thuật toán "
              "mới mà không phải sửa các mô-đun đã có."),
        ("table", "Bảng 3.1: Đặc tả các hàm chính của tầng xử lý",
         ["Hàm", "Tham số", "Kết quả trả về"],
         [
             ["search_steps", "lưới, xuất phát, đích, thuật toán, hàm ước lượng, trọng số",
              "bộ sinh các sự kiện của quá trình tìm kiếm"],
             ["search", "như trên",
              "đối tượng kết quả sau khi chạy xong toàn bộ"],
             ["neighbors", "một ô của lưới",
              "danh sách các cặp ô kề cùng chi phí bước đi"],
             ["weight", "một ô của lưới",
              "trọng số của ô, bằng vô cùng nếu là tường"],
             ["from_text, to_text", "danh sách dòng ký tự hoặc đối tượng lưới",
              "đối tượng lưới có đỉnh xuất phát, đỉnh đích hoặc chuỗi ký tự"],
             ["sample_maps", "cờ cấu hình bốn hay tám hướng",
              "danh sách sáu bộ dữ liệu mẫu đã dựng"],
             ["validate_path", "lưới, xuất phát, đích, đường đi",
              "cặp giá trị gồm cờ hợp lệ và thông báo mô tả"],
         ],
         [3.4, 6.4, 5.7]),

        ("h2", "3.4. Cấu trúc dữ liệu biểu diễn lưới"),
        ("p", "Lưới được biểu diễn bằng hai cấu trúc dữ liệu. Cấu trúc thứ nhất là ma trận "
              "chi phí hai chiều kích thước H nhân W, trong đó phần tử ở hàng r cột c là "
              "trọng số để đi vào ô đó. Ô bị chặn được biểu diễn bằng giá trị vô cùng, nhờ "
              "đó phép kiểm tra ô có đi được hay không chỉ là một phép so sánh. Cấu trúc "
              "thứ hai là bộ đệm danh sách đỉnh kề dạng bảng băm, lưu kết quả sinh lân cận "
              "của từng ô đã từng được hỏi tới. Bộ đệm này bị xoá mỗi khi lưới thay đổi "
              "cấu hình hoặc trọng số."),
        ("p", "Việc lưu đệm lân cận mang lại lợi ích đáng kể trong các thuật toán có mở "
              "lại đỉnh. Khi một đỉnh được sinh kề nhiều lần trong các vòng lặp khác nhau, "
              "chương trình không phải tính lại hệ số khoảng cách và kiểm tra cắt góc cho "
              "từng hướng, mà chỉ đọc lại danh sách đã tính trước. Chi phí bộ nhớ của bộ "
              "đệm là tuyến tính theo số ô đã được hỏi tới, trong khi lợi ích về thời gian "
              "thể hiện rõ nhất trên các bộ dữ liệu có nhiều đỉnh được sinh lặp lại."),
        ("p", "Để thuận tiện cho việc trao đổi dữ liệu và kiểm thử, lưới còn được biểu "
              "diễn dưới dạng văn bản với mỗi dòng tương ứng một hàng và mỗi ký tự tương "
              "ứng một ô. Cách biểu diễn này cho phép viết các bộ dữ liệu kiểm thử rất gọn "
              "ngay trong mã nguồn, đồng thời cho phép người dùng mở và chỉnh sửa bản đồ "
              "bằng bất kì trình soạn thảo văn bản nào. Bảng 3.2 liệt kê bộ ký tự được "
              "quy ước."),
        ("table", "Bảng 3.2: Quy ước ký tự trong tệp biểu diễn lưới",
         ["Ký tự", "Ý nghĩa", "Trọng số đi vào ô"],
         [
             ["dấu chấm", "ô trống đi được", "1"],
             ["dấu hai chấm", "địa hình nhẹ như cỏ hoặc đường mòn", "2"],
             ["dấu ngã", "địa hình nặng như cát lún hoặc nước nông", "4"],
             ["dấu bằng", "địa hình rất nặng như bùn lầy hoặc dốc đứng", "6"],
             ["dấu thăng", "tường, không thể đi vào", "vô cùng"],
             ["chữ S", "đỉnh xuất phát", "1"],
             ["chữ G", "đỉnh đích", "1"],
             ["dấu hoa thị", "ô thuộc đường đi khi kết xuất kết quả", "không áp dụng"],
             ["chữ o", "ô đã duyệt xong khi kết xuất kết quả", "không áp dụng"],
             ["dấu gạch nối", "ô đang chờ trong tập OPEN khi kết xuất", "không áp dụng"],
         ],
         [2.6, 8.6, 4.3]),

        ("h2", "3.5. Cấu trúc dữ liệu hàng đợi ưu tiên và các bảng tra cứu"),
        ("p", "Tập OPEN được cài đặt bằng cây vun đống nhị phân trên một mảng, sử dụng "
              "mô-đun hàng đợi ưu tiên của thư viện chuẩn. Mỗi phần tử trong đống là một "
              "bộ bốn thành phần gồm giá trị ưu tiên, giá trị ước lượng dùng để phá thế "
              "bằng, một số đếm tăng dần và toạ độ của ô. Số đếm tăng dần đóng vai trò "
              "quan trọng vì nếu hai phần tử có cùng hai giá trị đầu, phép so sánh sẽ "
              "chuyển sang so sánh toạ độ, điều này không gây lỗi nhưng làm mất tính ổn "
              "định của thứ tự duyệt. Việc thêm số đếm đảm bảo mọi phần tử đều so sánh "
              "được và thứ tự duyệt là xác định giữa các lần chạy."),
        ("p", "Bảng giá trị g và bảng cha được cài đặt bằng bảng băm với khoá là toạ độ ô. "
              "Bảng giá trị g lưu chi phí tốt nhất đã biết tới mỗi đỉnh đã sinh. Bảng cha "
              "lưu đỉnh đứng ngay trước trên đường đi tốt nhất tới đỉnh đó, phục vụ bước "
              "truy vết đường đi khi kết thúc. Chương trình còn duy trì một bảng độ sâu để "
              "ghi nhận độ sâu lớn nhất của cây tìm kiếm, phục vụ việc phân tích ở Chương "
              "4. Cả ba bảng đều chỉ được ghi cho các đỉnh đã sinh nên bộ nhớ sử dụng tỉ "
              "lệ với số đỉnh đã sinh chứ không phải với toàn bộ lưới."),
        ("p", "Khi một đỉnh đã nằm trong tập CLOSED được phát hiện có chi phí tốt hơn, "
              "chương trình xử lý theo hai chế độ được chọn bởi tham số cấu hình. Chế độ "
              "mặc định cho phép mở lại đỉnh, tức là loại đỉnh đó khỏi tập CLOSED và đưa "
              "trở lại tập OPEN với chi phí mới. Chế độ thứ hai khoá tập CLOSED, tức là bỏ "
              "qua mọi cập nhật cho đỉnh đã duyệt. Chương trình đếm riêng số lần mở lại "
              "đỉnh để phục vụ phân tích ở mục 4.8."),

        ("h2", "3.6. Thiết kế giao diện người dùng"),
        ("p", "Giao diện được chia thành hai vùng. Vùng bên trái là khung vẽ lưới, mỗi ô "
              "được vẽ bằng một hình chữ nhật có màu theo trạng thái hiện tại gồm nền địa "
              "hình, tập OPEN, tập CLOSED, đường đi, đỉnh xuất phát, đỉnh đích và đỉnh "
              "đang xét. Dưới khung vẽ là thanh trạng thái hiển thị thông tin của ô đang "
              "trỏ chuột và thông báo kết quả sau khi chạy xong. Vùng bên phải là bảng "
              "điều khiển gồm ba thẻ: thẻ chạy mô phỏng, thẻ bản đồ và thẻ hướng dẫn."),
        ("p", "Thẻ chạy mô phỏng gồm bốn nhóm chức năng. Nhóm thứ nhất chọn thuật toán, "
              "hàm ước lượng và trọng số, kèm dòng cảnh báo khi tổ hợp được chọn không "
              "đảm bảo tính tối ưu. Nhóm thứ hai gồm các nút chạy, dừng, tiến một bước và "
              "đặt lại, cùng thanh trượt điều chỉnh tốc độ mô phỏng. Nhóm thứ ba là bảng "
              "số liệu hiển thị toạ độ đỉnh đang xét, các giá trị g, h, f, số đỉnh đã "
              "duyệt, số đỉnh đã sinh, kích thước hai tập, độ sâu lớn nhất, chi phí đường "
              "đi, số ô, thời gian tìm kiếm và số vòng lặp. Nhóm thứ tư gồm hai nút so "
              "sánh bốn thuật toán và xuất kết quả ra tệp CSV."),
        ("p", "Thẻ bản đồ gồm các công cụ vẽ tường, tô địa hình, đặt đỉnh xuất phát và đặt "
              "đỉnh đích, các nút sinh vật cản ngẫu nhiên theo mật độ chọn trước, sinh mê "
              "cung, xoá toàn bộ lưới, nạp sáu bộ dữ liệu mẫu, mở và ghi tệp bản đồ, và "
              "các nút thay đổi cỡ ô để phóng to hoặc thu nhỏ khung vẽ. Thẻ hướng dẫn giải "
              "thích ý nghĩa các màu, liệt kê các phím tắt và nhắc lại định nghĩa của các "
              "đại lượng g, h, f để người dùng mới làm quen có thể hiểu ngay ý nghĩa của "
              "các con số xuất hiện trên màn hình."),
        ("figure", "docs/diagrams/hinh_3_3_luu_do_mo_phong.png",
         "Hình 3.3: Trình tự mô phỏng từng bước giữa giao diện và bộ máy tìm kiếm", 13.0),
        ("p", "Hình 3.3 mô tả trình tự tương tác giữa người dùng, giao diện, bộ máy tìm "
              "kiếm và lưới. Mỗi nhịp mô phỏng, giao diện gọi hàm sinh sự kiện để lấy ra "
              "một sự kiện, sau đó cập nhật màu của đúng những ô liên quan thay vì vẽ lại "
              "toàn bộ khung. Cách cập nhật cục bộ này giữ cho thao tác mô phỏng mượt ngay "
              "cả trên lưới có hơn một nghìn tám trăm ô. Khi nhận được sự kiện kết thúc, "
              "giao diện vẽ đường đi và nạp đầy đủ số liệu vào bảng thống kê."),

        ("h2", "3.7. Bộ dữ liệu mẫu và kịch bản thực nghiệm"),
        ("p", "Sáu bộ dữ liệu mẫu được sinh bởi chính chương trình theo các quy tắc xác "
              "định để đảm bảo mọi lần chạy đều cho cùng một kết quả. Bộ dữ liệu lưới "
              "trống dùng để quan sát hành vi của thuật toán khi không có vật cản. Bộ dữ "
              "liệu vật cản ngẫu nhiên dùng để kiểm thử khả năng vòng tránh với mật độ "
              "tường khoảng hai mươi tám phần trăm, có kiểm tra tính liên thông giữa đỉnh "
              "xuất phát và đỉnh đích trước khi chấp nhận bản đồ."),
        ("p", "Bộ dữ liệu mê cung được sinh bằng thuật toán đào lùi trên lưới có kích "
              "thước lẻ, cho ra cấu trúc có duy nhất một đường đi giữa hai ô bất kì. Bộ "
              "dữ liệu phòng và hành lang được sinh bằng cách tạo ngẫu nhiên các phòng "
              "chữ nhật rồi nối tâm các phòng bằng hành lang chữ L, mô phỏng cấu trúc của "
              "một toà nhà hoặc nhà máy. Bộ dữ liệu hành lang xoắn ốc được sinh bằng cách "
              "cho một tác nhân đi vòng vào tâm, tạo ra bản đồ chỉ có một lối đi duy nhất. "
              "Bộ dữ liệu địa hình trọng số rải ngẫu nhiên các vùng có trọng số hai, bốn "
              "và sáu để buộc thuật toán phải cân nhắc giữa đường ngắn và đường rẻ."),
        ("p", "Kịch bản thực nghiệm chạy trên tất cả sáu bộ dữ liệu với bốn thuật toán và "
              "bốn hàm ước lượng, ghi lại mười tám chỉ số cho mỗi lần chạy. Kết quả được "
              "xuất ra ba định dạng gồm tệp CSV để mở bằng bảng tính, tệp Markdown để dán "
              "vào báo cáo và tệp HTML có biểu đồ để xem nhanh. Ngoài ra kịch bản còn lưu "
              "lại một lần chạy kèm trực quan hoá bằng ký tự để có thể đối chiếu ngay trên "
              "dòng lệnh mà không cần mở giao diện đồ hoạ."),
    ]


# ====================================================================== #
# CHƯƠNG 4
# ====================================================================== #
def chapter4(ctx: dict) -> list[tuple]:
    n = ctx.get("nums", {})
    blocks: list[tuple] = [
        ("h1", "CHƯƠNG 4: CÀI ĐẶT, THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ"),

        ("h2", "4.1. Môi trường cài đặt và công cụ sử dụng"),
        ("p", "Chương trình được cài đặt bằng ngôn ngữ Python phiên bản 3.14 trên hệ điều "
              "hành Windows. Toàn bộ thư viện tìm kiếm, sinh dữ liệu mẫu và kiểm thử chỉ "
              "sử dụng thư viện chuẩn của Python, bao gồm mô-đun hàng đợi ưu tiên, mô-đun "
              "toán học, mô-đun đọc ghi tệp và mô-đun kiểm thử tự động. Giao diện đồ hoạ "
              "dùng Tkinter, cũng là thư viện có sẵn trong bản cài đặt chuẩn. Nhờ vậy, "
              "chương trình chạy được ngay sau khi cài Python mà không cần bước cài thêm "
              "gói phụ thuộc nào."),
        ("p", "Việc đo thời gian được thực hiện bằng đồng hồ đơn điệu có độ phân giải cao "
              "của mô-đun đo thời gian. Với mỗi lần tìm kiếm, chương trình ghi lại thời "
              "điểm bắt đầu trước khi khởi tạo tập OPEN và thời điểm kết thúc ngay sau khi "
              "trả về kết quả. Cách đo này chỉ tính thời gian bộ máy tìm kiếm thực sự chạy, "
              "không tính thời gian dựng giao diện, do đó số liệu đo được có thể so sánh "
              "trực tiếp giữa các thuật toán. Riêng số liệu hiển thị trên giao diện cũng "
              "được tính theo nguyên tắc tách riêng phần tìm kiếm và phần vẽ, chi tiết này "
              "được trình bày ở mục 4.10."),
        ("table", "Bảng 4.1: Môi trường cài đặt và cấu hình thử nghiệm",
         ["Thành phần", "Thông số"],
         [
             ["Hệ điều hành", "Windows, kiến trúc 64 bit"],
             ["Ngôn ngữ", "Python 3.14, chạy ở chế độ dòng lệnh và chế độ giao diện"],
             ["Thư viện dùng cho giao diện", "Tkinter có sẵn trong bản cài đặt chuẩn"],
             ["Thư viện dùng cho thực nghiệm", "Chỉ thư viện chuẩn, không dùng gói ngoài"],
             ["Kích thước lưới lớn nhất", "60 hàng nhân 30 cột, tương đương 1800 ô"],
             ["Số bộ dữ liệu mẫu", "6 bộ, sinh xác định theo hạt giống ngẫu nhiên"],
             ["Số ca kiểm thử tự động", "28 ca, chạy trong khoảng 0,2 giây"],
             ["Định dạng kết xuất", "CSV, JSON, Markdown, HTML, ảnh PNG"],
         ],
         [5.0, 10.5]),

        ("h2", "4.2. Sáu bộ dữ liệu mẫu"),
        ("p", "Sáu bộ dữ liệu mẫu được chọn để bao phủ các cấu trúc bản đồ khác nhau, từ "
              "trường hợp không có vật cản tới trường hợp lưới chỉ có một lối đi duy nhất. "
              "Hình 4.1 trình bày hình dạng của cả sáu bộ dữ liệu cùng tỉ lệ ô tường của "
              "mỗi bộ. Việc đặt chúng cạnh nhau cho thấy rõ sự khác biệt về cấu trúc và "
              "giải thích vì sao cùng một thuật toán lại có kết quả rất khác nhau giữa các "
              "bộ dữ liệu."),
        ("figure", "docs/figures/hinh_4_1_sau_bo_du_lieu_mau.png",
         "Hình 4.1: Sáu bộ dữ liệu mẫu dùng cho thực nghiệm, kèm kích thước và tỉ lệ tường",
         15.5),
        ("p", "Bộ dữ liệu lưới trống có kích thước ba mươi nhân hai mươi ô và không có "
              "tường. Bộ dữ liệu vật cản ngẫu nhiên có kích thước bốn mươi nhân hai mươi "
              "lăm ô với khoảng hai mươi tám phần trăm ô là tường. Bộ dữ liệu mê cung có "
              "kích thước bốn mươi mốt nhân hai mươi lăm ô, tỉ lệ tường hơn năm mươi phần "
              "trăm và là bản đồ liên thông yếu, nghĩa là giữa hai ô bất kì chỉ có đúng "
              "một đường đi. Bộ dữ liệu phòng và hành lang có kích thước sáu mươi nhân ba "
              "mươi ô, gồm mười phòng lớn nối với nhau bằng cửa hẹp. Bộ dữ liệu hành lang "
              "xoắn ốc có kích thước hai mươi lăm nhân hai mươi lăm ô và chỉ có một hành "
              "lang duy nhất đi từ ngoài vào tâm. Bộ dữ liệu địa hình trọng số có kích "
              "thước bốn mươi lăm nhân hai mươi tám ô với các vùng chi phí hai, bốn và "
              "sáu rải rác. Bảng 4.2 tổng hợp thông số của sáu bộ dữ liệu."),
        ("table_obj", ctx.get("tbl_datasets", (
            "Bảng 4.2: Thông số của sáu bộ dữ liệu mẫu",
            ["Bộ dữ liệu", "Kích thước", "Tỉ lệ tường", "Xuất phát", "Đích", "Số ô đi được"],
            [["chưa nạp số liệu", "", "", "", "", ""]],
            [4.2, 2.2, 2.1, 2.2, 2.2, 2.6], (1, 2, 3, 4, 5)))),

        ("h2", "4.3. Diễn biến quá trình tìm kiếm trên lưới vật cản"),
        ("p", "Hình 4.2 ghi lại bốn thời điểm của cùng một lần chạy A* trên bộ dữ liệu vật "
              "cản ngẫu nhiên. Ở thời điểm đầu, tập CLOSED chỉ là một vùng nhỏ bao quanh "
              "đỉnh xuất phát, còn tập OPEN là lớp ô mỏng nằm ở rìa vùng đó. Khi quá trình "
              "tiếp diễn, vùng đã duyệt mở rộng thành một dải hẹp uốn theo hướng đích thay "
              "vì lan đều ra bốn phía. Ở thời điểm thứ ba, dải đã duyệt gần chạm tới đích. "
              "Bức ảnh cuối cùng là kết quả sau khi tìm xong, với đường đi gồm bảy mươi ô "
              "và tổng chi phí bằng sáu mươi chín."),
        ("figure", "docs/figures/hinh_4_2_qua_trinh_astar.png",
         "Hình 4.2: Diễn biến quá trình A* trên lưới vật cản ngẫu nhiên qua bốn thời điểm",
         15.0),
        ("p", "Điều đáng chú ý trong Hình 4.2 là hình dạng của vùng đã duyệt. Nếu dùng "
              "tìm kiếm theo chi phí đều, vùng này sẽ là một hình tròn bán kính tăng dần "
              "cho tới khi chạm đích, tức là số đỉnh duyệt tỉ lệ với diện tích hình tròn. "
              "Với A*, vùng đã duyệt co lại thành một dải hẹp chạy theo hướng từ đỉnh xuất "
              "phát tới đỉnh đích. Chính hình dạng dải hẹp này là nguyên nhân trực tiếp "
              "giúp số đỉnh duyệt giảm từ sáu trăm chín mươi ba xuống còn một trăm hai "
              "mươi bảy trên cùng một bộ dữ liệu, tương ứng mức giảm khoảng tám mươi hai "
              "phần trăm."),

        ("h2", "4.4. Giao diện chương trình"),
        ("p", "Hình 4.3 là ảnh chụp màn hình của giao diện sau khi chạy xong thuật toán A* "
              "trên bộ dữ liệu mê cung. Bảng số liệu bên phải hiển thị số đỉnh đã duyệt là "
              "một trăm mười một, số đỉnh đã sinh là một trăm mười hai, chi phí đường đi "
              "bằng một trăm linh bốn, đường đi gồm một trăm linh năm ô và thời gian tìm "
              "kiếm dưới mười mili giây. Thanh trạng thái ở đáy khung vẽ nhắc lại kết quả "
              "này bằng một dòng thông báo ngắn."),
        ("figure", "docs/screenshots/01_tong_quan_giao_dien.png",
         "Hình 4.3: Giao diện chương trình sau khi hoàn tất tìm kiếm trên bộ dữ liệu mê cung",
         15.5),
        ("p", "Hình 4.4 là ảnh chụp màn hình tại thời điểm quá trình tìm kiếm chưa kết "
              "thúc. Ở trạng thái giữa chừng này, vùng màu tối phía dưới bên trái là tập "
              "CLOSED đã duyệt, viền xám nhạt là tập OPEN đang chờ, và ô viền đậm là đỉnh "
              "đang được xét có toạ độ hàng mười sáu cột mười lăm. Bảng số liệu hiển thị "
              "tương ứng giá trị g bằng hai mươi chín, giá trị h bằng bốn mươi và giá trị "
              "f bằng sáu mươi chín, cùng số đỉnh đã duyệt là sáu mươi bốn. Đây là hình "
              "ảnh minh hoạ trực tiếp cho cách A* mở rộng vùng tìm kiếm có định hướng."),
        ("figure", "docs/screenshots/02_dang_mo_phong_open_closed.png",
         "Hình 4.4: Trạng thái giữa chừng của quá trình tìm kiếm với hai tập OPEN và CLOSED",
         15.5),
        ("p", "Hình 4.5 là hộp thoại so sánh bốn thuật toán trên bộ dữ liệu phòng và hành "
              "lang. Bảng trong hộp thoại liệt kê chi phí thực của đường đi, số ô, số đỉnh "
              "đã duyệt, số đỉnh đã sinh, kích thước lớn nhất của tập OPEN và thời gian "
              "chạy của từng thuật toán. Ba thuật toán A*, tìm kiếm theo chi phí đều và "
              "tìm kiếm theo chiều rộng cho cùng chi phí bằng bốn mươi chín và được đánh "
              "dấu là tối ưu, trong khi tìm kiếm tham lam cho chi phí năm mươi bảy, tức là "
              "kém hơn mức tối ưu khoảng mười sáu phần trăm."),
        ("figure", "docs/screenshots/03_so_sanh_4_thuat_toan.png",
         "Hình 4.5: Hộp thoại so sánh bốn thuật toán trên cùng một bản đồ", 15.5),
        ("p", "Hình 4.6 minh hoạ bộ dữ liệu địa hình trọng số khi bật cấu hình tám hướng. "
              "Các ô có chữ số là ô địa hình nặng với chi phí tương ứng hai, bốn hoặc sáu. "
              "Bảng số liệu cho thấy chi phí đường đi bằng một trăm linh tám phẩy tám bốn "
              "mươi mốt, số ô trên đường đi là năm mươi bốn và thời gian tìm kiếm lớn hơn "
              "đáng kể so với các bộ dữ liệu khác. Việc cho phép đi chéo giúp đường đi "
              "ngắn hơn về số ô nhưng đồng thời làm tăng số đỉnh cần duyệt vì mỗi ô có "
              "tới tám ô kề."),
        ("figure", "docs/screenshots/04_dia_hinh_trong_so.png",
         "Hình 4.6: Bộ dữ liệu địa hình có trọng số với cấu hình tám hướng", 15.5),
        ("p", "Hình 4.7 là thẻ hướng dẫn của giao diện, trong đó giải thích ý nghĩa các "
              "màu và liệt kê các phím tắt. Việc đưa phần giải thích vào ngay trong chương "
              "trình giúp người dùng lần đầu sử dụng có thể hiểu đúng ý nghĩa của từng "
              "màu và từng con số mà không cần đọc tài liệu riêng. Bảng 4.3 tóm tắt các "
              "chỉ số mà giao diện hiển thị trong quá trình mô phỏng."),
        ("figure", "docs/screenshots/05_huong_dan_va_chu_thich.png",
         "Hình 4.7: Thẻ hướng dẫn và chú thích màu trong giao diện chương trình", 15.5),

        ("h2", "4.5. Kịch bản kiểm thử và kết quả kiểm thử"),
        ("p", "Bộ kiểm thử tự động gồm hai mươi tám ca, chia thành bảy nhóm. Nhóm thứ nhất "
              "kiểm tra các trường hợp cơ bản gồm đỉnh xuất phát trùng đỉnh đích, đích bị "
              "bao kín nên không có đường đi, đỉnh xuất phát hoặc đỉnh đích nằm trên tường, "
              "và trường hợp lưới trống yêu cầu chi phí đúng bằng khoảng cách Manhattan. "
              "Nhóm thứ hai kiểm tra tính tối ưu bằng cách so sánh chi phí của A* với chi "
              "phí của tìm kiếm theo chi phí đều trên cả sáu bộ dữ liệu với hai cấu hình "
              "bốn hướng và tám hướng."),
        ("p", "Nhóm thứ ba kiểm tra tính hợp lệ của đường đi gồm các điều kiện đường đi "
              "phải bắt đầu từ đúng đỉnh xuất phát, kết thúc tại đúng đích, không chứa ô "
              "lặp, mọi cặp ô liên tiếp phải kề nhau và không đi xuyên qua tường. Nhóm thứ "
              "tư kiểm tra các hàm ước lượng gồm điều kiện giá trị tại đích bằng không và "
              "điều kiện không ước lượng vượt quá chi phí tối ưu thực tế trên cả sáu bộ dữ "
              "liệu. Nhóm thứ năm kiểm tra các thuật toán đối chứng gồm việc tìm kiếm tham "
              "lam không bao giờ cho chi phí tốt hơn mức tối ưu và tìm kiếm theo chiều rộng "
              "cho số bước đúng bằng số bước của A* trên lưới không có trọng số."),
        ("p", "Nhóm thứ sáu kiểm tra dòng sự kiện của bộ máy tìm kiếm gồm việc số sự kiện "
              "duyệt đỉnh phải khớp với số đỉnh đã duyệt trong kết quả, và không có sự "
              "kiện nào trỏ tới ô là tường. Nhóm thứ bảy kiểm tra cấu trúc dữ liệu lưới "
              "gồm việc biểu diễn văn bản phải đọc lại đúng như đã ghi, số đỉnh kề của ô "
              "ở giữa lưới phải bằng bốn hoặc tám tuỳ cấu hình, quy tắc không cắt góc phải "
              "chặn được bước đi chéo xuyên qua khe hở giữa hai tường, và chi phí bước đi "
              "phải nhân đúng theo trọng số của ô đích. Bảng 4.4 trình bày các kịch bản "
              "kiểm thử tiêu biểu và Bảng 4.5 tổng hợp kết quả."),
        ("table_obj", ctx.get("tbl_tests", (
            "Bảng 4.4: Kịch bản kiểm thử tiêu biểu",
            ["Mã", "Kịch bản", "Kết quả mong đợi"],
            [["chưa nạp", "", ""]], [1.6, 6.9, 7.0], (0,))),
        ),
        ("table_obj", ctx.get("tbl_test_result", (
            "Bảng 4.5: Tổng hợp kết quả kiểm thử theo nhóm",
            ["Nhóm kiểm thử", "Số ca", "Kết quả"],
            [["chưa nạp", "", ""]], [8.0, 2.5, 5.0], (1, 2))),
        ),

        ("h2", "4.6. Thí nghiệm 1 và 2: so sánh A* với các thuật toán đối chứng"),
        ("p", "Thí nghiệm thứ nhất chạy A* với bốn hàm ước lượng khác nhau trên cả sáu bộ "
              "dữ liệu mẫu. Thí nghiệm thứ hai chạy thêm ba thuật toán đối chứng gồm tìm "
              "kiếm theo chi phí đều, tìm kiếm tham lam và tìm kiếm theo chiều rộng trên "
              "cùng bộ dữ liệu. Tất cả các lần chạy đều dùng cấu hình bốn hướng, hàm ước "
              "lượng Manhattan cho A* và tìm kiếm tham lam, và trọng số bằng một. Chi phí "
              "ghi trong bảng là chi phí thực của đường đi, đã tính đầy đủ trọng số địa "
              "hình, do đó có thể dùng để so sánh trực tiếp giữa các thuật toán."),
        ("p", "Kết quả đầy đủ của hai thí nghiệm được trình bày trong Bảng 4.6 và được "
              "biểu diễn bằng biểu đồ ở Hình 4.8. Cột tối ưu cho biết đường đi tìm được "
              "có chi phí đúng bằng chi phí tối ưu tham chiếu hay không, trong đó chi phí "
              "tham chiếu được lấy từ tìm kiếm theo chi phí đều. Kết quả cho thấy A* luôn "
              "đạt mức tối ưu, tìm kiếm theo chi phí đều và tìm kiếm theo chiều rộng cũng "
              "đạt mức tối ưu về chi phí thực trên mọi bộ dữ liệu, còn tìm kiếm tham lam "
              "không đạt mức tối ưu trên ba bộ dữ liệu."),
        ("table_obj", ctx.get("tbl_tn12", (
            "Bảng 4.6: Kết quả thí nghiệm 1 và 2 trên sáu bộ dữ liệu mẫu",
            ["Bộ dữ liệu", "Thuật toán", "h(n)", "Chi phí", "Ô", "Duyệt", "Sinh",
             "OPEN max", "Thời gian (ms)", "Tối ưu"],
            [["chưa nạp", "", "", "", "", "", "", "", "", ""]],
            [2.4, 3.0, 1.9, 1.5, 1.0, 1.3, 1.2, 1.5, 1.8, 1.4], (3, 4, 5, 6, 7, 8, 9))),
        ),
        ("figure", "docs/figures/hinh_4_3_dinh_duyet.png",
         "Hình 4.8: Số đỉnh đã duyệt của bốn thuật toán trên sáu bộ dữ liệu mẫu", 15.5),
        ("p", f"Trên bộ dữ liệu lưới trống, A* chỉ duyệt {n.get('trong_a', 49)} đỉnh trong "
              f"khi tìm kiếm theo chi phí đều phải duyệt {n.get('trong_ucs', 600)} đỉnh, "
              "tương ứng mức giảm hơn mười hai lần. Trên bộ dữ liệu vật cản ngẫu nhiên, "
              f"mức giảm là từ {n.get('vc_ucs', 693)} đỉnh xuống "
              f"{n.get('vc_a', 127)} đỉnh. Trên bộ dữ liệu phòng và hành lang, mức giảm "
              f"lớn nhất trong cả sáu bộ dữ liệu khi số đỉnh duyệt giảm từ "
              f"{n.get('ph_ucs', 1139)} xuống {n.get('ph_a', 70)} đỉnh. Nguyên nhân là "
              "cấu trúc phòng lớn nối bằng cửa hẹp khiến tìm kiếm không có thông tin phải "
              "lan ra toàn bộ các phòng, trong khi hàm ước lượng giúp A* đi thẳng tới "
              "phòng chứa đích."),
        ("p", f"Ngược lại, trên bộ dữ liệu hành lang xoắn ốc, cả bốn thuật toán đều duyệt "
              f"{n.get('xo_a', 287)} đỉnh, đúng bằng số ô đi được của bản đồ. Kết quả này "
              "không phải là sai sót mà là hệ quả tất yếu của cấu trúc bản đồ: khi chỉ có "
              "một lối đi duy nhất, mọi thuật toán đều buộc phải đi hết hành lang nên "
              "không có chỗ cho việc cắt giảm. Đây là ví dụ rõ ràng cho thấy hiệu quả của "
              "hàm ước lượng phụ thuộc vào cấu trúc của bài toán."),
        ("p", f"Trường hợp tìm kiếm tham lam cũng rất đáng chú ý. Thuật toán này duyệt ít "
              f"đỉnh nhất trên nhiều bộ dữ liệu, chẳng hạn chỉ {n.get('ph_greedy_exp', 62)} "
              "đỉnh trên bộ dữ liệu phòng và hành lang, nhưng chi phí đường đi lại là "
              f"{n.get('ph_greedy_cost', 57)} so với mức tối ưu "
              f"{n.get('ph_ucs_cost', 49)}. Trên bộ dữ liệu địa hình trọng số, mức chênh "
              f"lệch còn lớn hơn khi chi phí của tìm kiếm tham lam là "
              f"{n.get('dh_greedy_cost', 166)} so với {n.get('dh_ucs_cost', 128)}. Số đỉnh "
              "duyệt ít không đồng nghĩa với chất lượng đường đi tốt, và đây chính là lí "
              "do vì sao tìm kiếm tham lam không được dùng trong các ứng dụng đòi hỏi "
              "đường đi rẻ nhất."),
        ("p", f"Một quan sát khác liên quan tới tìm kiếm theo chiều rộng. Trên bộ dữ liệu "
              f"địa hình trọng số, thuật toán này cho đường đi có chi phí thực bằng "
              f"{n.get('dh_bfs_cost', 166)}, cao hơn mức tối ưu khoảng "
              "ba mươi phần trăm. Nguyên nhân là tìm kiếm theo chiều rộng coi mọi bước đi "
              "có cùng chi phí một và bỏ qua hoàn toàn trọng số địa hình, do đó nó ưu tiên "
              "đường có ít bước nhất dù đường đó phải đi xuyên qua vùng cát hoặc bùn. Kết "
              "quả này cho thấy tính tối ưu của một thuật toán chỉ có ý nghĩa trong khuôn "
              "khổ mô hình bài toán mà nó giả định."),
        ("table_obj", ctx.get("tbl_summary", (
            "Bảng 4.7: Mức giảm số đỉnh duyệt của A* so với tìm kiếm theo chi phí đều",
            ["Bộ dữ liệu", "A*", "Chi phí đều", "Mức giảm", "Chi phí A*", "Chi phí đều"],
            [["chưa nạp", "", "", "", "", ""]], [3.6, 1.6, 2.6, 2.0, 2.5, 2.5],
            (1, 2, 3, 4, 5))),
        ),

        ("h2", "4.7. Thí nghiệm 3: ảnh hưởng của hàm ước lượng"),
        ("p", "Thí nghiệm thứ ba giữ nguyên thuật toán A* và lần lượt thay hàm ước lượng "
              "bằng khoảng cách Manhattan, Euclid, Chebyshev và octile, đo số đỉnh phải "
              "duyệt trên bốn bộ dữ liệu đại diện. Mục đích của thí nghiệm là định lượng "
              "ảnh hưởng của độ chặt hàm ước lượng tới khối lượng công việc mà thuật toán "
              "phải thực hiện, đồng thời kiểm chứng nhận xét lý thuyết ở mục 2.6."),
        ("p", "Kết quả được trình bày trong Bảng 4.8 và Hình 4.9. Trên lưới trống, khoảng "
              "cách Manhattan chỉ cần bốn mươi chín đỉnh duyệt trong khi ba hàm còn lại "
              "cần hơn năm trăm đỉnh. Nguyên nhân là khoảng cách Manhattan khớp chính xác "
              "với chi phí thực trên lưới bốn hướng không có vật cản, do đó A* chỉ cần "
              "duyệt đúng các đỉnh nằm trên đường đi tối ưu. Khoảng cách Euclid và "
              "Chebyshev thấp hơn chi phí thực trong trường hợp này nên đỉnh được ưu tiên "
              "theo hướng khác, khiến thuật toán phải duyệt thêm nhiều đỉnh không cần thiết."),
        ("p", "Trên các bộ dữ liệu có vật cản, khoảng cách giữa các hàm ước lượng thu hẹp "
              "đáng kể vì cả bốn hàm đều trở nên lỏng hơn so với chi phí thực. Trên bộ dữ "
              "liệu vật cản ngẫu nhiên, số đỉnh duyệt của bốn hàm lần lượt là một trăm hai "
              "mươi bảy, bốn trăm chín mươi lăm, năm trăm linh tám và bốn trăm bảy mươi, "
              "tức là khoảng cách Manhattan vẫn tốt nhất nhưng mức chênh lệch chỉ còn "
              "khoảng bốn lần. Trên bộ dữ liệu địa hình trọng số, bốn hàm cho kết quả gần "
              "như bằng nhau vì trọng số địa hình lớn làm cho mọi ước lượng đều nhỏ hơn "
              "nhiều so với chi phí thực."),
        ("table_obj", ctx.get("tbl_tn_h", (
            "Bảng 4.8: Số đỉnh A* phải duyệt theo từng hàm ước lượng",
            ["Bộ dữ liệu", "Manhattan", "Euclid", "Chebyshev", "Octile"],
            [["chưa nạp", "", "", "", ""]], [4.0, 3.0, 3.0, 3.0, 3.0], (1, 2, 3, 4))),
        ),
        ("figure", "docs/figures/hinh_4_4_anh_huong_heuristic.png",
         "Hình 4.9: Số đỉnh A* phải duyệt theo từng hàm ước lượng, lưới 4 hướng", 15.5),
        ("p", "Kết luận rút ra từ thí nghiệm này gồm hai điểm. Thứ nhất, khi cấu hình di "
              "chuyển đã biết, hàm ước lượng khớp chính xác với chi phí thực là lựa chọn "
              "tốt nhất, do đó với lưới bốn hướng nên dùng khoảng cách Manhattan và với "
              "lưới tám hướng nên dùng khoảng cách octile. Thứ hai, khi bản đồ có nhiều vật "
              "cản hoặc có địa hình trọng số lớn, chênh lệch giữa các hàm ước lượng thu "
              "hẹp lại, nghĩa là lợi ích của việc chọn hàm ước lượng chặt không còn quyết "
              "định như trong trường hợp bản đồ thoáng."),

        ("h2", "4.8. Thí nghiệm 4: biến thể A* có trọng số"),
        ("p", "Thí nghiệm thứ tư khảo sát biến thể A* có trọng số bằng cách nhân thêm hệ "
              "số w lần lượt bằng một, một phẩy năm, hai và ba vào hàm ước lượng. Thí "
              "nghiệm được chạy trên bộ dữ liệu địa hình trọng số, là bộ dữ liệu bộc lộ rõ "
              "nhất sự đánh đổi giữa số đỉnh phải duyệt và chất lượng đường đi. Mỗi giá "
              "trị của w được chạy ở hai chế độ, chế độ cho phép mở lại đỉnh đã duyệt và "
              "chế độ khoá tập CLOSED."),
        ("p", "Kết quả trong Bảng 4.9 và Hình 4.10 cho thấy một hiện tượng thú vị. Khi w "
              "tăng lên một phẩy năm, số đỉnh duyệt giảm nhẹ từ một nghìn một trăm tám "
              "mươi bốn xuống một nghìn một trăm lẻ sáu đỉnh và chi phí đường đi vẫn giữ "
              "nguyên ở mức tối ưu. Khi w tăng lên hai và vẫn bật chế độ mở lại đỉnh, số "
              "đỉnh duyệt lại tăng vọt lên một nghìn ba trăm sáu mươi bốn, cao hơn cả "
              "trường hợp w bằng một. Nguyên nhân là giá trị ưu tiên không còn đơn điệu, "
              "khiến nhiều đỉnh bị mở lại và phải xét lại, làm phát sinh thêm công việc "
              "thay vì tiết kiệm công việc."),
        ("p", "Khi chuyển sang chế độ khoá tập CLOSED, bức tranh thay đổi hoàn toàn. Số "
              "đỉnh duyệt giảm mạnh và đơn điệu theo w, cụ thể là một nghìn một trăm tám "
              "mươi bốn, một nghìn không trăm lẻ một, sáu trăm bốn mươi và một trăm ba "
              "mươi sáu đỉnh cho bốn giá trị của w. Đổi lại, chi phí đường đi tăng dần và "
              "vượt khỏi mức tối ưu: ở w bằng hai chi phí là một trăm ba mươi bốn, ở w "
              "bằng ba chi phí là một trăm bốn mươi lăm, tức là cao hơn mức tối ưu một "
              "trăm hai mươi tám khoảng mười ba phần trăm."),
        ("table_obj", ctx.get("tbl_tn_w", (
            "Bảng 4.9: Kết quả khảo sát biến thể A* có trọng số",
            ["Bộ dữ liệu", "w", "Mở lại", "Chi phí", "Ô", "Duyệt", "Sinh", "OPEN max",
             "Thời gian (ms)", "Tối ưu"],
            [["chưa nạp", "", "", "", "", "", "", "", "", ""]],
            [2.2, 1.2, 1.4, 1.4, 0.9, 1.3, 1.2, 1.4, 1.8, 1.2], (1, 2, 3, 4, 5, 6, 7, 8, 9))),
        ),
        ("figure", "docs/figures/hinh_4_5_weighted_astar.png",
         "Hình 4.10: Đánh đổi giữa số đỉnh đã duyệt và chi phí đường đi theo trọng số w",
         15.5),
        ("p", "Từ thí nghiệm này có thể rút ra hai kết luận có giá trị thực tiễn. Thứ nhất, "
              "biến thể A* có trọng số chỉ thực sự tiết kiệm công việc khi tập CLOSED được "
              "khoá. Nếu vẫn cho phép mở lại đỉnh, việc tăng trọng số có thể phản tác dụng "
              "trên các lưới có trọng số địa hình. Thứ hai, việc tăng trọng số là một cách "
              "đánh đổi có kiểm soát: người thiết kế có thể chọn mức w phù hợp với ngân "
              "sách thời gian của ứng dụng, chấp nhận đường đi dài hơn một chút để có kết "
              "quả nhanh hơn nhiều. Trong ứng dụng mô phỏng đám đông hoặc trò chơi điện "
              "tử, mức đánh đổi này thường được chấp nhận để giữ khung hình ổn định."),

        ("h2", "4.9. Thí nghiệm 5: ảnh hưởng của cấu hình bốn hướng và tám hướng"),
        ("p", "Thí nghiệm thứ năm giữ nguyên thuật toán A* và bộ dữ liệu, chỉ thay đổi cấu "
              "hình di chuyển giữa bốn hướng và tám hướng. Khi chuyển sang tám hướng, "
              "chi phí của bước chéo được đặt bằng căn bậc hai của hai và hàm ước lượng "
              "được đổi từ khoảng cách Manhattan sang khoảng cách octile để giữ tính khả "
              "dụng. Thí nghiệm được chạy trên ba bộ dữ liệu là vật cản ngẫu nhiên, địa "
              "hình trọng số và mê cung."),
        ("p", "Kết quả trong Bảng 4.10 và Hình 4.11 cho thấy cấu hình tám hướng làm giảm "
              "cả chi phí đường đi lẫn số bước đi trên hai bộ dữ liệu có không gian mở. "
              "Trên bộ dữ liệu vật cản ngẫu nhiên, chi phí giảm từ sáu mươi chín xuống "
              "sáu mươi phẩy hai mươi mốt và số bước giảm từ sáu mươi chín xuống năm mươi "
              "bốn. Trên bộ dữ liệu địa hình trọng số, chi phí giảm từ một trăm hai mươi "
              "tám xuống một trăm linh tám phẩy tám bốn mươi mốt và số bước giảm từ bảy "
              "mươi mốt xuống năm mươi ba. Trên bộ dữ liệu mê cung, hai cấu hình cho kết "
              "quả hoàn toàn giống nhau vì hành lang của mê cung chỉ cho phép đi theo bốn "
              "hướng."),
        ("p", "Song song với việc giảm chi phí, cấu hình tám hướng làm tăng số đỉnh phải "
              "duyệt. Trên bộ dữ liệu vật cản ngẫu nhiên, số đỉnh duyệt tăng từ một trăm "
              "hai mươi bảy lên ba trăm lẻ năm, tức là tăng hơn hai lần. Nguyên nhân là hệ "
              "số phân nhánh tăng từ bốn lên tám, do đó với mỗi đỉnh được duyệt, thuật "
              "toán phải sinh và kiểm tra gấp đôi số đỉnh kề. Kết quả này cho thấy việc "
              "cho phép đi chéo là một quyết định thiết kế có hai mặt, cần cân nhắc theo "
              "yêu cầu cụ thể của ứng dụng."),
        ("table_obj", ctx.get("tbl_tn_8", (
            "Bảng 4.10: Kết quả so sánh cấu hình bốn hướng và tám hướng",
            ["Bộ dữ liệu", "Cấu hình", "h(n)", "Chi phí", "Ô", "Bước", "Duyệt", "Sinh",
             "Thời gian (ms)", "Tối ưu"],
            [["chưa nạp", "", "", "", "", "", "", "", "", ""]],
            [2.2, 1.8, 1.8, 1.4, 0.9, 1.0, 1.3, 1.2, 1.8, 1.2],
            (1, 2, 3, 4, 5, 6, 7, 8, 9))),
        ),
        ("figure", "docs/figures/hinh_4_6_4_huong_8_huong.png",
         "Hình 4.11: Ảnh hưởng của việc cho phép đi chéo tới chi phí và số bước đi", 15.5),

        ("h2", "4.10. Phân tích tổng hợp và độ tin cậy của số liệu"),
        ("p", "Kết quả của năm nhóm thí nghiệm cho phép rút ra bốn nhận định tổng hợp. "
              "Nhận định thứ nhất là A* đạt được mức giảm số đỉnh duyệt rất lớn so với "
              "tìm kiếm theo chi phí đều trên các bản đồ không phải hành lang đơn tuyến, "
              "trong khi chất lượng đường đi hoàn toàn không suy giảm. Nhận định thứ hai "
              "là lợi ích đó phụ thuộc vào cấu trúc của bản đồ, và trở nên bằng không trên "
              "các bản đồ chỉ có một lối đi duy nhất. Nhận định thứ ba là hàm ước lượng "
              "cần được chọn phù hợp với cấu hình di chuyển, nếu không sẽ mất tính tối ưu "
              "hoặc mất phần lớn lợi ích về số đỉnh duyệt."),
        ("p", f"Nhận định thứ tư liên quan tới mức giảm trung bình. Tính trên sáu bộ dữ "
              f"liệu, số đỉnh mà A* phải duyệt trung bình bằng khoảng "
              f"{n.get('share_pct', 54)} phần trăm số đỉnh của tìm kiếm theo chi phí đều. "
              "Chỉ số này bị chi phối mạnh bởi bộ dữ liệu hành lang xoắn ốc, nơi A* không "
              "thể giảm được đỉnh nào vì chỉ tồn tại một lối đi. Nếu loại bộ dữ liệu đặc "
              "biệt này ra khỏi phép tính, tỉ lệ trên giảm xuống còn khoảng "
              f"{n.get('share_pct_no_spiral', 45)} phần trăm. Việc báo cáo cả hai con số "
              "giúp tránh kết luận sai lệch do một bộ dữ liệu bất thường gây ra."),
        ("p", "Về độ tin cậy của số liệu, có ba điểm cần được nêu rõ để người đọc đánh "
              "giá đúng các bảng và biểu đồ trong chương này. Thứ nhất, số đo thời gian "
              "trong các bảng thí nghiệm là thời gian bộ máy tìm kiếm chạy, không bao gồm "
              "thời gian vẽ lên màn hình. Số hiển thị trên giao diện ở Hình 4.3 và Hình "
              "4.4 cũng được tính theo nguyên tắc tương tự, chỉ cộng thời gian thực thi "
              "của bộ máy tìm kiếm và loại bỏ thời gian giao diện chờ giữa các bước, do đó "
              "không bị phóng đại khi mô phỏng chậm."),
        ("p", "Thứ hai, các phép đo với mỗi cấu hình chỉ được thực hiện một lần cho mỗi bộ "
              "dữ liệu. Vì mọi bộ dữ liệu đều được sinh xác định theo hạt giống ngẫu nhiên "
              "cố định và thuật toán không dùng yếu tố ngẫu nhiên trong khi duyệt, kết quả "
              "lặp lại được tuyệt đối về số đỉnh duyệt, số đỉnh sinh và đường đi. Chỉ số "
              "thời gian có dao động giữa các lần chạy do ảnh hưởng của hệ điều hành, "
              "nhưng mức dao động nhỏ so với sự khác biệt giữa các thuật toán. Thứ ba, "
              "chi phí đường đi được tính bằng hàm tính chi phí trên chính đường đi trả "
              "về, không lấy từ giá trị ưu tiên của hàng đợi, do đó loại trừ được khả năng "
              "báo nhầm chi phí khi thuật toán bỏ qua trọng số địa hình như trường hợp tìm "
              "kiếm theo chiều rộng."),
    ]
    return blocks


# ====================================================================== #
# CHƯƠNG 5
# ====================================================================== #
def chapter5(ctx: dict) -> list[tuple]:
    return [
        ("h1", "CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN"),

        ("h2", "5.1. Kết quả đã đạt được"),
        ("p", "Đối chiếu với mục tiêu đặt ra ở mục 1.5, đề tài đã hoàn thành cả bốn nhóm "
              "công việc. Về mặt lý thuyết, báo cáo đã trình bày đầy đủ cơ sở của thuật "
              "toán A* gồm mô hình đồ thị của lưới, định nghĩa hàm ưu tiên, điều kiện khả "
              "dụng và nhất quán của hàm ước lượng, chứng minh tính tối ưu, phân tích độ "
              "phức tạp thời gian và bộ nhớ, cùng nhận xét về phạm vi hiệu quả của thuật "
              "toán. Các nội dung này tạo nền tảng để giải thích mọi kết quả đo đạc ở "
              "Chương 4."),
        ("p", "Về mặt cài đặt, đề tài đã xây dựng được một chương trình hoàn chỉnh gồm thư "
              "viện tìm kiếm độc lập, giao diện đồ hoạ cho phép chỉnh sửa bản đồ và quan "
              "sát quá trình tìm kiếm theo từng bước, kịch bản thực nghiệm tự động và bộ "
              "kiểm thử gồm hai mươi tám ca. Chương trình chạy được ở cả hai chế độ dòng "
              "lệnh và giao diện, chỉ dùng thư viện chuẩn của Python nên không cần bước "
              "cài đặt thêm gói phụ thuộc."),
        ("p", "Về mặt dữ liệu và thực nghiệm, đề tài đã xây dựng sáu bộ dữ liệu mẫu bao "
              "phủ các cấu trúc bản đồ khác nhau và thực hiện năm nhóm thí nghiệm đo đạc "
              "có định lượng. Kết quả thực nghiệm đã kiểm chứng được ba kết luận lý thuyết "
              "quan trọng gồm tính tối ưu của A* khi hàm ước lượng khả dụng, ảnh hưởng của "
              "độ chặt hàm ước lượng tới số đỉnh phải duyệt, và sự đánh đổi giữa tốc độ và "
              "chất lượng đường đi trong biến thể A* có trọng số."),
        ("p", "Về mặt minh chứng, toàn bộ số liệu dùng để viết báo cáo đều do chương trình "
              "sinh ra và được lưu lại dưới dạng tệp CSV, JSON, Markdown và HTML trong thư "
              "mục kết quả của đề tài. Nhờ vậy, mọi bảng và biểu đồ trong báo cáo đều có "
              "thể kiểm chứng lại bằng cách chạy lại kịch bản thực nghiệm, đây là điểm "
              "được đặc biệt chú trọng để đảm bảo tính trung thực của báo cáo."),

        ("h2", "5.2. Hạn chế của đề tài"),
        ("p", "Hạn chế thứ nhất là phạm vi không gian tìm kiếm còn nhỏ. Các bộ dữ liệu mẫu "
              "có kích thước tối đa sáu mươi nhân ba mươi ô, do đó các vấn đề về bộ nhớ "
              "của A* chưa bộc lộ. Trên các bài toán thực tế với bản đồ hàng triệu ô, chi "
              "phí bộ nhớ của tập OPEN và tập CLOSED sẽ là yếu tố giới hạn chính, và báo "
              "cáo chưa có số liệu thực nghiệm cho tình huống này."),
        ("p", "Hạn chế thứ hai là đề tài chưa xét bản đồ thay đổi theo thời gian. Trong "
              "các ứng dụng như robot tự hành, bản đồ có thể được cập nhật trong lúc di "
              "chuyển và đường đi phải được tính lại cục bộ. Việc cài đặt một thuật toán "
              "tìm kiếm gia tăng như D* Lite và so sánh với việc chạy lại A* từ đầu là một "
              "hướng nghiên cứu tự nhiên nhưng nằm ngoài phạm vi đã đăng ký của đề tài."),
        ("p", "Hạn chế thứ ba là các phép đo thời gian chỉ được thực hiện một lần cho mỗi "
              "cấu hình nên chưa có phân tích thống kê về phương sai. Mặc dù kết quả về số "
              "đỉnh duyệt và đường đi lặp lại được tuyệt đối, các kết luận về thời gian chỉ "
              "nên được hiểu là so sánh tương đối giữa các thuật toán chứ không phải là "
              "thông số tuyệt đối cho một cấu hình phần cứng cụ thể. Hạn chế thứ tư là "
              "giao diện chỉ chạy trên nền tảng có Tkinter, và việc mô phỏng trên lưới quá "
              "lớn sẽ làm tốc độ vẽ chậm đi đáng kể dù bộ máy tìm kiếm vẫn nhanh."),

        ("h2", "5.3. Hướng phát triển"),
        ("p", "Hướng phát triển thứ nhất là cài đặt thêm các biến thể tối ưu chuyên biệt cho "
              "lưới như tìm kiếm theo bước nhảy Jump Point Search và A* phân cấp, rồi so "
              "sánh trực tiếp với A* trên cùng bộ dữ liệu. Đây là hướng phát triển có giá "
              "trị học thuật cao vì cho phép định lượng thêm lợi ích của việc khai thác "
              "cấu trúc đều đặn của lưới. Hướng thứ hai là bổ sung tìm kiếm gia tăng cho "
              "bản đồ động, trong đó người dùng có thể thêm hoặc bỏ tường và quan sát "
              "chương trình cập nhật lại đường đi một cách cục bộ."),
        ("p", "Hướng phát triển thứ ba là mở rộng không gian tìm kiếm lên ba chiều dạng "
              "khối lập phương rời rạc, áp dụng cho bài toán lập kế hoạch bay của thiết bị "
              "bay không người lái hoặc di chuyển trong nhà nhiều tầng. Hướng thứ tư là "
              "tăng cường khả năng trực quan hoá bằng cách hiển thị bản đồ nhiệt của giá "
              "trị f và số lần mở lại đỉnh, giúp người học thấy được ảnh hưởng của việc "
              "chọn hàm ước lượng tới từng ô trên lưới."),
        ("p", "Hướng phát triển thứ năm là bổ sung chế độ so sánh nhiều thuật toán trên "
              "cùng một khung hình với thanh tiến trình đồng bộ, và chế độ xuất video mô "
              "phỏng để phục vụ thuyết trình. Hướng thứ sáu là đóng gói chương trình thành "
              "ứng dụng chạy độc lập để người dùng không cần cài Python, cùng với tài liệu "
              "hướng dẫn sử dụng ngắn gọn đi kèm."),
    ]


# ====================================================================== #
# TÀI LIỆU THAM KHẢO
# ====================================================================== #
def references(ctx: dict) -> list[tuple]:
    refs = [
        "Hart, P. E., Nilsson, N. J., Raphael, B. (1968). A Formal Basis for the Heuristic "
        "Determination of Minimum Cost Paths. IEEE Transactions on Systems Science and "
        "Cybernetics, 4(2), 100-107.",
        "Russell, S., Norvig, P. (2021). Artificial Intelligence: A Modern Approach, "
        "Fourth Edition. Pearson.",
        "Dechter, R., Pearl, J. (1985). Generalized Best-First Search Strategies and the "
        "Optimality of A*. Journal of the ACM, 32(3), 505-536.",
        "Dijkstra, E. W. (1959). A Note on Two Problems in Connexion with Graphs. "
        "Numerische Mathematik, 1, 269-271.",
        "Hart, P. E., Nilsson, N. J., Raphael, B. (1972). Correction to A Formal Basis for "
        "the Heuristic Determination of Minimum Cost Paths. SIGART Newsletter, 37, 28-29.",
        "Patel, A. (n.d.). Red Blob Games: Introduction to A* Pathfinding. "
        "Tài liệu trực tuyến, truy cập tháng 10 năm 2026.",
        "Koenig, S., Likhachev, M. (2002). D* Lite. Proceedings of the AAAI Conference on "
        "Artificial Intelligence, 476-483.",
        "Harabor, D., Grastien, A. (2011). Online Graph Pruning for Pathfinding on Grid "
        "Maps. Proceedings of the AAAI Conference on Artificial Intelligence, 1114-1119.",
        "Python Software Foundation (2026). The Python Standard Library: heapq, math, "
        "deque, unittest. Tài liệu trực tuyến, truy cập tháng 10 năm 2026.",
        "Python Software Foundation (2026). Tkinter: Python interface to Tcl/Tk. "
        "Tài liệu trực tuyến, truy cập tháng 10 năm 2026.",
        "Cormen, T. H., Leiserson, C. E., Rivest, R. L., Stein, C. (2022). Introduction to "
        "Algorithms, Fourth Edition. MIT Press.",
        "Cài đặt mẫu A* trên Wikipedia tiếng Anh, mục A* search algorithm, phiên bản tháng "
        "9 năm 2026. Tài liệu trực tuyến, dùng để đối chiếu mã giả.",
    ]
    blocks: list[tuple] = [("h1", "TÀI LIỆU THAM KHẢO")]
    for i, r in enumerate(refs, start=1):
        blocks.append(("ref", f"[{i}] {r}"))
    return blocks


# ====================================================================== #
# PHỤ LỤC A
# ====================================================================== #
def appendix(ctx: dict) -> list[tuple]:
    return [
        ("h1", "PHỤ LỤC A: MÃ NGUỒN CỐT LÕI"),
        ("p", "Phụ lục này trích hai phần mã nguồn quan trọng nhất của chương trình: hàm "
              "tìm kiếm của bộ máy A* và phần cập nhật trạng thái tìm kiếm của giao diện. "
              "Mã nguồn được trích nguyên văn từ tệp trong thư mục dự án, chỉ lược bỏ các "
              "phần xử lý giao diện không liên quan trực tiếp tới thuật toán."),

        ("h2", "A.1. Hàm tìm kiếm của bộ máy A*, UCS, Greedy và BFS"),
        ("code_file", "astar/search.py"),

        ("h2", "A.2. Phần cập nhật trạng thái mô phỏng của giao diện"),
        ("code_file", "gui_excerpt"),

        ("h2", "A.3. Cách chạy chương trình"),
        ("p", "Chương trình gồm bốn điểm vào được gom trong tệp main.py. Lệnh không kèm "
              "tham số sẽ mở giao diện đồ hoạ. Lệnh với tham số demo chạy một ví dụ và in "
              "lưới cùng đường đi ra màn hình dòng lệnh. Lệnh với tham số exp chạy toàn bộ "
              "thực nghiệm và ghi kết quả vào thư mục kết quả. Lệnh với tham số test chạy "
              "bộ kiểm thử tự động và in kết quả từng ca."),
        ("code_text", "python main.py          # mở giao diện mô phỏng\n"
                      "python main.py demo     # chạy ví dụ và in lưới ra console\n"
                      "python main.py exp      # chạy thực nghiệm, xuất results/\n"
                      "python main.py test     # chạy 28 ca kiểm thử tự động\n"
                      "python main.py info     # xem thông tin môi trường và dữ liệu mẫu"),
    ]
