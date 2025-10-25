from ab_random import RandChoice
from scrambler.scr_state import ScramblerConfig, ScramblerConfigSubSkip
from preset import PresetOpen, PresetSave
from gui.gui_common import *


class LoopChances:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Chances ", padding=3)

        self.l_pattern = ttk.Label(self.root, text="Pattern: ")
        self.e_pattern = CChance(self.root)
        self.l_pattern.grid(row=0, column=0, sticky="w")
        self.e_pattern.root.grid(row=0, column=1)

        self.l_repeat = ttk.Label(self.root, text="Repeat: ")
        self.e_repeat = CChance(self.root)
        self.l_repeat.grid(row=1, column=0, sticky="w")
        self.e_repeat.root.grid(row=1, column=1)

        self.l_count_full_length = ttk.Label(self.root, text="Count full length: ")
        self.e_count_full_length = CChance(self.root)
        self.l_count_full_length.grid(row=2, column=0, sticky="w")
        self.e_count_full_length.root.grid(row=2, column=1)

        self.l_count_pause_length = ttk.Label(self.root, text="Count pause length: ")
        self.e_count_pause_length = CChance(self.root)
        self.l_count_pause_length.grid(row=3, column=0, sticky="w")
        self.e_count_pause_length.root.grid(row=3, column=1)

        self.l_count_pattern_length = ttk.Label(self.root, text="Count pattern length: ")
        self.e_count_pattern_length = CChance(self.root)
        self.l_count_pattern_length.grid(row=4, column=0, sticky="w")
        self.e_count_pattern_length.root.grid(row=4, column=1)

        self.l_break_skips = ttk.Label(self.root, text="Skipping can break loop: ")
        self.e_break_skips = CChance(self.root)
        self.l_break_skips.grid(row=5, column=0, sticky="w")
        self.e_break_skips.root.grid(row=5, column=1)

        self.l_break_pattern = ttk.Label(self.root, text="Pattern can break loop: ")
        self.e_break_pattern = CChance(self.root)
        self.l_break_pattern.grid(row=6, column=0, sticky="w")
        self.e_break_pattern.root.grid(row=6, column=1)

        self.l_break_avgstart = ttk.Label(self.root, text="AST can break loop: ")
        self.e_break_avgstart = CChance(self.root)
        self.l_break_avgstart.grid(row=7, column=0, sticky="w")
        self.e_break_avgstart.root.grid(row=7, column=1)

    def apply_config(self, config: ScramblerConfig):
        config.loop_pattern_chance = self.e_pattern.get()
        config.loop_repeat_chance = self.e_repeat.get()
        config.loop_count_full_length = self.e_count_full_length.get()
        config.loop_count_pause_length = self.e_count_pause_length.get()
        config.loop_count_pattern_length = self.e_count_pattern_length.get()
        config.loop_break_skips = self.e_break_skips.get()
        config.loop_break_pattern = self.e_break_pattern.get()
        config.loop_break_avgstart = self.e_break_avgstart.get()

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.e_pattern, "loop_pattern_chance", "100"],
            [self.e_repeat, "loop_repeat_chance", "0"],
            [self.e_count_full_length, "loop_count_full_length", "100"],
            [self.e_count_pause_length, "loop_count_pause_length", "100"],
            [self.e_count_pattern_length, "loop_count_pattern_length", "100"],
            [self.e_break_skips, "loop_break_skips", "0"],
            [self.e_break_pattern, "loop_break_pattern", "0"],
            [self.e_break_avgstart, "loop_break_avgstart", "0"]
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("loop_pattern_chance", self.e_pattern.get_str())
        preset.add("loop_repeat_chance", self.e_repeat.get_str())
        preset.add("loop_count_full_length", self.e_count_full_length.get_str())
        preset.add("loop_count_pause_length", self.e_count_pause_length.get_str())
        preset.add("loop_count_pattern_length", self.e_count_pattern_length.get_str())
        preset.add("loop_break_skips", self.e_break_skips.get_str())
        preset.add("loop_break_pattern", self.e_break_pattern.get_str())
        preset.add("loop_break_avgstart", self.e_break_avgstart.get_str())


class LoopSkipVariant:
    def __init__(self, parent):
        self.root = ttk.Frame(parent, padding=3)

        self.l_weight = ttk.Label(self.root, text="Direction weight: ")
        self.e_weight = XEntry(self.root, width=6)
        self.l_weight.grid(row=0, column=0, sticky="w")
        self.e_weight.grid(row=0, column=1, pady=1)

        self.l_min_skip = ttk.Label(self.root, text="Minimum skip: ")
        self.e_min_skip = XEntry(self.root, width=6)
        self.l_min_skip_chance = ttk.Label(self.root, text="Chance: ")
        self.e_min_skip_chance = CChance(self.root)
        self.l_min_skip.grid(row=1, column=0, sticky="w")
        self.e_min_skip.grid(row=1, column=1)
        ttk.Label(self.root).grid(row=1, column=2)
        self.l_min_skip_chance.grid(row=1, column=3, sticky="w")
        self.e_min_skip_chance.root.grid(row=1, column=4)

        self.l_add_dev = ttk.Label(self.root, text="Additional deviation: ")
        self.e_add_dev = XEntry(self.root, width=6)
        self.l_add_dev_chance = ttk.Label(self.root, text="Chance: ")
        self.e_add_dev_chance = CChance(self.root)
        self.l_add_dev.grid(row=2, column=0, sticky="w")
        self.e_add_dev.grid(row=2, column=1)
        self.l_add_dev_chance.grid(row=2, column=3, sticky="w")
        self.e_add_dev_chance.root.grid(row=2, column=4)

    def conv_time(self, mode):
        self.e_min_skip.conv_time(mode)
        self.e_add_dev.conv_time(mode)

    def get_subconfig(self) -> (int, ScramblerConfigSubSkip):
        weight = int(self.e_weight.get())
        sub = ScramblerConfigSubSkip()

        sub.min_skip = float(self.e_min_skip.get())
        sub.min_skip_chance = self.e_min_skip_chance.get()
        sub.add_dev = float(self.e_add_dev.get())
        sub.add_dev_chance = self.e_add_dev_chance.get()

        return weight, sub

    def open_preset(self, ident, preset: PresetOpen):
        batch = [
            [self.e_weight, f"skip_{ident}_weight", "0"],
            [self.e_min_skip, f"skip_{ident}_min_skip", "0"],
            [self.e_min_skip_chance, f"skip_{ident}_min_skip_chance", "100"],
            [self.e_add_dev, f"skip_{ident}_add_dev", "0"],
            [self.e_add_dev_chance, f"skip_{ident}_add_dev_chance", "100"]
        ]

        preset.batch_set(batch)

    def save_preset(self, ident, preset: PresetSave):
        preset.add(f"skip_{ident}_weight", self.e_weight.get())
        preset.add(f"skip_{ident}_min_skip", self.e_min_skip.get())
        preset.add(f"skip_{ident}_min_skip_chance", self.e_min_skip_chance.get_str())
        preset.add(f"skip_{ident}_add_dev", self.e_add_dev.get())
        preset.add(f"skip_{ident}_add_dev_chance", self.e_add_dev_chance.get_str())
        preset.add_separator()


class LoopSkipping:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Skipping ", padding=3)

        self.l_chance = ttk.Label(self.root, text="Skip chance: ")
        self.e_chance = CChance(self.root)
        self.l_chance.grid(row=0, column=0, sticky="w")
        self.root.grid_columnconfigure(1, weight=1)
        self.e_chance.root.grid(row=0, column=1, sticky="w")

        self.f_modes = ttk.Notebook(self.root)
        self.f_forw = LoopSkipVariant(self.root)
        self.f_back = LoopSkipVariant(self.root)
        self.f_rand = LoopSkipVariant(self.root)

        self.f_modes.grid(row=1, column=0, columnspan=2)
        self.f_modes.add(self.f_forw.root, text="Forwards")
        self.f_modes.add(self.f_back.root, text="Backwards")
        self.f_modes.add(self.f_rand.root, text="Random")

    def apply_config(self, config: ScramblerConfig):
        config.skip_chance = self.e_chance.get()
        w_forw, config.skip_forw = self.f_forw.get_subconfig()
        w_back, config.skip_back = self.f_back.get_subconfig()
        w_rand, config.skip_rand = self.f_rand.get_subconfig()
        config.skip_weights = RandChoice([0, 1, 2], [w_forw, w_back, w_rand])

    def open_preset(self, preset: PresetOpen):
        self.e_chance.set(preset.get("skip_chance", "100"))
        self.f_forw.open_preset("forw", preset)
        self.f_back.open_preset("back", preset)
        self.f_rand.open_preset("rand", preset)

    def save_preset(self, preset: PresetSave):
        preset.add("skip_chance", self.e_chance.get_str())
        preset.add_separator()
        self.f_forw.save_preset("forw", preset)
        self.f_back.save_preset("back", preset)
        self.f_rand.save_preset("rand", preset)


class SubLoop:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Loop ", padding=3)
        self.f_chances = LoopChances(self.root)
        self.f_skipping = LoopSkipping(self.root)
        self.l_loop_begin = ttk.Label(self.root, text="Loop begin: ")
        self.e_loop_begin = XEntry(self.root, width=15)

        self.f_chances.root.grid(row=0, column=0, rowspan=2, padx=1, sticky="nw")
        self.f_skipping.root.grid(row=0, column=1, columnspan=3, padx=1, sticky="nw")
        self.l_loop_begin.grid(row=1, column=1, sticky="w", padx=2)
        self.e_loop_begin.grid(row=1, column=2, sticky="w")
        self.root.grid_columnconfigure(3, weight=1)

    def apply_config(self, config: ScramblerConfig):
        config.loop_begin = float(self.e_loop_begin.get())
        self.f_chances.apply_config(config)
        self.f_skipping.apply_config(config)

    def open_preset(self, preset: PresetOpen):
        self.e_loop_begin.set(preset.get("loop_begin", "0"))
        self.f_chances.open_preset(preset)
        self.f_skipping.open_preset(preset)

    def save_preset(self, preset: PresetSave):
        preset.add("loop_begin", self.e_loop_begin.get())
        self.f_chances.save_preset(preset)
        self.f_skipping.save_preset(preset)


class SubAST:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Average start times ", padding=3)

        self.l_chance = ttk.Label(self.root, text="Chance: ")
        self.e_chance = CChance(self.root)
        self.l_times = ttk.Label(self.root, text="Times: ")
        self.e_times = XEntry(self.root)
        self.l_weights = ttk.Label(self.root, text="Weights (optional): ")
        self.e_weights = XEntry(self.root)

        self.l_chance.grid(row=0, column=0, sticky="w")
        self.e_chance.root.grid(row=0, column=1, sticky="w")
        self.root.grid_columnconfigure(2, weight=1)
        self.l_times.grid(row=1, column=0, columnspan=3, sticky="w")
        self.e_times.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.l_weights.grid(row=3, column=0, columnspan=3, sticky="w")
        self.e_weights.grid(row=4, column=0, columnspan=3, sticky="ew")

        line_dev_plus_chance = ttk.Frame(self.root)
        self.l_deviation = ttk.Label(self.root, text="Deviation: ")
        self.e_deviation = XEntry(line_dev_plus_chance, width=6)
        self.l_dev_chance = ttk.Label(line_dev_plus_chance, text="D. chance:")
        self.e_dev_chance = CChance(line_dev_plus_chance)
        self.l_dev_direction = ttk.Label(self.root, text="Direction: ")
        self.e_dev_direction = CWeights(self.root, 2)
        self.l_dev_dir_hint = ttk.Label(self.root, text="Weight: <- vs ->")

        ttk.Label(self.root).grid(row=5, column=0)
        ttk.Label(line_dev_plus_chance).grid(row=0, column=2)
        self.l_deviation.grid(row=6, column=0, sticky="w")
        line_dev_plus_chance.grid(row=6, column=1, columnspan=2, sticky="w")
        self.e_deviation.grid(row=0, column=1, sticky="w", padx=1, pady=1)
        self.l_dev_chance.grid(row=0, column=3, sticky="w")
        self.e_dev_chance.root.grid(row=0, column=4, sticky="w")
        self.l_dev_direction.grid(row=7, column=0, sticky="w")
        self.e_dev_direction.root.grid(row=7, column=1, sticky="w")
        self.l_dev_dir_hint.grid(row=7, column=2)

        line_force_pattern = ttk.Frame(self.root)
        self.l_force_pattern = ttk.Label(line_force_pattern, text="Force pattern (chance): ")
        self.e_force_pattern = CChance(line_force_pattern)
        ttk.Label(self.root).grid(row=9, column=0)
        line_force_pattern.grid(row=10, column=0, columnspan=3, sticky="w")
        self.l_force_pattern.grid(row=0, column=0)
        self.e_force_pattern.root.grid(row=0, column=1)

    def apply_config(self, config: ScramblerConfig):
        config.avgstart_chance = self.e_chance.get()
        times = list(map(float, self.e_times.get().split()))
        weights = list(map(int, self.e_weights.get().split()))
        if len(weights) == 0:
            weights = [1] * len(times)
        config.avgstart_times = RandChoice(times, weights)

        config.avgstart_deviation = float(self.e_deviation.get())
        config.avgstart_dev_chance = self.e_dev_chance.get()
        config.avgstart_dev_direction = RandChoice([-1, 1], self.e_dev_direction.get())

        config.avgstart_force_pattern = self.e_force_pattern.get()

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.e_chance, "avgstart_chance", "0"],
            [self.e_times, "avgstart_times", "0"],
            [self.e_weights, "avgstart_weights", ""],
            [self.e_deviation, "avgstart_deviation", "0"],
            [self.e_dev_chance, "avgstart_dev_chance", "100"],
            [self.e_dev_direction, "avgstart_dev_direction", "1 1"],
            [self.e_force_pattern, "avgstart_force_pattern", "0"],
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("avgstart_chance", self.e_chance.get_str())
        preset.add("avgstart_times", self.e_times.get())
        preset.add("avgstart_weights", self.e_weights.get())
        preset.add("avgstart_deviation", self.e_deviation.get())
        preset.add("avgstart_dev_chance", self.e_dev_chance.get_str())
        preset.add("avgstart_dev_direction", self.e_dev_direction.get_str())
        preset.add("avgstart_force_pattern", self.e_force_pattern.get_str())
        preset.add_separator()


class TabPattern:
    def __init__(self, parent):
        self.root = ttk.Frame(parent, padding=10)
        self.pattern = SubLoop(self.root)
        self.avg_st_times = SubAST(self.root)

        self.root.grid_rowconfigure(0, weight=1)
        self.pattern.root.grid(row=0, column=0, sticky="ns")
        self.root.grid_columnconfigure(1, weight=1)
        self.avg_st_times.root.grid(row=0, column=1, sticky="nsew", padx=4)

    def convert_time(self, mode):
        self.pattern.f_skipping.f_forw.conv_time(mode)
        self.pattern.f_skipping.f_back.conv_time(mode)
        self.pattern.f_skipping.f_rand.conv_time(mode)
        self.pattern.e_loop_begin.conv_time(mode)

        self.avg_st_times.e_times.conv_time(mode)
        self.avg_st_times.e_deviation.conv_time(mode)

    def apply_config(self, config: ScramblerConfig):
        self.pattern.apply_config(config)
        self.avg_st_times.apply_config(config)

    def open_preset(self, preset: PresetOpen):
        self.pattern.open_preset(preset)
        self.avg_st_times.open_preset(preset)

    def save_preset(self, preset: PresetSave):
        self.pattern.save_preset(preset)
        self.avg_st_times.save_preset(preset)
