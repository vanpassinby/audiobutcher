import numpy as np
from gui.gui_common import tk, ttk
from gui.tools_misc import apply_window_style
from PIL import Image, ImageTk, ImageDraw
from common import *


def kernel(u):
    return np.exp(-0.5 * u ** 2) / np.sqrt(2 * np.pi)


def get_histogram(data: np.array, width=400, height=100, top_padding=5):
    # Returns: Image, Mean, Median, Mode, X min, X max

    data_mean = np.mean(data)
    data_std_dev = np.std(data)
    if not AB_VISUAL_ONSETS_ALL:
        filter_short = data >= data_mean - data_std_dev * 2
        filter_long = data <= data_mean + data_std_dev * 2
        data = data[filter_short & filter_long]
        del filter_short, filter_long

    bandwidth = 1.06 * data_std_dev * len(data) ** (-0.2)
    x_min, x_max = data.min(), data.max()
    x_width = max(1, x_max-x_min)
    x_vals = np.linspace(x_min, x_max, width)

    density = np.zeros_like(x_vals)
    for xi in data:
        density += kernel((x_vals - xi) / bandwidth)
    density /= (len(data) * bandwidth)
    y_vals = density / density.max() * (height - top_padding)

    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    points = [(i, height-y) for i, y in enumerate(y_vals)]
    polygon = [(0, height)] + points + [(width - 1, height)]
    draw.polygon(polygon, fill=(100, 160, 240))

    mean = data_mean
    median = np.median(data)
    mode_x = x_vals[np.argmax(density)]

    lines = [
        (mean, (255, 0, 0)),
        (median, (0, 128, 0)),
        (mode_x, (0, 0, 255)),
    ]

    for x_val, color in lines:
        x_pos = int((x_val - x_min) / x_width * (width - 1))
        draw.line([(x_pos, 0), (x_pos, height)], fill=color, width=2)

    return [image, mean, median, mode_x, x_min, x_max]


def slice_stats_window(parent, is_alt, lengths, sample_rate):
    def mouse_move(event):
        pos_scale = (event.x - 1) / (image.winfo_width() - 2)
        stamp = x_min + (x_max - x_min) * pos_scale
        text_label.configure(text=f"{stamp:.1f} ms")

    sr_k = 1000 / sample_rate
    hist_data = get_histogram(lengths)
    for i in range(1, len(hist_data)):
        hist_data[i] *= sr_k
    histogram, mean, median, mode_x, x_min, x_max = hist_data
    amount = len(lengths)
    min_val = np.min(lengths) * sr_k
    max_val = np.max(lengths) * sr_k

    root = tk.Toplevel(parent)
    root.title("Alternative slices" if is_alt else "Slices")
    apply_window_style(root)
    root.grab_set()
    root.focus_force()

    surface = ttk.Frame(root, padding=5)
    surface.pack()

    tk_image = ImageTk.PhotoImage(histogram)
    image = tk.Label(surface, image=tk_image, borderwidth=1, relief="solid")
    image.image = tk_image
    image.grid(row=0, column=0, columnspan=2, sticky="w")

    text_label = ttk.Label(surface)
    text_label.grid(row=1, column=1, sticky="e")

    ttk.Label(surface, text=f"Total {amount} slices").grid(row=1, column=0, sticky="w")
    ttk.Label(surface, text=f"Mean: {mean:.1f} ms (RED)").grid(row=2, column=0, sticky="w")
    ttk.Label(surface, text=f"Median: {median:.1f} ms (GREEN)").grid(row=3, column=0, sticky="w")
    ttk.Label(surface, text=f"Mode: {mode_x:.1f} ms (BLUE)").grid(row=4, column=0, sticky="w")
    ttk.Label(surface, text=f"Shortest slice: {min_val:.1f} ms").grid(row=5, column=0, sticky="w")
    ttk.Label(surface, text=f"Longest slice: {max_val:.1f} ms").grid(row=6, column=0, sticky="w")

    ttk.Button(surface, text="OK", command=root.destroy).grid(row=6, column=1, sticky="e")
    root.bind("<Escape>", lambda event: root.destroy())
    root.bind("<Return>", lambda event: root.destroy())
    image.bind("<Motion>", mouse_move)
    image.bind("<Leave>", lambda event: text_label.configure(text=""))
