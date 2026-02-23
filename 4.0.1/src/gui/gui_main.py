import traceback
from state import ABState
from preset import PresetOpen, PresetSave
from scrambler.scr_state import ScramblerConfig

from gui_tools.tools import *
from gui.gui_common import *
from gui.top_menu import TopMenu
from gui.tab_basic import TabBasic
from gui.tab_sustain import TabSustain
from gui.tab_pattern import TabPattern
from gui.tab_framing import TabFraming
from gui.tab_quantization import TabQuantization
from gui.tab_misc import TabMisc
from gui.tab_tweak import TabTweak

from localization import loc
from loc_tools import override_loc
from gui.tooltips import apply_tooltips
from gui.tab_quantization_detection import SliceDetectionGui
from gui_tools import edit_onsets, tools_preset, tools_scramble, tools_slices


class Toolbar:
    def __init__(self, parent, window: "MainWindow"):
        self.root = ttk.Frame(parent, padding=2)

        b_width = loc["_geometry"]["tb_button"]
        self.b_import = ttk.Button(self.root, text=loc["top_menu"]["toolbar"]["b_import"], width=b_width)
        self.b_scramble = ttk.Button(self.root, text="", width=b_width)
        self.b_preview = ttk.Button(self.root, text="", width=b_width)
        self.b_open_preset = ttk.Button(self.root, text=loc["top_menu"]["toolbar"]["b_open_preset"], width=b_width)
        self.b_save_preset = ttk.Button(self.root, text=loc["top_menu"]["toolbar"]["b_save_preset"], width=b_width)
        self.b_hints = ttk.Button(self.root, text=loc["top_menu"]["toolbar"]["b_hints_enable"], width=b_width)

        self.b_import.configure(command=window.cmd_load_audio)
        self.b_scramble.configure(command=window.cmd_x_scramble)
        self.b_preview.configure(command=window.cmd_preview)
        self.b_open_preset.configure(command=window.cmd_open_preset)
        self.b_save_preset.configure(command=window.cmd_save_preset)
        self.b_hints.configure(command=window.cmd_hints_set)

        self.b_import.pack(side="left")
        self.b_scramble.pack(side="left")
        if not AB_DISABLE_SIMPLEAUDIO:
            self.b_preview.pack(side="left")
        self.b_open_preset.pack(side="left")
        self.b_save_preset.pack(side="left")
        if not AB_HIDE_TOOLTIPS:
            self.b_hints.pack(side="right")


class TabCommon:
    def __init__(self, parent, window: "MainWindow"):
        self.root = ttk.Frame(parent, padding=1)

        self.x_use_seconds = CCheckbox(self.root, loc["top_menu"]["toolbar"]["x_use_seconds"])
        self.x_use_seed = CCheckbox(self.root, loc["top_menu"]["toolbar"]["x_use_seed"])
        self.e_seed = XEntry(self.root, width=16)

        self.x_use_seconds.root.pack(side="left")
        self.e_seed.pack(side="right", padx=1)
        self.x_use_seed.root.pack(side="right")

        self.u_menu = tk.Menu(self.root, tearoff=False)
        self.u_menu.add_command(label=loc["top_menu"]["presets"]["restore_seed"],
                                command=lambda: restore_last_seed(window))

        self.x_use_seed.root.configure(command=self.update)
        self.x_use_seed.root.bind("<Button-2>", self.show_seed_menu)
        self.x_use_seed.root.bind("<Button-3>", self.show_seed_menu)
        self.e_seed.bind("<Button-2>", self.show_seed_menu)
        self.e_seed.bind("<Button-3>", self.show_seed_menu)

    def show_seed_menu(self, event):
        self.u_menu.tk_popup(event.x_root, event.y_root)

    def update(self):
        if self.x_use_seed.get():
            self.e_seed.configure(state="normal")
        else:
            self.e_seed.configure(state="disabled")

    def apply_config(self, config):
        config.in_seconds = self.x_use_seconds.get()
        config.seed = self.e_seed.get() if self.x_use_seed.get() else any_seed(12)

    def open_preset(self, preset: PresetOpen):
        self.x_use_seconds.set(preset.get("conv2sec", "0"))
        self.x_use_seed.set(preset.get("use_seed", "0"))
        self.e_seed.set(preset.get("seed", ""))

    def save_preset(self, preset: PresetSave):
        preset.add("version", meta.ver_preset)
        preset.add("conv2sec", self.x_use_seconds.get_str())
        preset.add("use_seed", self.x_use_seed.get_str())
        preset.add("seed", self.e_seed.get())
        preset.add_separator()


class MainWindow:
    def __init__(self):
        if AB_ANDROID_MODE:
            self.root = tk.Toplevel()
        elif AB_DISABLE_TKDND2:
            self.root = tk.Tk()
        else:
            self.root = TkinterDnD.Tk()
            self.root.drop_target_register("DND_Files")
            self.root.dnd_bind("<<Drop>>", self.dnd_got_file)

        self.state = ABState()
        override_loc(self.state.sav_config.get("localization_path"))

        self.top_menu = TopMenu(self.root, self)
        self.f_toolbar = Toolbar(self.root, self)
        self.f_tabs = ttk.Notebook(self.root)
        self.f_basic = TabBasic(self.root)
        self.f_sustain = TabSustain(self.root)
        self.f_pattern = TabPattern(self.root)
        self.f_framing = TabFraming(self.root)
        self.f_quantization = TabQuantization(self.root)
        self.f_slice_detect = SliceDetectionGui(self.f_quantization.root, self.state)
        self.f_misc = TabMisc(self.root, self)
        self.f_tweak = TabTweak(self.root, self)
        self.f_common = TabCommon(self.root, self)
        self.u_progressbar = ttk.Progressbar(self.root)

        if not AB_HIDE_TOOLTIPS:
            apply_tooltips(self)

        self.root.config(menu=self.top_menu.root)
        self.f_toolbar.root.pack(side="top", fill="x")
        self.f_tabs.pack(fill="both", expand=True)
        self.f_common.root.pack(fill="x")
        self.f_slice_detect.root.grid(row=0, column=1, padx=4, sticky="nse")
        self.u_progressbar.pack(side="bottom", fill="x", padx=1, pady=1)

        self.f_tabs.add(self.f_basic.root, text=loc["tab_basic"]["name"])
        self.f_tabs.add(self.f_sustain.root, text=loc["tab_sustain"]["name"])
        self.f_tabs.add(self.f_pattern.root, text=loc["tab_pattern"]["name"])
        self.f_tabs.add(self.f_framing.root, text=loc["tab_framing"]["name"])
        self.f_tabs.add(self.f_quantization.root, text=loc["tab_quantization"]["name"])
        self.f_tabs.add(self.f_misc.root, text=loc["tab_misc"]["name"])
        self.f_tabs.add(self.f_tweak.root, text=loc["tab_tweaks"]["name"])

        apply_window_style(self.root)
        self.bind_commands()
        self.bind_slice_detection()
        self.f_common.x_use_seconds.root.configure(command=self.convert_time)
        self.f_sustain.set_sec_mode_ref(self.f_common.x_use_seconds)

    def bind_commands(self):
        self.root.bind("<Control-i>", lambda event: self.cmd_load_audio())
        self.root.bind("<Control-e>", lambda event: self.cmd_scramble())
        self.root.bind("<Control-r>", lambda event: self.cmd_refresh())

        if not AB_DISABLE_SIMPLEAUDIO:
            self.root.bind("<Control-p>", lambda event: self.cmd_preview())

        self.root.bind("<Control-o>", lambda event: self.cmd_open_preset())
        self.root.bind("<Control-s>", lambda event: self.cmd_save_preset())
        self.root.bind("<Control-n>", lambda event: self.cmd_default_settings())

    def bind_slice_detection(self):
        sd = self.f_slice_detect

        sd.b_gen_current.configure(command=lambda: tools_slices.detect_slices(self))
        sd.b_gen_other.configure(command=lambda: tools_slices.detect_slices(self, from_current=False))
        sd.b_get_statistics.configure(command=lambda: run(tools_slices.show_slice_stats, self))

        sd.b_file_load.configure(command=lambda: tools_slices.read_slc_file(self))
        sd.b_file_save.configure(command=lambda: tools_slices.write_slc_file(self))
        sd.b_file_edit.configure(command=lambda: edit_onsets.edit_onsets(self))
        sd.b_file_erase.configure(command=lambda: tools_slices.erase_slices(self))

    # Logic

    def py_error(self, text, exception, b_retry=False, **kwargs):
        label = loc["messages"]["error"]
        message = f"{text}\n\n{loc['messages']['error_info']}\n" + \
            (str(traceback.format_exc()) if self.state.get_pref_var("show_error_info") else
                f"{type(exception).__name__}: {exception}")

        if b_retry:
            return mb.askretrycancel(label, message, icon=mb.ERROR, **kwargs)

        else:
            mb.showerror(label, message, **kwargs)
            return 0

    def set_progress(self, a, b):
        self.state.scr_progress = (a, b)
        self.u_progressbar["value"] = a / b * 100

    def update_global(self):
        self.f_framing.lock_part_gen = (self.state.scr_state is not None)
        self.update_header()
        self.update_gui()

    def update_header(self):
        title_now = meta.full_name
        m_loc = loc["top_menu"]["toolbar"]

        if self.state.now_scrambling:
            self.f_toolbar.b_scramble.configure(text=m_loc["b_scramble_abort"])
        elif self.state.scr_state:
            self.f_toolbar.b_scramble.configure(text=m_loc["b_scramble_continue"])
        else:
            self.f_toolbar.b_scramble.configure(text=m_loc["b_scramble"])

        if self.state.audio:
            name = os.path.basename(self.state.cur_config.audio_path)
            in_sec = self.state.get_pref_var("audio_length_in_seconds")
            length = audio_length_str(self.state.audio.length, self.state.audio.sample_rate, in_sec)
            title_now += f" - {name} ({length})"

            self.f_toolbar.b_scramble.configure(state="normal")
            self.f_toolbar.b_preview.configure(state="normal")

        else:
            self.f_toolbar.b_scramble.configure(state="disabled")
            self.f_toolbar.b_preview.configure(state="disabled")

        if self.state.now_previewing:
            self.f_toolbar.b_preview.configure(text=m_loc["b_preview_stop"])
            self.f_toolbar.b_preview.configure(state="normal")
            title_now += f" - {loc['top_menu']['state_preview']}"
        else:
            self.f_toolbar.b_preview.configure(text=m_loc["b_preview"])

        self.root.title(title_now)

    def update_gui(self):
        self.f_common.update()
        self.f_basic.update()
        self.f_framing.update()
        self.f_quantization.update()
        self.f_misc.update()
        self.f_tweak.update()
        self.f_slice_detect.update()

    def convert_time(self):
        if not self.state.get_pref_var("conv_sec2ms"):
            return

        if self.f_common.x_use_seconds.get():
            mode = "ms2sec"
        else:
            mode = "sec2ms"

        self.f_basic.convert_time(mode)
        self.f_sustain.convert_time(mode)
        self.f_pattern.convert_time(mode)
        self.f_framing.convert_time(mode)
        self.f_misc.convert_time(mode)

    def dnd_got_file(self, event):
        path = event.data

        if path[0]=="{" and path[-1]=="}":
            path = path[1:-1]

        path = path.replace(r"\{", "{").replace(r"\}", "}").replace(r"\ ", " ")
        dnd_open_file(self, path)

    # Config Logic

    def get_config(self) -> ScramblerConfig:
        config = ScramblerConfig()

        self.f_common.apply_config(config)
        self.f_basic.apply_config(config)
        self.f_sustain.apply_config(config)
        self.f_pattern.apply_config(config)
        self.f_framing.apply_config(config)
        self.f_quantization.apply_config(config)
        self.f_misc.apply_config(config)
        self.f_tweak.apply_config(config)

        config.convert_seconds()
        return config

    def open_preset(self, preset: PresetOpen):
        self.f_common.open_preset(preset)
        self.f_basic.open_preset(preset)
        self.f_sustain.open_preset(preset)
        self.f_pattern.open_preset(preset)
        self.f_framing.open_preset(preset)
        self.f_quantization.open_preset(preset)
        self.f_misc.open_preset(preset)
        self.f_tweak.open_preset(preset)

    def save_preset(self, preset: PresetSave):
        self.f_common.save_preset(preset)
        self.f_basic.save_preset(preset)
        self.f_sustain.save_preset(preset)
        self.f_pattern.save_preset(preset)
        self.f_framing.save_preset(preset)
        self.f_quantization.save_preset(preset)
        self.f_misc.save_preset(preset)
        self.f_tweak.save_preset(preset)

    def factory_preset(self, contents):
        self.state.cur_config.last_preset_name = None
        self.open_preset(PresetOpen(data=contents))
        self.update_gui()

    # Commands

    def cmd_hints_set(self):
        m_loc = loc["top_menu"]["toolbar"]

        self.state.cur_config.show_hints = not self.state.cur_config.show_hints
        self.f_toolbar.b_hints.configure(text=m_loc["b_hints_disable"] if self.state.cur_config.show_hints
                                              else m_loc["b_hints_enable"])

    def cmd_load_audio(self):
        run(tools_scramble.load_audio, self)

    def cmd_x_scramble(self):
        if self.state.now_scrambling:
            self.cmd_scr_abort()
        else:
            self.cmd_scramble()

    def cmd_scramble(self):
        run(tools_scramble.scramble, self)

    def cmd_preview(self):
        if AB_DISABLE_SIMPLEAUDIO:
            return

        if self.state.now_previewing:
            tools_scramble.stop_preview()
        else:
            run(tools_scramble.scramble, self, True)

    def cmd_scr_abort(self):
        if not abort_confirm(self):
            return
        if self.state.now_scrambling:
            self.state.force_abort = True

    def cmd_refresh(self):
        run(tools_scramble.load_audio, self, self.state.cur_config.audio_path)

    def cmd_open_preset(self):
        tools_preset.open_preset(self)

    def cmd_save_preset(self):
        tools_preset.save_preset(self)

    def cmd_default_settings(self):
        self.state.cur_config.last_preset_name = None

        self.open_preset(PresetOpen())
        self.f_basic.e_duration.set("0 0 1000")
        self.f_basic.e_crossfade.set("0 5 5")
        self.f_sustain.e_weights.set("1 0 0 0 0")
        self.f_pattern.pattern.f_skipping.f_forw.e_weight.set("1")

        self.update_gui()
