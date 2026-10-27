# Đề tài 48 — Bảng kết quả thực nghiệm

## TN1 + TN2: A* với các h(n) và thuật toán đối chứng

| Bản đồ | Thuật toán | h(n) | w | Mở lại | Tìm thấy | Chi phí | Ô | Duyệt | Sinh | \|OPEN\|max | Thời gian (ms) | Hợp lệ | Tối ưu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| trong | A* | manhattan | 1 | ✔ | ✔ | 48.000 | 49 | 49 | 95 | 46 | 0.203 | ✔ | ✔ |
| trong | A* | euclidean | 1 | ✔ | ✔ | 48.000 | 49 | 553 | 600 | 47 | 1.470 | ✔ | ✔ |
| trong | A* | chebyshev | 1 | ✔ | ✔ | 48.000 | 49 | 553 | 600 | 47 | 1.473 | ✔ | ✔ |
| trong | A* | octile | 1 | ✔ | ✔ | 48.000 | 49 | 553 | 600 | 47 | 1.551 | ✔ | ✔ |
| trong | UCS (Dijkstra) | - | 1 | ✔ | ✔ | 48.000 | 49 | 600 | 600 | 19 | 1.345 | ✔ | ✔ |
| trong | Greedy Best-First | manhattan | 1 | ✔ | ✔ | 48.000 | 49 | 49 | 95 | 46 | 0.165 | ✔ | ✔ |
| trong | BFS | - | 1 | ✔ | ✔ | 48.000 | 49 | 600 | 600 | 19 | 0.803 | ✔ | ✔ |
| vat_can_ngau_nhien | A* | manhattan | 1 | ✔ | ✔ | 69.000 | 70 | 127 | 189 | 54 | 0.393 | ✔ | ✔ |
| vat_can_ngau_nhien | A* | euclidean | 1 | ✔ | ✔ | 69.000 | 70 | 495 | 529 | 38 | 1.216 | ✔ | ✔ |
| vat_can_ngau_nhien | A* | chebyshev | 1 | ✔ | ✔ | 69.000 | 70 | 508 | 568 | 47 | 1.329 | ✔ | ✔ |
| vat_can_ngau_nhien | A* | octile | 1 | ✔ | ✔ | 69.000 | 70 | 470 | 529 | 47 | 1.274 | ✔ | ✔ |
| vat_can_ngau_nhien | UCS (Dijkstra) | - | 1 | ✔ | ✔ | 69.000 | 70 | 693 | 693 | 30 | 1.505 | ✔ | ✔ |
| vat_can_ngau_nhien | Greedy Best-First | manhattan | 1 | ✔ | ✔ | 81.000 | 82 | 96 | 150 | 54 | 0.293 | ✔ | – |
| vat_can_ngau_nhien | BFS | - | 1 | ✔ | ✔ | 69.000 | 70 | 693 | 693 | 30 | 0.881 | ✔ | ✔ |
| me_cung | A* | manhattan | 1 | ✔ | ✔ | 104.000 | 105 | 111 | 112 | 1 | 0.238 | ✔ | ✔ |
| me_cung | A* | euclidean | 1 | ✔ | ✔ | 104.000 | 105 | 111 | 112 | 1 | 0.249 | ✔ | ✔ |
| me_cung | A* | chebyshev | 1 | ✔ | ✔ | 104.000 | 105 | 111 | 112 | 1 | 0.241 | ✔ | ✔ |
| me_cung | A* | octile | 1 | ✔ | ✔ | 104.000 | 105 | 111 | 112 | 1 | 0.253 | ✔ | ✔ |
| me_cung | UCS (Dijkstra) | - | 1 | ✔ | ✔ | 104.000 | 105 | 119 | 120 | 1 | 0.223 | ✔ | ✔ |
| me_cung | Greedy Best-First | manhattan | 1 | ✔ | ✔ | 104.000 | 105 | 105 | 107 | 2 | 0.219 | ✔ | ✔ |
| me_cung | BFS | - | 1 | ✔ | ✔ | 104.000 | 105 | 119 | 120 | 1 | 0.141 | ✔ | ✔ |
| phong_hanh_lang | A* | manhattan | 1 | ✔ | ✔ | 49.000 | 50 | 70 | 148 | 78 | 0.295 | ✔ | ✔ |
| phong_hanh_lang | A* | euclidean | 1 | ✔ | ✔ | 49.000 | 50 | 386 | 439 | 53 | 1.049 | ✔ | ✔ |
| phong_hanh_lang | A* | chebyshev | 1 | ✔ | ✔ | 49.000 | 50 | 454 | 511 | 55 | 1.257 | ✔ | ✔ |
| phong_hanh_lang | A* | octile | 1 | ✔ | ✔ | 49.000 | 50 | 367 | 422 | 53 | 1.056 | ✔ | ✔ |
| phong_hanh_lang | UCS (Dijkstra) | - | 1 | ✔ | ✔ | 49.000 | 50 | 1139 | 1166 | 38 | 2.728 | ✔ | ✔ |
| phong_hanh_lang | Greedy Best-First | manhattan | 1 | ✔ | ✔ | 57.000 | 58 | 62 | 132 | 70 | 0.242 | ✔ | – |
| phong_hanh_lang | BFS | - | 1 | ✔ | ✔ | 49.000 | 50 | 1139 | 1166 | 38 | 1.543 | ✔ | ✔ |
| xoan_oc | A* | manhattan | 1 | ✔ | ✔ | 286.000 | 287 | 287 | 287 | 0 | 0.570 | ✔ | ✔ |
| xoan_oc | A* | euclidean | 1 | ✔ | ✔ | 286.000 | 287 | 287 | 287 | 0 | 0.589 | ✔ | ✔ |
| xoan_oc | A* | chebyshev | 1 | ✔ | ✔ | 286.000 | 287 | 287 | 287 | 0 | 0.582 | ✔ | ✔ |
| xoan_oc | A* | octile | 1 | ✔ | ✔ | 286.000 | 287 | 287 | 287 | 0 | 0.608 | ✔ | ✔ |
| xoan_oc | UCS (Dijkstra) | - | 1 | ✔ | ✔ | 286.000 | 287 | 287 | 287 | 0 | 0.520 | ✔ | ✔ |
| xoan_oc | Greedy Best-First | manhattan | 1 | ✔ | ✔ | 286.000 | 287 | 287 | 287 | 0 | 0.536 | ✔ | ✔ |
| xoan_oc | BFS | - | 1 | ✔ | ✔ | 286.000 | 287 | 287 | 287 | 0 | 0.329 | ✔ | ✔ |
| dia_hinh | A* | manhattan | 1 | ✔ | ✔ | 128.000 | 72 | 1184 | 1483 | 181 | 3.742 | ✔ | ✔ |
| dia_hinh | A* | euclidean | 1 | ✔ | ✔ | 128.000 | 72 | 1195 | 1258 | 80 | 3.257 | ✔ | ✔ |
| dia_hinh | A* | chebyshev | 1 | ✔ | ✔ | 128.000 | 72 | 1196 | 1304 | 77 | 3.453 | ✔ | ✔ |
| dia_hinh | A* | octile | 1 | ✔ | ✔ | 128.000 | 72 | 1194 | 1257 | 88 | 3.391 | ✔ | ✔ |
| dia_hinh | UCS (Dijkstra) | - | 1 | ✔ | ✔ | 128.000 | 72 | 1218 | 1227 | 43 | 2.943 | ✔ | ✔ |
| dia_hinh | Greedy Best-First | manhattan | 1 | ✔ | ✔ | 166.000 | 72 | 72 | 141 | 69 | 0.256 | ✔ | – |
| dia_hinh | BFS | - | 1 | ✔ | ✔ | 166.000 | 72 | 1230 | 1230 | 27 | 1.728 | ✔ | – |

## TN3: Weighted A*

| Bản đồ | Thuật toán | h(n) | w | Mở lại | Tìm thấy | Chi phí | Ô | Duyệt | Sinh | \|OPEN\|max | Thời gian (ms) | Hợp lệ | Tối ưu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| trong | A* | manhattan | 1 | ✔ | ✔ | 48.000 | 49 | 49 | 95 | 46 | 0.180 | ✔ | ✔ |
| trong | A* | manhattan | 1.5 | ✔ | ✔ | 48.000 | 49 | 49 | 95 | 46 | 0.168 | ✔ | ✔ |
| trong | A* | manhattan | 2 | ✔ | ✔ | 48.000 | 49 | 49 | 95 | 46 | 0.166 | ✔ | ✔ |
| trong | A* | manhattan | 3 | ✔ | ✔ | 48.000 | 49 | 49 | 95 | 46 | 0.165 | ✔ | ✔ |
| trong | A* | manhattan | 2 | — | ✔ | 48.000 | 49 | 49 | 95 | 46 | 0.163 | ✔ | ✔ |
| trong | A* | manhattan | 3 | — | ✔ | 48.000 | 49 | 49 | 95 | 46 | 0.162 | ✔ | ✔ |
| vat_can_ngau_nhien | A* | manhattan | 1 | ✔ | ✔ | 69.000 | 70 | 127 | 189 | 54 | 0.397 | ✔ | ✔ |
| vat_can_ngau_nhien | A* | manhattan | 1.5 | ✔ | ✔ | 71.000 | 72 | 111 | 164 | 45 | 0.330 | ✔ | – |
| vat_can_ngau_nhien | A* | manhattan | 2 | ✔ | ✔ | 71.000 | 72 | 114 | 170 | 48 | 0.354 | ✔ | – |
| vat_can_ngau_nhien | A* | manhattan | 3 | ✔ | ✔ | 73.000 | 74 | 112 | 169 | 53 | 0.337 | ✔ | – |
| vat_can_ngau_nhien | A* | manhattan | 2 | — | ✔ | 73.000 | 74 | 107 | 157 | 46 | 0.309 | ✔ | – |
| vat_can_ngau_nhien | A* | manhattan | 3 | — | ✔ | 73.000 | 74 | 101 | 155 | 52 | 0.301 | ✔ | – |
| me_cung | A* | manhattan | 1 | ✔ | ✔ | 104.000 | 105 | 111 | 112 | 1 | 0.241 | ✔ | ✔ |
| me_cung | A* | manhattan | 1.5 | ✔ | ✔ | 104.000 | 105 | 111 | 112 | 1 | 0.234 | ✔ | ✔ |
| me_cung | A* | manhattan | 2 | ✔ | ✔ | 104.000 | 105 | 111 | 112 | 1 | 0.236 | ✔ | ✔ |
| me_cung | A* | manhattan | 3 | ✔ | ✔ | 104.000 | 105 | 105 | 107 | 2 | 0.227 | ✔ | ✔ |
| me_cung | A* | manhattan | 2 | — | ✔ | 104.000 | 105 | 111 | 112 | 1 | 0.233 | ✔ | ✔ |
| me_cung | A* | manhattan | 3 | — | ✔ | 104.000 | 105 | 105 | 107 | 2 | 0.225 | ✔ | ✔ |
| phong_hanh_lang | A* | manhattan | 1 | ✔ | ✔ | 49.000 | 50 | 70 | 148 | 78 | 0.291 | ✔ | ✔ |
| phong_hanh_lang | A* | manhattan | 1.5 | ✔ | ✔ | 51.000 | 52 | 67 | 141 | 73 | 0.263 | ✔ | – |
| phong_hanh_lang | A* | manhattan | 2 | ✔ | ✔ | 51.000 | 52 | 69 | 143 | 73 | 0.265 | ✔ | – |
| phong_hanh_lang | A* | manhattan | 3 | ✔ | ✔ | 55.000 | 56 | 63 | 134 | 71 | 0.250 | ✔ | – |
| phong_hanh_lang | A* | manhattan | 2 | — | ✔ | 53.000 | 54 | 66 | 137 | 70 | 0.254 | ✔ | – |
| phong_hanh_lang | A* | manhattan | 3 | — | ✔ | 53.000 | 54 | 63 | 133 | 70 | 0.246 | ✔ | – |
| xoan_oc | A* | manhattan | 1 | ✔ | ✔ | 286.000 | 287 | 287 | 287 | 0 | 0.572 | ✔ | ✔ |
| xoan_oc | A* | manhattan | 1.5 | ✔ | ✔ | 286.000 | 287 | 287 | 287 | 0 | 0.561 | ✔ | ✔ |
| xoan_oc | A* | manhattan | 2 | ✔ | ✔ | 286.000 | 287 | 287 | 287 | 0 | 0.559 | ✔ | ✔ |
| xoan_oc | A* | manhattan | 3 | ✔ | ✔ | 286.000 | 287 | 287 | 287 | 0 | 0.556 | ✔ | ✔ |
| xoan_oc | A* | manhattan | 2 | — | ✔ | 286.000 | 287 | 287 | 287 | 0 | 0.560 | ✔ | ✔ |
| xoan_oc | A* | manhattan | 3 | — | ✔ | 286.000 | 287 | 287 | 287 | 0 | 0.570 | ✔ | ✔ |
| dia_hinh | A* | manhattan | 1 | ✔ | ✔ | 128.000 | 72 | 1184 | 1483 | 181 | 3.767 | ✔ | ✔ |
| dia_hinh | A* | manhattan | 1.5 | ✔ | ✔ | 128.000 | 72 | 1106 | 1558 | 174 | 3.806 | ✔ | ✔ |
| dia_hinh | A* | manhattan | 2 | ✔ | ✔ | 129.000 | 74 | 1364 | 1956 | 241 | 5.041 | ✔ | – |
| dia_hinh | A* | manhattan | 3 | ✔ | ✔ | 145.000 | 72 | 136 | 245 | 103 | 0.485 | ✔ | – |
| dia_hinh | A* | manhattan | 2 | — | ✔ | 134.000 | 74 | 640 | 987 | 168 | 2.375 | ✔ | – |
| dia_hinh | A* | manhattan | 3 | — | ✔ | 145.000 | 72 | 132 | 240 | 102 | 0.467 | ✔ | – |

## TN5: 4 hướng so với 8 hướng

| Bản đồ | Thuật toán | h(n) | w | Mở lại | Tìm thấy | Chi phí | Ô | Duyệt | Sinh | \|OPEN\|max | Thời gian (ms) | Hợp lệ | Tối ưu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| vat_can_ngau_nhien | A* | manhattan | 1 | ✔ | ✔ | 69.000 | 70 | 127 | 189 | 54 | 0.412 | ✔ | ✔ |
| vat_can_ngau_nhien | A* | octile | 1 | ✔ | ✔ | 60.213 | 55 | 305 | 430 | 70 | 1.060 | ✔ | ✔ |
| dia_hinh | A* | manhattan | 1 | ✔ | ✔ | 128.000 | 72 | 1184 | 1483 | 181 | 3.789 | ✔ | ✔ |
| dia_hinh | A* | octile | 1 | ✔ | ✔ | 108.841 | 54 | 1172 | 1668 | 218 | 4.975 | ✔ | ✔ |
| me_cung | A* | manhattan | 1 | ✔ | ✔ | 104.000 | 105 | 111 | 112 | 1 | 0.242 | ✔ | ✔ |
| me_cung | A* | octile | 1 | ✔ | ✔ | 104.000 | 105 | 111 | 112 | 1 | 0.260 | ✔ | ✔ |
