import weakref
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui_main import MainWindow

import webbrowser
from state import PREFERENCES
from gui_tools.tools import *
from gui.gui_common import *
from factory_presets import presets
from localization import loc


class MenuFile:
    def __init__(self, parent, window: "MainWindow"):
        m_loc = loc["top_menu"]["file"]
        self.root = tk.Menu(parent, tearoff=False)
        self.sel_length = tk.Menu(self.root, tearoff=False)

        self.root.add_command(label=m_loc["import"], accelerator="Ctrl+I", command=window.cmd_load_audio)
        self.root.add_command(label=m_loc["export"], accelerator="Ctrl+E", command=window.cmd_scramble)
        self.root.add_command(label=m_loc["refresh"], accelerator="Ctrl+R", command=window.cmd_refresh)
        self.root.add_separator()

        if not AB_DISABLE_SIMPLEAUDIO:
            self.root.add_command(label=m_loc["preview"], accelerator="Ctrl+P", command=window.cmd_preview)
            self.root.add_cascade(label=m_loc["preview_length"], menu=self.sel_length)
            self.root.add_separator()

        def command_prev_length():
            window.state.sav_config.set("len_preview", window.state.cur_config.len_preview.get())
        for val in [10, 30, 60, 120]:
            self.sel_length.add_radiobutton(label=m_loc["n_seconds"].format(N_SEC=val), command=command_prev_length,
                                            value=val, var=window.state.cur_config.len_preview)

        self.root.add_command(label=m_loc["audio_info"], command=lambda: audio_information(window))
        self.root.add_separator()

        self.root.add_command(label=m_loc["quit"], command=sys.exit)


class MenuPresets:
    def __init__(self, parent, window: "MainWindow"):
        m_loc = loc["top_menu"]["presets"]
        self.root = tk.Menu(parent, tearoff=False)
        self.factory = tk.Menu(self.root, tearoff=False)

        self.root.add_command(label=m_loc["open"], accelerator="Ctrl+O", command=window.cmd_open_preset)
        self.root.add_command(label=m_loc["save"], accelerator="Ctrl+S", command=window.cmd_save_preset)
        self.root.add_command(label=m_loc["default"], accelerator="Ctrl+N", command=window.cmd_default_settings)
        self.root.add_separator()
        self.root.add_cascade(label=m_loc["factory"], menu=self.factory)
        self.root.add_command(label=m_loc["restore_seed"], command=lambda: restore_last_seed(window))

        for p_name, p_content in presets:
            if p_name == "_sep_":
                self.factory.add_separator()
            else:
                self.factory.add_command(label=m_loc.get(p_name, p_name),
                                         command=lambda p=p_content: window.factory_preset(p))


class MenuPreferences:
    def __init__(self, parent, window: "MainWindow"):
        m_loc = loc["top_menu"]["preferences"]
        self.root = tk.Menu(parent, tearoff=False)
        loc_sub_menu = tk.Menu(self.root, tearoff=False)

        self.root.add_command(label=m_loc["locate_ffmpeg"], command=lambda: locate_ffmpeg(window))
        self.root.add_cascade(label=m_loc["language"], menu=loc_sub_menu)
        loc_sub_menu.add_command(label=m_loc["lang_select_loc"], command=lambda: locate_localization(window))
        loc_sub_menu.add_command(label=m_loc["lang_reset_loc"], command=lambda: reset_localization(window))
        self.root.add_separator()

        for var in PREFERENCES:
            if var == "_sep_":
                self.root.add_separator()
            else:
                if (OS_IS_UNIX or OS_IS_OTHER) and var == "open_scr_folder":
                    continue
                self.root.add_checkbutton(label=m_loc.get(var, var),
                                          var=window.state.cur_config.pref_var[var],
                                          command=lambda v_name=var: window.state.sav_config.set(
                                              v_name, window.state.cur_config.pref_var[v_name].get()))

        window_lnk = weakref.ref(window)
        window.state.cur_config.pref_var["audio_length_in_seconds"].trace_add(
            "write", lambda *args: window_lnk().update_header()
        )


class MenuHelp:
    def __init__(self, parent):
        m_loc = loc["top_menu"]["help"]
        self.root = tk.Menu(parent, tearoff=False)

        self.root.add_command(label=m_loc["discord"], command=lambda: webbrowser.open(meta.link_discord))
        self.root.add_separator()

        self.root.add_command(label=m_loc["license"], command=lambda: webbrowser.open(meta.link_license))
        self.root.add_command(label=m_loc["about"], command=about_box)


class TopMenu:
    def __init__(self, parent, window: "MainWindow"):
        self.root = tk.Menu(parent, tearoff=False)
        self.m_file = MenuFile(self.root, window)
        self.m_presets = MenuPresets(self.root, window)
        self.m_preferences = MenuPreferences(self.root, window)
        self.m_help = MenuHelp(self.root)

        self.root.add_cascade(label=loc["top_menu"]["file"]["name"], menu=self.m_file.root)
        self.root.add_cascade(label=loc["top_menu"]["presets"]["name"], menu=self.m_presets.root)
        self.root.add_cascade(label=loc["top_menu"]["preferences"]["name"], menu=self.m_preferences.root)
        self.root.add_cascade(label=loc["top_menu"]["help"]["name"], menu=self.m_help.root)
