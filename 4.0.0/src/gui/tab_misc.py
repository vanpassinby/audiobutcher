import weakref
from slicing import Onsets
from ab_random import RandChoice
from scrambler.scr_state import ScramblerConfig

from preset import PresetOpen, PresetSave
from gui.gui_common import *
from gui.slice_detect import edit_slices


class SubShift:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Segment shifting ", padding=3)

        self.l_deviation = ttk.Label(self.root, text="Deviation: ")
        self.e_deviation = CDistribution(self.root)
        self.l_chance = ttk.Label(self.root, text="Chance: ")
        self.e_chance = CChance(self.root)

        ttk.Label(self.root).grid(row=0, column=2)
        self.l_deviation.grid(row=0, column=0, sticky="w")
        self.e_deviation.root.grid(row=0, column=1, sticky="w")
        self.l_chance.grid(row=0, column=3, sticky="w")
        self.e_chance.root.grid(row=0, column=4, sticky="w")

        line2 = ttk.Frame(self.root)
        self.l_dev_direction = ttk.Label(line2, text="Direction: <- vs ->")
        self.e_dev_direction = CWeights(line2, 2)
        self.x_dev_proportional = CCheckbox(line2, text="Proportional to frame length (%)")

        line2.grid(row=2, column=0, columnspan=5, sticky="w")
        ttk.Label(line2).grid(row=0, column=2)
        self.l_dev_direction.grid(row=0, column=0)
        self.e_dev_direction.root.grid(row=0, column=1)
        self.x_dev_proportional.root.grid(row=0, column=3)

    def apply_config(self, config: ScramblerConfig):
        config.shift_deviation = self.e_deviation.get()
        config.shift_chance = self.e_chance.get()
        config.shift_dev_proportional = self.x_dev_proportional.get()
        config.shift_dev_direction = RandChoice([-1, 1], self.e_dev_direction.get())

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.e_deviation, "shift_deviation", "0 0 0"],
            [self.e_chance, "shift_chance", "0"],
            [self.x_dev_proportional, "shift_dev_proportional", "0"],
            [self.e_dev_direction, "shift_dev_direction", "1 1"]
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("shift_deviation", self.e_deviation.get_str())
        preset.add("shift_chance", self.e_chance.get_str())
        preset.add("shift_dev_proportional", self.x_dev_proportional.get_str())
        preset.add("shift_dev_direction", self.e_dev_direction.get_str())
        preset.add_separator()


class SubFadeCutoff:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Fade cutoff (%) ", padding=3)

        self.l_fade_in_cut_dist = ttk.Label(self.root, text="Fade-in: ")
        self.e_fade_in_cut_dist = CDistribution(self.root)
        self.l_fade_in_cut_chance = ttk.Label(self.root, text="Chance: ")
        self.e_fade_in_cut_chance = CChance(self.root)

        ttk.Label(self.root).grid(row=0, column=2)
        self.l_fade_in_cut_dist.grid(row=0, column=0, sticky="w")
        self.e_fade_in_cut_dist.root.grid(row=0, column=1)
        self.l_fade_in_cut_chance.grid(row=0, column=3, sticky="w")
        self.e_fade_in_cut_chance.root.grid(row=0, column=4)

        self.l_fade_out_cut_dist = ttk.Label(self.root, text="Fade-out: ")
        self.e_fade_out_cut_dist = CDistribution(self.root)
        self.l_fade_out_cut_chance = ttk.Label(self.root, text="Chance: ")
        self.e_fade_out_cut_chance = CChance(self.root)

        self.l_fade_out_cut_dist.grid(row=1, column=0, sticky="w")
        self.e_fade_out_cut_dist.root.grid(row=1, column=1)
        self.l_fade_out_cut_chance.grid(row=1, column=3, sticky="w")
        self.e_fade_out_cut_chance.root.grid(row=1, column=4)

    def apply_config(self, config: ScramblerConfig):
        config.fade_in_cut_dist = self.e_fade_in_cut_dist.get()
        config.fade_in_cut_chance = self.e_fade_in_cut_chance.get()
        config.fade_out_cut_dist = self.e_fade_out_cut_dist.get()
        config.fade_out_cut_chance = self.e_fade_out_cut_chance.get()

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.e_fade_in_cut_dist, "fade_in_cut_dist", "0 0 0"],
            [self.e_fade_in_cut_chance, "fade_in_cut_chance", "100"],
            [self.e_fade_out_cut_dist, "fade_out_cut_dist", "0 0 0"],
            [self.e_fade_out_cut_chance, "fade_out_cut_chance", "100"],
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("fade_in_cut_dist", self.e_fade_in_cut_dist.get_str())
        preset.add("fade_in_cut_chance", self.e_fade_in_cut_chance.get_str())
        preset.add("fade_out_cut_dist", self.e_fade_out_cut_dist.get_str())
        preset.add("fade_out_cut_chance", self.e_fade_out_cut_chance.get_str())
        preset.add_separator()


class SubVolMute:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Mute ", padding=3)

        self.l_mute_chance = ttk.Label(self.root, text="Mute chance: ")
        self.e_mute_chance = CChance(self.root)
        self.l_mute_to_pause = ttk.Label(self.root, text="Resize muted segment\nto pause length (chance): ",
                                         anchor="center")
        self.e_mute_to_pause = CChance(self.root)

        ttk.Label(self.root).grid(row=0, column=2)
        self.l_mute_chance.grid(row=0, column=0, sticky="w")
        self.e_mute_chance.root.grid(row=0, column=1, sticky="w")
        self.l_mute_to_pause.grid(row=0, column=3, sticky="w")
        self.e_mute_to_pause.root.grid(row=0, column=4, sticky="w")

    def apply_config(self, config: ScramblerConfig):
        config.volume_mute_chance = self.e_mute_chance.get()
        config.volume_mute_to_pause = self.e_mute_to_pause.get()

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.e_mute_chance, "volume_mute_chance", "0"],
            [self.e_mute_to_pause, "volume_mute_to_pause", "0"]
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("volume_mute_chance", self.e_mute_chance.get_str())
        preset.add("volume_mute_to_pause", self.e_mute_to_pause.get_str())


class SubVolume:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Volume change ", padding=3)

        self.l_alt_chance = ttk.Label(self.root, text="Chance: ")
        self.e_alt_chance = CChance(self.root)
        self.l_alt_chance.grid(row=0, column=0, sticky="w")
        self.e_alt_chance.root.grid(row=0, column=1, sticky="w")

        self.l_change = ttk.Label(self.root, text="V. change: ")
        self.e_change = CDistribution(self.root)
        ttk.Label(self.root).grid(row=0, column=2)
        self.l_change.grid(row=0, column=3, sticky="w")
        self.e_change.root.grid(row=0, column=4, sticky="w")

        self.l_direction = ttk.Label(self.root, text="Direction: ")
        self.e_direction = CWeights(self.root, amount=2)
        self.l_direction_hint = ttk.Label(self.root, text="Softer vs louder (weight)")
        self.l_direction.grid(row=1, column=3, sticky="w")
        self.e_direction.root.grid(row=1, column=4, sticky="w")
        self.l_direction_hint.grid(row=1, column=4, sticky="e")

        self.f_mute = SubVolMute(self.root)
        self.f_mute.root.grid(row=2, column=0, columnspan=5, sticky="w")

    def apply_config(self, config: ScramblerConfig):
        config.volume_alt_chance = self.e_alt_chance.get()
        config.volume_change = self.e_change.get()
        config.volume_direction = RandChoice([-1, +1], self.e_direction.get())
        self.f_mute.apply_config(config)

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.e_alt_chance, "volume_alt_chance", "0"],
            [self.e_change, "volume_change", "0 0 0"],
            [self.e_direction, "volume_direction", "1 1"]
        ]

        preset.batch_set(batch)
        self.f_mute.open_preset(preset)

    def save_preset(self, preset: PresetSave):
        preset.add("volume_alt_chance", self.e_alt_chance.get_str())
        preset.add("volume_change", self.e_change.get_str())
        preset.add("volume_direction", self.e_direction.get_str())
        self.f_mute.save_preset(preset)
        preset.add_separator()


class SubIntroLoop:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Intro loop ", padding=3)

        self.l_intro_loop_length = ttk.Label(self.root, text="Intro length: ")
        self.e_intro_loop_length = XEntry(self.root, width=8)
        self.l_intro_loop_length.grid(row=0, column=0, sticky="w")
        self.e_intro_loop_length.grid(row=0, column=1, padx=1, pady=1, sticky="w")

        self.l_intro_loop_chance = ttk.Label(self.root, text="Loop chance: ")
        self.e_intro_loop_chance = CChance(self.root, ent_w=8)
        self.l_intro_loop_chance.grid(row=1, column=0, sticky="w")
        self.e_intro_loop_chance.root.grid(row=1, column=1, sticky="w")

    def apply_config(self, config: ScramblerConfig):
        config.intro_loop_length = float(self.e_intro_loop_length.get())
        config.intro_loop_chance = self.e_intro_loop_chance.get()

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.e_intro_loop_length, "intro_loop_length", "0"],
            [self.e_intro_loop_chance, "intro_loop_chance", "0"],
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("intro_loop_length", self.e_intro_loop_length.get())
        preset.add("intro_loop_chance", self.e_intro_loop_chance.get_str())
        preset.add_separator()


class SubQuanPlacement:
    def __init__(self, parent, window):
        self.root = ttk.LabelFrame(parent, text=" Placement quantization ", padding=3)
        self.onset_data = Onsets([], 1000)
        ref_window = weakref.ref(window)

        self.c_mode = XCombobox(self.root, state="readonly", values=meta.cb_place_quan)
        self.l_step = ttk.Label(self.root, text="Step: ")
        self.e_step = XEntry(self.root, width=6)
        self.l_length_k = ttk.Label(self.root, text="Length K: ")
        self.e_length_k = XEntry(self.root, width=6)
        self.l_strength = ttk.Label(self.root, text="Strength: ")
        self.e_strength = CChance(self.root, ent_w=6)
        self.b_edit_onsets = ttk.Button(self.root, text="Edit onsets")

        self.root.grid_columnconfigure(0, weight=1)
        self.c_mode.grid(row=0, column=0, columnspan=2, pady=1, sticky="we")
        self.l_step.grid(row=1, column=0, sticky="w")
        self.e_step.grid(row=1, column=1, padx=1, pady=1, sticky="w")
        self.l_strength.grid(row=3, column=0, sticky="w")
        self.e_strength.root.grid(row=3, column=1, sticky="w")
        self.b_edit_onsets.grid(row=4, column=0, columnspan=2, pady=1)

        self.c_mode.bind("<<ComboboxSelected>>", lambda _: self.update())
        self.b_edit_onsets.configure(command=lambda: edit_slices(ref_window(), self.onset_data))

    def update(self):
        self.e_step.configure(state="normal" if self.c_mode.current() == 1 else "disabled")
        self.e_strength.e_chance.configure(state="disabled" if self.c_mode.current() == 0 else "normal")

    def convert_time(self, mode):
        try:
            if float(self.e_step.get()) > 0:
                self.e_step.conv_time(mode)
        except ValueError:
            pass

    def apply_config(self, config: ScramblerConfig):
        config.quan_place_mode = self.c_mode.current()
        config.quan_place_step = float(self.e_step.get())
        config.quan_place_strength = abs(float(self.e_strength.get_str()))
        config.quan_place_onsets = self.onset_data

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.c_mode, "quan_place_mode", "0"],
            [self.e_step, "quan_place_step", "0"],
            [self.e_strength, "quan_place_strength", "100"]
        ]

        preset.batch_set(batch)

        onsets = list(map(int, preset.get("quan_place_onsets", "").split()))
        onset_sr = int(preset.get("quan_place_onsets_sr", "1000"))
        self.onset_data.override(Onsets(onsets, onset_sr))

    def save_preset(self, preset: PresetSave):
        preset.add("quan_place_mode", self.c_mode.current())
        preset.add("quan_place_step", self.e_step.get())
        preset.add("quan_place_strength", self.e_strength.get_str())
        preset.add("quan_place_onsets", self.onset_data.as_str)
        preset.add("quan_place_onsets_sr", self.onset_data.sample_rate)
        preset.add_separator()


class TabMisc:
    def __init__(self, parent, window):
        self.root = ttk.Frame(parent, padding=10)
        self.shift = SubShift(self.root)
        self.cutoff = SubFadeCutoff(self.root)
        self.volume = SubVolume(self.root)
        self.intro_loop = SubIntroLoop(self.root)
        self.place_quan = SubQuanPlacement(self.root, window)

        self.shift.root.grid(row=0, column=0, sticky="we")
        self.cutoff.root.grid(row=1, column=0, sticky="we", pady=2)
        self.volume.root.grid(row=2, column=0, sticky="we")
        self.intro_loop.root.grid(row=0, column=1, padx=4, sticky="ns")
        self.place_quan.root.grid(row=1, column=1, rowspan=2, padx=4, pady=2, sticky="nw")

    def update(self):
        self.place_quan.update()

    def convert_time(self, mode):
        if not self.shift.x_dev_proportional.get():
            self.shift.e_deviation.conv_time(mode)
        self.intro_loop.e_intro_loop_length.conv_time(mode)
        self.place_quan.convert_time(mode)

    def apply_config(self, config: ScramblerConfig):
        self.shift.apply_config(config)
        self.cutoff.apply_config(config)
        self.volume.apply_config(config)
        self.intro_loop.apply_config(config)
        self.place_quan.apply_config(config)

    def open_preset(self, preset: PresetOpen):
        self.shift.open_preset(preset)
        self.cutoff.open_preset(preset)
        self.volume.open_preset(preset)
        self.intro_loop.open_preset(preset)
        self.place_quan.open_preset(preset)

    def save_preset(self, preset: PresetSave):
        self.shift.save_preset(preset)
        self.cutoff.save_preset(preset)
        self.volume.save_preset(preset)
        self.intro_loop.save_preset(preset)
        self.place_quan.save_preset(preset)
