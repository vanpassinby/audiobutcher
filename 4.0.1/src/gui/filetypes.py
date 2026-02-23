from localization import loc
m_loc = loc["filetypes"]


all_files = (m_loc["all"], "*.*")

ext_audio_import = [
    (m_loc["popular"], "*.wav *.mp3 *.ogg *.flac"),
    ("Wave", "*.wav"),
    ("FLAC", "*.flac"),
    ("MPEG Layer-3", "*.mp3"),
    ("Ogg Vorbis", "*.ogg"),
    all_files
]

ext_audio_import_more = [
    (m_loc["popular"], "*.wav *.flac *.mp3 *.ogg *.aac *.wma *.m4a *.opus *.alac *.aiff *.aif *.mp4 *.avi *.mov *.mkv *.wmv *.webm *.mpeg *.mpg *.3gp"),

    (m_loc["popular_audio"], "*.wav *.flac *.mp3 *.ogg *.aac *.wma *.m4a *.opus *.alac *.aiff *.aif"),
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

    (m_loc["popular_video"], "*.mp4 *.avi *.mov *.mkv *.wmv *.webm *.mpeg *.mpg *.3gp"),
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

ext_localization = [(m_loc["json"], "*.json"), all_files]

ext_preset = [(m_loc["preset"], "*.ab4"), all_files]

ext_preset_all = [
    (m_loc["preset_all"], "*.ab4 *.ab3 *.abp"),
    (m_loc["preset_40"], "*.ab4"),
    (m_loc["preset_30"], "*.ab3"),
    (m_loc["preset_2x"], "*.abp"),
    all_files
]

ext_midi = [(m_loc["midi"], "*.mid *.midi"), all_files]
ext_slices = [(m_loc["ab_slices"], "*.ab_slices"), all_files]
ext_slices_alt = [(m_loc["ab_slices_alt"], "*.ab_slices_alt"), all_files]

ext_slices_all = [
    (m_loc["ab_slices_all"], "*.ab_slices *.ab_slices_alt *.abo *.sto"),
    (m_loc["ab_slices"], "*.ab_slices"),
    (m_loc["ab_slices_alt"], "*.ab_slices_alt"),
    (m_loc["ab_onsets_legacy"], "*.abo *.sto"),
    all_files
]

export_formats = [
    # Name - AB internal code - Extension - File types
    ("Wave (Signed 16 bit)", "wav16", "wav", ext_wave),
    ("Wave (Signed 24 bit)", "wav24", "wav", ext_wave),
    ("Wave (Signed 32 bit)", "wav32", "wav", ext_wave),
    ("Wave (32 bit float)", "wav32f", "wav", ext_wave),
    ("FLAC (Signed 16 bit)", "flac16", "flac", ext_flac),
    ("FLAC (Signed 24 bit)", "flac24", "flac", ext_flac),
    ("MPEG Layer-3", "mp3", "mp3", ext_mp3)
]
