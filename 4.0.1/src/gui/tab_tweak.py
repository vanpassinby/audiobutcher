import base64

from preset import PresetOpen, PresetSave
from abpl.abpl_tools import format_script
from scrambler.scr_state import ScramblerConfig

from gui.gui_common import *
from gui_tools.edit_abpl import edit_abpl


class SubConsec:
    def __init__(self, parent):
        m_loc = loc["tab_tweaks"]
        self.root = ttk.LabelFrame(parent, text=m_loc["f_seg0_consec"], padding=3)

        self.x_seg0_pause = CCheckbox(self.root, m_loc["x_seg0_pause"])
        self.x_seg0_repeat = CCheckbox(self.root, m_loc["x_seg0_repeat"])
        self.x_seg0_sustain = CCheckbox(self.root, text=m_loc["x_seg0_sustain"])
        self.x_seg0_muted = CCheckbox(self.root, text=m_loc["x_seg0_muted"])

        self.x_seg0_pause.root.grid(row=0, column=0, sticky="w")
        self.x_seg0_repeat.root.grid(row=1, column=0, sticky="w")
        self.x_seg0_sustain.root.grid(row=2, column=0, sticky="w")
        self.x_seg0_muted.root.grid(row=3, column=0, sticky="w")

        ttk.Label(self.root).grid(row=0, column=1)
        self.x_volume_pause_is_mute = CCheckbox(self.root, text=m_loc["x_volume_pause_is_mute"])
        self.x_volume_pause_is_mute.root.grid(row=0, column=2, columnspan=2, sticky="w")

        self.l_repeat_consec_chance = ttk.Label(self.root, text=m_loc["l_repeat_consec_chance"])
        self.e_repeat_consec_chance = CChance(self.root)
        self.l_repeat_consec_chance.grid(row=1, column=2, sticky="w")
        self.e_repeat_consec_chance.root.grid(row=1, column=3, sticky="w")

        self.l_volume_mute_consec_chance = ttk.Label(self.root, text=m_loc["l_volume_mute_consec_chance"])
        self.e_volume_mute_consec_chance = CChance(self.root)
        self.l_volume_mute_consec_chance.grid(row=3, column=2, sticky="w")
        self.e_volume_mute_consec_chance.root.grid(row=3, column=3, sticky="w")

    def apply_config(self, config: ScramblerConfig):
        config.seg0_pause = self.x_seg0_pause.get()
        config.seg0_repeat = self.x_seg0_repeat.get()
        config.seg0_sustain = self.x_seg0_sustain.get()
        config.seg0_muted = self.x_seg0_muted.get()
        config.volume_pause_is_mute = self.x_volume_pause_is_mute.get()
        config.repeat_consec_chance = self.e_repeat_consec_chance.get()
        config.volume_mute_consec_chance = self.e_volume_mute_consec_chance.get()

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.x_seg0_pause, "seg0_pause", "0"],
            [self.x_seg0_repeat, "seg0_repeat", "0"],
            [self.x_seg0_sustain, "seg0_sustain", "0"],
            [self.x_seg0_muted, "seg0_muted", "0"],
            [self.x_volume_pause_is_mute, "volume_pause_is_mute", "0"],
            [self.e_repeat_consec_chance, "repeat_consec_chance", "100"],
            [self.e_volume_mute_consec_chance, "volume_mute_consec_chance", "100"],
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("seg0_pause", self.x_seg0_pause.get_str())
        preset.add("seg0_repeat", self.x_seg0_repeat.get_str())
        preset.add("seg0_sustain", self.x_seg0_sustain.get_str())
        preset.add("seg0_muted", self.x_seg0_muted.get_str())
        preset.add("volume_pause_is_mute", self.x_volume_pause_is_mute.get_str())
        preset.add("repeat_consec_chance", self.e_repeat_consec_chance.get_str())
        preset.add("volume_mute_consec_chance", self.e_volume_mute_consec_chance.get_str())
        preset.add_separator()


class SubTweak:
    cb_no_yes = BiDict(["no", "yes"])
    cb_random_start_selection = BiDict(["prior_length", "prior_start"])
    cb_reverse_double_mode = BiDict(["allowed", "rev1", "rev2"])
    cb_crossfade_comp_mode = BiDict(["shorten", "cutoff"])
    cb_quan_dur_bpm = BiDict(["by_end", "by_length"])

    def __init__(self, parent):
        m_loc = loc["tab_tweaks"]
        cbx_w = loc["_geometry"]["cb_tweak_option"]

        self.root = ttk.LabelFrame(parent, text=m_loc["f_minor"], padding=3)
        self.root.columnconfigure(1, weight=1)

        self.l_random_start_selection = ttk.Label(self.root, text=m_loc["l_random_start_selection"])
        self.c_random_start_selection = YCombobox(self.root, width=cbx_w, state="readonly",
                                               items=self.cb_random_start_selection,
                                               loc_part=m_loc["c_random_start_selection"])
        self.l_random_start_selection.grid(row=0, column=0, sticky="w")
        self.c_random_start_selection.grid(row=0, column=1, sticky="e", pady=1)


        self.l_reverse_double_mode = ttk.Label(self.root, text=m_loc["l_reverse_double_mode"])
        self.c_reverse_double_mode = YCombobox(self.root, width=cbx_w, state="readonly",
                                               items=self.cb_reverse_double_mode,
                                               loc_part=m_loc["c_reverse_double_mode"])
        self.l_reverse_double_mode.grid(row=1, column=0, sticky="w")
        self.c_reverse_double_mode.grid(row=1, column=1, sticky="e", pady=1)

        self.l_pause_apply_effects = ttk.Label(self.root, text=m_loc["l_pause_apply_effects"])
        self.c_pause_apply_effects = YCombobox(self.root, width=cbx_w, state="readonly",
                                               items=self.cb_no_yes, loc_part=m_loc["c_no_yes"])
        self.l_pause_apply_effects.grid(row=2, column=0, sticky="w")
        self.c_pause_apply_effects.grid(row=2, column=1, sticky="e", pady=1)

        self.l_crossfade_comp_mode = ttk.Label(self.root, text=m_loc["l_crossfade_comp_mode"])
        self.c_crossfade_comp_mode = YCombobox(self.root, width=cbx_w, state="readonly",
                                               items=self.cb_crossfade_comp_mode,
                                               loc_part=m_loc["c_crossfade_comp_mode"])
        self.l_crossfade_comp_mode.grid(row=3, column=0, sticky="w")
        self.c_crossfade_comp_mode.grid(row=3, column=1, sticky="e", pady=1)

        self.l_fade_in_plus_preroll = ttk.Label(self.root, text=m_loc["l_fade_in_plus_preroll"])
        self.c_fade_in_plus_preroll = YCombobox(self.root, width=cbx_w, state="readonly",
                                                items=self.cb_no_yes, loc_part=m_loc["c_no_yes"])
        self.l_fade_in_plus_preroll.grid(row=4, column=0, sticky="w")
        self.c_fade_in_plus_preroll.grid(row=4, column=1, sticky="e", pady=1)

        self.l_quan_duration_bpm_mode = ttk.Label(self.root, text=m_loc["l_quan_duration_bpm_mode"])
        self.c_quan_duration_bpm_mode = YCombobox(self.root, width=cbx_w, state="readonly",
                                                  items=self.cb_quan_dur_bpm,
                                                  loc_part=m_loc["c_quan_duration_bpm_mode"])
        self.l_quan_duration_bpm_mode.grid(row=5, column=0, sticky="w")
        self.c_quan_duration_bpm_mode.grid(row=5, column=1, sticky="e", pady=1)

    def apply_config(self, config: ScramblerConfig):
        config.duration_priority = (self.c_random_start_selection.current() == 0)
        config.reverse_double_mode = self.c_reverse_double_mode.current()
        config.pause_apply_effects = bool(self.c_pause_apply_effects.current())
        config.crossfade_comp_mode = self.c_crossfade_comp_mode.current()
        config.fade_in_plus_preroll = bool(self.c_fade_in_plus_preroll.current())
        config.quan_duration_bpm_mode = self.c_quan_duration_bpm_mode.current()
        config.abpl_enabled = True

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.c_random_start_selection, "random_start_selection", "prior_length"],
            [self.c_reverse_double_mode, "reverse_double_mode", "allowed"],
            [self.c_pause_apply_effects, "pause_apply_effects", "yes"],
            [self.c_crossfade_comp_mode, "crossfade_comp_mode", "shorten"],
            [self.c_fade_in_plus_preroll, "fade_in_plus_preroll", "no"],
            [self.c_quan_duration_bpm_mode, "quan_duration_bpm_mode", "by_end"],
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("random_start_selection", self.c_random_start_selection.get_str())
        preset.add("reverse_double_mode", self.c_reverse_double_mode.get_str())
        preset.add("pause_apply_effects", self.c_pause_apply_effects.get_str())
        preset.add("crossfade_comp_mode", self.c_crossfade_comp_mode.get_str())
        preset.add("fade_in_plus_preroll", self.c_fade_in_plus_preroll.get_str())
        preset.add("quan_duration_bpm_mode", self.c_quan_duration_bpm_mode.get_str())


class SubTrim:
    def __init__(self, parent):
        m_loc = loc["tab_tweaks"]
        self.root = ttk.LabelFrame(parent, text=m_loc["f_trim"], padding=3)

        self.x_trim1 = CCheckbox(self.root, m_loc["x_trim_from"])
        self.e_trim1 = XEntry(self.root, width=10)
        self.x_trim1.root.grid(row=0, column=0, sticky="w")
        self.e_trim1.grid(row=0, column=1, sticky="e", padx=1, pady=1)

        self.x_trim2 = CCheckbox(self.root, m_loc["x_trim_to"])
        self.e_trim2 = XEntry(self.root, width=10)
        self.x_trim2.root.grid(row=1, column=0, sticky="w")
        self.e_trim2.grid(row=1, column=1, sticky="e", padx=1, pady=1)

        self.x_trim1.root.configure(command=self.update)
        self.x_trim2.root.configure(command=self.update)

        self.x_trim_slices = CCheckbox(self.root, text=m_loc["x_trim_slices"])
        self.x_trim_slices2 = CCheckbox(self.root, text=m_loc["x_trim_slices2"])
        self.x_trim_loop_start = CCheckbox(self.root, text=m_loc["x_trim_loop_start"])
        self.x_trim_avgstart = CCheckbox(self.root, text=m_loc["x_trim_avgstart"])
        self.x_trim_slices.root.grid(row=2, column=0, columnspan=2, sticky="w")
        self.x_trim_slices2.root.grid(row=3, column=0, columnspan=2, sticky="w")
        self.x_trim_loop_start.root.grid(row=4, column=0, columnspan=2, sticky="w")
        self.x_trim_avgstart.root.grid(row=5, column=0, columnspan=2, sticky="w")

    def update(self):
        if self.x_trim1.get():
            self.e_trim1.configure(state="normal")
            self.x_trim_slices.root.configure(state="normal")
            self.x_trim_slices2.root.configure(state="normal")
            self.x_trim_loop_start.root.configure(state="normal")
            self.x_trim_avgstart.root.configure(state="normal")
        else:
            self.e_trim1.configure(state="disabled")
            self.x_trim_slices.root.configure(state="disabled")
            self.x_trim_slices2.root.configure(state="disabled")
            self.x_trim_loop_start.root.configure(state="disabled")
            self.x_trim_avgstart.root.configure(state="disabled")

        if self.x_trim2.get():
            self.e_trim2.configure(state="normal")
        else:
            self.e_trim2.configure(state="disabled")

    def convert_time(self, mode):
        self.e_trim1.conv_time(mode)
        self.e_trim2.conv_time(mode)

    def apply_config(self, config: ScramblerConfig):
        config.trim1 = 0 if not self.x_trim1.get() else float(self.e_trim1.get())
        config.trim2 = 0 if not self.x_trim2.get() else float(self.e_trim2.get())
        config.trim_slices = self.x_trim_slices.get()
        config.trim_slices2 = self.x_trim_slices2.get()
        config.trim_loop_start = self.x_trim_loop_start.get()
        config.trim_avgstart = self.x_trim_avgstart.get()

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.e_trim1, "trim1", "0"],
            [self.x_trim1, "trim1_x", "0"],
            [self.e_trim2, "trim2", "0"],
            [self.x_trim2, "trim2_x", "0"],
            [self.x_trim_slices, "trim_slices", "1"],
            [self.x_trim_slices2, "trim_slices2", "1"],
            [self.x_trim_loop_start, "trim_loop_start", "1"],
            [self.x_trim_avgstart, "trim_avgstart", "1"],
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("trim1", self.e_trim1.get())
        preset.add("trim1_x", self.x_trim1.get_str())
        preset.add("trim2", self.e_trim2.get())
        preset.add("trim2_x", self.x_trim2.get_str())
        preset.add("trim_slices", self.x_trim_slices.get_str())
        preset.add("trim_slices2", self.x_trim_slices2.get_str())
        preset.add("trim_loop_start", self.x_trim_loop_start.get_str())
        preset.add("trim_avgstart", self.x_trim_avgstart.get_str())
        preset.add_separator()


class SubABPL:
    def __init__(self, parent, window):
        m_loc = loc["tab_tweaks"]

        self.root = ttk.LabelFrame(parent, text=m_loc["f_abpl"], padding=3)
        self.x_abpl_enabled = CCheckbox(self.root, m_loc["x_abpl_enabled"])
        self.script = ""

        self.x_abpl_enabled.root.pack()
        ttk.Button(self.root, text=m_loc["b_abpl_edit"], command=lambda: edit_abpl(window)).pack()

    def apply_config(self, config: ScramblerConfig):
        config.abpl_enabled = self.x_abpl_enabled.get()
        config.abpl_script = format_script(self.script)

    def open_preset(self, preset: PresetOpen):
        preset.batch_set([[self.x_abpl_enabled, "abpl_enabled", "1"]])
        try:
            script_b64 = preset.get("abpl_script", "")
            self.script = base64.b64decode(script_b64.encode("utf-8")).decode("utf-8")
        except Exception as e:
            self.script = f"# {e}"

    def save_preset(self, preset: PresetSave):
        script_b64 = base64.b64encode(self.script.encode("utf-8")).decode("utf-8")
        preset.add("abpl_enabled", self.x_abpl_enabled.get_str())
        preset.add("abpl_script", script_b64)
        preset.add_separator()


class TabTweak:
    def __init__(self, parent, window):
        self.root = ttk.Frame(parent, padding=10)

        col1 = ttk.Frame(self.root)
        col2 = ttk.Frame(self.root)

        self.cons = SubConsec(col1)
        self.main = SubTweak(col1)
        self.trim = SubTrim(col2)
        self.abpl = SubABPL(col2, window)

        col1.grid(row=0, column=0, sticky="n")
        col2.grid(row=0, column=1, sticky="n", padx=4)

        self.cons.root.pack(fill="x")
        self.main.root.pack(fill="x")
        self.trim.root.pack(fill="x")
        self.abpl.root.pack(fill="x")

    def update(self):
        self.trim.update()

    def convert_time(self, mode):
        self.trim.convert_time(mode)

    def apply_config(self, config: ScramblerConfig):
        self.cons.apply_config(config)
        self.main.apply_config(config)
        self.trim.apply_config(config)
        self.abpl.apply_config(config)

    def open_preset(self, preset: PresetOpen):
        self.cons.open_preset(preset)
        self.main.open_preset(preset)
        self.trim.open_preset(preset)
        self.abpl.open_preset(preset)

    def save_preset(self, preset: PresetSave):
        self.cons.save_preset(preset)
        self.main.save_preset(preset)
        self.abpl.save_preset(preset)
        self.trim.save_preset(preset)
