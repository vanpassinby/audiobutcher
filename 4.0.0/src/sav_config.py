import os.path
from common import HOME_PATH
from configparser import RawConfigParser

DEFAULTS = {
    "dir_audio": HOME_PATH,
    "dir_export": HOME_PATH,
    "dir_presets": HOME_PATH,
    "dir_slices": HOME_PATH,
    "dir_slices_midi": HOME_PATH,
    "ffmpeg_path": "",

    "len_export": "120",
    "len_preview": "30",

    "unix_filenames": "1",
    "show_error_info": "0",
    "conv_sec2ms": "1",
    "disable_completion_dialog": "0",

    "audio_length_in_seconds": "0",
    "export_length_in_seconds": "0",
    "show_ffmpeg_formats": "0",
    "remember_dnd_path": "1",
    "open_scr_folder": "1",

    "slices_erase": "1",
    "slices_auto": "0",
    "slices_alt_auto": "0",
}


class SavedConfig:
    def __init__(self, file, sec_name):
        self.config = RawConfigParser()
        self.file = os.path.abspath(file)
        self.sec_name = sec_name

        try:
            self.config.read(self.file, encoding="utf-8")
        except Exception as e:
            print(f"Error: Config file: {e}")

        if not self.config.has_section(self.sec_name):
            self.config[self.sec_name] = {}

    def set(self, option, value):
        self.config[self.sec_name][option] = str(value)

        with open(self.file, "w", encoding="utf-8") as cfg_file:
            self.config.write(cfg_file)

    def get(self, option):
        return self.config.get(self.sec_name, option, fallback=DEFAULTS[option])
