from state import ABState
from slicing import Onsets, METHODS
from gui.gui_common import *


class SliceDetectionGui:
    def __init__(self, parent, glob_state: ABState):
        m_loc = loc["slice_detection"]
        self.root = ttk.LabelFrame(parent, text=m_loc["f_slice_detection"], padding=3)
        self.glob_state = glob_state
        self.values = {     # Method, Sens
            0: (0, "80"),  # Normal slices
            1: (0, "80"),  # Alt slices
        }

        self.c_selection = XCombobox(self.root, state="readonly",
                                     values=localize_list(["slices", "alt_slices"], m_loc["slice_types"]))
        self.c_selection.grid(row=0, column=0, columnspan=3, sticky="we")
        self.root.grid_columnconfigure(2, weight=1)

        col1 = ttk.Frame(self.root, padding=2)
        col2 = ttk.Frame(self.root, padding=2)
        col1.grid(row=1, column=0)
        col2.grid(row=1, column=1, sticky="n")

        self.l_method = ttk.Label(col1, text=m_loc["l_method"])
        self.c_method = XCombobox(col1, width=20, state="readonly",
                                  values=localize_list([m[0] for m in METHODS], m_loc["methods"]))
        self.l_sens = ttk.Label(col1, text=m_loc["l_sens"])
        self.e_sens = CChance(col1, ent_w=5)

        self.l_method.grid(row=0, column=0, sticky="w")
        self.c_method.grid(row=0, column=1, pady=1, sticky="e")
        self.l_sens.grid(row=1, column=0, sticky="w")
        self.e_sens.root.grid(row=1, column=1, sticky="e")

        self.b_gen_current = ttk.Button(col1, text=m_loc["b_gen_current"])
        self.b_gen_other = ttk.Button(col1, text=m_loc["b_gen_other"])
        self.b_get_statistics = ttk.Button(col1, text=m_loc["b_get_statistics"])
        self.b_gen_current.grid(row=2, column=0, columnspan=2, sticky="we")
        self.b_gen_other.grid(row=3, column=0, columnspan=2, sticky="we")
        self.b_get_statistics.grid(row=4, column=0, columnspan=2, sticky="we")

        self.b_file_load = ttk.Button(col2, text=m_loc["b_file_load"])
        self.b_file_save = ttk.Button(col2, text=m_loc["b_file_save"])
        self.b_file_edit = ttk.Button(col2, text=m_loc["b_file_edit"])
        self.b_file_erase = ttk.Button(col2, text=m_loc["b_file_erase"])

        self.b_file_load.grid(row=0, column=0, sticky="we")
        self.b_file_save.grid(row=1, column=0, sticky="we")
        self.b_file_edit.grid(row=2, column=0, sticky="we")
        self.b_file_erase.grid(row=3, column=0, sticky="we")

        self.c_selection.bind("<<ComboboxSelected>>", lambda event: self.values_set())
        self.c_method.bind("<<ComboboxSelected>>", lambda event: self.values_update())
        self.e_sens.e_chance.bind("<KeyRelease>", lambda event: self.values_update())

        self.c_selection.set(0)
        self.values_set()

    def get_selection(self):
        return self.c_selection.current()

    def get_selected_slices(self, selection=None) -> Onsets:
        if selection is None:
            selection = self.get_selection()

        return self.glob_state.slices_alt if selection == 1 else self.glob_state.slices

    def values_set(self):
        method, sens = self.values[self.get_selection()]
        self.c_method.current(method)
        self.e_sens.set(sens)
        self.update()

    def values_update(self):
        method = self.c_method.current()
        sens = self.e_sens.get_str()
        self.values[self.get_selection()] = method, sens
        self.update()

    def update(self):
        if self.glob_state.audio is None:
            self.b_gen_current.configure(state="disabled")
        else:
            self.b_gen_current.configure(state="normal")

        slices = self.get_selected_slices()
        if slices.are_there:
            self.b_file_save.configure(state="normal")
            self.b_file_erase.configure(state="normal")
        else:
            self.b_file_save.configure(state="disabled")
            self.b_file_erase.configure(state="disabled")

        if slices.are_there:
            self.b_get_statistics.configure(state="normal")
        else:
            self.b_get_statistics.configure(state="disabled")

        if METHODS[self.c_method.current()][2]:
            self.e_sens.e_chance.configure(state="normal")
        else:
            self.e_sens.e_chance.configure(state="disabled")
