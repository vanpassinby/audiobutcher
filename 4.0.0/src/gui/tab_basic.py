from ab_random import *
from ab_tools import str_list_with_range
from scrambler.scr_state import ScramblerConfig
from preset import PresetOpen, PresetSave
from gui.gui_common import *


class SpeedChange:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Speed change ", padding=5)

        self.l_speed_main = ttk.Label(self.root, text="Main speed: ")
        self.e_speed_main = XEntry(self.root, width=10)
        self.c_speed_measure = XCombobox(self.root, width=30, values=meta.cb_speed_mode, state="readonly")
        self.l_speed_alter = ttk.Label(self.root, text="Speed alteration chance: ")
        self.e_speed_alter = CChance(self.root, padding=0)

        self.l_speed_main.grid(row=0, column=0, sticky="w")
        self.e_speed_main.grid(row=0, column=1)
        self.c_speed_measure.grid(row=0, column=2, padx=2)
        self.root.grid_columnconfigure(3, weight=1)
        self.l_speed_alter.grid(row=0, column=4)
        self.e_speed_alter.root.grid(row=0, column=5)

        self.l_speed_variations = ttk.Label(self.root, text="Speed variations: ")
        self.e_speed_variations = XEntry(self.root)
        self.l_speed_weights = ttk.Label(self.root, text="Weights (optional): ")
        self.e_speed_weights = XEntry(self.root)
        self.l_speed_affect_mode = ttk.Label(self.root, text="Length scaling: ")
        self.c_speed_affect_mode = XCombobox(self.root, values=meta.cb_speed_affect, state="readonly")

        self.l_speed_variations.grid(row=1, column=0, sticky="w")
        self.e_speed_variations.grid(row=1, column=1, columnspan=5, pady=2, sticky="ew")
        self.l_speed_weights.grid(row=2, column=0, sticky="w")
        self.e_speed_weights.grid(row=2, column=1, columnspan=5, sticky="ew")
        self.l_speed_affect_mode.grid(row=3, column=0, sticky="w")
        self.c_speed_affect_mode.grid(row=3, column=1, columnspan=5, pady=2, sticky="ew")

    def apply_config(self, config: ScramblerConfig):
        def conv(speed):
            if mode == 0:
                return 2 ** (float(speed) / 12)
            elif mode == 1:
                return 1 + float(speed) / 100
            elif mode == 2:
                return float(speed)
            else:
                return 0

        mode = self.c_speed_measure.current()
        config.speed_main = conv(self.e_speed_main.get())
        config.speed_alter_chance = self.e_speed_alter.get()

        speed_v = list(map(conv, str_list_with_range(self.e_speed_variations.get())))
        speed_w = list(map(int, self.e_speed_weights.get().split()))
        if len(speed_w) == 0:
            speed_w = [1] * len(speed_v)

        config.speed_variations = RandChoice(speed_v, speed_w)
        config.speed_affect_mode = self.c_speed_affect_mode.current()

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.e_speed_main, "speed_main", "0"],
            [self.c_speed_measure, "speed_measure", "0"],
            [self.e_speed_alter, "speed_alter_chance", "0"],
            [self.e_speed_variations, "speed_variations", "0"],
            [self.e_speed_weights, "speed_weights", ""],
            [self.c_speed_affect_mode, "speed_affect_mode", "0"]
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("speed_main", self.e_speed_main.get())
        preset.add("speed_measure", self.c_speed_measure.current())
        preset.add("speed_alter_chance", self.e_speed_alter.get_str())
        preset.add("speed_variations", self.e_speed_variations.get())
        preset.add("speed_weights", self.e_speed_weights.get())
        preset.add("speed_affect_mode", self.c_speed_affect_mode.current())
        preset.add_separator()


class TabBasic:
    def __init__(self, parent):
        self.root = ttk.Frame(parent, padding=10)
        ttk.Label(self.root, width=1).grid(row=0, column=3)
        ttk.Label(self.root, width=1).grid(row=0, column=6)

        self.l_duration = ttk.Label(self.root, text="Segment length: ")
        self.e_duration = CDistribution(self.root)
        self.l_reverse1 = ttk.Label(self.root, text="First reverse chance: ")
        self.e_reverse1 = CChance(self.root)
        self.l_reverse2 = ttk.Label(self.root, text="Second reverse chance: ")
        self.e_reverse2 = CChance(self.root)

        self.l_duration.grid(row=0, column=0, columnspan=2, sticky="w")
        self.e_duration.root.grid(row=0, column=2)
        self.l_reverse1.grid(row=0, column=4, sticky="w")
        self.e_reverse1.root.grid(row=0, column=5)
        self.l_reverse2.grid(row=0, column=7, sticky="w")
        self.e_reverse2.root.grid(row=0, column=8)

        self.l_pause = ttk.Label(self.root, text="Pause length: ")
        self.e_pause = CDistribution(self.root)
        self.l_pause_chance = ttk.Label(self.root, text="Pause chance: ")
        self.e_pause_chance = CChance(self.root)
        self.l_consec_pause_chance = ttk.Label(self.root, text="Consecutive pause chance: ")
        self.e_consec_pause_chance = CChance(self.root)

        self.l_pause.grid(row=1, column=0, columnspan=2, sticky="w")
        self.e_pause.root.grid(row=1, column=2)
        self.l_pause_chance.grid(row=1, column=4, sticky="w")
        self.e_pause_chance.root.grid(row=1, column=5)
        self.l_consec_pause_chance.grid(row=1, column=7, sticky="w")
        self.e_consec_pause_chance.root.grid(row=1, column=8)

        self.l_crossfade = ttk.Label(self.root, text="Crossfade length: ")
        self.e_crossfade = CDistribution(self.root)
        self.l_crossfade_chance = ttk.Label(self.root, text="Crossfade chance: ")
        self.e_crossfade_chance = CChance(self.root)

        self.l_crossfade.grid(row=2, column=0, columnspan=2, sticky="w")
        self.e_crossfade.root.grid(row=2, column=2)
        self.l_crossfade_chance.grid(row=2, column=4, sticky="w")
        self.e_crossfade_chance.root.grid(row=2, column=5)

        self.l_fadein = ttk.Label(self.root, text="Fade-in length: ")
        self.x_fadein_perc = CCheckbox(self.root, "%")
        self.e_fadein = CDistribution(self.root)
        self.l_fadein_chance = ttk.Label(self.root, text="Fade-in chance: ")
        self.e_fadein_chance = CChance(self.root)

        self.l_fadein.grid(row=3, column=0, sticky="w")
        self.x_fadein_perc.root.grid(row=3, column=1, sticky="e")
        self.e_fadein.root.grid(row=3, column=2)
        self.l_fadein_chance.grid(row=3, column=4, sticky="w")
        self.e_fadein_chance.root.grid(row=3, column=5)

        self.l_fade_only_into_pauses = ttk.Label(self.root, text="Fade only into pauses (chance): ")
        self.e_fade_only_into_pauses = CChance(self.root)
        self.l_fade_only_into_pauses.grid(row=3, column=7, sticky="w")
        self.e_fade_only_into_pauses.root.grid(row=3, column=8)

        self.l_fadeout = ttk.Label(self.root, text="Fade-out length: ")
        self.x_fadeout_perc = CCheckbox(self.root, "%")
        self.x_fadeout_perc.root.configure(command=self.update)
        self.e_fadeout = CDistribution(self.root)
        self.l_fadeout_chance = ttk.Label(self.root, text="Fade-out chance: ")
        self.e_fadeout_chance = CChance(self.root)
        self.x_fade_out_perc_note = CCheckbox(self.root, text="Measure fade-out from last slice")

        self.l_fadeout.grid(row=4, column=0, sticky="w")
        self.x_fadeout_perc.root.grid(row=4, column=1, sticky="e")
        self.e_fadeout.root.grid(row=4, column=2)
        self.l_fadeout_chance.grid(row=4, column=4, sticky="w")
        self.e_fadeout_chance.root.grid(row=4, column=5)
        self.x_fade_out_perc_note.root.grid(row=4, column=7, columnspan=2, sticky="w")

        self.l_repeat = ttk.Label(self.root, text="Repeat amount: ")
        self.e_repeat = CDistribution(self.root)
        self.l_repeat_chance = ttk.Label(self.root, text="Repeat chance: ")
        self.e_repeat_chance = CChance(self.root)
        self.x_repeat_in_mss = CCheckbox(self.root, text="Measure repeats in ms/sec")

        self.l_repeat.grid(row=6, column=0, columnspan=2, sticky="w")
        self.e_repeat.root.grid(row=6, column=2)
        self.l_repeat_chance.grid(row=6, column=4, sticky="w")
        self.e_repeat_chance.root.grid(row=6, column=5)
        self.x_repeat_in_mss.root.grid(row=6, column=7, columnspan=2, sticky="w")

        self.l_reappear = ttk.Label(self.root, text="Reappear interval: ")
        self.e_reappear = CDistribution(self.root)
        self.l_reappear_chance = ttk.Label(self.root, text="Reappear chance: ")
        self.e_reappear_chance = CChance(self.root)
        self.l_reappear_reoccur_chance = ttk.Label(self.root, text="Allow reoccurrence (chance): ")
        self.e_reappear_reoccur_chance = CChance(self.root)

        self.l_reappear.grid(row=7, column=0, columnspan=2, sticky="w")
        self.e_reappear.root.grid(row=7, column=2)
        self.l_reappear_chance.grid(row=7, column=4, sticky="w")
        self.e_reappear_chance.root.grid(row=7, column=5)
        self.l_reappear_reoccur_chance.grid(row=7, column=7, sticky="w")
        self.e_reappear_reoccur_chance.root.grid(row=7, column=8)

        self.f_speed_change = SpeedChange(self.root)
        self.f_speed_change.root.grid(row=8, column=0, columnspan=9, sticky="ew")

    def update(self):
        if self.x_fadeout_perc.get():
            self.x_fade_out_perc_note.root.configure(state="normal")
        else:
            self.x_fade_out_perc_note.root.configure(state="disabled")
            self.x_fade_out_perc_note.set(0)

    def convert_time(self, mode):
        self.e_duration.conv_time(mode)
        self.e_pause.conv_time(mode)
        self.e_crossfade.conv_time(mode)

        if not self.x_fadein_perc.get():
            self.e_fadein.conv_time(mode)
        if not self.x_fadeout_perc.get():
            self.e_fadeout.conv_time(mode)
        if self.x_repeat_in_mss.get():
            self.e_repeat.conv_time(mode)

    def apply_config(self, config: ScramblerConfig):
        config.duration_dist = self.e_duration.get()
        config.reverse1_chance = self.e_reverse1.get()
        config.reverse2_chance = self.e_reverse2.get()

        config.pause_dist = self.e_pause.get()
        config.pause_chance = self.e_pause_chance.get()
        config.pause_consec_chance = self.e_consec_pause_chance.get()

        config.crossfade = self.e_crossfade.get()
        config.crossfade_chance = self.e_crossfade_chance.get()

        config.fade_in_dist = self.e_fadein.get()
        config.fade_in_perc = self.x_fadein_perc.get()
        config.fade_in_chance = self.e_fadein_chance.get()

        config.fade_out_dist = self.e_fadeout.get()
        config.fade_out_perc = self.x_fadeout_perc.get()
        config.fade_out_chance = self.e_fadeout_chance.get()

        config.fade_only_into_pauses = self.e_fade_only_into_pauses.get()
        config.fade_out_perc_note = self.x_fade_out_perc_note.get()

        config.repeat_dist = self.e_repeat.get()
        config.repeat_chance = self.e_repeat_chance.get()
        config.repeat_in_mss = self.x_repeat_in_mss.get()

        config.reappear_after_dist = self.e_reappear.get()
        config.reappear_chance = self.e_reappear_chance.get()
        config.reappear_reoccur_chance = self.e_reappear_reoccur_chance.get()

        self.f_speed_change.apply_config(config)

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.e_duration, "duration_dist", "0 0 0"],
            [self.e_reverse1, "reverse1_chance", "0"],
            [self.e_reverse2, "reverse2_chance", "0"],

            [self.e_pause, "pause_dist", "0 0 0"],
            [self.e_pause_chance, "pause_chance", "0"],
            [self.e_consec_pause_chance, "pause_consec_chance", "0"],

            [self.e_crossfade, "crossfade", "0 0 0"],
            [self.e_crossfade_chance, "crossfade_chance", "100"],

            [self.e_fadein, "fade_in_dist", "0 0 0"],
            [self.x_fadein_perc, "fade_in_perc", "0"],
            [self.e_fadein_chance, "fade_in_chance", "100"],

            [self.e_fadeout, "fade_out_dist", "0 0 0"],
            [self.x_fadeout_perc, "fade_out_perc", "0"],
            [self.e_fadeout_chance, "fade_out_chance", "100"],

            [self.e_fade_only_into_pauses, "fade_only_into_pauses", "0"],
            [self.x_fade_out_perc_note, "fade_out_perc_note", "0"],

            [self.e_repeat, "repeat_dist", "0 0 0"],
            [self.e_repeat_chance, "repeat_chance", "0"],
            [self.x_repeat_in_mss, "repeat_in_mss", "0"],

            [self.e_reappear, "reappear_after_dist", "0 0 0"],
            [self.e_reappear_chance, "reappear_chance", "0"],
            [self.e_reappear_reoccur_chance, "reappear_reoccur_chance", "0"]
        ]

        preset.batch_set(batch)
        self.f_speed_change.open_preset(preset)

    def save_preset(self, preset: PresetSave):
        preset.add("duration_dist", self.e_duration.get_str())
        preset.add("reverse1_chance", self.e_reverse1.get_str())
        preset.add("reverse2_chance", self.e_reverse2.get_str())
        preset.add("pause_dist", self.e_pause.get_str())
        preset.add("pause_chance", self.e_pause_chance.get_str())
        preset.add("pause_consec_chance", self.e_consec_pause_chance.get_str())
        preset.add("crossfade", self.e_crossfade.get_str())
        preset.add("crossfade_chance", self.e_crossfade_chance.get_str())
        preset.add_separator()

        preset.add("fade_in_dist", self.e_fadein.get_str())
        preset.add("fade_in_perc", self.x_fadein_perc.get_str())
        preset.add("fade_in_chance", self.e_fadein_chance.get_str())
        preset.add("fade_out_dist", self.e_fadeout.get_str())
        preset.add("fade_out_perc", self.x_fadeout_perc.get_str())
        preset.add("fade_out_chance", self.e_fadeout_chance.get_str())
        preset.add("fade_only_into_pauses", self.e_fade_only_into_pauses.get_str())
        preset.add("fade_out_perc_note", self.x_fade_out_perc_note.get_str())
        preset.add_separator()

        preset.add("repeat_dist", self.e_repeat.get_str())
        preset.add("repeat_chance", self.e_repeat_chance.get_str())
        preset.add("repeat_in_mss", self.x_repeat_in_mss.get_str())
        preset.add("reappear_after_dist", self.e_reappear.get_str())
        preset.add("reappear_chance", self.e_reappear_chance.get_str())
        preset.add("reappear_reoccur_chance", self.e_reappear_reoccur_chance.get_str())
        preset.add_separator()

        self.f_speed_change.save_preset(preset)
