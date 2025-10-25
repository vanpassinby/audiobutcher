import sys
import shutil

import audio
import scrambler.scr_main as scrambler
from scrambler.scr_state import ScramblerState
from preset import PresetOpen, PresetSave
from convert_ab2 import convert_ab2
from convert_ab3 import convert_ab3

from gui.tools_misc import *
from gui.export_dialog import DlgExport
from gui.slice_detect import detect_slices, read_slc_file
from gui.cfg_check import check_wrong_config, check_ram_overflow
import tkinter.messagebox as mb

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui_main import MainWindow


def about_box():
    mb.showinfo(meta.title, meta.description.format(sys.version))


def audio_information(window: "MainWindow"):
    aud = window.state.audio

    if not isinstance(aud, audio.Audio):
        return

    report = ""
    report += f"Path: {os.path.abspath(window.state.cur_config.audio_path)}\n\n"
    report += f"Sample rate: {aud.sample_rate}\n"
    report += f"Sample format: {aud.data.dtype}\n"
    report += f"Channels: {aud.channels}" + {1: " (Mono)", 2: " (Stereo)"}.get(aud.channels, "") + "\n"
    report += f"Length: {aud.length / aud.sample_rate} seconds\n"
    report += f"Length (samples): {aud.length}"

    mb.showinfo("Audio information", report, parent=window.root)


def locate_ffmpeg(window: "MainWindow"):
    path = fd.askdirectory(initialdir=window.state.sav_config.get("ffmpeg_path"))
    if not path:
        return

    window.state.sav_config.set("ffmpeg_path", path)
    upd_ffmpeg_path(window)

    if not (shutil.which("ffmpeg", path=path) or shutil.which("ffprobe", path=path)):
        mb.showwarning("Locate FFmpeg folder", "Parameters have been updated. However, the selected folder does not contain FFmpeg or FFprobe, so imports may fail.",
                       parent=window.root)


def upd_ffmpeg_path(window: "MainWindow"):
    audio.FFMPEG_PATH = window.state.sav_config.get("ffmpeg_path")


def restore_last_seed(window: "MainWindow"):
    if window.state.cur_config.last_seed:
        window.f_common.x_use_seed.set(1)
        window.f_common.e_seed.set(window.state.cur_config.last_seed)
        window.f_common.update()


def abort_confirm(window: "MainWindow"):
    text = "Are you sure you want to abort scrambling?\n"\
        "The current rendered length is {} out of {} ({:.1%}).\n"\
        "If you abort, scrambling cannot be resumed.\n"\
        "The audio will still be exported or previewed."

    sr = window.state.audio.sample_rate
    a = audio_length_str(window.state.scr_progress[0], sr)
    b = audio_length_str(window.state.scr_progress[1], sr)
    p = window.state.scr_progress[0] / window.state.scr_progress[1]

    return mb.askyesno("Abort", text.format(a, b, p), icon="warning")


def load_audio(window: "MainWindow", path=None, rem_path=True, alter_slices=True):
    if not path:
        path = get_audio_path(window)
        if not path:
            return

    if rem_path:
        window.state.sav_config.set("dir_audio", os.path.dirname(path))

    s_finish(window, reset=True)
    window.u_progressbar.configure(mode="indeterminate")
    window.u_progressbar.start()

    try:
        if window.state.get_pref_var("slices_erase") and alter_slices:
            window.state.slices.erase()
            window.state.slices_alt.erase()
        window.state.audio = None
        window.update_gui()
        window.state.load_audio(path)
        success = True

    except Exception as e:
        window.py_error("Import", meta.def_error.format("importing audio"), e)
        success = False

    window.update_global()

    if success:
        run(mb.showinfo, "Import", "Audio imported successfully.", parent=window.root)

        if alter_slices:
            if window.state.get_pref_var("slices_auto"):
                detect_slices(window, 0, silent=True)

            if window.state.get_pref_var("slices_alt_auto"):
                detect_slices(window, 1, silent=True)

    window.u_progressbar.configure(mode="determinate")
    window.u_progressbar.stop()


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

# Opening preset

def preset_warning(p_version, ab_version):
    mb.showwarning("Warning", f"This preset was created using an unknown version of AudioButcher ({p_version}). It will be opened as a {ab_version} preset. Some parameters may be corrupted or lost.")


def preset_back_comp_check(preset: PresetOpen, path=""):
    vers_ab2 = ("2.1.0", "2.1.1", "2.2.0", "2.2.1.00", "2.2.2.00", "2.2.3.00")
    vers_ab3 = ("3.0.0", "3.0.1", "3.1.0")
    vers_ab4 = ("4.0.0",)

    preset.check_ab3()
    ext = os.path.splitext(path)[1].lower()

    version = preset.get("version", "2.1.0" if ext == ".abp" else "Not specified")
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
        return preset


def open_preset(window: "MainWindow", path=None, rem_path=True):
    if not path:
        directory = window.state.sav_config.get("dir_presets")

        path = fd.askopenfilename(filetypes=meta.ext_preset_all, initialdir=directory)
        if not path:
            return

    window.state.cur_config.last_preset_name = simple_file_name(path)
    if rem_path:
        window.state.sav_config.set("dir_presets", os.path.dirname(path))

    try:
        preset = PresetOpen(path=path)
        preset = preset_back_comp_check(preset, path=path)
        window.open_preset(preset)

    except Exception as e:
        window.py_error("Preset", meta.def_error.format("opening preset"), e)

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

    path = fd.asksaveasfilename(defaultextension=meta.ext_preset, filetypes=meta.ext_preset,
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
        window.py_error("Preset", meta.def_error.format("saving preset"), e)

# Scrambling

def s_finish(window: "MainWindow", reset=False):
    if reset:
        window.state.scr_state = None

    if window.state.scr_state:
        window.state.scr_state.config = None
        window.set_progress(window.state.scr_state.scr_position, window.state.scr_state.target_length)
    else:
        window.set_progress(0, -1)

    window.state.now_scrambling = False
    window.state.force_abort = False  # Not sure if this is where it should be

    window.update_global()


def s_try_export(window: "MainWindow", scr_state: ScramblerState, options: dict, show_msg=True):
    while True:
        try:
            scr_state.slicecr.write(options["path"], options["format"])

            if show_msg:
                open_file = mb.askyesno("Complete!",
                                        "Scrambling complete.\nDo you want to open your file now?",
                                        default="no", icon="info")

                if open_file:
                    try:
                        if window.state.get_pref_var("open_scr_folder") and not (OS_IS_UNIX or OS_IS_OTHER):
                            open_d(options["path"])
                        else:
                            open_f(options["path"])
                    except:
                        mb.showerror("Open file", "Failed.")

                return

            else:
                message_bump()
                return

        except Exception as e:
            retry = window.py_error("Export", meta.def_error.format("exporting audio"), e, b_retry=True)
            if retry:
                options = DlgExport(window, ask_length=False).result
                if not options:
                    return
            else:
                return


def s_partial_info(window: "MainWindow", scr_state: ScramblerState, options: dict):
    sr = scr_state.audio.sample_rate
    done = audio_length_str(scr_state.scr_position, sr)
    target = audio_length_str(options["length"], sr)
    perc = scr_state.scr_position / options["length"]
    mb.showinfo("Partial generation",
                "Generated {} of {} ({:.1%}).\nAdjust settings if needed, then click 'Continue'."
                .format(done, target, perc), parent=window.root)


def s_play_preview(window: "MainWindow", slicecr: audio.Audio):
    window.state.now_previewing = True
    window.update_header()

    try:
        to_mono = slicecr.channels > 2
        new_sr = min(audio.PLAY_SUPPORTED, key=lambda x: abs(x-slicecr.sample_rate))

        slicecr.refactored(to_mono, new_sr).play().wait_done()

    except Exception as e:
        window.py_error("Preview", meta.def_error.format("previewing"), e)

    window.state.now_previewing = False
    window.update_header()


def stop_preview():
    if not AB_DISABLE_SIMPLEAUDIO:
        simpleaudio.stop_all()


def scramble(window: "MainWindow", preview=False):
    # Flag check
    if window.state.now_scrambling or (preview and window.state.now_previewing):
        return
    window.state.now_scrambling = True
    window.update_header()

    # Apply config
    try:
        scr_config = window.get_config()
    except Exception as e:
        window.py_error("Scrambling", meta.def_error.format("reading configuration"), e)
        s_finish(window)
        return

    # Checks
    if check_wrong_config(window, window.state, scr_config):
        s_finish(window)
        return

    # Getting export/preview options
    if preview:
        options = {
            "length": int(window.state.cur_config.len_preview.get() * window.state.audio.sample_rate),
            "partial": 0,
        }
    else:
        options = DlgExport(window, auto_rewrite_confirmed=bool(window.state.scr_state)).result

    if (not options) or check_ram_overflow(options["length"], window.state.audio.channels):
        s_finish(window)
        return

    # Prepare
    if window.state.scr_state:
        prepare = False
        if preview:
            scr_state = window.state.scr_state.get_copy_for_preview(options["length"])
        else:
            scr_state = window.state.scr_state
    else:
        prepare = True
        scr_state = ScramblerState()
        if not preview:
            window.state.scr_state = scr_state

    scr_state.config = scr_config
    scr_state.target_length = options["length"]
    if preview or options["partial"] <= 0:
        scr_state.current_goal = scr_state.target_length
    else:
        scr_state.current_goal = options["partial"]

    try:
        if prepare:
            window.state.cur_config.last_seed = scr_config.seed
            scrambler.prepare(scr_state, window.state)
        scrambler.prepare_ii(scr_state)
    except Exception as e:
        window.py_error("Scrambling", meta.def_error.format("scrambling"), e)
        s_finish(window, reset=True)
        return

    # Scramble
    begin_time = time.time()
    scrambler.scramble(scr_state, window.state, window.set_progress, window.py_error)
    print(f"Scrambled in {(time.time() - begin_time):.3f} seconds.")

    # Export / Preview
    finished = preview or scr_state.scr_position >= options["length"] or window.state.force_abort or scr_state.failed

    if scr_state.scr_position <= 0:
        s_finish(window, reset=(not preview))
        return

    if finished:
        scr_state.slicecr.crop(0, min(scr_state.scr_position, options["length"]))
        scr_state.slicecr.fix_range()

    if scr_state.warnings:
        warn_text = "\n".join(f"{k}: {v}" for k, v in scr_state.warnings.items())
        mb.showwarning("Warnings", warn_text)

    if preview:
        run(s_play_preview, window, scr_state.slicecr)
    else:
        show_msg = not window.state.get_pref_var("disable_completion_dialog")
        if finished:
            s_try_export(window, scr_state, options, show_msg)
        elif show_msg:
            s_partial_info(window, scr_state, options)
        else:
            message_bump()

    s_finish(window, reset=(finished and not preview))
