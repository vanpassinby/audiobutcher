from scrambler.scr_state import ScramblerConfig
from preset import PresetOpen, PresetSave
from gui.gui_common import *


class SubQuanMain:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Quantization ", padding=3)

        self.l_quan_mode = ttk.Label(self.root, text="Mode: ")
        self.c_quan_mode = XCombobox(self.root, width=10, state="readonly", values=meta.cb_quan_modes)
        self.root.grid_columnconfigure(1, weight=1)
        self.l_quan_mode.grid(row=0, column=0, sticky="w")
        self.c_quan_mode.grid(row=0, column=2, sticky="e")

        self.l_quan_bpm = ttk.Label(self.root, text="BPM: ")
        self.e_quan_bpm = XEntry(self.root, width=0)
        self.l_quan_bpm.grid(row=1, column=0, sticky="w")
        self.e_quan_bpm.grid(row=1, column=2, sticky="we", pady=2)

        frame = ttk.LabelFrame(self.root, text=" Chances + Direction ", padding=3)
        frame.grid(row=2, column=0, columnspan=3)
        ttk.Label(frame).grid(row=0, column=2)

        self.l_quan_pattern = ttk.Label(frame, text="Start (Pattern): ")
        self.e_quan_pattern = CChance(frame)
        self.c_quan_pattern_dir = XCombobox(frame, width=8, state="readonly", values=meta.cb_quan_directions+["Equal"])
        self.l_quan_pattern.grid(row=0, column=0, sticky="w")
        self.e_quan_pattern.root.grid(row=0, column=1)
        self.c_quan_pattern_dir.grid(row=0, column=3)

        self.l_quan_ast = ttk.Label(frame, text="Start (AST): ")
        self.e_quan_ast = CChance(frame)
        self.c_quan_ast_dir = XCombobox(frame, width=8, state="readonly", values=meta.cb_quan_directions+["Auto"])
        self.l_quan_ast.grid(row=1, column=0, sticky="w")
        self.e_quan_ast.root.grid(row=1, column=1)
        self.c_quan_ast_dir.grid(row=1, column=3)

        self.l_quan_loop = ttk.Label(frame, text="Start (Loop): ")
        self.e_quan_loop = CChance(frame)
        self.c_quan_loop_dir = XCombobox(frame, width=8, state="readonly", values=meta.cb_quan_directions)
        self.l_quan_loop.grid(row=2, column=0, sticky="w")
        self.e_quan_loop.root.grid(row=2, column=1)
        self.c_quan_loop_dir.grid(row=2, column=3)

        self.l_quan_skip = ttk.Label(frame, text="Start (Loop - Skip): ")
        self.e_quan_skip = CChance(frame)
        self.c_quan_skip_dir = XCombobox(frame, width=8, state="readonly", values=meta.cb_quan_directions+["Auto"])
        self.l_quan_skip.grid(row=3, column=0, sticky="w")
        self.e_quan_skip.root.grid(row=3, column=1)
        self.c_quan_skip_dir.grid(row=3, column=3)

        self.l_quan_duration = ttk.Label(frame, text="Segment duration: ")
        self.e_quan_duration = CChance(frame)
        self.c_quan_duration_dir = XCombobox(frame, width=8, state="readonly", values=meta.cb_quan_directions)
        self.l_quan_duration.grid(row=4, column=0, sticky="w")
        self.e_quan_duration.root.grid(row=4, column=1)
        self.c_quan_duration_dir.grid(row=4, column=3)

        self.l_quan_sustain = ttk.Label(frame, text="Sustain portion: ")
        self.e_quan_sustain = CChance(frame)
        self.c_quan_sustain_dir = XCombobox(frame, width=8, state="readonly", values=meta.cb_quan_directions)
        self.l_quan_sustain.grid(row=5, column=0, sticky="w")
        self.e_quan_sustain.root.grid(row=5, column=1)
        self.c_quan_sustain_dir.grid(row=5, column=3)

        self.l_quan_frame = ttk.Label(frame, text="Frame begin/end: ")
        self.e_quan_frame = CChance(frame)
        self.c_quan_frame_dir = XCombobox(frame, width=8, state="readonly", values=meta.cb_quan_directions)
        self.l_quan_frame.grid(row=6, column=0, sticky="w")
        self.e_quan_frame.root.grid(row=6, column=1)
        self.c_quan_frame_dir.grid(row=6, column=3)

        self.l_quan_alt_slices = ttk.Label(frame, text="Use alt. slices: ")
        self.e_quan_alt_slices = CChance(frame)
        self.l_quan_alt_slices.grid(row=7, column=0, sticky="w")
        self.e_quan_alt_slices.root.grid(row=7, column=1)

    def update(self, bpm=True, chances=True, alt_c=True):
        self.e_quan_bpm.configure(state="normal" if bpm else "disabled")
        self.update_chances(state="normal" if chances else "disabled")
        self.update_directions(state="readonly" if chances else "disabled")
        self.e_quan_alt_slices.e_chance.configure(state="normal" if alt_c else "disabled")

    def update_chances(self, state: str):
        elements_chance = [
            self.e_quan_pattern,
            self.e_quan_ast,
            self.e_quan_loop,
            self.e_quan_skip,
            self.e_quan_duration,
            self.e_quan_sustain,
            self.e_quan_frame]

        for element in elements_chance:
            element.e_chance.configure(state=state)

    def update_directions(self, state: str):
        elements_direction = [
            self.c_quan_pattern_dir,
            self.c_quan_ast_dir,
            self.c_quan_loop_dir,
            self.c_quan_skip_dir,
            self.c_quan_duration_dir,
            self.c_quan_sustain_dir,
            self.c_quan_frame_dir]

        for element in elements_direction:
            element.configure(state=state)

    def apply_config(self, config: ScramblerConfig):
        config.quan_mode = self.c_quan_mode.current()
        config.quan_bpm = float(self.e_quan_bpm.get())
        config.quan_pattern = self.e_quan_pattern.get()
        config.quan_pattern_dir = self.c_quan_pattern_dir.current()
        config.quan_ast = self.e_quan_ast.get()
        config.quan_ast_dir = self.c_quan_ast_dir.current()
        config.quan_loop = self.e_quan_loop.get()
        config.quan_loop_dir = self.c_quan_loop_dir.current()
        config.quan_skip = self.e_quan_skip.get()
        config.quan_skip_dir = self.c_quan_skip_dir.current()
        config.quan_duration = self.e_quan_duration.get()
        config.quan_duration_dir = self.c_quan_duration_dir.current()
        config.quan_sustain = self.e_quan_sustain.get()
        config.quan_sustain_dir = self.c_quan_sustain_dir.current()
        config.quan_frame = self.e_quan_frame.get()
        config.quan_frame_dir = self.c_quan_frame_dir.current()
        config.quan_alt_slices = self.e_quan_alt_slices.get()

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.c_quan_mode, "quan_mode", "0"],
            [self.e_quan_bpm, "quan_bpm", "120.000"],
            [self.e_quan_pattern, "quan_pattern", "100"],
            [self.c_quan_pattern_dir, "quan_pattern_dir", "3"],
            [self.e_quan_ast, "quan_ast", "100"],
            [self.c_quan_ast_dir, "quan_ast_dir", "3"],
            [self.e_quan_loop, "quan_loop", "100"],
            [self.c_quan_loop_dir, "quan_loop_dir", "0"],
            [self.e_quan_skip, "quan_skip", "100"],
            [self.c_quan_skip_dir, "quan_skip_dir", "3"],
            [self.e_quan_duration, "quan_duration", "100"],
            [self.c_quan_duration_dir, "quan_duration_dir", "0"],
            [self.e_quan_sustain, "quan_sustain", "100"],
            [self.c_quan_sustain_dir, "quan_sustain_dir", "0"],
            [self.e_quan_frame, "quan_frame", "100"],
            [self.c_quan_frame_dir, "quan_frame_dir", "0"],
            [self.e_quan_alt_slices, "quan_alt_slices", "100"]
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("quan_mode", self.c_quan_mode.current())
        preset.add("quan_bpm", self.e_quan_bpm.get())
        preset.add("quan_pattern", self.e_quan_pattern.get_str())
        preset.add("quan_pattern_dir", self.c_quan_pattern_dir.current())
        preset.add("quan_ast", self.e_quan_ast.get_str())
        preset.add("quan_ast_dir", self.c_quan_ast_dir.current())
        preset.add("quan_loop", self.e_quan_loop.get_str())
        preset.add("quan_loop_dir", self.c_quan_loop_dir.current())
        preset.add("quan_skip", self.e_quan_skip.get_str())
        preset.add("quan_skip_dir", self.c_quan_skip_dir.current())
        preset.add("quan_duration", self.e_quan_duration.get_str())
        preset.add("quan_duration_dir", self.c_quan_duration_dir.current())
        preset.add("quan_sustain", self.e_quan_sustain.get_str())
        preset.add("quan_sustain_dir", self.c_quan_sustain_dir.current())
        preset.add("quan_frame", self.e_quan_frame.get_str())
        preset.add("quan_frame_dir", self.c_quan_frame_dir.current())
        preset.add("quan_alt_slices", self.e_quan_alt_slices.get_str())
        preset.add_separator()


class SubQuanAlt:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Use alternative slices for: ", padding=3)

        self.x_quan_alt_pattern = CCheckbox(self.root, text="Start (Pattern)")
        self.x_quan_alt_ast = CCheckbox(self.root, text="Start (AST)")
        self.x_quan_alt_loop = CCheckbox(self.root, text="Start (Loop)")
        self.x_quan_alt_skip = CCheckbox(self.root, text="Start (Loop - Skip)")
        self.x_quan_alt_duration = CCheckbox(self.root, text="Segment duration")
        self.x_quan_alt_portion = CCheckbox(self.root, text="Sustain portion")
        self.x_quan_alt_frame = CCheckbox(self.root, text="Frame begin/end")

        ttk.Label(self.root).grid(column=1, row=0)
        self.x_quan_alt_pattern.root.grid(column=0, row=0, sticky="w")
        self.x_quan_alt_ast.root.grid(column=0, row=1, sticky="w")
        self.x_quan_alt_loop.root.grid(column=0, row=2, sticky="w")
        self.x_quan_alt_skip.root.grid(column=0, row=3, sticky="w")
        self.x_quan_alt_duration.root.grid(column=2, row=0, sticky="w")
        self.x_quan_alt_portion.root.grid(column=2, row=1, sticky="w")
        self.x_quan_alt_frame.root.grid(column=2, row=2, sticky="w")

    def update(self, enabled=True):
        elements = [self.x_quan_alt_pattern,
                    self.x_quan_alt_ast,
                    self.x_quan_alt_loop,
                    self.x_quan_alt_skip,
                    self.x_quan_alt_duration,
                    self.x_quan_alt_portion,
                    self.x_quan_alt_frame]
        state = "normal" if enabled else "disabled"

        for element in elements:
            element.root.configure(state=state)

    def apply_config(self, config: ScramblerConfig):
        config.quan_alt_pattern = self.x_quan_alt_pattern.get()
        config.quan_alt_ast = self.x_quan_alt_ast.get()
        config.quan_alt_loop = self.x_quan_alt_loop.get()
        config.quan_alt_skip = self.x_quan_alt_skip.get()
        config.quan_alt_duration = self.x_quan_alt_duration.get()
        config.quan_alt_portion = self.x_quan_alt_portion.get()
        config.quan_alt_frame = self.x_quan_alt_frame.get()

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.x_quan_alt_pattern, "quan_alt_pattern", "0"],
            [self.x_quan_alt_ast, "quan_alt_ast", "0"],
            [self.x_quan_alt_loop, "quan_alt_loop", "0"],
            [self.x_quan_alt_skip, "quan_alt_skip", "0"],
            [self.x_quan_alt_duration, "quan_alt_duration", "0"],
            [self.x_quan_alt_portion, "quan_alt_portion", "0"],
            [self.x_quan_alt_frame, "quan_alt_frame", "0"]
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("quan_alt_pattern", self.x_quan_alt_pattern.get_str())
        preset.add("quan_alt_ast", self.x_quan_alt_ast.get_str())
        preset.add("quan_alt_loop", self.x_quan_alt_loop.get_str())
        preset.add("quan_alt_skip", self.x_quan_alt_skip.get_str())
        preset.add("quan_alt_duration", self.x_quan_alt_duration.get_str())
        preset.add("quan_alt_portion", self.x_quan_alt_portion.get_str())
        preset.add("quan_alt_frame", self.x_quan_alt_frame.get_str())
        preset.add_separator()


class TabQuantization:
    def __init__(self, parent):
        self.root = ttk.Frame(parent, padding=10)
        self.f_main = SubQuanMain(self.root)
        self.f_alt = SubQuanAlt(self.root)

        self.root.grid_rowconfigure(0, weight=1)
        self.f_main.root.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.f_alt.root.grid(row=1, column=1, padx=4, sticky="nw")

        self.f_main.c_quan_mode.bind("<<ComboboxSelected>>", lambda event: self.update())

    def update(self):
        mode = self.f_main.c_quan_mode.current()

        if mode == 1:  # Slices
            self.f_main.update(bpm=False, chances=True, alt_c=True)
            self.f_alt.update(enabled=True)
        elif mode == 2:  # BPM
            self.f_main.update(bpm=True, chances=True, alt_c=False)
            self.f_alt.update(enabled=False)
        else:  # None / Error
            self.f_main.update(bpm=False, chances=False, alt_c=False)
            self.f_alt.update(enabled=False)

    def apply_config(self, config: ScramblerConfig):
        self.f_main.apply_config(config)
        self.f_alt.apply_config(config)

    def open_preset(self, preset: PresetOpen):
        self.f_main.open_preset(preset)
        self.f_alt.open_preset(preset)

    def save_preset(self, preset: PresetSave):
        self.f_main.save_preset(preset)
        self.f_alt.save_preset(preset)
