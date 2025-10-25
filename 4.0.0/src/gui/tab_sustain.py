from ab_random import RandChoice
from scrambler.scr_state import ScramblerConfig, ScramblerConfigSubSustain
from preset import PresetOpen, PresetSave
from gui.gui_common import *


class SustainVariant:
    def __init__(self, parent):
        self.root = ttk.Frame(parent, padding=5)
        self.sec_mode_ref = None

        self.u_menu = tk.Menu(self.root, tearoff=False)
        self.u_menu.add_command(label="Preset: Mirrored segment", command=lambda: self.set_preset(1))
        self.u_menu.add_command(label="Preset: Mirrored segment (full)", command=lambda: self.set_preset(2))
        self.u_menu.add_command(label="Preset: Mirrored segment (asymmetrical)", command=lambda: self.set_preset(3))
        self.u_menu.add_command(label="Preset: Fade-out tail", command=lambda: self.set_preset(4))
        self.u_menu.add_separator()
        self.u_menu.add_command(label="Clear", command=lambda: self.set_preset(0))
        self.root.bind("<Button-2>", self.show_menu)
        self.root.bind("<Button-3>", self.show_menu)

        self.l_crossfade = ttk.Label(self.root, text="Crossfade: ")
        self.e_crossfade = XEntry(self.root, width=6)
        self.l_crossfade.grid(row=0, column=0, sticky="w")
        self.e_crossfade.grid(row=0, column=1, padx=1, pady=1, sticky="w")

        self.l_length = ttk.Label(self.root, text="Sustain length: ")
        self.e_length = CDistribution(self.root)
        self.l_length_mode = ttk.Label(self.root, text="Mode: ")
        self.c_length_mode = XCombobox(self.root, width=20, values=meta.cb_sustain_portion, state="readonly")
        self.x_length_exact = CCheckbox(self.root, "Exact")

        self.l_length.grid(row=1, column=0, sticky="w")
        self.e_length.root.grid(row=1, column=1, sticky="w")
        ttk.Label(self.root).grid(row=1, column=2)
        self.l_length_mode.grid(row=1, column=3, sticky="w")
        self.c_length_mode.grid(row=1, column=4, sticky="w")
        self.x_length_exact.root.grid(row=1, column=5, padx=1, sticky="w")

        self.l_portion_length = ttk.Label(self.root, text="Portion length: ")
        self.e_portion_length = CDistribution(self.root)
        self.x_portion_proportional = CCheckbox(self.root, "Proportional to segment length (%)")
        self.l_portion_minimum = ttk.Label(self.root, text="Minimal required portion: ")
        self.e_portion_minimum = XEntry(self.root, width=6)

        self.l_portion_length.grid(row=2, column=0, sticky="w")
        self.e_portion_length.root.grid(row=2, column=1, sticky="w")
        self.x_portion_proportional.root.grid(row=2, column=3, columnspan=3, sticky="w")
        self.l_portion_minimum.grid(row=3, column=0, sticky="w")
        self.e_portion_minimum.grid(row=3, column=1, sticky="w", padx=1, pady=1)

        self.x_allow_quan = CCheckbox(self.root, "Allow portion quantization")
        self.l_shift_chance = ttk.Label(self.root, text="Shift chance: ")
        self.e_shift_chance = CChance(self.root)
        self.l_reverse_chance = ttk.Label(self.root, text="Reverse chance: ")
        self.e_reverse_chance = CChance(self.root)
        self.l_consec_chance = ttk.Label(self.root, text="Consecutiveness chance: ")
        self.e_consec_chance = CChance(self.root)

        self.root.grid_columnconfigure(6, weight=1)
        ttk.Label(self.root).grid(row=4, column=0)
        self.x_allow_quan.root.grid(row=5, column=0, columnspan=2, sticky="w")
        self.l_shift_chance.grid(row=6, column=0, sticky="w")
        self.e_shift_chance.root.grid(row=6, column=1, sticky="w")
        self.l_reverse_chance.grid(row=7, column=0, sticky="w")
        self.e_reverse_chance.root.grid(row=7, column=1, sticky="w")
        self.l_consec_chance.grid(row=8, column=0, sticky="w")
        self.e_consec_chance.root.grid(row=8, column=1, sticky="w")

    def show_menu(self, event):
        self.u_menu.tk_popup(event.x_root, event.y_root)

    def set_preset(self, idx):
        sec_mode = self.sec_mode_ref is not None and self.sec_mode_ref.get()

        if idx == 0:
            self.open_preset(0, PresetOpen(data=""))

        elif idx == 1:  # Mirror
            self.e_length.set("0 1 1")
            self.c_length_mode.set(1)
            self.x_length_exact.set(1)
            self.e_portion_length.set("0 100 100")
            self.x_portion_proportional.set(1)
            self.e_portion_minimum.set(0)
            self.e_shift_chance.set(100)

        elif idx == 2:  # Mirror - Full
            self.e_length.set("0 1 1")
            self.c_length_mode.set(1)
            self.x_length_exact.set(1)
            self.e_portion_length.set("0 100 100")
            self.x_portion_proportional.set(1)
            self.e_portion_minimum.set(0)
            self.e_shift_chance.set(0)

        elif idx == 3:  # Mirror - Asymmetrical
            self.e_length.set("0 1 1")
            self.c_length_mode.set(1)
            self.x_length_exact.set(1)
            self.e_portion_length.set("0 0 100")
            self.x_portion_proportional.set(1)
            self.e_portion_minimum.set(0)
            self.e_shift_chance.set(100)

        elif idx == 4:  # Tail
            self.e_length.set("0 100 100")
            self.c_length_mode.set(4)
            self.x_length_exact.set(1)
            self.e_portion_length.set("0 0.4 0.4" if sec_mode else "0 400 400")
            self.x_portion_proportional.set(0)
            self.e_portion_minimum.set(0.1 if sec_mode else 100)
            self.e_shift_chance.set(0)

    def convert_time(self, mode):
        self.e_crossfade.conv_time(mode)
        self.e_portion_minimum.conv_time(mode)

        if self.c_length_mode.current() == 0:
            self.e_length.conv_time(mode)

        if not self.x_portion_proportional.get():
            self.e_portion_length.conv_time(mode)

    def get_subconfig(self) -> ScramblerConfigSubSustain:
        sub = ScramblerConfigSubSustain()
        sub.crossfade = abs(float(self.e_crossfade.get()))

        sub.length = self.e_length.get()
        sub.length_mode = self.c_length_mode.current()
        sub.length_exact = self.x_length_exact.get()

        sub.portion_length = self.e_portion_length.get()
        sub.portion_proportional = self.x_portion_proportional.get()
        sub.portion_minimum = abs(float(self.e_portion_minimum.get()))

        sub.allow_quan = self.x_allow_quan.get()
        sub.shift_chance = self.e_shift_chance.get()
        sub.reverse_chance = self.e_reverse_chance.get()
        sub.consec_chance = self.e_consec_chance.get()

        return sub

    def open_preset(self, ident, preset: PresetOpen):
        batch = [
            [self.e_crossfade, f"sustain{ident}_crossfade", "0"],
            [self.e_length, f"sustain{ident}_length", "0 0 0"],
            [self.c_length_mode, f"sustain{ident}_length_mode", "0"],
            [self.x_length_exact, f"sustain{ident}_length_exact", "0"],
            [self.e_portion_length, f"sustain{ident}_portion_length", "0 0 0"],
            [self.x_portion_proportional, f"sustain{ident}_portion_proportional", "0"],
            [self.e_portion_minimum, f"sustain{ident}_portion_minimum", "0"],
            [self.x_allow_quan, f"sustain{ident}_allow_quan", "0"],
            [self.e_shift_chance, f"sustain{ident}_shift_chance", "0"],
            [self.e_reverse_chance, f"sustain{ident}_reverse_chance", "0"],
            [self.e_consec_chance, f"sustain{ident}_consec_chance", "100"]
        ]

        preset.batch_set(batch)

    def save_preset(self, ident, preset: PresetSave):
        preset.add(f"sustain{ident}_crossfade", self.e_crossfade.get())
        preset.add(f"sustain{ident}_length", self.e_length.get_str())
        preset.add(f"sustain{ident}_length_mode", self.c_length_mode.current())
        preset.add(f"sustain{ident}_length_exact", self.x_length_exact.get_str())
        preset.add(f"sustain{ident}_portion_length", self.e_portion_length.get_str())
        preset.add(f"sustain{ident}_portion_proportional", self.x_portion_proportional.get_str())
        preset.add(f"sustain{ident}_portion_minimum", self.e_portion_minimum.get())
        preset.add(f"sustain{ident}_allow_quan", self.x_allow_quan.get_str())
        preset.add(f"sustain{ident}_shift_chance", self.e_shift_chance.get_str())
        preset.add(f"sustain{ident}_reverse_chance", self.e_reverse_chance.get_str())
        preset.add(f"sustain{ident}_consec_chance", self.e_consec_chance.get_str())
        preset.add_separator()


class TabSustain:
    def __init__(self, parent):
        self.root = ttk.Frame(parent, padding=10)

        self.l_chance = ttk.Label(self.root, text="Sustain chance: ")
        self.e_chance = CChance(self.root)
        self.l_weights = ttk.Label(self.root, text="Variant weights: ")
        self.e_weights = CWeights(self.root, 5)

        self.l_chance.grid(row=0, column=0, sticky="w")
        self.e_chance.root.grid(row=0, column=1)
        ttk.Label(self.root).grid(row=0, column=2)
        self.l_weights.grid(row=0, column=3)
        self.e_weights.root.grid(row=0, column=4)
        self.root.grid_columnconfigure(5, weight=1)

        self.f_variants = ttk.Notebook(self.root)
        self.f_var1 = SustainVariant(self.root)
        self.f_var2 = SustainVariant(self.root)
        self.f_var3 = SustainVariant(self.root)
        self.f_var4 = SustainVariant(self.root)
        self.f_var5 = SustainVariant(self.root)

        self.f_variants.grid(row=1, column=0, columnspan=6, sticky="nsew")
        self.root.grid_rowconfigure(1, weight=1)
        self.f_variants.add(self.f_var1.root, text="Variant 1")
        self.f_variants.add(self.f_var2.root, text="Variant 2")
        self.f_variants.add(self.f_var3.root, text="Variant 3")
        self.f_variants.add(self.f_var4.root, text="Variant 4")
        self.f_variants.add(self.f_var5.root, text="Variant 5")

    def set_sec_mode_ref(self, sec_mode_ref):
        self.f_var1.sec_mode_ref = sec_mode_ref
        self.f_var2.sec_mode_ref = sec_mode_ref
        self.f_var3.sec_mode_ref = sec_mode_ref
        self.f_var4.sec_mode_ref = sec_mode_ref
        self.f_var5.sec_mode_ref = sec_mode_ref

    def convert_time(self, mode):
        self.f_var1.convert_time(mode)
        self.f_var2.convert_time(mode)
        self.f_var3.convert_time(mode)
        self.f_var4.convert_time(mode)
        self.f_var5.convert_time(mode)

    def apply_config(self, config: ScramblerConfig):
        config.sustain_chance = self.e_chance.get()
        config.sustain_weights = RandChoice([0, 1, 2, 3, 4], self.e_weights.get())

        config.sustain_var1 = self.f_var1.get_subconfig()
        config.sustain_var2 = self.f_var2.get_subconfig()
        config.sustain_var3 = self.f_var3.get_subconfig()
        config.sustain_var4 = self.f_var4.get_subconfig()
        config.sustain_var5 = self.f_var5.get_subconfig()

    def open_preset(self, preset: PresetOpen):
        batch = [
            [self.e_chance, "sustain_chance", "0"],
            [self.e_weights, "sustain_weights", "0 0 0 0 0"]
        ]

        preset.batch_set(batch)
        self.f_var1.open_preset(1, preset)
        self.f_var2.open_preset(2, preset)
        self.f_var3.open_preset(3, preset)
        self.f_var4.open_preset(4, preset)
        self.f_var5.open_preset(5, preset)

    def save_preset(self, preset: PresetSave):
        preset.add("sustain_chance", self.e_chance.get_str())
        preset.add("sustain_weights", self.e_weights.get_str())
        preset.add_separator()

        self.f_var1.save_preset(1, preset)
        self.f_var2.save_preset(2, preset)
        self.f_var3.save_preset(3, preset)
        self.f_var4.save_preset(4, preset)
        self.f_var5.save_preset(5, preset)
