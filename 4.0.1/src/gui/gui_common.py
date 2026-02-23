import ab_random
from ab_tools import int1
from typing import Optional
from loc_tools import localize_list
from localization import loc

import tkinter as tk
import tkinter.ttk as ttk


class BiDict:
    def __init__(self, values: list, legacy_map: Optional[dict] = None):
        self.val_dict = {value: idx for idx, value in enumerate(values)}

        if legacy_map:
            self.legacy_map = legacy_map
        else:
            self.legacy_map = {str(i): i for i in range(len(values))}

        self.rev_dict = {}
        for key, value in self.val_dict.items():
            self.rev_dict[value] = key

    def get_keys(self):
        return list(self.val_dict.keys())

    def get(self, key):
        return self.val_dict.get(
            key,
            self.legacy_map.get(key, -1)
        )

    def rget(self, key):
        return self.rev_dict.get(key, "_")


class XEntry(ttk.Entry):
    def set(self, text):
        state = self["state"]
        self.configure(state="normal")
        self.delete(0, tk.END)
        self.insert(0, str(text))
        self.configure(state=state)

    def mult(self, k):
        new_numbers = []
        for string in self.get().split():
            try:
                number = float(string) * k
            except ValueError:
                number = string
            else:
                if number % 1 == 0:
                    number = int(number)
            new_numbers.append(str(number))
        self.set(" ".join(new_numbers))

    def conv_time(self, mode):
        if mode == "sec2ms":
            self.mult(1000)
        if mode == "ms2sec":
            self.mult(0.001)


class XCombobox(ttk.Combobox):
    def set(self, idx):
        try:
            self.current(int(float(idx)))
        except:
            self.configure(state="normal")
            self.delete(0, "end")
            self.insert(0, "?")
            self.configure(state="readonly")


class YCombobox(ttk.Combobox):
    def __init__(self, *args, items: BiDict, loc_part: dict, **kwargs):
        super().__init__(*args, **kwargs, values=localize_list(items.get_keys(), loc_part))
        self.items = items

    def get_str(self):
        return self.items.rget(self.current())

    def set(self, value: str):
        try:
            idx = self.items.get(value)
            self.current(idx)
        except:
            self.configure(state="normal")
            self.delete(0, "end")
            self.insert(0, "?")
            self.configure(state="readonly")


class CDistribution:
    rand_dists = BiDict(["uniform", "gauss", "gauss_c", "lognorm", "exp"])
    rand_dists_sym = ["-", "±", "±", ",", "", "?"]

    def __init__(self, parent, padding=1):
        self.enabled = True
        self.root = ttk.Frame(parent, padding=padding)

        self.e_val1 = XEntry(self.root, width=6)
        self.l_sep1 = ttk.Label(self.root, text="-", width=1, anchor="center")
        self.e_val2 = XEntry(self.root, width=6)
        self.l_sep2 = ttk.Label(self.root, text="/", width=1, anchor="center")
        self.c_mode = YCombobox(self.root, width=loc["_geometry"]["cb_rand_dist"], state="readonly",
                                items=self.rand_dists, loc_part=loc["meta"]["rand_dists"])

        self.e_val1.grid(row=0, column=0)
        self.l_sep1.grid(row=0, column=1)
        self.e_val2.grid(row=0, column=2)
        self.l_sep2.grid(row=0, column=3)
        self.c_mode.grid(row=0, column=4)

        self.c_mode.bind("<<ComboboxSelected>>", lambda event: self.update())

    def set_state(self, enabled=True):
        self.enabled = enabled
        self.update()

    def update(self):
        sep_txt = self.rand_dists_sym[self.c_mode.current()]
        self.l_sep1.configure(text=sep_txt)

        if self.enabled:
            self.e_val1.configure(state="normal")
            self.c_mode.configure(state="readonly")
        else:
            self.e_val1.configure(state="disabled")
            self.c_mode.configure(state="disabled")

        if self.c_mode.current() == 4 or not self.enabled:
            self.e_val2.configure(state="disabled")
        else:
            self.e_val2.configure(state="normal")

    def get(self):
        mode = self.c_mode.current()
        val1 = float(self.e_val1.get())
        val2 = 0 if mode == 4 else float(self.e_val2.get())
        return ab_random.RandNumber(mode, val1, val2)

    def get_str(self):
        mode = self.c_mode.get_str()
        val1 = self.e_val1.get()
        val2 = self.e_val2.get()
        return f"{mode} {val1} {val2}"

    def set(self, string: str):
        sep = string.split() + ["?", "?", "?"]
        self.c_mode.set(sep[0])
        self.e_val1.set(sep[1])
        self.e_val2.set(sep[2])
        self.update()

    def conv_time(self, mode):
        if self.c_mode.current() != 3:
            self.e_val1.conv_time(mode)
            self.e_val2.conv_time(mode)


class CChance:
    def __init__(self, parent, padding=1, ent_w=4):
        self.root = ttk.Frame(parent, padding=padding)

        self.e_chance = XEntry(self.root, width=ent_w)
        self.l_chance = ttk.Label(self.root, text="%", width=2)

        self.e_chance.grid(row=0, column=0)
        self.l_chance.grid(row=0, column=1)

    def get(self):
        return ab_random.RandChance(float(self.e_chance.get()))

    def get_str(self):
        return self.e_chance.get()

    def set(self, value):
        self.e_chance.set(value)


class CCheckbox:
    def __init__(self, parent, text: str):
        self.variable = tk.IntVar()
        self.root = ttk.Checkbutton(parent, text=text, variable=self.variable)

    def get(self):
        return bool(self.variable.get())

    def get_str(self):
        return "1" if self.get() else "0"

    def set(self, value):
        self.variable.set(int1(value))


class CWeights:
    def __init__(self, parent, amount: int, ent_w=4, padding=1):
        self.root = ttk.Frame(parent, padding=padding)
        self.entries: list[XEntry] = []

        first = False
        for n in range(amount):
            if not first:
                first = True
            else:
                ttk.Label(self.root, text="/", width=1, anchor="center").pack(side="left")

            entry = XEntry(self.root, width=ent_w)
            self.entries.append(entry)
            entry.pack(side="left")

    def get(self):
        return [int(entry.get()) for entry in self.entries]

    def get_str(self):
        return " ".join(entry.get() for entry in self.entries)

    def set(self, weights):
        weights = weights.split() + [0] * len(self.entries)
        for i in range(len(self.entries)):
            self.entries[i].set(weights[i])
