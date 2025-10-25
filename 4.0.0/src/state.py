from typing import Optional
from ab_tools import int1

from common import *
import tkinter as tk
from sav_config import SavedConfig, DEFAULTS

from audio import Audio
from slicing import Onsets
from scrambler.scr_state import ScramblerState


PREFERENCES = {
    "unix_filenames": "Generate unique file names",
    "show_error_info": "Show additional error information",
    "conv_sec2ms": "Automatic ms-sec conversion",
    "disable_completion_dialog": "Disable 'scrambling complete' dialog",
    "_sep1": None,
    "audio_length_in_seconds": "Show audio length in seconds",
    "export_length_in_seconds": "Show export length in seconds",
    "show_ffmpeg_formats": "Show more import formats (FFmpeg)",
    "remember_dnd_path": "Remember dropped file path",
    "open_scr_folder": "Open scrambled audio in folder",
    "_sep2": None,
    "slices_erase": "Erase slices after new file imported",
    "slices_auto": "Automatically detect slices",
    "slices_alt_auto": "Automatically detect alternative slices"
}


class CurConfig:
    def __init__(self):
        self.audio_path = None
        self.exp_last_file_name = "untitled"
        self.exp_last_format = 0

        self.exp_partial_length = "0"
        self.exp_partial_enabled = False

        self.last_seed = None
        self.last_preset_name = None
        self.show_hints = False

        self.len_preview = tk.IntVar()
        self.pref_var: dict[str, tk.IntVar] = {}
        for var in PREFERENCES:
            if not var.startswith("_sep"):
                self.pref_var[var] = tk.IntVar()


class ABState:
    def __init__(self):
        self.audio: Optional[Audio] = None
        self.scr_state: Optional[ScramblerState] = None
        self.scr_progress = (0, -1)

        self.slices = Onsets([], 1000)
        self.slices_alt = Onsets([], 1000)

        self.now_scrambling = False
        self.now_previewing = False
        self.force_abort = False

        self.cur_config = CurConfig()
        self.sav_config = SavedConfig(os.path.join(HOME_PATH, ".audiobutcher"), "AudioButcher_Config")
        self.sync_configs()

    def sync_configs(self):
        self.cur_config.len_preview.set(int1(self.sav_config.get("len_preview"), DEFAULTS["len_preview"]))
        for option_name, variable in self.cur_config.pref_var.items():
            variable.set(int1(self.sav_config.get(option_name)))

    def get_pref_var(self, var_name: str):
        return bool(self.cur_config.pref_var[var_name].get())

    def load_audio(self, audio_path: str):
        self.cur_config.audio_path = audio_path
        self.audio = Audio.load(audio_path)
