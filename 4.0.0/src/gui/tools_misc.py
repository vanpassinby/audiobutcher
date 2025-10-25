import time
import random
from threading import Thread

from common import *
from gui.gui_common import *
import tkinter.filedialog as fd


def run(function, *args, **kwargs):
    thread = Thread(target=function, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    return thread


def any_seed(length: int):
    symbols = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890-_"
    return "".join(random.choices(symbols, k=length))


def simple_file_name(path):
    return os.path.splitext(os.path.basename(path))[0]


def unix_filename():
    return f"untitled_{round(time.time())}"


def message_bump():
    if OS_IS_WINDOWS:
        winsound.MessageBeep(winsound.MB_ICONASTERISK)


def audio_length_str(len_samples: int, sample_rate: int, in_seconds=True):
    length = round(len_samples / sample_rate)
    if in_seconds:
        return f"{length}s"
    elif length > 3600:
        return f"{length//3600}:{length%3600//60:02d}:{length%60:02d}"
    else:
        return f"{length//60}:{length%60:02d}"


def apply_window_style(window, resize_w=False, resize_h=False):
    resize_w = AB_RESIZABLE_WINDOWS or resize_w
    resize_h = AB_RESIZABLE_WINDOWS or resize_h
    window.resizable(resize_w, resize_h)

    if not AB_DISABLE_ICON:
        icon = tk.PhotoImage(data=meta.icon_b64, format="png")
        window.iconphoto(True, icon)


def get_audio_path(window):
    directory = window.state.sav_config.get("dir_audio")

    if window.state.get_pref_var("show_ffmpeg_formats"):
        file_types = meta.ext_audio_import_more
    else:
        file_types = meta.ext_audio_import

    return fd.askopenfilename(filetypes=file_types, initialdir=directory)
