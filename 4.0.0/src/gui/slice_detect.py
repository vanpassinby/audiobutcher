import numpy as np
from common import *

from audio import Audio
from state import ABState
from slicing import Onsets
from scrambler.scr_main import calc_trim_pos
from configparser import RawConfigParser
import slicing

from gui.gui_common import *
from gui.tools_misc import run, get_audio_path, apply_window_style
from gui.visual_stat import slice_stats_window
import tkinter.messagebox as mb
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
from tkinter.scrolledtext import ScrolledText

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from gui.gui_main import MainWindow


METHODS = [
    # Name - Function - Is sens required
    ("Standard", slicing.detect_onsets_spectro, True),
    ("Amplitude - STE", slicing.detect_onsets_amp_ste, True),
    ("Amplitude - RMS", slicing.detect_onsets_amp_rms, True),
    ("Classic", slicing.detect_onsets_classic, False)
]

if AB_DISABLE_LIBROSA:
    del METHODS[3]
    del METHODS[0]


def file_to_slices(file_path: str):
    rcp = RawConfigParser()
    try:
        rcp.read(file_path, encoding="utf-8")
    except:
        return 0

    sample_rate = rcp.get("Slices", "sample_rate", fallback="ERROR")
    onsets = rcp.get("Slices", "onsets", fallback="ERROR")

    sample_rate = int(sample_rate.strip())
    onsets = list(map(int, onsets.split()))

    return Onsets(onsets, sample_rate)


def file_to_slices_old(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        onsets = list(map(float, file.read().split()))

    return Onsets(onsets, 1000)


def detect_slices(window: "MainWindow", selection=None, from_current=True, silent=False):
    try:
        root = window.f_slice_detect
        if not selection:
            selection = root.get_selection()

        method = root.values[selection][0]
        onset_function = METHODS[method][1]
        sens_arg = {} if not METHODS[method][2] else {"sens": float(root.values[selection][1])}

        if from_current:
            audio = window.state.audio
        else:
            audio_path = get_audio_path(window)
            if not audio_path:
                return
            audio = Audio.load(audio_path)

        slices = onset_function(audio, **sens_arg)
        root.get_selected_slices().override(slices)

        note_alt = "alternative " if selection == 1 else ""
        window.update_gui()
        run(mb.showinfo, "Slices", f"{slices.amount} onsets detected for {note_alt}slices.", parent=window.root)

    except Exception as e:
        if not silent:
            window.py_error("Slices", meta.def_error.format("detecting slices"), e)


def read_slc_file(window: "MainWindow", path=None, selection=None, rem_path=True):
    try:
        # Choose file
        if path is None:
            initial_dir = window.state.sav_config.get("dir_slices")
            path = fd.askopenfilename(filetypes=meta.ext_slices_all, initialdir=initial_dir)

            if not path:
                return

        if rem_path:
            window.state.sav_config.set("dir_slices", os.path.dirname(path))

        # Load file
        onsets = file_to_slices(path)
        if onsets == 0:  # Fallback: Read in old format
            onsets = file_to_slices_old(path)

        # Apply
        if not selection:
            selection = window.f_slice_detect.get_selection()
        if selection == 0:
            window.state.slices = onsets
        elif selection == 1:
            window.state.slices_alt = onsets
        window.update_gui()

    except Exception as e:
        window.py_error("Slices", meta.def_error.format("opening slices"), e)


def write_slc_file(window: "MainWindow", slices=None, ext=None, parent=None):
    try:
        # Get slices
        if slices and ext:
            slices: Onsets = slices
        else:
            selection = window.f_slice_detect.get_selection()
            if selection == 0:
                slices = window.state.slices
                ext = meta.ext_slices
            elif selection == 1:
                slices = window.state.slices_alt
                ext = meta.ext_slices_alt
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
        window.py_error("Slices", meta.def_error.format("saving slices"), e, parent=parent)


def erase_slices(window: "MainWindow"):
    window.f_slice_detect.get_selected_slices().erase()
    window.update_gui()


def show_slice_stats(window: "MainWindow"):
    ui_trim = window.f_tweak.trim
    selection = window.f_slice_detect.get_selection()
    if selection == 0:
        slices = window.state.slices
        shift = ui_trim.x_trim_slices.get()
    elif selection == 1:
        slices = window.state.slices_alt
        shift = ui_trim.x_trim_slices2.get()
    else:
        return

    mult = 1000 if window.f_common.x_use_seconds.get() else 1
    t1 = 0 if not ui_trim.x_trim1.get() else float(ui_trim.e_trim1.get()) * mult
    t2 = 0 if not ui_trim.x_trim2.get() else float(ui_trim.e_trim2.get()) * mult
    t1, t2 = calc_trim_pos(window.state.audio, t1, t2)
    if t1 >= t2:
        return

    sample_rate = window.state.audio.sample_rate
    slices = slicing.convert_onsets(slices, t1*shift, sample_rate, t2-t1)
    lengths = np.diff(slices)

    slice_stats_window(window.root, (selection == 1), lengths, sample_rate)


class SliceDetectionGui:
    def __init__(self, parent, glob_state: ABState):
        self.root = ttk.LabelFrame(parent, text=" Slice detection ", padding=3)
        self.glob_state = glob_state
        self.values = {     # Method, Sens
            0: (0, "80"),  # Normal slices
            1: (0, "80"),  # Alt slices
        }

        self.c_selection = XCombobox(self.root, state="readonly", values=["Slices", "Alternative slices"])
        self.c_selection.grid(row=0, column=0, columnspan=3, sticky="we")
        self.root.grid_columnconfigure(2, weight=1)

        col1 = ttk.Frame(self.root, padding=2)
        col2 = ttk.Frame(self.root, padding=2)
        col1.grid(row=1, column=0)
        col2.grid(row=1, column=1, sticky="n")

        self.l_method = ttk.Label(col1, text="Method: ")
        self.c_method = XCombobox(col1, width=20, state="readonly", values=[m[0] for m in METHODS])
        self.l_sens = ttk.Label(col1, text="Sensitivity: ")
        self.e_sens = CChance(col1, ent_w=5)

        self.l_method.grid(row=0, column=0, sticky="w")
        self.c_method.grid(row=0, column=1, pady=1, sticky="e")
        self.l_sens.grid(row=1, column=0, sticky="w")
        self.e_sens.root.grid(row=1, column=1, sticky="e")

        self.b_gen_current = ttk.Button(col1, text="Generate from current audio")
        self.b_gen_other = ttk.Button(col1, text="Generate from other file")
        self.b_get_statistics = ttk.Button(col1, text="Get statistics")
        self.b_gen_current.grid(row=2, column=0, columnspan=2, sticky="we")
        self.b_gen_other.grid(row=3, column=0, columnspan=2, sticky="we")
        self.b_get_statistics.grid(row=4, column=0, columnspan=2, sticky="we")

        self.b_file_load = ttk.Button(col2, text="Apply slices from file")
        self.b_file_save = ttk.Button(col2, text="Save slices to file")
        self.b_file_edit = ttk.Button(col2, text="Manually edit slices")
        self.b_file_erase = ttk.Button(col2, text="Erase slices")

        self.b_file_load.grid(row=0, column=0, sticky="we")
        self.b_file_save.grid(row=1, column=0, sticky="we")
        self.b_file_edit.grid(row=2, column=0, sticky="we")
        self.b_file_erase.grid(row=3, column=0, sticky="we")

        self.c_selection.bind("<<ComboboxSelected>>", lambda event: self.values_set())
        self.c_method.bind("<<ComboboxSelected>>", lambda event: self.values_update())
        self.e_sens.e_chance.bind("<KeyRelease>", lambda event: self.values_update())

        self.c_selection.set(0)
        self.values_set()

    def get_selection(self):
        return self.c_selection.current()

    def get_selected_slices(self) -> Onsets:
        return self.glob_state.slices_alt if self.get_selection() == 1 else self.glob_state.slices

    def values_set(self):
        method, sens = self.values[self.get_selection()]
        self.c_method.current(method)
        self.e_sens.set(sens)
        self.update()

    def values_update(self):
        method = self.c_method.current()
        sens = self.e_sens.get_str()
        self.values[self.get_selection()] = method, sens
        self.update()

    def update(self):
        if self.glob_state.audio is None:
            self.b_gen_current.configure(state="disabled")
        else:
            self.b_gen_current.configure(state="normal")

        slices = self.get_selected_slices()
        if slices.are_there:
            self.b_file_save.configure(state="normal")
            self.b_file_erase.configure(state="normal")
        else:
            self.b_file_save.configure(state="disabled")
            self.b_file_erase.configure(state="disabled")

        if self.glob_state.audio is not None and slices.are_there:
            self.b_get_statistics.configure(state="normal")
        else:
            self.b_get_statistics.configure(state="disabled")

        if METHODS[self.c_method.current()][2]:
            self.e_sens.e_chance.configure(state="normal")
        else:
            self.e_sens.e_chance.configure(state="disabled")


def random_slices(window: "MainWindow", slc_window: tk.Toplevel, ed_field: ScrolledText, sample_rate: int):
    def finish():
        root.destroy()
        slc_window.focus_force()
        slc_window.grab_set()
        ed_field.focus_force()
        slc_window.update_idletasks()

    def b_ok():
        try:
            generator = e_length.get()
            if generator.check_wrong_mode() or generator.check_wrong_gauss():
                return

            onsets = [0]
            final_length = int(window.state.audio.length / window.state.audio.sample_rate * sample_rate)
            while True:
                s_len = round(generator.get() * sample_rate / 1000)
                if onsets[-1] + s_len >= final_length:
                    break
                else:
                    onsets.append(onsets[-1] + s_len)

            result = " ".join(str(o) for o in onsets)
            ed_field.delete("1.0", "end")
            ed_field.insert("1.0", result)
            finish()

        except Exception as e:
            window.py_error("Slices", meta.def_error.format("generating random slices"), e, parent=root)

    root = tk.Toplevel(slc_window)
    root.title("Generate random slices")
    root.bind("<Return>", lambda event: b_ok())
    root.bind("<Escape>", lambda event: finish())

    face = ttk.Frame(root, padding=5)
    face.pack(expand=True, fill="both")
    ttk.Label(face, text="Slice length (in milliseconds):", anchor="center") \
        .grid(row=0, column=0, columnspan=2, sticky="we")
    e_length = CDistribution(face)
    e_length.root.grid(row=1, column=0, columnspan=2, sticky="we", pady=10)
    ttk.Button(face, text="OK", command=b_ok).grid(row=2, column=0)
    ttk.Button(face, text="Cancel", command=finish).grid(row=2, column=1)
    apply_window_style(root)

    root.grab_set()
    root.focus_force()
    e_length.set("0 0 1000")
    e_length.e_val1.focus_set()


def edit_slices(window: "MainWindow", onsets_now: Optional[Onsets]=None):
    def show_sr():
        text_sample_rate.configure(text=f"Sample rate: {sample_rate}")

    def get_elements():
        return edit_field.get("1.0", "end").split()

    def get_txt_onsets() -> Onsets:
        onsets = list(map(float, get_elements()))
        return Onsets(onsets, int(sample_rate))

    def ask_new_sample_rate(title):
        return sd.askinteger(title, "New sample rate:", initialvalue=sample_rate, parent=root)

    def apply_onsets():
        try:
            onsets_now.override(get_txt_onsets())
        except Exception as e:
            window.py_error("Slices", meta.def_error.format("processing slices"), e, parent=root)
        finally:
            window.update_gui()
            edit_field.focus_set()

    def export_onsets():
        try:
            onsets = get_txt_onsets()
            ext = meta.ext_slices_alt if is_alt else meta.ext_slices
            write_slc_file(window, onsets, ext, root)
        except Exception as e:
            window.py_error("Slices", meta.def_error.format("processing slices"), e, parent=root)
        edit_field.focus_set()

    def sort_onsets():
        numbers = set()
        misc = []

        for e in get_elements():
            try:
                numbers.add(int(float(e)))
            except:
                misc.append(e)

        new_string = " ".join(list(map(str, sorted(numbers))) + misc)
        edit_field.delete("1.0", "end")
        edit_field.insert("1.0", new_string)
        edit_field.focus_set()

    def clear_onsets():
        if window.state.audio:
            nonlocal sample_rate
            sample_rate = window.state.audio.sample_rate
            show_sr()

        edit_field.delete("1.0", "end")
        edit_field.focus_set()

    def import_onsets(onsets: Onsets):
        nonlocal sample_rate

        if onsets.are_there:
            sample_rate = onsets.sample_rate
        elif window.state.audio:
            sample_rate = window.state.audio.sample_rate
        else:
            sample_rate = 1000

        edit_field.delete("1.0", "end")
        edit_field.insert("1.0", onsets.as_str)
        show_sr()

    def slices_from_midi():
        nonlocal sample_rate

        try:
            initial_dir = window.state.sav_config.get("dir_slices_midi")
            path = fd.askopenfilename(filetypes=meta.ext_midi, initialdir=initial_dir, parent=root)
            if not path:
                return
            window.state.sav_config.set("dir_slices_midi", os.path.dirname(path))

            sr = sample_rate if not window.state.audio else window.state.audio.sample_rate
            onsets = slicing.import_midi(path, sr)

            edit_field.delete("1.0", "end")
            edit_field.insert("1.0", " ".join(str(o) for o in onsets))
            sample_rate = sr
            show_sr()

        except Exception as e:
            window.py_error("MIDI", meta.def_error.format("importing MIDI"), e, parent=root)

    def sr_shift():
        shift_amt = sd.askfloat("Shift", "Shift by:", initialvalue=0, parent=root)

        if shift_amt:
            new_slices = []
            for s in get_elements():
                try:
                    new_s = float(s) + shift_amt
                    new_slices.append(str(round(new_s)))
                except:
                    new_slices.append(s)

            edit_field.delete("1.0", "end")
            edit_field.insert("1.0", " ".join(new_slices))
            edit_field.focus_set()
            show_sr()

    def sr_resample():
        nonlocal sample_rate
        new_sr = ask_new_sample_rate("Resample")

        if new_sr and new_sr > 0:
            new_slices = []
            for s in get_elements():
                try:
                    new_s = float(s) / sample_rate * new_sr
                    new_slices.append(str(round(new_s)))
                except:
                    new_slices.append(s)

            sample_rate = new_sr
            edit_field.delete("1.0", "end")
            edit_field.insert("1.0", " ".join(new_slices))
            edit_field.focus_set()
            show_sr()

    def sr_override():
        nonlocal sample_rate
        new_sr = ask_new_sample_rate("Override")
        if new_sr and new_sr > 0:
            sample_rate = new_sr
            edit_field.focus_set()
            show_sr()

    if onsets_now:
        is_alt = False
    else:
        is_alt = window.f_slice_detect.get_selection() == 1
        onsets_now = window.f_slice_detect.get_selected_slices()

    root = tk.Toplevel(window.root)
    root.title(f"Edit onsets")
    root.geometry("640x480")
    apply_window_style(root, resize_w=True, resize_h=True)
    root.grab_set()
    root.focus_force()
    root.bind("<Escape>", lambda event: root.destroy())

    sample_rate = 1000

    ui_menu = tk.Menu(root, tearoff=False)
    ui_menu_sub_import = tk.Menu(ui_menu, tearoff=False)
    ui_menu_sub_tools = tk.Menu(ui_menu, tearoff=False)
    root.configure(menu=ui_menu)

    ui_menu.add_cascade(label="Import", menu=ui_menu_sub_import)
    ui_menu_sub_import.add_command(label="Current slices", command=lambda: import_onsets(window.state.slices))
    ui_menu_sub_import.add_command(label="Current alternative slices",
                                   command=lambda: import_onsets(window.state.slices_alt))
    if not AB_DISABLE_PRETTY_MIDI:
        ui_menu_sub_import.add_command(label="External MIDI file", command=slices_from_midi)

    ui_menu.add_cascade(label="Tools", menu=ui_menu_sub_tools)
    ui_menu_sub_tools.add_command(label="Shift", command=sr_shift)
    ui_menu_sub_tools.add_command(label="Resample", command=sr_resample)
    ui_menu_sub_tools.add_command(label="Override sample rate", command=sr_override)
    ui_menu_sub_tools.add_separator()
    ui_menu_sub_tools.add_command(label="Generate random",
                                  command=lambda: random_slices(window, root, edit_field, sample_rate),
                                  state="normal" if window.state.audio else "disabled")

    edit_field = ScrolledText(root, wrap="word")

    panel_top = ttk.Frame(root, padding=1)
    panel_top.pack(side="top", fill="x")
    ttk.Button(panel_top, text="Apply", command=apply_onsets).pack(side="left")
    ttk.Button(panel_top, text="Export", command=export_onsets).pack(side="left")
    ttk.Button(panel_top, text="Sort", command=sort_onsets).pack(side="left")
    ttk.Button(panel_top, text="Clear", command=clear_onsets).pack(side="right")

    panel_bot = ttk.Frame(root, padding=1)
    panel_bot.pack(side="bottom", fill="x")
    text_sample_rate = ttk.Label(panel_bot)
    text_sample_rate.pack(side="left")

    edit_field.pack(fill="both", expand=True)
    import_onsets(onsets_now)
    edit_field.focus_set()
    root.update_idletasks()
