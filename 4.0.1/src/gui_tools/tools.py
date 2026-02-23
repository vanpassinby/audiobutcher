import sys
import shutil
import audio

from gui_tools.tools_misc import *
from gui_tools.tools_preset import open_preset
from gui_tools.tools_slices import read_slc_file
from gui_tools.tools_scramble import load_audio
import gui.filetypes as fts
import tkinter.messagebox as mb
import tkinter.filedialog as fd

from loc_tools import override_loc
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui_main import MainWindow


def about_box():
    description = loc["meta"]["credit_ab"].format(
        AB=meta.name, VERSION=meta.version, VER_NOTE=meta.ver_note,
        REL_MONTH=loc["meta"]["months"][meta.rel_month-1], REL_YEAR=meta.rel_year) + "\n\n" + \
        loc["meta"]["credit_team"].format(TEAM=meta.credit_team) + "\n\n" + \
        (loc["loc_credit"] + "\n\n" if loc["loc_credit"] else "") + \
        loc["meta"]["credit_python"].format(PY_VERSION=sys.version)

    mb.showinfo(meta.full_name, description)


def audio_information(window: "MainWindow"):
    aud = window.state.audio
    m_loc = loc["audio_information"]

    if not isinstance(aud, audio.Audio):
        return

    report = [""] * 6
    report[0] = f"{m_loc['path']}{os.path.abspath(window.state.cur_config.audio_path)}\n"
    report[1] = f"{m_loc['sample_rate']}{aud.sample_rate}"
    report[2] = f"{m_loc['sample_format']}{aud.data.dtype}"
    report[3] = f"{m_loc['channels']}{aud.channels}"
    if aud.channels == 1 or aud.channels == 2:
        report[3] += m_loc["ch_mono" if aud.channels == 1 else "ch_stereo"]
    report[4] = f"{m_loc['length_sec']}{aud.length / aud.sample_rate :.3f} {loc['meta']['time']['sec_long']}"
    report[5] = f"{m_loc['length_samp']}{aud.length}"

    mb.showinfo(m_loc["title"], "\n".join(report), parent=window.root)


def locate_ffmpeg(window: "MainWindow"):
    path = fd.askdirectory(initialdir=window.state.sav_config.get("ffmpeg_path"))
    if not path:
        return

    window.state.sav_config.set("ffmpeg_path", path)
    upd_ffmpeg_path(window)

    if not (shutil.which("ffmpeg", path=path) or shutil.which("ffprobe", path=path)):
        mb.showwarning(loc["top_menu"]["preferences"]["locate_ffmpeg"],
                       loc["messages"]["warn_ffmpeg_update"],
                       parent=window.root)


def locate_localization(window: "MainWindow"):
    loc_path_curr = window.state.sav_config.get("localization_path")
    loc_path = fd.askopenfilename(filetypes=fts.ext_localization, initialdir=os.path.dirname(loc_path_curr))
    if not loc_path:
        return

    try:
        override_loc(loc_path, failsafe=False)
    except Exception as e:
        window.py_error(loc["messages"]["loc_cant_load"], e)
        return

    window.state.sav_config.set("localization_path", loc_path)
    mb.showinfo(loc["messages"]["loc_title"], loc["messages"]["loc_success"])


def reset_localization(window: "MainWindow"):
    window.state.sav_config.set("localization_path", "")
    mb.showinfo(loc["messages"]["loc_title"], loc["messages"]["loc_success"])


def upd_ffmpeg_path(window: "MainWindow"):
    audio.FFMPEG_PATH = window.state.sav_config.get("ffmpeg_path")


def restore_last_seed(window: "MainWindow"):
    if window.state.cur_config.last_seed:
        window.f_common.x_use_seed.set(1)
        window.f_common.e_seed.set(window.state.cur_config.last_seed)
        window.f_common.update()


def abort_confirm(window: "MainWindow"):
    sr = window.state.audio.sample_rate
    in_sec = window.state.get_pref_var("audio_length_in_seconds")

    current = audio_length_str(window.state.scr_progress[0], sr, in_sec)
    target = audio_length_str(window.state.scr_progress[1], sr, in_sec)
    progress = window.state.scr_progress[0] / window.state.scr_progress[1]

    return mb.askyesno(loc["messages"]["scr_abort_title"],
                       loc["messages"]["scr_abort_confirm"]
                       .format(CURRENT=current, TARGET=target, PROGRESS=progress),
                       icon="warning")


def dnd_open_file(window: "MainWindow", path, aud_load_alter_slices=True):
    rem_path = window.state.get_pref_var("remember_dnd_path")
    ext = os.path.splitext(path)[1].lower()

    if os.path.isdir(path) or not os.path.exists(path):
        pass
    elif ext in (".ab4", ".ab3", ".abp"):
        open_preset(window, path, rem_path)
    elif ext in (".ab_slices", ".abo"):
        read_slc_file(window, path, 0, rem_path)
    elif ext in (".ab_slices_alt", ".sto"):
        read_slc_file(window, path, 1, rem_path)
    else:
        run(load_audio, window, path, rem_path, aud_load_alter_slices)
