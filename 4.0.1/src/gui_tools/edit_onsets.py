import math
import slicing
from common import *
import gui.filetypes as fts

from gui.gui_common import *
from gui_tools.tools_slices import write_slc_file
from gui_tools.tools_misc import apply_window_style, def_error

import tkinter.filedialog as fd
import tkinter.simpledialog as sd
from tkinter.scrolledtext import ScrolledText

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from gui.gui_main import MainWindow


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
            window.py_error(def_error("slice_randgen"), e, parent=root)

    root = tk.Toplevel(slc_window)
    root.title(loc["edit_onsets"]["m_tools_random"])
    root.bind("<Return>", lambda event: b_ok())
    root.bind("<Escape>", lambda event: finish())

    face = ttk.Frame(root, padding=5)
    face.pack(expand=True, fill="both")
    ttk.Label(face, text=loc["edit_onsets"]["l_random_length"], anchor="center") \
        .grid(row=0, column=0, columnspan=2, sticky="we")
    e_length = CDistribution(face)
    e_length.root.grid(row=1, column=0, columnspan=2, sticky="we", pady=10)
    ttk.Button(face, text=loc["meta"]["buttons"]["ok"], command=b_ok).grid(row=2, column=0)
    ttk.Button(face, text=loc["meta"]["buttons"]["cancel"], command=finish).grid(row=2, column=1)
    apply_window_style(root)

    root.grab_set()
    root.focus_force()
    e_length.set("0 0 1000")
    e_length.e_val1.focus_set()


def edit_onsets(window: "MainWindow", onsets_now: Optional[slicing.Onsets]=None):
    m_loc = loc["edit_onsets"]

    # Some tools

    def set_sr(new_sr):
        nonlocal sample_rate
        sample_rate = new_sr
        text_sample_rate.configure(text=f"{m_loc['l_sample_rate']}{sample_rate}")

    def get_elements():
        return edit_field.get("1.0", "end").split()

    def get_txt_onsets() -> slicing.Onsets:
        onsets = list(map(float, get_elements()))
        return slicing.Onsets(onsets, int(sample_rate))

    def get_onsets_quick():
        numbers = {0}
        misc = []

        for e in get_elements():
            try:
                numbers.add(int(float(e)))
            except:
                misc.append(e)

        onsets = sorted(numbers)
        if window.state.audio is not None:
            audio_length = round(window.state.audio.length / window.state.audio.sample_rate * sample_rate)
            if audio_length > onsets[-1]:
                onsets.append(audio_length)

        return onsets, misc

    def insert_ons_txt(onsets: list[int], misc: Optional[list[str]]=None):
        onsets_str = list(map(str, onsets))
        if misc is not None:
            onsets_str.extend(misc)

        edit_field.delete("1.0", "end")
        edit_field.insert("1.0", " ".join(onsets_str))
        edit_field.focus_set()

    def ask_new_sample_rate(title):
        return sd.askinteger(title, m_loc["l_new_sample_rate"], initialvalue=sample_rate, parent=root)

    # Import menu

    def apply_onsets():
        try:
            onsets_now.override(get_txt_onsets())
        except Exception as e:
            window.py_error(def_error("slice_process"), e, parent=root)
        finally:
            window.update_gui()
            edit_field.focus_set()

    def export_onsets():
        try:
            onsets = get_txt_onsets()
            ext = fts.ext_slices_alt if is_alt else fts.ext_slices
            write_slc_file(window, onsets, ext, root)
        except Exception as e:
            window.py_error(def_error("slice_process"), e, parent=root)
        edit_field.focus_set()

    def sort_onsets():
        numbers = set()
        misc = []

        for e in get_elements():
            try:
                numbers.add(int(float(e)))
            except:
                misc.append(e)

        insert_ons_txt(sorted(numbers), misc)

    def clear_onsets():
        if window.state.audio:
            set_sr(window.state.audio.sample_rate)

        edit_field.delete("1.0", "end")
        edit_field.focus_set()

    def import_onsets(onsets: slicing.Onsets):
        if onsets.are_there:
            sr = onsets.sample_rate
        elif window.state.audio:
            sr = window.state.audio.sample_rate
        else:
            sr = 1000

        set_sr(sr)
        edit_field.delete("1.0", "end")
        edit_field.insert("1.0", onsets.as_str)
        edit_field.focus_set()

    def slices_from_midi():
        try:
            initial_dir = window.state.sav_config.get("dir_slices_midi")
            path = fd.askopenfilename(filetypes=fts.ext_midi, initialdir=initial_dir, parent=root)
            if not path:
                return
            window.state.sav_config.set("dir_slices_midi", os.path.dirname(path))

            sr = sample_rate if not window.state.audio else window.state.audio.sample_rate
            onsets = slicing.import_midi(path, sr)

            set_sr(sr)
            insert_ons_txt(onsets)

        except Exception as e:
            window.py_error(def_error("midi_import"), e, parent=root)

    # Tools menu

    def sr_shift():
        shift_amt = sd.askfloat(m_loc["m_tools_shift"], m_loc["l_shift"], initialvalue=0, parent=root)

        if shift_amt:
            new_slices = []
            for s in get_elements():
                try:
                    new_s = float(s) + shift_amt
                    new_slices.append(str(round(new_s)))
                except:
                    new_slices.append(s)

            insert_ons_txt(new_slices)

    def sr_resample():
        new_sr = ask_new_sample_rate(m_loc["m_tools_resample"])

        if new_sr and new_sr > 0:
            new_slices = []
            for s in get_elements():
                try:
                    new_s = float(s) / sample_rate * new_sr
                    new_slices.append(str(round(new_s)))
                except:
                    new_slices.append(s)

            set_sr(new_sr)
            insert_ons_txt(new_slices)

    def sr_override():
        new_sr = ask_new_sample_rate(m_loc["m_tools_override_sr"])
        if new_sr and new_sr > 0:
            set_sr(new_sr)
            edit_field.focus_set()

    def divide_long():
        threshold_ms = sd.askfloat(m_loc["m_tools_divide_long"], m_loc["l_division_threshold"],
                                initialvalue=5000, parent=root)
        if threshold_ms is None:
            return
        threshold = round(threshold_ms * sample_rate / 1000)

        onsets, misc = get_onsets_quick()

        onsets_new = []
        for i in range(len(onsets)-1):
            slice_length = onsets[i+1] - onsets[i]

            n_divs = math.ceil(slice_length / threshold)
            step = int(slice_length / n_divs)
            for j in range(n_divs):
                onsets_new.append(onsets[i] + step*j)
        onsets_new.append(onsets[-1])

        insert_ons_txt(onsets_new, misc)

    def merge_short():
        threshold_ms = sd.askfloat(m_loc["m_tools_merge_short"], m_loc["l_merge_threshold"],
                                   initialvalue=30, parent=root)
        if threshold_ms is None:
            return
        threshold = round(threshold_ms * sample_rate / 1000)
        onsets, misc = get_onsets_quick()

        onsets_new = [0]
        for onset in onsets:
            if onset == 0:
                continue
            if onset - onsets_new[-1] >= threshold:
                onsets_new.append(onset)

        insert_ons_txt(onsets_new, misc)

    # GUI

    sample_rate = 1000
    if onsets_now:
        is_alt = False
    else:
        is_alt = window.f_slice_detect.get_selection() == 1
        onsets_now = window.f_slice_detect.get_selected_slices()

    root = tk.Toplevel(window.root)
    root.title(m_loc["title"])
    root.geometry("640x480")
    apply_window_style(root, resize_w=True, resize_h=True)
    root.grab_set()
    root.focus_force()
    root.bind("<Escape>", lambda event: root.destroy())

    ui_menu = tk.Menu(root, tearoff=False)
    ui_menu_sub_import = tk.Menu(ui_menu, tearoff=False)
    ui_menu_sub_tools = tk.Menu(ui_menu, tearoff=False)
    root.configure(menu=ui_menu)

    ui_menu.add_cascade(label=m_loc["m_import"], menu=ui_menu_sub_import)
    ui_menu_sub_import.add_command(label=m_loc["m_import_slices"],
                                   command=lambda: import_onsets(window.state.slices))
    ui_menu_sub_import.add_command(label=m_loc["m_import_alt_slices"],
                                   command=lambda: import_onsets(window.state.slices_alt))
    if not AB_DISABLE_PRETTY_MIDI:
        ui_menu_sub_import.add_command(label=m_loc["m_import_midi"], command=slices_from_midi)

    ui_menu.add_cascade(label=m_loc["m_tools"], menu=ui_menu_sub_tools)
    ui_menu_sub_tools.add_command(label=m_loc["m_tools_shift"], command=sr_shift)
    ui_menu_sub_tools.add_command(label=m_loc["m_tools_resample"], command=sr_resample)
    ui_menu_sub_tools.add_command(label=m_loc["m_tools_override_sr"], command=sr_override)
    ui_menu_sub_tools.add_separator()
    ui_menu_sub_tools.add_command(label=m_loc["m_tools_divide_long"], command=divide_long)
    ui_menu_sub_tools.add_command(label=m_loc["m_tools_merge_short"], command=merge_short)
    ui_menu_sub_tools.add_command(label=m_loc["m_tools_random"],
                                  command=lambda: random_slices(window, root, edit_field, sample_rate),
                                  state="normal" if window.state.audio else "disabled")

    edit_field = ScrolledText(root, wrap="word")

    panel_top = ttk.Frame(root, padding=1)
    panel_top.pack(side="top", fill="x")
    ttk.Button(panel_top, text=m_loc["b_apply"], command=apply_onsets).pack(side="left")
    ttk.Button(panel_top, text=m_loc["b_export"], command=export_onsets).pack(side="left")
    ttk.Button(panel_top, text=m_loc["b_sort"], command=sort_onsets).pack(side="left")
    ttk.Button(panel_top, text=m_loc["b_clear"], command=clear_onsets).pack(side="right")

    panel_bot = ttk.Frame(root, padding=1)
    panel_bot.pack(side="bottom", fill="x")
    text_sample_rate = ttk.Label(panel_bot)
    text_sample_rate.pack(side="left")

    edit_field.pack(fill="both", expand=True)
    import_onsets(onsets_now)
    edit_field.focus_set()
    root.update_idletasks()
