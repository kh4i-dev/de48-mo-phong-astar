"""Kiểm tra dung lượng, tỉ lệ khung và cỡ chữ hiệu dụng của ảnh khi chèn vào A4."""
import glob
import os
import sys

from PIL import Image

TEXT_WIDTH_PT = 439.0   # bề rộng vùng in A4 với lề 3.5/2 cm

for folder, label in (("docs/diagrams/images", "SƠ ĐỒ"), ("docs/figures", "BIỂU ĐỒ"),
                      ("docs/screenshots", "ẢNH CHỤP")):
    files = sorted(glob.glob(os.path.join(folder, "*.png")))
    if not files:
        continue
    print(f"=== {label} ({folder}) ===")
    for p in files:
        im = Image.open(p)
        w, h = im.size
        ratio = w / h if h else 0
        flag = ""
        if ratio > 2.4 or ratio < 0.28:
            flag = "  <-- TỈ LỆ KHUNG XẤU"
        print(f"  {os.path.basename(p):42} {w:5}x{h:<5} ratio={ratio:5.2f} "
              f"{os.path.getsize(p)//1024:5}KB{flag}")
    print()
