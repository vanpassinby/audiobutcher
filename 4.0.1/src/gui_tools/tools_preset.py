from preset import PresetOpen, PresetSave
from convert_ab2 import convert_ab2
from convert_ab3 import convert_ab3

from gui_tools.tools_misc import *
import tkinter.messagebox as mb

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui_main import MainWindow


def preset_warning(p_version, ab_version):
    if p_version is None:
        p_version = loc["messages"]["warn_preset_not_specified"]

    mb.showwarning(loc["messages"]["warning"], loc["messages"]["warn_preset_unknown"]
                   .format(VERSION=p_version, FALLBACK_VER=ab_version))


def preset_back_comp_check(preset: PresetOpen, path=""):
    vers_ab2 = ("2.1.0", "2.1.1", "2.2.0", "2.2.1.00", "2.2.2.00", "2.2.3.00")
    vers_ab3 = ("3.0.0", "3.0.1", "3.1.0")
    vers_ab4 = ("4.0.0", "4.0.1")

    preset.check_ab3()
    ext = os.path.splitext(path)[1].lower()

    version = preset.get("version", "2.1.0" if ext == ".abp" else None)
    unknown_vers = version not in (vers_ab2+vers_ab3+vers_ab4)

    if version in vers_ab2 or (unknown_vers and ext == ".abp"):
        if unknown_vers:
            preset_warning(version, "2.2.3")
        return convert_ab2(preset)

    elif version in vers_ab3 or (unknown_vers and ext == ".ab3"):
        if unknown_vers:
            preset_warning(version, "3.0.0")
        return convert_ab3(preset)

    else:
        if unknown_vers:
            preset_warning(version, meta.version)
        return preset, version


def fix_abpl400(window: "MainWindow", p_version):
    script = window.f_tweak.abpl.script

    if p_version == "4.0.0" and script:
        window.f_tweak.abpl.script = "!ABPL400\n\n" + script


def open_preset(window: "MainWindow", path=None, rem_path=True):
    if not path:
        directory = window.state.sav_config.get("dir_presets")

        path = fd.askopenfilename(filetypes=fts.ext_preset_all, initialdir=directory)
        if not path:
            return

    window.state.cur_config.last_preset_name = simple_file_name(path)
    if rem_path:
        window.state.sav_config.set("dir_presets", os.path.dirname(path))

    try:
        preset = PresetOpen(path=path)
        preset, version = preset_back_comp_check(preset, path=path)
        window.open_preset(preset)

        fix_abpl400(window, version)

    except Exception as e:
        window.py_error(def_error("preset_open"), e)

    window.update_gui()


def save_preset(window: "MainWindow"):
    directory = window.state.sav_config.get("dir_presets")

    if window.state.cur_config.last_preset_name:
        initial_file = window.state.cur_config.last_preset_name + ".ab4"
    else:
        if window.state.audio:
            initial_file = f"{simple_file_name(window.state.cur_config.audio_path)} preset.ab4"
        else:
            initial_file = None

    path = fd.asksaveasfilename(defaultextension=fts.ext_preset, filetypes=fts.ext_preset,
                                initialdir=directory, initialfile=initial_file)
    if not path:
        return

    window.state.cur_config.last_preset_name = simple_file_name(path)
    window.state.sav_config.set("dir_presets", os.path.dirname(path))

    try:
        preset = PresetSave()
        window.save_preset(preset)
        preset.write(path)

    except Exception as e:
        window.py_error(def_error("preset_save"), e)
