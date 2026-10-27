"""Smoke test giao diện: khởi tạo app, chạy mô phỏng, kiểm tra các luồng chính."""
import sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import tkinter as tk
import gui
from gui import AStarApp, VIEW_MODES
from astar.maps import sample_maps

# Vô hiệu hoá hộp thoại modal để test tự động không bị treo
gui.messagebox.showinfo = lambda *a, **k: None
gui.messagebox.showerror = lambda *a, **k: None
gui.filedialog.askopenfilename = lambda *a, **k: ""
gui.filedialog.asksaveasfilename = lambda *a, **k: ""

def log(*a):
    print(*a, flush=True)

root = tk.Tk()
app = AStarApp(root)
root.update()

def pump(n=400, delay=0.001):
    for _ in range(n):
        root.update()
        time.sleep(delay)

# 1) chạy mô phỏng đầy đủ
app.run()
pump(600)
root.update()
log("run + finished:", app.finished, "| found:", bool(app.result and app.result.found),
      "| path:", len(app.path), "| expanded:", len(app.closed))

# 2) từng bước
app.clear_search(); app.step_once(); pump(30)
log("step_once ok, closed =", len(app.closed))

# 3) tắt/bật đi chéo
app.diagonal.set(True); app._on_toggle_diagonal(); pump(20)
log("diagonal =", app.grid.diagonal, "| h =", app.heuristic.get())
app.diagonal.set(False); app._on_toggle_diagonal(); pump(20)

# 4) đổi thuật toán
for m in VIEW_MODES:
    app.algorithm.set(m); app._on_algo_change(); pump(10)
    app.clear_search(); app.run(); pump(300)
    log(f"  {m:20} -> finished={app.finished} "
          f"found={bool(app.result and app.result.found)}")

# 5) nạp cả 6 bộ dữ liệu mẫu
for mp in sample_maps():
    app._load_sample(mp); pump(15)
    app.run(); pump(900)
    log(f"  map {mp.key:18} ok, cells_drawn={len(app.items)}")

# 6) sinh bản đồ
app.gen_random(); pump(20)
app.gen_maze(); pump(20)
app.gen_empty(); pump(20)
log("gen random/maze/empty ok")

# 7) zoom + fit
app.zoom(+4); app.zoom(-6); app.fit_cells(); pump(40)
log("cell size =", app.cell)

# 8) so sánh 4 thuật toán + xuất CSV
app.compare_all(); pump(60)
for w in root.winfo_children():
    if isinstance(w, tk.Toplevel):
        w.destroy()
app.export_csv()
for w in root.winfo_children():
    if isinstance(w, tk.Toplevel):
        w.destroy()
pump(20)
log("compare_all ok, last_results =", len(app.last_results))

# 9) chạm chuột: vẽ tường, tô địa hình, đặt start/goal
class E:  # đối tượng giả lập sự kiện chuột
    def __init__(self, x, y): self.x, self.y = x, y
c = app.cell
app.tool.set("wall"); app._on_paint(E(3 * c + 2, 3 * c + 2))
app.tool.set("terrain"); app._on_paint(E(5 * c + 2, 5 * c + 2))
app.tool.set("start"); app._on_paint(E(2 * c + 2, 2 * c + 2))
app.tool.set("goal"); app._on_paint(E(6 * c + 2, 6 * c + 2))
app._on_paint(E(3 * c + 2, 3 * c + 2), erase=True)
app._on_hover(E(4 * c + 2, 4 * c + 2))
log("mouse tools ok | start/weight:", app.start, app.grid.weight((5, 5)))

root.destroy()
log("SMOKE GUI: OK")

