"""
capture_gui.py - Chụp ảnh màn hình THẬT của giao diện mô phỏng A*.

Ảnh chụp được dùng làm hình minh hoạ trong báo cáo BTL (thư mục docs/screenshots/).
Yêu cầu môi trường có desktop thật (Windows). Chạy:

    <python-có-Pillow> tools/capture_gui.py
"""

from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk

from PIL import ImageGrab

import gui
from gui import AStarApp, VIEW_MODES
from astar.maps import sample_maps

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "screenshots")
os.makedirs(OUT, exist_ok=True)

# Chặn hộp thoại modal làm treo kịch bản tự động
gui.messagebox.showinfo = lambda *a, **k: None
gui.messagebox.showerror = lambda *a, **k: None

root = tk.Tk()
app = AStarApp(root)
root.geometry("1500x920+20+20")
root.update()
root.lift()
try:
    root.attributes("-topmost", True)
except Exception:
    pass


def pump(n: int = 200, delay: float = 0.004) -> None:
    for _ in range(n):
        root.update()
        time.sleep(delay)


def grab_window(win: tk.Misc, path: str, pad: int = 0) -> str:
    """Chụp đúng vùng cửa sổ: chụp toàn màn hình rồi cắt theo khung cửa sổ.

    Cách này tránh mọi sai lệch do scaling/DPI giữa toạ độ Tk và pixel màn hình.
    """
    win.update_idletasks()
    win.update()
    win.lift()
    time.sleep(0.5)
    x = win.winfo_rootx() - pad
    y = win.winfo_rooty() - pad
    w = win.winfo_width() + 2 * pad
    h = win.winfo_height() + 2 * pad
    full = ImageGrab.grab(all_screens=True)          # (0,0) đến hết màn hình, pixel thật
    sx = full.size[0] / max(1, win.winfo_screenwidth())
    sy = full.size[1] / max(1, win.winfo_screenheight())
    shot = full.crop((int(x * sx), int(y * sy), int((x + w) * sx), int((y + h) * sy)))
    shot.save(path)
    print(f"  ✓ {os.path.basename(path)}  {shot.size[0]}x{shot.size[1]}  "
          f"{os.path.getsize(path):,} B  (scale {sx:.2f}x{sy:.2f}, "
          f"cell={app.cell}, canvas={app.canvas.winfo_width()}x{app.canvas.winfo_height()})")
    return path


maps = {m.key: m for m in sample_maps()}


def load(key: str) -> None:
    """Nạp bản đồ mẫu rồi canh lại cỡ ô cho lưới lấp đầy khung vẽ."""
    app._load_sample(maps[key])
    root.update()
    app.fit_cells()
    root.update()


print("1) Tổng quan giao diện (A* trên mê cung, đã tìm xong đường):")
load("me_cung")
app.speed.set(200)
app.run()
pump(900)
grab_window(root, os.path.join(OUT, "01_tong_quan_giao_dien.png"), pad=4)

print("2) Trạng thái ĐANG mô phỏng, dừng giữa chừng (tập OPEN/CLOSED đang lan ra):")
load("vat_can_ngau_nhien")
# Tiến từng bước cố định để dừng đúng lúc tìm kiếm chưa xong
app.clear_search()
for _ in range(150):
    app.step_once()
root.update()
grab_window(root, os.path.join(OUT, "02_dang_mo_phong_open_closed.png"), pad=4)

print("3) Hộp thoại so sánh 4 thuật toán:")
load("phong_hanh_lang")
app.compare_all()
pump(80)
top = [w for w in root.winfo_children() if isinstance(w, tk.Toplevel)]
if top:
    dlg = top[-1]
    dlg.lift()
    try:
        dlg.attributes("-topmost", True)
    except Exception:
        pass
    grab_window(dlg, os.path.join(OUT, "03_so_sanh_4_thuat_toan.png"), pad=6)
    dlg.destroy()

print("4) Lưới có trọng số địa hình (chi phí 2/4/6) và bảng số liệu:")
load("dia_hinh")
app.diagonal.set(True)
app._on_toggle_diagonal()
app.speed.set(200)
app.run()
pump(900)
grab_window(root, os.path.join(OUT, "04_dia_hinh_trong_so.png"), pad=4)

print("5) Tab hướng dẫn và chú thích màu:")
load("xoan_oc")
app.diagonal.set(False)
app._on_toggle_diagonal()
nb = None
for child in root.winfo_children():
    for sub in child.winfo_children():
        if isinstance(sub, gui.ttk.Notebook):
            nb = sub
if nb is not None:
    nb.select(2)
pump(40)
grab_window(root, os.path.join(OUT, "05_huong_dan_va_chu_thich.png"), pad=4)

root.destroy()
print("\nHoàn tất chụp ảnh giao diện ->", OUT)

