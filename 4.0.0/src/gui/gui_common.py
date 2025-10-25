import meta
import ab_random
from ab_tools import int1

import tkinter as tk
import tkinter.ttk as ttk


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
            self.insert(0, "<Error>")
            self.configure(state="readonly")


class CDistribution:
    def __init__(self, parent, padding=1, ent_w=6, cbx_w=15):
        self.enabled = True
        self.root = ttk.Frame(parent, padding=padding)

        self.e_val1 = XEntry(self.root, width=ent_w)
        self.l_sep1 = ttk.Label(self.root, text="-", width=1, anchor="center")
        self.e_val2 = XEntry(self.root, width=ent_w)
        self.l_sep2 = ttk.Label(self.root, text="/", width=1, anchor="center")
        self.c_mode = XCombobox(self.root, width=cbx_w, values=meta.rand_dists, state="readonly")

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
        sep_txt = meta.rand_dists_sym[self.c_mode.current()]
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
        mode = self.c_mode.current()
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
        return "1" if self.variable.get() else "0"

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
