from gui.gui_common import *
from gui_tools.tools_misc import *
from gui.time_entry import TimeEntry
import tkinter.filedialog as fd
import tkinter.messagebox as mb

import gui.filetypes as fts
from localization import loc
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui_main import MainWindow


class DlgExport:
    def __init__(self, window: "MainWindow", ask_length=True, auto_rewrite_confirmed=False):
        self.result = {}
        self.ask_length = ask_length
        self.rewrite_confirmed_auto = auto_rewrite_confirmed
        self.rewrite_confirmed_name = None
        self.state = window.state

        m_loc = loc["export_dialog"]
        self.body = tk.Toplevel(window.root)
        self.body.title(m_loc["title"])

        self.root = ttk.Frame(self.body, padding=10)
        self.root.pack(fill="x")
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, uniform="row")
        self.root.grid_rowconfigure(1, uniform="row")
        self.root.grid_rowconfigure(2, uniform="row")

        self.l_file = ttk.Label(self.root, text=m_loc["l_export_fname"])
        self.e_file = XEntry(self.root, width=50)
        self.b_file_browse = ttk.Button(self.root, command=self.cmd_browse_file,
                                        text=loc["meta"]["buttons"]["browse"])
        self.l_file.grid(row=0, column=0, sticky="w")
        self.e_file.grid(row=0, column=1, padx=1, sticky="ew")
        self.b_file_browse.grid(row=0, column=2)

        self.l_directory = ttk.Label(self.root, text=m_loc["l_export_folder"])
        self.e_directory = XEntry(self.root)
        self.b_directory_browse = ttk.Button(self.root, command=self.cmd_browse_directory,
                                             text=loc["meta"]["buttons"]["browse"])
        self.l_directory.grid(row=1, column=0, sticky="w")
        self.e_directory.grid(row=1, column=1, padx=1, sticky="ew")
        self.b_directory_browse.grid(row=1, column=2)

        self.l_format = ttk.Label(self.root, text=m_loc["l_export_format"])
        self.c_format = XCombobox(self.root, state="readonly",
                                  values=[fmt[0] for fmt in fts.export_formats])
        self.l_format.grid(row=2, column=0, sticky="w")
        self.c_format.grid(row=2, column=1, padx=1, sticky="we")

        self.bottom = ttk.Frame(self.body, padding=10)
        self.l_length = ttk.Label(self.bottom, text=m_loc["l_export_length"])
        self.x_partial = CCheckbox(self.bottom, text=m_loc["x_export_partial"])

        if window.state.get_pref_var("export_length_in_seconds"):
            self.e_length = XEntry(self.bottom, width=10)
            ttk.Label(self.bottom, text=loc["meta"]["time"]["sec_long"]).grid(row=0, column=2, padx=1)
            self.e_partial = XEntry(self.bottom, width=10)
            ttk.Label(self.bottom, text=loc["meta"]["time"]["sec_long"]).grid(row=1, column=2, padx=1)
        else:
            self.e_length = TimeEntry(self.bottom)
            self.e_partial = TimeEntry(self.bottom)

        self.bottom.pack(fill="x")
        self.l_length.grid(row=0, column=0, sticky="w")
        self.e_length.grid(row=0, column=1, padx=1, pady=1)
        self.x_partial.root.grid(row=1, column=0, sticky="w")
        self.e_partial.grid(row=1, column=1, padx=1, pady=1)

        self.buttons = ttk.Frame(self.body, padding=10)
        self.b_ok = ttk.Button(self.buttons, text=loc["meta"]["buttons"]["ok"], command=self.cmd_ok)
        self.b_cancel = ttk.Button(self.buttons, text=loc["meta"]["buttons"]["cancel"], command=self.cmd_cancel)

        self.buttons.pack(fill="x")
        self.b_cancel.pack(side="right")
        self.b_ok.pack(side="right")

        self.config_entries()
        apply_window_style(self.body, resize_w=True)

        self.body.grab_set()
        self.body.focus_force()
        self.e_file.focus_set()
        self.body.wait_window()

    def config_entries(self):
        # Fill
        fn_unix = self.state.get_pref_var("unix_filenames") and not self.rewrite_confirmed_auto
        self.e_file.set(unix_filename() if fn_unix else self.state.cur_config.exp_last_file_name)
        self.e_directory.set(self.state.sav_config.get("dir_export"))
        self.c_format.set(self.state.cur_config.exp_last_format)
        self.e_length.set(self.state.sav_config.get("len_export"))
        self.e_partial.set(self.state.cur_config.exp_partial_length)
        self.x_partial.set(int(self.state.cur_config.exp_partial_enabled))

        # Disable
        if not self.ask_length:
            self.e_length.configure(state="disabled")
            self.x_partial.root.configure(state="disabled")

        # Bind
        self.body.bind("<Return>", lambda _: self.cmd_ok())
        self.body.bind("<Escape>", lambda _: self.cmd_cancel())
        self.x_partial.root.configure(command=self.config_partial)

        self.config_partial()
        if self.rewrite_confirmed_auto:
            self.rewrite_confirmed_name = self.e_file.get()

    def config_partial(self):
        self.state.cur_config.exp_partial_enabled = self.x_partial.get()
        if not (self.ask_length and self.x_partial.get()):
            self.e_partial.configure(state="disabled")
        else:
            self.e_partial.configure(state="normal")

    def apply_config(self, path, format_id):
        def len_2_sample(length):
            return round(float(length) * self.state.audio.sample_rate)

        self.result = {
            "path": path,
            "format": fts.export_formats[format_id][1],
            "length": len_2_sample(self.e_length.get()) if self.ask_length else 0,
            "partial": len_2_sample(self.e_partial.get()) if (self.ask_length and self.x_partial.get()) else 0,
        }

        self.state.sav_config.set("dir_export", os.path.dirname(path))
        self.state.cur_config.exp_last_file_name = simple_file_name(path)
        self.state.cur_config.exp_last_format = format_id

        if self.ask_length:
            self.state.sav_config.set("len_export", self.e_length.get())
        if self.ask_length and self.x_partial.get():
            self.state.cur_config.exp_partial_length = self.e_partial.get()

    def apply(self):
        f_name = self.e_file.get()
        format_id = self.c_format.current()
        m_loc = loc["export_dialog"]

        path = os.path.join(self.e_directory.get(), f_name)
        if os.path.splitext(path)[1].lower() != "."+fts.export_formats[format_id][2].lower():
            path += "." + fts.export_formats[format_id][2]
        self.apply_config(path, format_id)

        # TODO: Partial generation: Error if length increases

        if format_id == -1:
            mb.showerror(m_loc["title"], m_loc["err_wrong_format"], parent=self.root)
            return

        if not os.path.exists(os.path.dirname(path)):
            mb.showerror(m_loc["title"], m_loc["err_folder_not_exist"], parent=self.root)
            return

        if os.path.exists(path) and f_name != self.rewrite_confirmed_name:
            overwrite = mb.askyesno(m_loc["title"], icon="warning", parent=self.root,
                                    message=m_loc["err_overwrite"].format(FNAME=os.path.basename(path)))
            if not overwrite:
                return

        self.body.destroy()

    def cmd_ok(self):
        try:
            self.apply()
        except Exception as e:
            self.result.clear()
            mb.showerror("Error", str(e), parent=self.root)

    def cmd_cancel(self):
        self.result.clear()
        self.body.destroy()

    def cmd_browse_file(self):
        format_id = self.c_format.current()
        if format_id == -1:
            filetypes = fts.all_files
            default_extension = None
        else:
            filetypes = fts.export_formats[format_id][3]
            default_extension = fts.export_formats[format_id][2]

        init_name = self.e_file.get() + (f".{default_extension}" if default_extension else "")
        path = fd.asksaveasfilename(filetypes=filetypes, defaultextension=default_extension,
                                    initialdir=self.e_directory.get(), initialfile=init_name)

        if not path:
            return

        self.e_file.set(os.path.basename(path))
        self.e_directory.set(os.path.dirname(path))
        self.rewrite_confirmed_name = os.path.basename(path)

    def cmd_browse_directory(self):
        path = fd.askdirectory(initialdir=self.e_directory.get())

        if not path:
            return

        self.e_directory.set(path)
