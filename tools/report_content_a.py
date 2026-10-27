"""
report_content_a.py - Nội dung phần đầu, Chương 1 và Chương 2 của báo cáo BTL.

Mỗi hàm trả về danh sách khối nội dung (block) để build_report.py dựng thành DOCX.
Quy ước văn phong: văn xuôi tiếng Việt, không dùng gạch dài, không bôi đậm trong
thân bài, hạn chế gạch đầu dòng, không dùng từ sáo rỗng.
"""

from __future__ import annotations

# ====================================================================== #
# PHẦN ĐẦU
# ====================================================================== #
def front_matter(ctx: dict) -> list[tuple]:
    return [
        ("h1", "LỜI NÓI ĐẦU"),
        ("p", "Bài toán tìm đường trên lưới là một trong những bài toán kinh điển của "
              "khoa học máy tính, xuất hiện ở hầu hết các hệ thống có yếu tố di chuyển "
              "trong không gian rời rạc như trò chơi điện tử, robot tự hành, phần mềm "
              "chỉ đường, mô phỏng giao thông hay điều phối xe tự động trong kho hàng. "
              "Đặc điểm chung của nhóm bài toán này là không gian tìm kiếm lớn, yêu cầu "
              "thời gian phản hồi ngắn và đòi hỏi đường đi tìm được phải đúng, hợp lệ và "
              "tốt nhất theo một tiêu chí chi phí nào đó."),
        ("p", "Thuật toán A* do Hart, Nilsson và Raphael công bố năm 1968 là lời giải "
              "được sử dụng rộng rãi nhất cho nhóm bài toán nêu trên. Điểm cốt lõi của "
              "A* là việc đánh giá mỗi đỉnh bằng hàm ưu tiên f(n) = g(n) + h(n), trong "
              "đó g(n) là chi phí thực đã bỏ ra để đi từ đỉnh xuất phát tới n, còn h(n) "
              "là ước lượng chi phí từ n tới đích. Nhờ thành phần h(n), A* tập trung tìm "
              "kiếm về phía có khả năng chứa lời giải thay vì lan ra mọi hướng như tìm "
              "kiếm theo chiều rộng, và vẫn giữ được tính tối ưu khi h(n) thỏa mãn điều "
              "kiện khả dụng."),
        ("p", "Trong khuôn khổ học phần Kĩ thuật lập trình nâng cao, em chọn Đề tài 48 với "
              "nội dung mô phỏng thuật toán A* trong bài toán tìm đường trên lưới. Mục "
              "tiêu của đề tài không dừng ở việc cài đặt một hàm tìm đường cho ra kết quả "
              "đúng, mà còn phải làm rõ cơ sở lý thuyết của thuật toán, phân tích độ "
              "phức tạp, so sánh với các thuật toán đối chứng, và quan trọng nhất là xây "
              "dựng một chương trình hoàn chỉnh có giao diện cho phép quan sát trực quan "
              "từng bước mà thuật toán thực hiện."),
        ("p", "Chương trình được cài đặt bằng ngôn ngữ Python, chỉ sử dụng thư viện chuẩn, "
              "trong đó giao diện đồ hoạ dùng Tkinter. Bộ máy tìm kiếm được thiết kế theo "
              "hướng phát sự kiện, cho phép giao diện hiển thị tập đỉnh đang chờ, tập đỉnh "
              "đã duyệt và đường đi cuối cùng theo thời gian thực. Toàn bộ số liệu dùng "
              "cho phần thực nghiệm của báo cáo do chính chương trình sinh ra và được lưu "
              "lại thành tệp CSV, JSON, HTML để có thể kiểm chứng lại."),
        ("p", "Nội dung báo cáo gồm năm chương. Chương 1 trình bày bối cảnh, phát biểu bài "
              "toán, khảo sát các giải pháp hiện hành và xác định mục tiêu, phạm vi của "
              "đề tài. Chương 2 trình bày cơ sở lý thuyết về không gian trạng thái, các "
              "hàm ước lượng h(n), thuật toán A*, chứng minh tính tối ưu và phân tích độ "
              "phức tạp. Chương 3 trình bày phân tích thiết kế chương trình gồm kiến trúc "
              "phân tầng, sơ đồ lớp, cấu trúc dữ liệu lưới và thiết kế giao diện. Chương 4 "
              "trình bày việc cài đặt, các kịch bản kiểm thử và năm nhóm thí nghiệm đo "
              "đạc kèm phân tích kết quả. Chương 5 tổng kết kết quả đạt được, nêu hạn chế "
              "và đề xuất hướng phát triển."),
        ("p", "Trong quá trình thực hiện, em đã cố gắng vận dụng kiến thức của học phần vào "
              "từng bước của đề tài, từ việc lựa chọn cấu trúc dữ liệu, phân tích độ phức "
              "tạp, đến việc kiểm chứng kết quả bằng thực nghiệm. Do kiến thức và thời gian "
              "còn hạn chế, báo cáo khó tránh khỏi thiếu sót, em rất mong nhận được ý kiến "
              "góp ý của thầy để hoàn thiện hơn."),

        ("h1", "DANH MỤC THUẬT NGỮ VÀ TỪ VIẾT TẮT"),
        ("p", "Bảng dưới đây liệt kê các thuật ngữ và từ viết tắt được sử dụng thống nhất "
              "trong toàn bộ báo cáo. Các thuật ngữ tiếng Anh chuyên ngành được giữ nguyên "
              "ở dạng gốc và giải thích nghĩa tiếng Việt ở lần xuất hiện đầu tiên."),
        ("table", "Bảng 0.1: Danh mục thuật ngữ và từ viết tắt dùng trong báo cáo",
         ["Thuật ngữ", "Giải thích"],
         [
             ["A*", "Thuật toán tìm kiếm có thông tin dùng hàm ưu tiên f(n) = g(n) + h(n)"],
             ["BFS", "Breadth First Search, tìm kiếm theo chiều rộng, mọi bước cùng chi phí 1"],
             ["UCS", "Uniform Cost Search, tìm kiếm theo chi phí đều, tương đương Dijkstra"],
             ["GBFS", "Greedy Best First Search, tìm kiếm tham lam chỉ dựa vào h(n)"],
             ["OPEN", "Tập đỉnh đã sinh nhưng chưa duyệt, còn gọi là biên tìm kiếm (frontier)"],
             ["CLOSED", "Tập đỉnh đã được lấy ra và xét xong"],
             ["g(n)", "Chi phí thực tế nhỏ nhất tạm thời từ đỉnh xuất phát tới n"],
             ["h(n)", "Hàm ước lượng chi phí từ n tới đích, còn gọi là heuristic"],
             ["f(n)", "Giá trị ưu tiên của đỉnh n trong hàng đợi, f(n) = g(n) + w.h(n)"],
             ["w", "Trọng số nhân vào h(n) trong biến thể weighted A*, mặc định bằng 1"],
             ["Khả dụng", "Tính chất h(n) không ước lượng vượt quá chi phí thực tới đích"],
             ["Nhất quán", "Tính chất h(n) thỏa bất đẳng thức tam giác giữa hai đỉnh kề"],
             ["Lưới", "Đồ thị rời rạc hai chiều, mỗi ô là một đỉnh, có 4 hoặc 8 ô kề"],
             ["Ô kề", "Ô lân cận theo 4 hướng hoặc 8 hướng của một ô"],
             ["Cắt góc", "Hành vi cho phép đi chéo xuyên qua khe hở giữa hai ô tường"],
             ["GUI", "Graphical User Interface, giao diện đồ hoạ người dùng"],
             ["CSV", "Comma Separated Values, định dạng tệp văn bản phân tách bằng dấu"],
             ["BTL", "Bài tập lớn"],
             ["TNUT", "Trường Đại học Kỹ thuật Công nghiệp Thái Nguyên"],
         ],
         [3.6, 11.9]),
        ("p", "Ngoài các thuật ngữ trên, báo cáo dùng thống nhất đơn vị chi phí không có "
              "thứ nguyên. Một bước đi sang ô kề theo bốn hướng có chi phí bằng trọng số "
              "của ô được đi vào. Một bước đi chéo có chi phí bằng căn bậc hai của hai "
              "nhân với trọng số của ô được đi vào, phản ánh đúng tỉ lệ khoảng cách hình "
              "học giữa cạnh và đường chéo của hình vuông đơn vị."),

        ("h1", "MỤC LỤC"),
        ("toc", r'TOC \o "1-3" \h \z \u'),

        ("h1", "DANH MỤC BẢNG BIỂU"),
        ("tot", r'TOC \h \z \c "Bảng"'),

        ("h1", "DANH MỤC HÌNH ẢNH"),
        ("tof", r'TOC \h \z \c "Hình"'),
    ]


# ====================================================================== #
# CHƯƠNG 1
# ====================================================================== #
def chapter1(ctx: dict) -> list[tuple]:
    return [
        ("h1", "CHƯƠNG 1: TỔNG QUAN VÀ PHÁT BIỂU BÀI TOÁN"),

        ("h2", "1.1. Bối cảnh của bài toán tìm đường trên lưới"),
        ("p", "Tìm đường là bài toán xuất hiện mỗi khi một tác nhân cần di chuyển từ một "
              "vị trí ban đầu tới một vị trí đích trong một không gian có chướng ngại. "
              "Trong thực tế, không gian đó có thể là mặt bằng của một nhà kho, mạng lưới "
              "đường phố của một thành phố, bản đồ của một màn chơi điện tử, hay vùng làm "
              "việc của một cánh tay robot. Điểm chung của các không gian này là chúng đều "
              "được rời rạc hoá thành các đơn vị nhỏ, và việc rời rạc hoá như vậy dẫn trực "
              "tiếp tới mô hình lưới hai chiều với mỗi ô là một trạng thái."),
        ("p", "Mô hình lưới có nhiều ưu điểm về mặt kĩ thuật. Thứ nhất, việc xác định các ô "
              "kề của một ô chỉ cần cộng trừ toạ độ theo một bảng hướng cố định, nhờ đó "
              "không cần lưu trữ danh sách cạnh tường minh như với đồ thị tổng quát. Thứ "
              "hai, lưới cho phép gán thêm trọng số cho từng ô để mô tả địa hình có chi "
              "phí di chuyển khác nhau như đường nhựa, bãi cỏ, cát lún hay bùn lầy. Thứ "
              "ba, kết quả tìm kiếm trên lưới rất dễ trực quan hoá, điều này đặc biệt phù "
              "hợp với mục tiêu mô phỏng của đề tài."),
        ("p", "Trong bối cảnh học tập, yêu cầu tìm đường trên lưới còn là ví dụ gọn gàng "
              "để minh hoạ mối quan hệ giữa ba nhóm thuật toán duyệt đồ thị cơ bản. Tìm "
              "kiếm theo chiều rộng tối ưu khi mọi bước đi có cùng chi phí. Tìm kiếm theo "
              "chi phí đều tối ưu khi các bước đi có chi phí khác nhau nhưng phải duyệt "
              "theo mọi hướng. A* giữ được tính tối ưu của tìm kiếm theo chi phí đều trong "
              "khi định hướng tìm kiếm về phía đích nhờ hàm ước lượng. Việc đặt ba thuật "
              "toán cạnh nhau trên cùng một bộ dữ liệu cho phép định lượng rõ ràng lợi ích "
              "mà tri thức đặc thù của bài toán mang lại."),

        ("h2", "1.2. Phát biểu bài toán và các ký hiệu"),
        ("p", "Bài toán được phát biểu như sau. Cho một lưới chữ nhật gồm H hàng và W cột. "
              "Mỗi ô được xác định bằng cặp toạ độ (r, c) với r là chỉ số hàng và c là chỉ "
              "số cột. Mỗi ô có một trọng số w(r, c) là chi phí để đi vào ô đó. Ô bị chặn, "
              "còn gọi là tường, được biểu diễn bằng trọng số vô cùng. Hai ô được gọi là "
              "kề nhau nếu toạ độ của chúng khác nhau không quá một đơn vị trên mỗi trục, "
              "trong đó cấu hình bốn hướng chỉ xét các ô kề cạnh còn cấu hình tám hướng "
              "xét thêm các ô kề góc."),
        ("p", "Cho một ô xuất phát S và một ô đích G, yêu cầu của bài toán là tìm một dãy "
              "ô liên tiếp S = n0, n1, ..., nk = G sao cho mỗi cặp ô liên tiếp đều kề nhau, "
              "không ô nào là tường, và tổng chi phí của dãy là nhỏ nhất có thể. Chi phí "
              "của một bước đi từ ô a sang ô b được tính bằng hệ số khoảng cách của bước "
              "đi nhân với trọng số của ô đích b. Hệ số khoảng cách bằng một khi bước đi "
              "theo bốn hướng và bằng căn bậc hai của hai khi bước đi chéo. Trường hợp "
              "không tồn tại dãy nào thoả mãn các điều kiện trên, chương trình phải kết "
              "luận rõ ràng rằng không có đường đi."),
        ("p", "Bảng 1.1 tổng hợp các ký hiệu được dùng xuyên suốt báo cáo. Việc cố định "
              "ký hiệu ngay từ đầu giúp các công thức ở Chương 2 và các bảng số liệu ở "
              "Chương 4 luôn được hiểu theo cùng một nghĩa."),
        ("table", "Bảng 1.1: Các ký hiệu dùng trong báo cáo",
         ["Ký hiệu", "Ý nghĩa", "Mặc định"],
         [
             ["H, W", "Số hàng và số cột của lưới", "25 và 40"],
             ["(r, c)", "Toạ độ của một ô, r là hàng, c là cột", "gốc ở góc trên trái"],
             ["S, G", "Ô xuất phát và ô đích", "góc dưới trái và góc trên phải"],
             ["w(r, c)", "Trọng số của ô, chi phí để đi vào ô đó", "1,0; ô tường bằng vô cùng"],
             ["c(a, b)", "Chi phí của một bước đi từ ô a sang ô b", "1,0 hoặc căn hai của hai"],
             ["g(n)", "Chi phí thực nhỏ nhất tạm thời từ S tới n", "khởi tạo bằng vô cùng"],
             ["h(n)", "Hàm ước lượng chi phí từ n tới G", "chọn trong bảng 2.1"],
             ["f(n)", "Giá trị ưu tiên dùng xếp hàng đợi", "g(n) cộng w nhân h(n)"],
             ["b", "Hệ số phân nhánh, số ô kề trung bình", "4 hoặc 8 theo cấu hình"],
             ["d", "Độ sâu của lời giải, số bước trên đường đi tối ưu", "tuỳ bộ dữ liệu"],
         ],
         [2.3, 8.4, 4.8]),
        ("p", "Với cách phát biểu trên, lưới được xem như một đồ thị có hướng với tập đỉnh "
              "là các ô đi được và tập cạnh là các cặp ô kề hợp lệ. Trọng số của cạnh phụ "
              "thuộc vào hướng đi và trọng số của ô đích, do đó đồ thị có trọng số không "
              "âm. Tính chất không âm này là điều kiện để các thuật toán tìm kiếm theo chi "
              "phí và A* cho kết quả tối ưu."),

        ("h2", "1.3. Khảo sát các giải pháp hiện hành"),
        ("p", "Trước khi cài đặt, em đã khảo sát bốn nhóm giải pháp thường được dùng cho "
              "bài toán tìm đường trên lưới. Nhóm thứ nhất là tìm kiếm không có thông tin "
              "gồm tìm kiếm theo chiều rộng và tìm kiếm theo chi phí đều hay còn gọi là "
              "Dijkstra. Hai thuật toán này đảm bảo tìm được đường đi tốt nhất theo tiêu "
              "chí chi phí tương ứng nhưng không sử dụng bất kì hiểu biết nào về vị trí "
              "của đích, vì vậy chúng lan ra theo mọi hướng và duyệt số đỉnh xấp xỉ diện "
              "tích của vùng liên thông chứa đỉnh xuất phát."),
        ("p", "Nhóm thứ hai là tìm kiếm tham lam, đại diện là Greedy Best First Search. "
              "Thuật toán này chỉ dùng h(n) để quyết định đỉnh nào được xét tiếp, nhờ đó "
              "tốc độ rất nhanh trên nhiều bản đồ nhưng không có bảo đảm về chất lượng "
              "đường đi. Trên các bản đồ có vật cản dạng phòng kín hoặc hành lang quanh "
              "co, thuật toán này dễ bị hút vào một hướng cụt và buộc phải quay lại với "
              "chi phí lớn hơn mức tối ưu."),
        ("p", "Nhóm thứ ba là tìm kiếm có thông tin, đại diện là A*. Thuật toán kết hợp "
              "chi phí đã bỏ ra với ước lượng chi phí còn lại, nhờ đó vừa giữ được tính "
              "tối ưu khi hàm ước lượng khả dụng, vừa giảm mạnh số đỉnh phải duyệt so với "
              "tìm kiếm theo chi phí đều. Biến thể weighted A* nhân thêm trọng số lớn hơn "
              "một vào h(n) để đổi chất lượng đường đi lấy tốc độ, phù hợp với các ứng "
              "dụng cần phản hồi nhanh."),
        ("p", "Nhóm thứ tư là các kĩ thuật tối ưu chuyên biệt cho lưới như tìm kiếm theo "
              "bước nhảy Jump Point Search, tìm kiếm A* phân cấp cho bản đồ lớn, và các "
              "thuật toán tìm kiếm gia tăng như D* Lite dùng khi bản đồ thay đổi trong lúc "
              "di chuyển. Các kĩ thuật này cho hiệu năng cao hơn nhưng phụ thuộc vào giả "
              "thiết rất cụ thể về dữ liệu, chẳng hạn lưới phải đồng nhất về chi phí hoặc "
              "phải có cấu trúc phân cấp sẵn. Bảng 1.2 tóm tắt ưu điểm và hạn chế của "
              "từng nhóm."),
        ("table", "Bảng 1.2: So sánh ưu, nhược điểm của các nhóm giải pháp tìm đường trên lưới",
         ["Nhóm giải pháp", "Ưu điểm", "Hạn chế"],
         [
             ["Tìm kiếm theo chiều rộng", "Đơn giản, đúng đắn, tối ưu theo số bước",
              "Chỉ đúng khi mọi bước cùng chi phí, duyệt rất nhiều đỉnh"],
             ["Tìm kiếm theo chi phí đều (Dijkstra)", "Tối ưu với trọng số không âm, ổn định",
              "Không định hướng, duyệt gần như toàn bộ vùng liên thông"],
             ["Greedy Best First", "Nhanh, ít bộ nhớ, dễ cài đặt",
              "Không bảo đảm tối ưu, chất lượng đường đi dao động mạnh"],
             ["A* và weighted A*", "Tối ưu khi h khả dụng, giảm mạnh số đỉnh duyệt",
              "Chất lượng phụ thuộc h, bộ nhớ tăng theo số đỉnh sinh"],
             ["Jump Point Search, A* phân cấp", "Rất nhanh trên lưới lớn, đồng nhất",
              "Giả thiết chặt về dữ liệu, cài đặt phức tạp"],
             ["D* Lite và A* gia tăng", "Thích nghi khi bản đồ thay đổi",
              "Phức tạp, chỉ cần thiết cho bài toán động"],
         ],
         [4.3, 5.5, 5.7]),

        ("h2", "1.4. Các thách thức kĩ thuật của đề tài"),
        ("p", "Thách thức thứ nhất là việc lựa chọn hàm ước lượng. Một hàm ước lượng quá "
              "thấp sẽ khiến A* suy giảm thành tìm kiếm theo chi phí đều và mất đi lợi thế "
              "định hướng. Một hàm ước lượng quá cao có thể vượt quá chi phí thực tế, làm "
              "mất tính tối ưu và cho ra đường đi không còn là tốt nhất. Vì vậy đề tài phải "
              "cài đặt nhiều hàm ước lượng khác nhau, có cơ chế đánh giá tính khả dụng theo "
              "cấu hình lưới, và có thực nghiệm đo đạc để thấy rõ ảnh hưởng của từng hàm."),
        ("p", "Thách thức thứ hai là ảnh hưởng của cấu hình di chuyển. Khi cho phép đi "
              "chéo, chi phí của một bước chéo phải lớn hơn chi phí của một bước thẳng để "
              "phản ánh đúng khoảng cách hình học. Nếu đặt sai hệ số này, đường đi tìm được "
              "sẽ có hình dạng sai lệch rõ rệt. Ngoài ra cần xử lý trường hợp đi chéo xuyên "
              "qua khe hở giữa hai ô tường, một tình huống có thể khiến đường đi lọt qua "
              "vách mỏng và không còn hợp lệ về mặt hình học."),
        ("p", "Thách thức thứ ba là yêu cầu trực quan hoá. Muốn quan sát được thuật toán "
              "đang làm gì, chương trình phải cho phép tạm dừng giữa chừng, hiển thị đồng "
              "thời tập đỉnh đang chờ, tập đỉnh đã duyệt và đỉnh đang xét, đồng thời cập "
              "nhật các đại lượng g(n), h(n), f(n) theo thời gian thực. Điều này đòi hỏi bộ "
              "máy tìm kiếm phải được thiết kế theo hướng phát sự kiện thay vì chạy một "
              "mạch từ đầu đến cuối."),
        ("p", "Thách thức thứ tư là tính trung thực và khả năng kiểm chứng của số liệu. "
              "Các kết luận trong báo cáo phải dựa trên số liệu đo được từ chính chương "
              "trình, không được suy đoán. Vì vậy toàn bộ thí nghiệm được thực hiện bằng "
              "một kịch bản tự động chạy trên sáu bộ dữ liệu mẫu, kết quả được ghi ra tệp "
              "CSV và tệp báo cáo HTML để có thể chạy lại và đối chiếu bất cứ lúc nào."),

        ("h2", "1.5. Mục tiêu, đối tượng và phạm vi của đề tài"),
        ("p", "Mục tiêu của đề tài gồm bốn điểm. Điểm thứ nhất là trình bày đầy đủ cơ sở lý "
              "thuyết của thuật toán A* gồm định nghĩa hàm ưu tiên, điều kiện khả dụng và "
              "nhất quán của hàm ước lượng, chứng minh tính tối ưu và phân tích độ phức "
              "tạp thời gian cùng bộ nhớ. Điểm thứ hai là xây dựng chương trình hoàn chỉnh "
              "bằng Python có giao diện đồ hoạ cho phép chỉnh sửa lưới, chọn thuật toán và "
              "quan sát quá trình tìm kiếm theo từng bước."),
        ("p", "Điểm thứ ba là chuẩn bị một bộ dữ liệu mẫu đa dạng, bao phủ các tình huống "
              "khác nhau như lưới trống, vật cản rải rác, mê cung, cấu trúc phòng, hành "
              "lang xoắn ốc và địa hình có trọng số, nhằm bộc lộ điểm mạnh và điểm yếu của "
              "từng thuật toán. Điểm thứ tư là thực hiện các thí nghiệm so sánh có định "
              "lượng, bao gồm so sánh A* với các thuật toán đối chứng, so sánh các hàm ước "
              "lượng, khảo sát biến thể weighted A* và khảo sát ảnh hưởng của việc cho phép "
              "đi chéo."),
        ("p", "Đối tượng nghiên cứu của đề tài là các thuật toán tìm kiếm trên đồ thị có "
              "trọng số không âm, cụ thể là A*, tìm kiếm theo chi phí đều, tìm kiếm tham "
              "lam và tìm kiếm theo chiều rộng. Phạm vi nghiên cứu giới hạn ở không gian "
              "hai chiều dạng lưới với kích thước tối đa khoảng sáu mươi ô mỗi chiều, số "
              "bước đi giới hạn theo bốn hoặc tám hướng, chi phí địa hình nhận một trong "
              "các giá trị một, hai, bốn hoặc sáu. Đề tài không xét các biến thể tìm kiếm "
              "trong không gian liên tục, không xét tìm đường cho nhiều tác nhân cùng lúc "
              "và không xét bản đồ thay đổi theo thời gian."),

        ("h2", "1.6. Bố cục của báo cáo"),
        ("p", "Báo cáo được tổ chức thành năm chương. Chương 1 giới thiệu bối cảnh, phát "
              "biểu bài toán, khảo sát các giải pháp hiện hành và xác định mục tiêu, phạm "
              "vi nghiên cứu. Chương 2 trình bày cơ sở lý thuyết, trong đó trọng tâm là "
              "các hàm ước lượng, thuật toán A* và phân tích độ phức tạp. Chương 3 trình "
              "bày phân tích thiết kế chương trình gồm kiến trúc phân tầng, sơ đồ lớp, cấu "
              "trúc dữ liệu và thiết kế giao diện."),
        ("p", "Chương 4 trình bày kết quả cài đặt và thực nghiệm. Chương này mô tả môi "
              "trường cài đặt, sáu bộ dữ liệu mẫu, giao diện chương trình, bộ kịch bản "
              "kiểm thử và năm nhóm thí nghiệm đo đạc. Kết quả của mỗi nhóm thí nghiệm "
              "được trình bày dưới dạng bảng số liệu kèm biểu đồ và phần phân tích nguyên "
              "nhân. Chương 5 tổng kết những kết quả đã đạt được, nêu các hạn chế còn tồn "
              "tại và đề xuất hướng phát triển tiếp theo."),
        ("p", "Phần cuối báo cáo gồm danh mục tài liệu tham khảo và phụ lục mã nguồn. Phụ "
              "lục A trích dẫn phần mã nguồn cốt lõi của thuật toán A* và của giao diện để "
              "người đọc có thể đối chiếu giữa phần trình bày lý thuyết và phần cài đặt "
              "thực tế."),
    ]


# ====================================================================== #
# CHƯƠNG 2
# ====================================================================== #
def chapter2(ctx: dict) -> list[tuple]:
    return [
        ("h1", "CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ THUẬT TOÁN A*"),

        ("h2", "2.1. Không gian trạng thái và mô hình đồ thị của lưới"),
        ("p", "Một bài toán tìm kiếm được mô hình hoá bằng bộ bốn thành phần gồm trạng thái "
              "ban đầu, tập hành động, hàm chuyển trạng thái và hàm chi phí. Với bài toán "
              "tìm đường trên lưới, trạng thái ban đầu là ô xuất phát S, tập trạng thái là "
              "tất cả các ô đi được, tập hành động của một ô là các bước di chuyển sang ô "
              "kề, hàm chuyển trạng thái trả về ô kề tương ứng, và hàm chi phí trả về chi "
              "phí của bước đi như đã định nghĩa ở mục 1.2."),
        ("p", "Bộ bốn thành phần này tương đương với một đồ thị có hướng G = (V, E) trong "
              "đó mỗi đỉnh của V là một ô đi được và mỗi cạnh của E là một cặp ô kề hợp "
              "lệ. Với cấu hình bốn hướng, mỗi đỉnh trong vùng bên trong lưới có đúng bốn "
              "đỉnh kề, do đó hệ số phân nhánh trung bình của đồ thị xấp xỉ bốn. Với cấu "
              "hình tám hướng, hệ số phân nhánh xấp xỉ tám nhưng số cạnh bị chặn trên bởi "
              "ba phần tư số đỉnh khi áp dụng quy tắc không cắt góc. Trên lưới có vật cản, "
              "hệ số phân nhánh thực tế nhỏ hơn giá trị lý thuyết và phụ thuộc vào mật độ "
              "tường của bộ dữ liệu."),
        ("p", "Độ sâu của lời giải, ký hiệu là d, bằng số bước đi trên đường đi tối ưu. "
              "Với lưới kích thước H hàng và W cột, độ sâu tối đa trong trường hợp xấu "
              "nhất có thể lên tới H nhân W khi đường đi buộc phải đi qua gần hết các ô, "
              "điển hình là bộ dữ liệu hành lang xoắn ốc được trình bày ở Chương 4. Các "
              "đại lượng b và d này là hai tham số quyết định độ phức tạp của mọi thuật "
              "toán tìm kiếm được phân tích trong chương này."),
        ("p", "Một đặc điểm quan trọng của lưới là cấu trúc lân cận rất đều đặn. Vì toạ độ "
              "của ô kề luôn bằng toạ độ của ô hiện tại cộng thêm một vectơ trong bảng "
              "hướng cố định, việc sinh đỉnh kề chỉ tốn thời gian hằng số cho mỗi đỉnh. "
              "Trong cài đặt của đề tài, danh sách đỉnh kề của một ô còn được lưu đệm "
              "theo ô, nhờ đó các lần sinh lân cận lặp lại không phải tính lại chi phí. "
              "Đây là một tối ưu quan trọng vì trong tìm kiếm có mở lại đỉnh, cùng một ô "
              "có thể được sinh kề nhiều lần."),

        ("h2", "2.2. Hàm ưu tiên và họ thuật toán tìm kiếm"),
        ("p", "Hầu hết thuật toán tìm kiếm trên đồ thị có trọng số đều được mô tả bằng một "
              "khung chung. Khung này duy trì hai tập đỉnh, tập OPEN chứa các đỉnh đã được "
              "sinh ra và đang chờ xét, và tập CLOSED chứa các đỉnh đã được lấy ra xử lý. "
              "Ở mỗi vòng lặp, thuật toán lấy ra khỏi tập OPEN một đỉnh theo một quy tắc "
              "xác định bởi hàm ưu tiên, đưa đỉnh đó vào tập CLOSED, kiểm tra điều kiện "
              "dừng, rồi sinh các đỉnh kề và cập nhật chi phí của chúng. Sự khác biệt giữa "
              "các thuật toán nằm ở hàm ưu tiên và ở chính sách cập nhật đỉnh đã có trong "
              "tập OPEN hoặc tập CLOSED."),
        ("p", "Tìm kiếm theo chiều rộng coi mọi bước đi có cùng chi phí bằng một và dùng "
              "hàng đợi hai đầu theo nguyên tắc vào trước ra trước. Tìm kiếm theo chi phí "
              "đều dùng hàng đợi ưu tiên với khoá là g(n), nhờ đó đỉnh có chi phí đã bỏ ra "
              "nhỏ nhất luôn được xét trước. Tìm kiếm tham lam dùng khoá là h(n), chỉ quan "
              "tâm tới ước lượng khoảng cách còn lại. A* dùng khoá là tổng của hai thành "
              "phần, tức là kết hợp thông tin thực tế với thông tin ước lượng."),
        ("p", "Trạng thái của một đỉnh trong quá trình tìm kiếm được mô tả bằng sáu bước "
              "chuyển như Hình 2.1. Ban đầu mọi đỉnh nằm ở trạng thái chưa biết với giá "
              "trị g bằng vô cùng. Khi một đỉnh kề được sinh ra và có chi phí tốt hơn giá "
              "trị hiện có, đỉnh đó chuyển sang trạng thái nằm trong tập OPEN. Đỉnh ở trong "
              "tập OPEN có thể được cập nhật nhiều lần nếu tìm thấy đường đi rẻ hơn. Khi "
              "đỉnh được lấy ra theo tiêu chí ưu tiên, đỉnh chuyển sang tập CLOSED và giá "
              "trị g của nó được coi là đã chốt. Nếu hàm ước lượng không nhất quán, một "
              "đỉnh đã ở tập CLOSED vẫn có thể được mở lại khi phát hiện đường đi tốt hơn. "
              "Quá trình kết thúc khi đỉnh được xét chính là đích, hoặc khi tập OPEN rỗng "
              "tức là không tồn tại đường đi."),
        ("figure", "docs/diagrams/hinh_2_1_vong_doi_dinh.png",
         "Hình 2.1: Vòng đời trạng thái của một đỉnh trong quá trình tìm kiếm, từ chưa biết "
         "sang tập mở, sang tập đóng và kết thúc khi gặp đích", 9.0),
        ("p", "Việc phân biệt rõ tập OPEN và tập CLOSED có ý nghĩa cả về lý thuyết lẫn về "
              "mặt cài đặt. Về lý thuyết, tính đúng đắn của A* dựa trên việc mỗi đỉnh chỉ "
              "được chốt giá trị g khi nó thực sự có chi phí nhỏ nhất có thể. Về mặt cài "
              "đặt, hai tập này còn là cơ sở để giao diện tô màu, giúp người học nhìn thấy "
              "trực tiếp mức độ lan rộng của từng thuật toán trên cùng một bản đồ."),

        ("h2", "2.3. Hàm ước lượng h(n) và các tính chất"),
        ("p", "Hàm ước lượng h(n) là thành phần mang thông tin đặc thù của bài toán vào "
              "thuật toán tìm kiếm. Để A* giữ được tính tối ưu, h(n) phải thoả mãn điều "
              "kiện khả dụng, nghĩa là với mọi đỉnh n, giá trị h(n) không được lớn hơn "
              "chi phí thực nhỏ nhất từ n tới đích. Trên lưới, điều kiện này được đảm bảo "
              "bằng cách nhân khoảng cách hình học với chi phí bước nhỏ nhất của lưới. "
              "Nếu lưới có địa hình trọng số lớn hơn một, việc nhân với chi phí bước nhỏ "
              "nhất vẫn giữ được tính khả dụng vì mọi bước đi thực tế đều có chi phí không "
              "nhỏ hơn giá trị đó."),
        ("p", "Một tính chất mạnh hơn của hàm ước lượng là tính nhất quán, còn gọi là điều "
              "kiện đơn điệu. Hàm h được gọi là nhất quán nếu với mọi cặp đỉnh kề nhau a "
              "và b, giá trị h(a) không lớn hơn tổng của chi phí bước đi từ a tới b và giá "
              "trị h(b). Điều kiện này chính là dạng rời rạc của bất đẳng thức tam giác. "
              "Khi h nhất quán, giá trị f(n) dọc theo bất kì đường đi nào cũng không giảm, "
              "do đó A* chỉ cần duyệt mỗi đỉnh một lần và không phải mở lại đỉnh đã đóng. "
              "Tất cả các hàm ước lượng dùng cho lưới bốn hướng và tám hướng trong đề tài "
              "đều nhất quán khi hệ số chi phí bước đi được đặt đúng."),
        ("formula", "h(n) ≤ h*(n)", "2.1"),
        ("formula", "h(a) ≤ c(a, b) + h(b)", "2.2"),
        ("p", "Bốn hàm ước lượng được cài đặt trong đề tài gồm khoảng cách Manhattan, "
              "khoảng cách Euclid, khoảng cách Chebyshev và khoảng cách octile. Khoảng "
              "cách Manhattan là tổng của hiệu số hàng và hiệu số cột, phù hợp với lưới "
              "bốn hướng và cho giá trị chính xác khi không có vật cản. Khoảng cách Euclid "
              "là khoảng cách theo đường thẳng, luôn nhỏ hơn hoặc bằng chi phí thực nên "
              "khả dụng cho cả hai cấu hình nhưng thường lỏng hơn khoảng cách Manhattan "
              "trên lưới bốn hướng."),
        ("p", "Khoảng cách Chebyshev là giá trị lớn nhất của hiệu số hàng và hiệu số cột, "
              "phù hợp với lưới tám hướng khi bước chéo có chi phí bằng một. Khoảng cách "
              "octile là trường hợp đặc biệt quan trọng vì nó khớp chính xác với chi phí "
              "thực của lưới tám hướng, trong đó mỗi bước chéo có chi phí bằng căn bậc hai "
              "của hai. Vì khớp chính xác nên khoảng cách octile là hàm ước lượng chặt nhất "
              "mà vẫn khả dụng cho lưới tám hướng, và trong thực nghiệm ở Chương 4 nó cho "
              "số đỉnh duyệt ít nhất. Bảng 2.1 tóm tắt tính chất của từng hàm."),
        ("table", "Bảng 2.1: Các hàm ước lượng được cài đặt và tính chất",
         ["Hàm h(n)", "Công thức", "Khả dụng cho"],
         [
             ["Manhattan", "h = |dr| + |dc|", "Lưới 4 hướng, bước thẳng chi phí 1"],
             ["Euclid", "h = căn của (dr^2 + dc^2)", "Cả lưới 4 hướng và 8 hướng"],
             ["Chebyshev", "h = max(|dr|, |dc|)", "Lưới 8 hướng khi bước chéo chi phí 1"],
             ["Octile", "h = (dr + dc) + (căn hai trừ hai) nhân min(dr, dc)",
              "Lưới 8 hướng, bước chéo chi phí căn hai"],
             ["Trung tính", "h = 0", "Mọi lưới, khi đó A* suy giảm thành Dijkstra"],
         ],
         [2.6, 7.2, 5.7]),
        ("p", "Cần lưu ý rằng khoảng cách Manhattan không khả dụng trên lưới tám hướng. Lý "
              "do là trên lưới tám hướng, chi phí thực để đi từ một ô tới một ô chéo kề "
              "chỉ là căn bậc hai của hai, trong khi khoảng cách Manhattan lại báo giá trị "
              "bằng hai. Giá trị ước lượng vượt quá chi phí thực khiến A* có thể chọn nhầm "
              "đỉnh và cho ra đường đi không tối ưu. Chương trình vì vậy có cơ chế cảnh báo "
              "trên giao diện mỗi khi người dùng chọn tổ hợp thuật toán và hàm ước lượng "
              "không đảm bảo tính khả dụng."),

        ("h2", "2.4. Thuật toán A* chi tiết và chứng minh tính tối ưu"),
        ("p", "A* là trường hợp riêng của khung tìm kiếm nêu ở mục 2.2 với hàm ưu tiên là "
              "tổng của chi phí đã bỏ ra và chi phí ước lượng còn lại. Quy trình của thuật "
              "toán gồm việc khởi tạo tập OPEN với đỉnh xuất phát, lặp lại việc lấy ra "
              "đỉnh có giá trị ưu tiên nhỏ nhất, kiểm tra đích, sinh đỉnh kề và cập nhật "
              "chi phí. Hình 2.2 trình bày lưu đồ của thuật toán với đầy đủ các nhánh xử lý."),
        ("figure", "docs/diagrams/hinh_2_2_giai_thuat_astar.png",
         "Hình 2.2: Lưu đồ thuật toán A* từ khâu khởi tạo, vòng lặp lấy đỉnh ưu tiên, "
         "cập nhật đỉnh kề cho tới khi trả về đường đi hoặc kết luận vô nghiệm", 11.0),
        ("p", "Cấu trúc dữ liệu cho tập OPEN là hàng đợi ưu tiên cài bằng cây vun đống "
              "nhị phân, cho phép lấy ra đỉnh có khoá nhỏ nhất và thêm đỉnh mới với độ "
              "phức tạp logarit. Song song với hàng đợi, thuật toán lưu một bảng giá trị g "
              "cho các đỉnh đã sinh và một bảng cha để truy vết đường đi khi kết thúc. Việc "
              "dùng bảng băm cho hai bảng này giúp thao tác tra cứu và cập nhật có độ phức "
              "tạp trung bình hằng số."),
        ("p", "Một chi tiết kĩ thuật ảnh hưởng rõ rệt tới thời gian chạy của A* là cách "
              "phá vỡ thế bằng của các giá trị ưu tiên. Trên lưới trống, rất nhiều đỉnh có "
              "cùng giá trị f, và thứ tự chúng được lấy ra có thể làm số đỉnh duyệt thay "
              "đổi đáng kể dù chi phí đường đi cuối cùng không đổi. Trong cài đặt của đề "
              "tài, khi hai đỉnh có cùng f thì đỉnh có h nhỏ hơn được ưu tiên trước, tức "
              "là ưu tiên đỉnh gần đích hơn. Kỹ thuật này giữ nguyên tính tối ưu nhưng "
              "thường rút ngắn đáng kể số đỉnh phải duyệt."),
        ("p", "Một chi tiết kĩ thuật khác là chính sách mở lại đỉnh. Khi hàm ước lượng kém "
              "chặt, chẳng hạn trong weighted A* với trọng số lớn hơn một, giá trị ưu tiên "
              "có thể không đơn điệu và một đỉnh đã ở tập CLOSED vẫn có thể được tìm thấy "
              "với chi phí g nhỏ hơn. Chương trình cho phép bật hoặc tắt chính sách này. "
              "Khi bật, thuật toán trung thực về mặt lý thuyết nhưng có thể phải xét lại "
              "nhiều đỉnh. Khi tắt, thuật toán chạy nhanh hơn nhưng chất lượng đường đi có "
              "thể giảm. Ảnh hưởng của hai chế độ này được định lượng ở mục 4.8."),
        ("p", "Trước khi trình bày chứng minh tính tối ưu, cần nêu một bổ đề cơ bản. Với "
              "hàm ước lượng khả dụng, mọi đỉnh n được lấy ra khỏi tập OPEN để đưa vào tập "
              "CLOSED đều có giá trị g(n) đúng bằng chi phí nhỏ nhất từ đỉnh xuất phát tới "
              "n. Chứng minh bổ đề này được thực hiện bằng phản chứng. Giả sử tồn tại đỉnh "
              "đầu tiên khi được lấy ra có giá trị g lớn hơn chi phí thực tối ưu. Gọi đường "
              "đi tối ưu tới đỉnh đó có đỉnh cuối cùng nằm trong tập OPEN là m. Đỉnh m có "
              "giá trị g đúng bằng chi phí tối ưu tới nó theo giả thiết về tính đầu tiên. "
              "Khi đó giá trị ưu tiên của m bằng chi phí tối ưu tới m cộng với ước lượng từ "
              "m tới đích, không vượt quá chi phí tối ưu của toàn đường đi, trong khi giá "
              "trị ưu tiên của đỉnh được lấy ra lại lớn hơn. Vì hàng đợi ưu tiên luôn lấy "
              "đỉnh có khoá nhỏ nhất, m phải được lấy ra trước, mâu thuẫn với giả thiết. "
              "Bổ đề được chứng minh."),
        ("p", "Tính tối ưu của A* là hệ quả trực tiếp của bổ đề trên. Giả sử đỉnh đích được "
              "lấy ra khỏi tập OPEN khi vẫn còn một đường đi rẻ hơn chưa được khám phá. "
              "Theo bổ đề, giá trị g của đích lúc đó đúng bằng chi phí nhỏ nhất tìm được "
              "tới đích, mà giá trị này lại lớn hơn chi phí của đường đi rẻ hơn. Lập luận "
              "tương tự chứng minh bổ đề cho thấy phải tồn tại một đỉnh trên đường đi rẻ "
              "hơn có giá trị ưu tiên nhỏ hơn, và đỉnh đó sẽ được lấy ra trước đích, dẫn "
              "tới mâu thuẫn. Vì vậy A* với hàm ước lượng khả dụng luôn trả về đường đi có "
              "chi phí nhỏ nhất. Kết quả này cũng được kiểm chứng bằng thực nghiệm ở mục "
              "4.6, nơi chi phí của A* luôn trùng khớp với chi phí của tìm kiếm theo chi "
              "phí đều trên cả sáu bộ dữ liệu."),
        ("formula", "f(n) = g(n) + w · h(n)", "2.3"),
        ("p", "Trong công thức trên, w là trọng số của biến thể A* có trọng số. Khi w bằng "
              "một thì hàm ưu tiên trở về dạng cổ điển f(n) = g(n) + h(n) và thuật toán "
              "giữ nguyên tính tối ưu nếu hàm ước lượng khả dụng. Khi w lớn hơn một thì "
              "thuật toán ưu tiên đi nhanh về phía đích, đổi lại đường đi có thể không còn "
              "là đường rẻ nhất. Ảnh hưởng định lượng của trọng số w được khảo sát ở mục 4.8."),
        ("figure", "docs/figures/hinh_2_3_g_h_f.png",
         "Hình 2.3: Minh hoạ các đại lượng g(n), h(n), f(n) tại một bước của A* trên lưới "
         "có vật cản", 13.5),
        ("p", "Hình 2.3 minh hoạ cách các đại lượng xuất hiện trong một bước chạy thực tế. "
              "Tại bước thứ mười bốn của quá trình tìm kiếm, đỉnh đang xét là ô có toạ độ "
              "hàng sáu cột năm, với chi phí đã bỏ ra bằng mười một, ước lượng khoảng cách "
              "tới đích bằng tám và giá trị ưu tiên bằng mười chín. Vùng màu xám đậm là "
              "các đỉnh đã duyệt xong, vùng xám nhạt là các đỉnh đang chờ trong tập OPEN, "
              "và đường kẻ đậm là đường đi tạm thời tốt nhất tính tới thời điểm đó. Hình "
              "này cũng cho thấy A* không lan đều ra mọi hướng mà tập trung phát triển về "
              "phía đích."),

        ("h2", "2.5. Phân tích độ phức tạp của thuật toán"),
        ("p", "Độ phức tạp thời gian của A* trong trường hợp xấu nhất là O(b mũ d), trong "
              "đó b là hệ số phân nhánh và d là độ sâu của lời giải. Đây là chặn trên "
              "tương ứng với trường hợp hàm ước lượng không mang lại thông tin, tức là "
              "h(n) bằng không trên toàn bộ lưới. Khi đó A* suy giảm thành tìm kiếm theo "
              "chi phí đều và phải duyệt toàn bộ vùng liên thông. Ngược lại, khi hàm ước "
              "lượng khớp chính xác với chi phí thực, nghĩa là h(n) bằng h*(n) với mọi "
              "đỉnh, A* chỉ duyệt đúng các đỉnh nằm trên đường đi tối ưu và độ phức tạp "
              "giảm xuống còn O(d)."),
        ("p", "Trường hợp thực tế nằm giữa hai cực trị trên. Nếu hàm ước lượng khả dụng và "
              "sai số của nó bị chặn bởi một hằng số, số đỉnh duyệt có thể được chứng minh "
              "là bậc đa thức theo độ sâu. Trên lưới, khi hàm ước lượng khả dụng và khá "
              "chặt, vùng đỉnh được duyệt có dạng gần giống một hình bầu dục kéo dài giữa "
              "đỉnh xuất phát và đỉnh đích, do đó số đỉnh duyệt xấp xỉ tỉ lệ với số ô nằm "
              "trong hình bầu dục đó chứ không phải toàn bộ lưới. Mức độ thu hẹp này phụ "
              "thuộc vào chiều dài đường đi và mật độ vật cản."),
        ("p", "Độ phức tạp bộ nhớ của A* là O(b mũ d) do thuật toán phải lưu toàn bộ tập "
              "OPEN và tập CLOSED. Đây là hạn chế lớn nhất của A* trong các bài toán có "
              "không gian trạng thái khổng lồ, và cũng là động lực ra đời của các biến thể "
              "tiết kiệm bộ nhớ như tìm kiếm sâu dần theo ngưỡng chi phí và A* có giới hạn "
              "bộ nhớ. Với đề tài này, lưới có kích thước tối đa khoảng một nghìn tám trăm "
              "ô nên bộ nhớ không phải là yếu tố giới hạn. Tuy nhiên việc nêu rõ đặc điểm "
              "này là cần thiết để giải thích vì sao trong thực nghiệm, biểu đồ kích thước "
              "tập OPEN lớn nhất lại là một trong các chỉ số được ghi nhận."),
        ("p", "Chi phí của từng thao tác cơ bản cũng cần được xem xét. Thao tác lấy đỉnh "
              "có khoá nhỏ nhất khỏi cây vun đống tốn thời gian logarit theo kích thước "
              "tập OPEN. Thao tác sinh đỉnh kề tốn thời gian hằng số cho mỗi đỉnh kề nhờ "
              "bảng hướng cố định và bộ đệm lân cận. Thao tác tra cứu và cập nhật bảng giá "
              "trị g có độ phức tạp trung bình hằng số. Vì vậy độ phức tạp của một vòng "
              "lặp chính là logarit theo số đỉnh sinh ra, và tổng thời gian chạy tỉ lệ với "
              "số đỉnh sinh nhân với logarit của số đỉnh sinh. Kết quả đo đạc ở Chương 4 "
              "phù hợp với phân tích này khi thời gian chạy bám sát số đỉnh đã duyệt."),
        ("table", "Bảng 2.2: Tổng hợp độ phức tạp của các thuật toán tìm kiếm trên lưới",
         ["Thuật toán", "Hàm ưu tiên", "Thời gian xấu nhất", "Bộ nhớ", "Tối ưu"],
         [
             ["Tìm kiếm theo chiều rộng", "vào trước ra trước, chi phí bước bằng 1",
              "O(b mũ d)", "O(b mũ d)", "Chỉ khi mọi bước cùng chi phí"],
             ["Tìm kiếm theo chi phí đều", "g(n)", "O(b mũ d)", "O(b mũ d)", "Có, với trọng số không âm"],
             ["Greedy Best First", "h(n)", "O(b mũ d)", "O(b mũ d)", "Không"],
             ["A*", "g(n) cộng h(n)", "O(b mũ d), tốt hơn nhiều trên thực tế",
              "O(b mũ d)", "Có, khi h khả dụng"],
             ["A* có trọng số w", "g(n) cộng w nhân h(n)", "O(b mũ d)",
              "O(b mũ d)", "Không, chi phí tối đa bằng w lần tối ưu"],
         ],
         [4.0, 4.2, 3.3, 1.8, 2.2]),

        ("h2", "2.6. Nhận xét về phạm vi hiệu quả của A*"),
        ("p", "Từ phân tích ở mục 2.5 có thể rút ra ba nhận xét định hướng cho phần thực "
              "nghiệm. Nhận xét thứ nhất là lợi ích của A* so với tìm kiếm theo chi phí "
              "đều tỉ lệ với độ chặt của hàm ước lượng. Trên lưới trống với cấu hình bốn "
              "hướng, khoảng cách Manhattan là hàm ước lượng khớp chính xác nên số đỉnh "
              "duyệt giảm tới hơn mười lần. Trên cùng bộ dữ liệu đó, khoảng cách Euclid "
              "lỏng hơn đáng kể nên số đỉnh duyệt gần bằng trường hợp không dùng thông tin. "
              "Đây là lý do vì sao việc chọn hàm ước lượng phù hợp với cấu hình di chuyển "
              "quan trọng không kém việc cài đặt đúng thuật toán."),
        ("p", "Nhận xét thứ hai là cấu trúc của bản đồ có thể vô hiệu hoá lợi ích của hàm "
              "ước lượng. Trên bộ dữ liệu hành lang xoắn ốc, toàn bộ lưới chỉ có một lối "
              "đi duy nhất từ đỉnh xuất phát tới đích, do đó mọi thuật toán buộc phải duyệt "
              "gần hết số ô. Trong trường hợp này, hàm ước lượng dù chặt tới đâu cũng không "
              "giúp giảm số đỉnh duyệt, điều này cho thấy chất lượng của thuật toán tìm "
              "kiếm luôn phụ thuộc vào cấu trúc của bài toán chứ không chỉ phụ thuộc vào "
              "bản thân thuật toán."),
        ("p", "Nhận xét thứ ba là việc cho phép đi chéo làm giảm rõ rệt chi phí đường đi "
              "nhưng làm tăng số đỉnh cần duyệt trên mỗi bước, bởi hệ số phân nhánh tăng "
              "từ bốn lên tám. Hai xu hướng này ngược chiều nhau, và lựa chọn cấu hình nào "
              "phụ thuộc vào yêu cầu của ứng dụng. Với ứng dụng mô phỏng chuyển động của "
              "robot trong mặt bằng, cấu hình tám hướng thường cho đường đi tự nhiên hơn "
              "vì cho phép di chuyển theo đường chéo. Với ứng dụng mô phỏng di chuyển trên "
              "hệ thống đường phố, cấu hình bốn hướng lại phù hợp hơn vì các tuyến đường "
              "thực tế vuông góc với nhau."),

        ("h2", "2.7. Các biến thể và hướng mở rộng liên quan"),
        ("p", "A* có nhiều biến thể được sử dụng rộng rãi trong thực tế. Biến thể A* có "
              "trọng số nhân thêm hệ số lớn hơn một vào hàm ước lượng, nhờ đó giảm số đỉnh "
              "duyệt nhưng phải đánh đổi bằng chất lượng đường đi. Trên các lưới có địa "
              "hình trọng số, hành vi của biến thể này phức tạp hơn so với lưới đồng nhất "
              "và sẽ được phân tích kĩ ở mục 4.8. Biến thể A* với chính sách không mở lại "
              "đỉnh đã đóng thường được dùng trong công nghiệp vì đơn giản và ổn định, dù "
              "về mặt lý thuyết nó có thể cho kết quả không tối ưu trong một số trường hợp."),
        ("p", "Các biến thể phức tạp hơn gồm tìm kiếm theo bước nhảy Jump Point Search, "
              "hoạt động bằng cách nhảy qua các ô có cùng hướng đi trên lưới đồng nhất để "
              "giảm số đỉnh sinh, tìm kiếm A* phân cấp cho bản đồ lớn bằng cách chia bản đồ "
              "thành nhiều tầng, và A* gia tăng như D* Lite cho bản đồ thay đổi theo thời "
              "gian. Các biến thể này đều là hướng phát triển tiềm năng của đề tài và được "
              "đề cập ở mục 5.3."),
        ("p", "Về phương diện học tập, việc cài đặt và so sánh bốn thuật toán trên cùng một "
              "khung tìm kiếm giúp làm rõ rằng tìm kiếm theo chiều rộng, tìm kiếm theo chi "
              "phí đều và A* chỉ khác nhau ở hàm ưu tiên và ở chính sách cập nhật đỉnh, "
              "trong khi toàn bộ khung duyệt đồ thị là giống nhau. Cách nhìn thống nhất "
              "này cũng là cơ sở để thiết kế mô-đun tìm kiếm của chương trình, được trình "
              "bày ở Chương 3."),
    ]
