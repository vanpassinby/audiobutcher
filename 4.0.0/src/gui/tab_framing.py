from scrambler.scr_state import ScramblerConfig
from preset import PresetOpen, PresetSave
from gui.gui_common import *


class SubFramingGeneral:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" General ", padding=3)

        self.x_enabled = CCheckbox(self.root, "Framing")
        self.l_frame_size = ttk.Label(self.root, text="Frame size: ")
        self.e_frame_size = CDistribution(self.root)
        self.x_use_seed = CCheckbox(self.root, "Seed: ")
        self.e_seed = XEntry(self.root)
        self.l_speed_ratio = ttk.Label(self.root, text="Speed ratio: ")
        self.e_speed_ratio = XEntry(self.root)
        self.x_alt_reverse = CCheckbox(self.root, text="Use alternative reverse method")

        self.x_enabled.root.grid(row=0, column=0, sticky="w")
        self.l_frame_size.grid(row=1, column=0, sticky="w")
        self.e_frame_size.root.grid(row=1, column=1, sticky="e")
        self.x_use_seed.root.grid(row=2, column=0, sticky="w")
        self.e_seed.grid(row=2, column=1, padx=1, pady=1, sticky="we")
        self.l_speed_ratio.grid(row=3, column=0, sticky="w")
        self.e_speed_ratio.grid(row=3, column=1, padx=1, pady=1, sticky="we")
        self.x_alt_reverse.root.grid(row=4, column=0, columnspan=2, sticky="w")

        frame_force = ttk.Frame(self.root)
        self.l_force_duration = ttk.Label(frame_force, text="Force duration (chance): ")
        self.e_force_duration = CChance(frame_force)
        self.l_force_for_pattern = ttk.Label(frame_force, text="Force for pattern (chance): ")
        self.e_force_for_pattern = CChance(frame_force)
        self.l_force_for_ast = ttk.Label(frame_force, text="Force for AST (chance): ")
        self.e_force_for_ast = CChance(frame_force)

        ttk.Label(self.root).grid(row=5, column=0)
        frame_force.grid(row=6, column=0, columnspan=2, sticky="w")
        self.l_force_duration.grid(row=0, column=0, sticky="w")
        self.e_force_duration.root.grid(row=0, column=1, sticky="e")
        self.l_force_for_pattern.grid(row=1, column=0, sticky="w")
        self.e_force_for_pattern.root.grid(row=1, column=1, sticky="e")
        self.l_force_for_ast.grid(row=2, column=0, sticky="w")
        self.e_force_for_ast.root.grid(row=2, column=1, sticky="e")

    def apply_config(self, config: ScramblerConfig):
        config.framing = self.x_enabled.get()
        config.framing_frame_size = self.e_frame_size.get()
        if self.x_use_seed.get():
            config.framing_seed = self.e_seed.get()
        else:
            config.framing_seed = None
        config.framing_speed_ratio = self.e_speed_ratio.get()
        config.framing_alt_reverse = self.x_alt_reverse.get()
        config.framing_force_duration = self.e_force_duration.get()
        config.framing_force_for_pattern = self.e_force_for_pattern.get()
        config.framing_force_for_ast = self.e_force_for_ast.get()

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.x_enabled, "framing", "0"],
            [self.e_frame_size, "framing_frame_size", "0 0 0"],
            [self.x_use_seed, "framing_use_seed", "0"],
            [self.e_seed, "framing_seed", ""],
            [self.e_speed_ratio, "framing_speed_ratio", "1/1"],
            [self.x_alt_reverse, "framing_alt_reverse", "0"],

            [self.e_force_duration, "framing_force_duration", "100"],
            [self.e_force_for_pattern, "framing_force_for_pattern", "100"],
            [self.e_force_for_ast, "framing_force_for_ast", "100"]
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("framing", self.x_enabled.get_str())
        preset.add("framing_frame_size", self.e_frame_size.get_str())
        preset.add("framing_use_seed", self.x_use_seed.get_str())
        preset.add("framing_seed", self.e_seed.get())
        preset.add("framing_speed_ratio", self.e_speed_ratio.get())
        preset.add("framing_alt_reverse", self.x_alt_reverse.get_str())
        preset.add("framing_force_duration", self.e_force_duration.get_str())
        preset.add("framing_force_for_pattern", self.e_force_for_pattern.get_str())
        preset.add("framing_force_for_ast", self.e_force_for_ast.get_str())
        preset.add_separator()


class SubFramingEnvelope:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Customize envelope ", padding=3)

        self.x_attack = CCheckbox(self.root, text="Attack: ")
        self.e_attack_dist = CDistribution(self.root)
        self.x_hold = CCheckbox(self.root, text="Hold: ")
        self.e_hold_dist = CDistribution(self.root)
        self.x_decay = CCheckbox(self.root, text="Decay: ")
        self.e_decay_dist = CDistribution(self.root)
        self.x_crossfade_endless = CCheckbox(self.root, text="Endless crossfade")

        self.x_attack.root.grid(row=0, column=0, sticky="w")
        self.e_attack_dist.root.grid(row=0, column=1, sticky="e")
        self.x_hold.root.grid(row=1, column=0, sticky="w")
        self.e_hold_dist.root.grid(row=1, column=1, sticky="e")
        self.x_decay.root.grid(row=2, column=0, sticky="w")
        self.e_decay_dist.root.grid(row=2, column=1, sticky="e")
        self.x_crossfade_endless.root.grid(row=3, column=0, columnspan=2, sticky="w")

        self.x_attack.root.configure(command=self.update)
        self.x_hold.root.configure(command=self.update)
        self.x_decay.root.configure(command=self.update)

    def update(self, enabled=True):
        if enabled:
            self.x_attack.root.configure(state="normal")
            self.x_hold.root.configure(state="normal")
            self.x_decay.root.configure(state="normal")
            self.x_crossfade_endless.root.configure(state="normal")
        else:
            self.x_attack.root.configure(state="disabled")
            self.x_hold.root.configure(state="disabled")
            self.x_decay.root.configure(state="disabled")
            self.x_crossfade_endless.root.configure(state="disabled")

        if enabled and self.x_attack.get():
            self.e_attack_dist.set_state(enabled=True)
        else:
            self.e_attack_dist.set_state(enabled=False)

        if enabled and self.x_hold.get():
            self.e_hold_dist.set_state(enabled=True)
        else:
            self.e_hold_dist.set_state(enabled=False)

        if enabled and self.x_decay.get():
            self.e_decay_dist.set_state(enabled=True)
        else:
            self.e_decay_dist.set_state(enabled=False)

    def apply_config(self, config: ScramblerConfig):
        config.fr_env_attack = self.x_attack.get()
        config.fr_env_attack_dist = self.e_attack_dist.get()
        config.fr_env_hold = self.x_hold.get()
        config.fr_env_hold_dist = self.e_hold_dist.get()
        config.fr_env_decay = self.x_decay.get()
        config.fr_env_decay_dist = self.e_decay_dist.get()
        config.fr_env_crossfade_endless = self.x_crossfade_endless.get()

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.x_attack, "fr_env_attack", "0"],
            [self.e_attack_dist, "fr_env_attack_dist", "0 0 0"],
            [self.x_hold, "fr_env_hold", "0"],
            [self.e_hold_dist, "fr_env_hold_dist", "0 0 0"],
            [self.x_decay, "fr_env_decay", "0"],
            [self.e_decay_dist, "fr_env_decay_dist", "0 0 0"],
            [self.x_crossfade_endless, "fr_env_crossfade_endless", "0"]
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("fr_env_attack", self.x_attack.get_str())
        preset.add("fr_env_attack_dist", self.e_attack_dist.get_str())
        preset.add("fr_env_hold", self.x_hold.get_str())
        preset.add("fr_env_hold_dist", self.e_hold_dist.get_str())
        preset.add("fr_env_decay", self.x_decay.get_str())
        preset.add("fr_env_decay_dist", self.e_decay_dist.get_str())
        preset.add("fr_env_crossfade_endless", self.x_crossfade_endless.get_str())
        preset.add_separator()


class SubFramingAltLength:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Length settings ", padding=3)

        self.l_soft = ttk.Label(self.root, text="Length scale: ")
        self.e_soft = CChance(self.root, ent_w=4)
        self.l_hard = ttk.Label(self.root, text="Hard length cutoff: ")
        self.e_hard = CChance(self.root, ent_w=4)

        self.l_soft.grid(row=1, column=0, sticky="w")
        self.e_soft.root.grid(row=1, column=1, sticky="w")
        self.l_hard.grid(row=2, column=0, sticky="w")
        self.e_hard.root.grid(row=2, column=1, sticky="w")

    def update(self, enabled=True):
        if enabled:
            self.e_soft.e_chance.configure(state="normal")
            self.e_hard.e_chance.configure(state="normal")
        else:
            self.e_soft.e_chance.configure(state="disabled")
            self.e_hard.e_chance.configure(state="disabled")

    def apply_config(self, config: ScramblerConfig):
        config.fr_length_soft = abs(float(self.e_soft.get_str()))
        config.fr_length_hard = abs(float(self.e_hard.get_str()))

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.e_soft, "fr_length_soft", "100"],
            [self.e_hard, "fr_length_hard", "100"]
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("fr_length_soft", self.e_soft.get_str())
        preset.add("fr_length_hard", self.e_hard.get_str())
        preset.add_separator()


class SubFramingSimplify:
    def __init__(self, parent):
        self.root = ttk.LabelFrame(parent, text=" Simplify ", padding=3)

        self.x_enable = CCheckbox(self.root, text="Enabled")
        self.l_step = ttk.Label(self.root, text="Step size: ")
        self.e_step = XEntry(self.root, width=6)
        self.l_severity = ttk.Label(self.root, text="Severity: ")
        self.e_severity = CChance(self.root, ent_w=6)

        self.x_enable.root.grid(row=0, column=0, columnspan=2, sticky="w")
        self.l_step.grid(row=1, column=0, sticky="w")
        self.e_step.grid(row=1, column=1, padx=1, pady=1, sticky="w")
        self.l_severity.grid(row=2, column=0, sticky="w")
        self.e_severity.root.grid(row=2, column=1, sticky="w")

        self.x_enable.root.configure(command=self.update)

    def update(self, enabled=True):
        if enabled:
            self.x_enable.root.configure(state="normal")
        else:
            self.x_enable.root.configure(state="disabled")

        if enabled and self.x_enable.get():
            self.e_step.configure(state="normal")
            self.e_severity.e_chance.configure(state="normal")
        else:
            self.e_step.configure(state="disabled")
            self.e_severity.e_chance.configure(state="disabled")

    def apply_config(self, config: ScramblerConfig):
        config.fr_simplify = self.x_enable.get()
        config.fr_simplify_step = abs(float(self.e_step.get()))
        config.fr_simplify_severity = abs(float(self.e_severity.get_str()))

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.x_enable, "fr_simplify", "0"],
            [self.e_step, "fr_simplify_step", "0"],
            [self.e_severity, "fr_simplify_severity", "0"]
        ]

        preset.batch_set(batch)

    def save_preset(self, preset: PresetSave):
        preset.add("fr_simplify", self.x_enable.get_str())
        preset.add("fr_simplify_step", self.e_step.get())
        preset.add("fr_simplify_severity", self.e_severity.get_str())
        preset.add_separator()


class TabFraming:
    def __init__(self, parent):
        self.lock_part_gen = True

        self.root = ttk.Frame(parent, padding=10)
        self.general = SubFramingGeneral(self.root)
        self.envelope = SubFramingEnvelope(self.root)
        self.alt_length = SubFramingAltLength(self.root)
        self.simplify = SubFramingSimplify(self.root)

        self.root.grid_rowconfigure(2, weight=1)
        self.general.root.grid(row=0, column=0, rowspan=3, sticky="wns")
        self.envelope.root.grid(row=0, column=1, padx=4, sticky="nw")
        self.alt_length.root.grid(row=1, column=1, padx=4, sticky="nw")
        self.simplify.root.grid(row=2, column=1, padx=4, sticky="nw")

        self.general.x_enabled.root.configure(command=self.update)
        self.general.x_use_seed.root.configure(command=self.update)

    def update(self):
        if self.general.x_enabled.get():
            self.general.e_frame_size.set_state(enabled=True)
            self.general.x_use_seed.root.configure(state="normal")

            if self.general.x_use_seed.get():
                self.general.e_seed.configure(state="normal")
            else:
                self.general.e_seed.configure(state="disabled")

            self.general.e_speed_ratio.configure(state="normal")
            self.general.x_alt_reverse.root.configure(state="normal")
            self.general.e_force_duration.e_chance.configure(state="normal")
            self.general.e_force_for_pattern.e_chance.configure(state="normal")
            self.general.e_force_for_ast.e_chance.configure(state="normal")

            self.envelope.update()
            self.alt_length.update()
            self.simplify.update()

        else:
            self.general.e_frame_size.set_state(enabled=False)
            self.general.x_use_seed.root.configure(state="disabled")
            self.general.e_seed.configure(state="disabled")
            self.general.e_speed_ratio.configure(state="disabled")
            self.general.x_alt_reverse.root.configure(state="disabled")
            self.general.e_force_duration.e_chance.configure(state="disabled")
            self.general.e_force_for_pattern.e_chance.configure(state="disabled")
            self.general.e_force_for_ast.e_chance.configure(state="disabled")

            self.envelope.update(enabled=False)
            self.alt_length.update(enabled=False)
            self.simplify.update(enabled=False)

        if self.lock_part_gen:
            self.general.x_enabled.root.configure(state="disabled")
            self.general.e_frame_size.set_state(enabled=False)
            self.general.x_use_seed.root.configure(state="disabled")
            self.general.e_seed.configure(state="disabled")

            self.simplify.x_enable.root.configure(state="disabled")
            self.simplify.e_step.configure(state="disabled")
            self.simplify.e_severity.e_chance.configure(state="disabled")

        else:
            self.general.x_enabled.root.configure(state="normal")

    def convert_time(self, mode):
        self.general.e_frame_size.conv_time(mode)
        self.envelope.e_attack_dist.conv_time(mode)
        self.envelope.e_hold_dist.conv_time(mode)
        self.envelope.e_decay_dist.conv_time(mode)

    def apply_config(self, config: ScramblerConfig):
        self.general.apply_config(config)
        self.envelope.apply_config(config)
        self.alt_length.apply_config(config)
        self.simplify.apply_config(config)

    def open_preset(self, preset: PresetOpen):
        self.general.open_preset(preset)
        self.envelope.open_preset(preset)
        self.alt_length.open_preset(preset)
        self.simplify.open_preset(preset)

    def save_preset(self, preset: PresetSave):
        self.general.save_preset(preset)
        self.envelope.save_preset(preset)
        self.alt_length.save_preset(preset)
        self.simplify.save_preset(preset)
