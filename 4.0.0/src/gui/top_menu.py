import weakref
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui_main import MainWindow

import webbrowser
from state import PREFERENCES
from gui.tools import *
from gui.gui_common import *
from gui.factory_presets import presets


class MenuFile:
    def __init__(self, parent, window: "MainWindow"):
        self.root = tk.Menu(parent, tearoff=False)
        self.sel_length = tk.Menu(self.root, tearoff=False)

        self.root.add_command(label="Import audio file...", accelerator="Ctrl+I", command=window.cmd_load_audio)
        self.root.add_command(label="Scramble and export...", accelerator="Ctrl+E", command=window.cmd_scramble)
        self.root.add_command(label="Refresh file", accelerator="Ctrl+R", command=window.cmd_refresh)
        self.root.add_separator()

        if not AB_DISABLE_SIMPLEAUDIO:
            self.root.add_command(label="Start/stop preview", accelerator="Ctrl+P", command=window.cmd_preview)
            self.root.add_cascade(label="Preview length", menu=self.sel_length)
            self.root.add_separator()

        def command_prev_length():
            window.state.sav_config.set("len_preview", window.state.cur_config.len_preview.get())
        for val in [10, 30, 60, 120]:
            self.sel_length.add_radiobutton(label=f"{val} seconds", command=command_prev_length, value=val,
                                            var=window.state.cur_config.len_preview)

        self.root.add_command(label="Restore the last seed", command=lambda: restore_last_seed(window))
        self.root.add_command(label="Get audio information", command=lambda: audio_information(window))
        self.root.add_command(label="Locate FFmpeg folder", command=lambda: locate_ffmpeg(window))
        self.root.add_separator()

        self.root.add_command(label="Quit", command=sys.exit)


class MenuPresets:
    def __init__(self, parent, window: "MainWindow"):
        self.root = tk.Menu(parent, tearoff=False)
        self.factory = tk.Menu(self.root, tearoff=False)

        self.root.add_command(label="Open preset...", accelerator="Ctrl+O", command=window.cmd_open_preset)
        self.root.add_command(label="Save preset...", accelerator="Ctrl+S", command=window.cmd_save_preset)
        self.root.add_command(label="Default settings", accelerator="Ctrl+N", command=window.cmd_default_settings)
        self.root.add_separator()
        self.root.add_cascade(label="Factory presets", menu=self.factory)

        for p_name, p_content in presets.items():
            if p_name.startswith("_sep"):
                self.factory.add_separator()
            else:
                self.factory.add_command(label=p_name, command=lambda p=p_content: window.factory_preset(p))


class MenuPreferences:
    def __init__(self, parent, window: "MainWindow"):
        self.root = tk.Menu(parent, tearoff=False)

        for var, name in PREFERENCES.items():
            if var.startswith("_sep"):
                self.root.add_separator()
            else:
                if (OS_IS_UNIX or OS_IS_OTHER) and var == "open_scr_folder":
                    continue
                self.root.add_checkbutton(label=name, var=window.state.cur_config.pref_var[var],
                                          command=lambda v_name=var: window.state.sav_config.set(
                                              v_name, window.state.cur_config.pref_var[v_name].get()
                                          ))

        window_lnk = weakref.ref(window)
        window.state.cur_config.pref_var["audio_length_in_seconds"].trace_add(
            "write", lambda *args: window_lnk().update_header()
        )


class MenuHelp:
    def __init__(self, parent):
        self.root = tk.Menu(parent, tearoff=False)

        self.root.add_command(label="Join our Discord server", command=lambda: webbrowser.open(meta.link_discord))
        self.root.add_separator()

        self.root.add_command(label="License...", command=lambda: webbrowser.open(meta.link_license))
        self.root.add_command(label="About...", command=about_box)


class TopMenu:
    def __init__(self, parent, window: "MainWindow"):
        self.root = tk.Menu(parent, tearoff=False)
        self.m_file = MenuFile(self.root, window)
        self.m_presets = MenuPresets(self.root, window)
        self.m_preferences = MenuPreferences(self.root, window)
        self.m_help = MenuHelp(self.root)

        self.root.add_cascade(label="File", menu=self.m_file.root)
        self.root.add_cascade(label="Presets", menu=self.m_presets.root)
        self.root.add_cascade(label="Preferences", menu=self.m_preferences.root)
        self.root.add_cascade(label="Help", menu=self.m_help.root)
