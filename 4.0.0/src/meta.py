import sys

title = "AudioButcher v4.0.0-p"
version = "4.0.0"
icon_b64 = "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"

description = """AudioButcher ver. 4.0.0 (Public Release), November 2025

Brought to you by the AudioButcher Team:
auspicious_mika, MightInvisible, osdwa, Shriki, vanpassinby, ZachMan

Runs in Python {}
""".format(sys.version)

dir_name = "AudioButcher"
def_error = "Unexpected error occurred while {}."

link_discord = "https://discord.gg/gNHxMmfTy4"
link_license = "https://www.gnu.org/licenses/gpl-3.0.txt"


# Comboboxes

rand_dists = ["Uniform", "Gauss", "Gauss (Clipped)", "Lognormal", "Exponential"]
rand_dists_sym = ["-", "±", "±", ",", "", "?"]
cb_speed_mode = ["Semitones", "Percent change", "Speed multiplier"]
cb_speed_affect = ["Disabled", "Relative to main speed", "Relative to original speed"]
cb_sustain_portion = ["Total length", "Portion [N] times", "% of portion", "% of segment", "% of fade-out"]
cb_quan_modes = ["None", "Slices", "BPM"]
cb_quan_directions = ["Closest", "<-", "->"]
cb_place_quan = ["Disabled", "By fixed step", "To onsets"]

cb_no_yes = ["No", "Yes"]
cb_crossfade_comp_mode = ["Shorten", "Cut off"]
cb_reverse_double_mode = ["Allowed", "Only reverse-1", "Only reverse-2"]
cb_quan_dur_bpm = ["By end position", "By length"]


# File extensions

all_files = ("All files", "*.*")

ext_audio_import = [
    ("Popular formats", "*.wav *.mp3 *.ogg *.flac"),
    ("Wave", "*.wav"),
    ("FLAC", "*.flac"),
    ("MPEG Layer-3", "*.mp3"),
    ("Ogg Vorbis", "*.ogg"),
    all_files
]

ext_audio_import_more = [
    ("Popular formats", "*.wav *.flac *.mp3 *.ogg *.aac *.wma *.m4a *.opus *.alac *.aiff *.aif *.mp4 *.avi *.mov *.mkv *.wmv *.webm *.mpeg *.mpg *.3gp"),
    ("~ Popular audio formats ~", "*.wav *.flac *.mp3 *.ogg *.aac *.wma *.m4a *.opus *.alac *.aiff *.aif"),
    ("Wave", "*.wav"),
    ("FLAC", "*.flac"),
    ("MPEG Layer-3", "*.mp3"),
    ("Ogg Vorbis", "*.ogg"),
    ("AAC", "*.aac"),
    ("Windows Media Audio", "*.wma"),
    ("MPEG-4 Audio", "*.m4a"),
    ("Opus", "*.opus"),
    ("ALAC", "*.alac"),
    ("AIFF", "*.aiff *.aif"),
    ("~ Popular video formats ~", "*.mp4 *.avi *.mov *.mkv *.wmv *.webm *.mpeg *.mpg *.3gp"),
    ("MPEG-4 Part 14", "*.mp4"),
    ("Audio Video Interleave", "*.avi"),
    ("Apple QuickTime Movie", "*.mov"),
    ("Matroska Video", "*.mkv"),
    ("Windows Media Video", "*.wmv"),
    ("Web Media File", "*.webm"),
    ("Moving Picture Experts Group", "*.mpeg *.mpg"),
    ("3rd Generation Partnership Project", "*.3gp"),
    all_files
]

ext_wave = [("Wave", "*.wav"), all_files]
ext_flac = [("FLAC", "*.flac"), all_files]
ext_mp3 = [("MPEG Layer-3", "*.mp3"), all_files]

ext_preset = [("AudioButcher Preset", "*.ab4"), all_files]

ext_preset_all = [
    ("All AudioButcher Presets", "*.ab4 *.ab3 *.abp"),
    ("AudioButcher 4.0 Preset", "*.ab4"),
    ("AudioButcher 3.0 Preset", "*.ab3"),
    ("AudioButcher 2.x Preset", "*.abp"),
    all_files
]

ext_midi = [("MIDI files", "*.mid *.midi"), all_files]
ext_slices = [("AudioButcher Slices", "*.ab_slices"), all_files]
ext_slices_alt = [("AudioButcher Alternative Slices", "*.ab_slices_alt"), all_files]

ext_slices_all = [
    ("All AudioButcher Slice files", "*.ab_slices *.ab_slices_alt *.abo *.sto"),
    ("AudioButcher Slices", "*.ab_slices"),
    ("AudioButcher Alternative Slices", "*.ab_slices_alt"),
    ("AudioButcher 2.2/3.0 Onsets", "*.abo *.sto"),
    all_files
]

export_formats = [
    # Name - Internal AB code - Extension - File types
    ("Wave (Signed 16 bit)", "wav16", "wav", ext_wave),
    ("Wave (Signed 24 bit)", "wav24", "wav", ext_wave),
    ("Wave (Signed 32 bit)", "wav32", "wav", ext_wave),
    ("Wave (32 bit float)", "wav32f", "wav", ext_wave),
    ("FLAC (Signed 16 bit)", "flac16", "flac", ext_flac),
    ("FLAC (Signed 24 bit)", "flac24", "flac", ext_flac),
    ("MPEG Layer-3", "mp3", "mp3", ext_mp3)
]
