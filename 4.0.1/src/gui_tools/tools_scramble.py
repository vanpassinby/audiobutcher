import audio
import scrambler.scr_main as scrambler
from scrambler.scr_state import ScramblerState

from gui_tools.tools_misc import *
from gui_tools.tools_slices import detect_slices
from gui_tools.export_dialog import DlgExport
from gui_tools.cfg_check import check_wrong_config, check_ram_overflow
import tkinter.messagebox as mb

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui_main import MainWindow


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
        window.py_error(def_error("audio_import"), e)
        success = False

    window.update_global()

    if success:
        run(mb.showinfo, loc["messages"]["aud_import_title"],
            loc["messages"]["aud_import_success"], parent=window.root)

        if alter_slices:
            if window.state.get_pref_var("slices_auto"):
                detect_slices(window, selection=0)

            if window.state.get_pref_var("slices_alt_auto"):
                detect_slices(window, selection=1)

    window.u_progressbar.configure(mode="determinate")
    window.u_progressbar.stop()


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
                open_file = mb.askyesno(loc["messages"]["scr_complete_title"],
                                        loc["messages"]["scr_complete_success"],
                                        default="no", icon="info")

                if open_file:
                    try:
                        if window.state.get_pref_var("open_scr_folder") and not (OS_IS_UNIX or OS_IS_OTHER):
                            open_d(options["path"])
                        else:
                            open_f(options["path"])
                    except Exception as e:
                        window.py_error(def_error("file_open"), e)

                return

            else:
                message_bump()
                return

        except Exception as e:
            retry = window.py_error(def_error("audio_export"), e, b_retry=True)
            if retry:
                options = DlgExport(window, ask_length=False).result
                if not options:
                    return
            else:
                return


def s_partial_info(window: "MainWindow", scr_state: ScramblerState, options: dict):
    sr = scr_state.audio.sample_rate
    in_sec = window.state.get_pref_var("audio_length_in_seconds")

    done = audio_length_str(scr_state.scr_position, sr, in_sec)
    target = audio_length_str(options["length"], sr, in_sec)
    perc = scr_state.scr_position / options["length"]

    mb.showinfo(loc["messages"]["scr_partial_title"],
                loc["messages"]["scr_partial_complete"]
                .format(CURRENT=done, TARGET=target, PROGRESS=perc), parent=window.root)


def s_play_preview(window: "MainWindow", slicecr: audio.Audio):
    window.state.now_previewing = True
    window.update_header()

    try:
        to_mono = slicecr.channels > 2
        new_sr = min(audio.PLAY_SUPPORTED, key=lambda x: abs(x-slicecr.sample_rate))

        slicecr.refactored(to_mono, new_sr).play().wait_done()

    except Exception as e:
        window.py_error(def_error("preview"), e)

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
        window.py_error(def_error("config_read"), e)
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
        window.py_error(def_error("scramble"), e)
        s_finish(window, reset=True)
        return

    # Scramble
    begin_time = time.time()
    scrambler.scramble(scr_state, window.state, window.set_progress,
                       lambda exc: window.py_error(def_error("scramble"), exc, b_retry=True))
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
