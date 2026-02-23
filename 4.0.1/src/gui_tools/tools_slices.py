import slicing
import numpy as np
from audio import Audio
from scrambler.scr_main import calc_trim_pos
from configparser import RawConfigParser

from gui_tools.tools_misc import *
from gui_tools.visual_stat import slice_stats_window
import tkinter.messagebox as mb

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui_main import MainWindow


def file_to_slices(file_path: str):
    rcp = RawConfigParser()
    try:
        rcp.read(file_path, encoding="utf-8")
    except: # Fallback: Read in old format
        return file_to_slices_old(file_path)

    sample_rate = rcp.get("Slices", "sample_rate", fallback="ERROR")
    onsets = rcp.get("Slices", "onsets", fallback="ERROR")

    sample_rate = int(sample_rate.strip())
    onsets = list(map(int, onsets.split()))

    return slicing.Onsets(onsets, sample_rate)


def file_to_slices_old(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        onsets = list(map(float, file.read().split()))

    return slicing.Onsets(onsets, 1000)


def read_slc_file(window: "MainWindow", path=None, selection=None, rem_path=True):
    try:
        # Choose file
        if path is None:
            initial_dir = window.state.sav_config.get("dir_slices")
            path = fd.askopenfilename(filetypes=fts.ext_slices_all, initialdir=initial_dir)

            if not path:
                return

        if rem_path:
            window.state.sav_config.set("dir_slices", os.path.dirname(path))

        # Apply
        onsets = file_to_slices(path)
        window.f_slice_detect.get_selected_slices(selection).override(onsets)
        window.update_gui()

    except Exception as e:
        window.py_error(def_error("slice_open"), e)


def write_slc_file(window: "MainWindow", slices=None, ext=None, parent=None):
    try:
        # Get slices
        if slices and ext:
            slices: slicing.Onsets = slices
        else:
            selection = window.f_slice_detect.get_selection()
            if selection == 0:
                slices = window.state.slices
                ext = fts.ext_slices
            elif selection == 1:
                slices = window.state.slices_alt
                ext = fts.ext_slices_alt
            else:
                return

        # Get path
        initial_dir = window.state.sav_config.get("dir_slices")
        path = fd.asksaveasfilename(defaultextension=ext, filetypes=ext, initialdir=initial_dir)
        if not path:
            return
        window.state.sav_config.set("dir_slices", os.path.dirname(path))

        content = "[Slices]\nsample_rate = {}\nonsets = {}".format(
            slices.sample_rate, " ".join(str(o) for o in slices.onsets)
        )
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

    except Exception as e:
        window.py_error(def_error("slice_save"), e, parent=parent)


def detect_slices(window: "MainWindow", selection=None, from_current=True):
    try:
        root = window.f_slice_detect
        if selection is None:
            selection = root.get_selection()

        method = root.values[selection][0]
        onset_function = slicing.METHODS[method][1]
        sens_arg = {} if not slicing.METHODS[method][2] else {"sens": float(root.values[selection][1])}

        if from_current:
            audio = window.state.audio
        else:
            audio_path = get_audio_path(window)
            if not audio_path:
                return
            audio = Audio.load(audio_path)

        slices = onset_function(audio, **sens_arg)
        root.get_selected_slices(selection).override(slices)

        window.update_gui()
        slc_type = loc["slice_detection"]["slice_types"]["alt_slices" if selection == 1 else "slices"]
        run(mb.showinfo, loc["slice_detection"]["msg_onsets_title"],
            loc["slice_detection"]["msg_onsets_detected"].format(N_ONS=slices.amount, SLC_TYPE=slc_type),
            parent=window.root)

    except Exception as e:
        window.py_error(def_error("slice_detection"), e)


def erase_slices(window: "MainWindow"):
    window.f_slice_detect.get_selected_slices().erase()
    window.update_gui()


def show_slice_stats(window: "MainWindow"):
    ui_trim = window.f_tweak.trim
    selection = window.f_slice_detect.get_selection()
    slices = window.f_slice_detect.get_selected_slices(selection)
    if selection == 0:
        shift = ui_trim.x_trim_slices.get()
    elif selection == 1:
        shift = ui_trim.x_trim_slices2.get()
    else:
        return

    if window.state.audio:
        sample_rate = window.state.audio.sample_rate
        mult = 1000 if window.f_common.x_use_seconds.get() else 1

        t1 = 0 if not ui_trim.x_trim1.get() else float(ui_trim.e_trim1.get()) * mult
        t2 = 0 if not ui_trim.x_trim2.get() else float(ui_trim.e_trim2.get()) * mult
        t1, t2 = calc_trim_pos(window.state.audio, t1, t2)
        if t1 >= t2:
            return

    else:
        t1 = 0
        t2 = slices.onsets.max()
        sample_rate = slices.sample_rate

    slices_np = slicing.convert_onsets(slices, t1*shift, sample_rate, t2-t1)
    slice_stats_window(window.root, (selection == 1), np.diff(slices_np), sample_rate,
                       visual_onsets_all=window.state.get_pref_var("visual_onsets_all"))
