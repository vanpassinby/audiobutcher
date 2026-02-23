loc = {
    "loc_credit": "",

    "_geometry": {
        "tb_button": 15,
        "cb_rand_dist": 15,
        "cb_speed_measure": 30,
        "cb_sustain_length_mode": 20,
        "cb_quan_mode": 10,
        "cb_quan_direction": 8,
        "cb_tweak_option": 15
    },

    "meta": {
        "credit_ab": "{AB} ver. {VERSION} ({VER_NOTE}), {REL_MONTH} {REL_YEAR}",
        "credit_team": "Brought to you by the AudioButcher Team:\n{TEAM}",
        "credit_python": "Runs in Python {PY_VERSION}",

        "months": ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"],

        "time": {
            "hms": ["h", "m", "s"],
            "ms_short": "ms",
            "sec_short": "s",
            "sec_long": "seconds"
        },

        "buttons": {
            "ok": "OK",
            "cancel": "Cancel",
            "browse": "Browse"
        },

        "rand_dists": {
            "uniform": "Uniform",
            "gauss": "Gauss",
            "gauss_c": "Gauss (Clipped)",
            "lognorm": "Lognormal",
            "exp": "Exponential"
        }
    },

    "messages": {
        "error": "Error",
        "warning": "Warning",
        "error_info": "Error information:",

        "err_unexpected": "Unexpected error occurred while {ACTION}.",
        "err_unexpected_actions": {
            "slice_detection": "detecting slices",
            "slice_open": "opening slices",
            "slice_save": "saving slices",
            "slice_randgen": "generating random slices",
            "slice_process": "processing slices",

            "midi_import": "importing MIDI",
            "audio_import": "importing audio",
            "audio_export": "exporting audio",

            "preset_open": "opening preset",
            "preset_save": "saving preset",
            "config_read": "reading configuration",

            "preview": "previewing",
            "scramble": "scrambling",
            "file_open": "opening file"
        },

        "warn_ffmpeg_update": "Parameters have been updated. However, the selected folder does not contain FFmpeg or FFprobe, so imports may fail.",
        "warn_preset_unknown": "This preset was created using an unknown version of AudioButcher ({VERSION}). It will be opened as a {FALLBACK_VER} preset. Some parameters may be corrupted or lost.",
        "warn_preset_not_specified": "Not specified",

        "loc_title": "Localization",
        "loc_cant_load": "Can't load this localization file.",
        "loc_success": "Please restart the application for the localization to take full effect.",

        "aud_import_title": "Import",
        "aud_import_success": "Audio imported successfully.",

        "scr_abort_title": "Abort",
        "scr_abort_confirm": "Are you sure you want to abort scrambling?\nThe current rendered length is {CURRENT} out of {TARGET} ({PROGRESS:.1%}).\nIf you abort, scrambling cannot be resumed.\nThe audio will still be exported or previewed.",

        "scr_partial_title": "Partial generation",
        "scr_partial_complete": "Generated {CURRENT} of {TARGET} ({PROGRESS:.1%}).\nAdjust settings if needed, then click 'Continue'.",

        "scr_export_title": "Export",
        "scr_preview_title": "Preview",
        "scr_complete_title": "Complete!",
        "scr_complete_success": "Scrambling complete.\nDo you want to open your file now?"
    },

    "cfg_check": {
        "msg_import": "You have to first import an audio file!",
        "msg_dropdowns": "Please check all dropdowns!",
        "msg_clipped_gauss": "In CLIPPED GAUSS random mode, the sum of the parameters must be greater than 0!",
        "msg_warn_lognorm": "In LOGNORMAL random mode, parameters with sum greater than 10 are not recommended! Continue anyway?",
        "msg_zero_weights": "Total of {PARAM} weights must be greater than zero!",
        "msg_zero_weights_params": {
            "speed": "speed variation",
            "sustain": "sustain variation",
            "skip_dir": "skip direction",
            "ast": "average start time",
            "ast_dev": "average start time deviation",
            "shift_dir": "segment shift direction",
            "volume": "volume change direction"
        },
        "msg_zero_segm_length": "Segment length can't be zero!",
        "msg_zero_frame_length": "Frame length can't be zero!",
        "msg_negative_speed": "Speed cannot be zero or negative!",
        "msg_spd_weight_mismatch": "The number of speeds and their weights must match! ({E} vs {W})\nYou can leave the weights field blank for equal weighting.",
        "msg_ast_weight_mismatch": "The number of average start times and their weights must match! ({E} vs {W})\nYou can leave the weights field blank for equal weighting.",
        "msg_zero_sustain": "Sustain portion can't be zero! (Variant #{N_VAR})",
        "msg_framing_wrong_math": "In [Framing: Speed ratio], math equations can only include numbers, operators (. + - * /), parentheses, special words ([length], [length_samp], [sample_rate]) and spaces!",
        "msg_quan_slice": "You can't use SLICES quantization mode without slices detected.\nDo you want to detect slices now?",
        "msg_zero_bpm": "Quantization BPM can't be zero!",
        "msg_warn_performance": "This operation will require at least {REQ} MB of RAM, amounting to {PERC:.1%} of your currently available memory. Continuing may affect your device's performance.\nWould you like to proceed?"
    },

    "filetypes": {
        "all": "All files",
        "popular": "Popular formats",
        "popular_audio": "~ Popular audio formats ~",
        "popular_video": "~ Popular video formats ~",

        "preset": "AudioButcher Preset",
        "preset_2x": "AudioButcher 2.x Preset",
        "preset_30": "AudioButcher 3.0 Preset",
        "preset_40": "AudioButcher 4.0 Preset",
        "preset_all": "All AudioButcher Presets",

        "json": "JSON files",
        "midi": "MIDI files",
        "ab_slices": "AudioButcher Slices",
        "ab_slices_alt": "AudioButcher Alternative Slices",
        "ab_slices_all": "All AudioButcher Slice files",
        "ab_onsets_legacy": "AudioButcher 2.2/3.0 Onsets"
    },

    "top_menu": {
        "state_preview": "Previewing",

        "file": {
            "name": "File",
            "import": "Import audio file...",
            "export": "Scramble and export...",
            "refresh": "Refresh file",
            "preview": "Start/stop preview",
            "preview_length": "Preview length",
            "n_seconds": "{N_SEC} seconds",
            "audio_info": "Get audio information",
            "quit": "Quit"
        },

        "presets": {
            "name": "Presets",
            "open": "Open preset...",
            "save": "Save preset...",
            "default": "Default settings",
            "factory": "Factory presets",
            "restore_seed": "Restore the last seed",

            "p_basic": "Basic scrambling",
            "p_basic2": "Basic scrambling II",
            "p_basic3": "Basic scrambling III",
            "p_repeat": "Repeats demo",
            "p_reappear": "Reappearance demo",
            "p_sustain": "Sustain demo",
            "p_sustain2": "Sustain demo II",
            "p_sustain3": "Sustain demo III",
            "p_loop_pattern": "Loop & pattern demo",
            "p_loop_pattern2": "Loop & pattern demo II",
            "p_ast": "Average start times demo",
            "p_framing": "Framing demo",
            "p_framing2": "Framing demo II",
            "p_quan": "Quantization demo",
            "p_general": "General demo",
            "p_sustain_loop": "Sustain + Loop demo",
            "p_reverse_slices": "Reverse each slice",
            "p_another_demo": "Another demo (feat. Framing)"
        },

        "preferences": {
            "name": "Preferences",
            "locate_ffmpeg": "Locate FFmpeg folder",
            "language": "Language",
            "lang_select_loc": "Select localization file",
            "lang_reset_loc": "Reset localization",

            "unix_filenames": "Generate unique file names",
            "show_error_info": "Show additional error information",
            "conv_sec2ms": "Automatic ms-sec conversion",
            "disable_completion_dialog": "Disable 'scrambling complete' dialog",

            "audio_length_in_seconds": "Show audio length in seconds",
            "export_length_in_seconds": "Show export length in seconds",
            "show_ffmpeg_formats": "Show more import formats (FFmpeg)",
            "remember_dnd_path": "Remember dropped file path",
            "open_scr_folder": "Open scrambled audio in folder",

            "visual_onsets_all": "Show slice length distribution in full",
            "slices_erase": "Erase slices after new file imported",
            "slices_auto": "Automatically detect slices",
            "slices_alt_auto": "Automatically detect alternative slices"
        },

        "help": {
            "name": "Help",
            "discord": "Join our Discord server",
            "license": "License...",
            "about": "About..."
        },

        "toolbar": {
            "b_import": "Import audio",
            "b_scramble": "Scramble",
            "b_scramble_abort": "Abort",
            "b_scramble_continue": "Continue",
            "b_preview": "Preview",
            "b_preview_stop": "Stop",
            "b_open_preset": "Open preset",
            "b_save_preset": "Save preset",
            "b_hints_enable": "Enable hints",
            "b_hints_disable": "Disable hints",
            "x_use_seconds": "Measure in seconds",
            "x_use_seed": "Generate from seed: "
        }
    },

    "tab_basic": {
        "name": "Basic",

        "l_duration": "Segment length: ",
        "l_reverse1": "First reverse chance: ",
        "l_reverse2": "Second reverse chance: ",
        "l_pause": "Pause length: ",
        "l_pause_chance": "Pause chance: ",
        "l_consec_pause_chance": "Consecutive pause chance: ",

        "l_crossfade": "Crossfade length: ",
        "l_crossfade_chance": "Crossfade chance: ",
        "l_fadein": "Fade-in length: ",
        "l_fadein_chance": "Fade-in chance: ",
        "l_fade_only_into_pauses": "Fade only into pauses (chance): ",
        "l_fadeout": "Fade-out length: ",
        "l_fadeout_chance": "Fade-out chance: ",
        "x_fade_out_perc_note": "Measure fade-out from last slice",

        "l_repeat": "Repeat amount: ",
        "l_repeat_chance": "Repeat chance: ",
        "x_repeat_in_mss": "Measure repeats in ms/sec",
        "l_reappear": "Reappear interval: ",
        "l_reappear_chance": "Reappear chance: ",
        "l_reappear_reoccur_chance": "Allow reoccurrence (chance): ",

        "f_speed_change": " Speed change ",
        "l_speed_main": "Main speed: ",
        "l_speed_alter": "Speed alteration chance: ",
        "e_speed_alter": {
            "semitones": "Semitones",
            "perc_change": "Percent change",
            "speed_mult": "Speed multiplier"
        },

        "l_speed_variations": "Speed variations: ",
        "l_speed_weights": "Weights (optional): ",
        "l_speed_affect_mode": "Length scaling: ",
        "c_speed_affect_mode": {
            "disabled": "Disabled",
            "to_main": "Relative to main speed",
            "to_original": "Relative to original speed"
        }
    },

    "tab_sustain": {
        "name": "Sustain",

        "l_chance": "Sustain chance: ",
        "l_weights": "Variant weights: ",
        "t_variant": "Variant {N_VAR}",

        "l_crossfade": "Crossfade: ",
        "l_length": "Sustain length: ",
        "l_length_mode": "Mode: ",
        "c_length_mode": {
            "total": "Total length",
            "n_portion": "Portion [N] times",
            "p_portion": "% of portion",
            "p_segment": "% of segment",
            "p_fadeout": "% of fade-out"
        },
        "x_length_exact": "Exact",

        "l_portion_length": "Portion length: ",
        "x_portion_proportional": "Proportional to segment length (%)",
        "l_portion_minimum": "Minimal required portion: ",

        "x_allow_quan": "Allow portion quantization",
        "l_shift_chance": "Shift chance: ",
        "l_reverse_chance": "Reverse chance: ",
        "l_consec_chance": "Consecutiveness chance: ",

        "preset_menu": {
            "mirror": "Preset: Mirrored segment",
            "mirror_full": "Preset: Mirrored segment (full)",
            "mirror_asym": "Preset: Mirrored segment (asymmetrical)",
            "fadeout": "Preset: Fade-out tail",
            "clear": "Clear"
        }
    },

    "tab_pattern": {
        "name": "Pattern",

        "f_loop": " Loop ",
        "l_loop_begin": "Loop begin: ",
        "f_loop_chances": " Chances ",
        "l_pattern": "Pattern: ",
        "l_repeat": "Repeat: ",

        "l_count_full_length": "Count full length: ",
        "l_count_pause_length": "Count pause length: ",
        "l_count_pattern_length": "Count pattern length: ",
        "l_break_skips": "Skipping can break loop: ",
        "l_break_pattern": "Pattern can break loop: ",
        "l_break_avgstart": "AST can break loop: ",

        "f_loop_skipping": " Skipping ",
        "l_skip_chance": "Skip chance: ",
        "t_skip_modes_forw": "Forwards",
        "t_skip_modes_back": "Backwards",
        "t_skip_modes_rand": "Random",
        "l_direction_weight": "Direction weight: ",
        "l_min_skip": "Minimum skip: ",
        "l_min_skip_chance": "Chance: ",
        "l_add_dev": "Additional deviation: ",
        "l_add_dev_chance": "Chance: ",

        "t_skip_forw": "Forwards",
        "t_skip_back": "Backwards",
        "t_skip_rand": "Random",

        "f_loop_ast": " Average start times ",
        "l_ast_chance": "Chance: ",
        "l_ast_times": "Times: ",
        "l_ast_weights": "Weights (optional): ",
        "l_ast_deviation": "Deviation: ",
        "l_ast_dev_chance": "D. chance: ",
        "l_ast_dev_direction": "Direction: ",
        "l_ast_dev_dir_hint": "Weight: <- vs ->",
        "l_ast_force_pattern": "Force pattern (chance): "
    },

    "tab_framing": {
        "name": "Framing",

        "f_general": " General ",
        "x_framing_enable": "Framing",
        "l_frame_size": "Frame size: ",
        "x_use_seed": "Seed: ",
        "l_speed_ratio": "Speed ratio: ",
        "x_alt_reverse": "Use alternative reverse method",
        "x_reverse_order": "Reverse frame order",

        "l_force_duration": "Override duration: ",
        "l_force_for_pattern": "Override parameters (pattern): ",
        "l_force_for_ast": "Override parameters (AST): ",

        "f_envelope": " Customize envelope ",
        "x_env_attack": "Attack: ",
        "x_env_hold": "Hold: ",
        "x_env_decay": "Decay: ",
        "x_env_crossfade_endless": "Endless crossfade",

        "f_length": " Length settings ",
        "l_length_scale": "Length scale: ",
        "l_length_cutoff": "Hard length cutoff: ",

        "f_simplify": " Simplify ",
        "x_simplify_enable": "Enabled",
        "l_simplify_step": "Step size: ",
        "l_simplify_severity": "Severity: "
    },

    "tab_quantization": {
        "name": "Quantization",

        "f_quan": " Quantization ",
        "l_quan_mode": "Mode: ",
        "c_quan_mode": {
            "none": "None",
            "slices": "Slices",
            "bpm": "BPM"
        },
        "l_quan_bpm": "BPM: ",

        "f_quan_chances": " Chances + Direction ",
        "l_quan_pattern": "Start (Pattern): ",
        "l_quan_ast": "Start (AST): ",
        "l_quan_loop": "Start (Loop): ",
        "l_quan_skip": "Start (Loop - Skip): ",
        "l_quan_duration": "Segment duration: ",
        "l_quan_sustain": "Sustain portion: ",
        "l_quan_frame": "Frame begin/end: ",
        "l_quan_alt_slices": "Use alt. slices: ",

        "c_quan_directions": {
            "closest": "Closest",
            "back": "<-",
            "forw": "->",
            "auto": "Auto",
            "equal": "Equal"
        },

        "f_quan_alt": " Use alternative slices for: ",
        "x_quan_alt_pattern": "Start (Pattern)",
        "x_quan_alt_ast": "Start (AST)",
        "x_quan_alt_loop": "Start (Loop)",
        "x_quan_alt_skip": "Start (Loop - Skip)",
        "x_quan_alt_duration": "Segment duration",
        "x_quan_alt_portion": "Sustain portion",
        "x_quan_alt_frame": "Frame begin/end"
    },

    "tab_misc": {
        "name": "Miscellaneous",

        "f_shift": " Segment shifting ",
        "l_shift_deviation": "Deviation: ",
        "l_shift_chance": "Chance: ",
        "l_shift_dev_direction": "Direction: <- vs ->",
        "x_shift_dev_proportional": "Proportional to frame length (%)",

        "f_fade": " Fade cutoff ",
        "l_fade_in_cut_dist": "Fade-in: ",
        "l_fade_in_cut_chance": "Chance: ",
        "l_fade_out_cut_dist": "Fade-out: ",
        "l_fade_out_cut_chance": "Chance: ",

        "f_volume": " Volume change ",
        "l_volume_chance": "Chance: ",
        "l_volume_change": "V. change: ",
        "l_vol_direction": "Direction: ",
        "l_vol_direction_hint": "Softer vs louder (weight)",

        "f_mute": " Mute ",
        "l_mute_chance": "Mute chance: ",
        "l_mute_to_pause": "Resize muted segment\nto pause length (chance): ",

        "f_intro_loop": " Intro loop ",
        "l_intro_loop_length": "Intro length: ",
        "l_intro_loop_chance": "Loop chance: ",

        "f_quan_placement": " Placement quantization ",
        "c_quan_placement_mode": {
            "disabled": "Disabled",
            "by_fixed_step": "By fixed step",
            "to_onsets": "To onsets"
        },
        "l_quan_placement_step": "Step: ",
        "l_quan_placement_strength": "Strength: ",
        "b_quan_placement_edit_onsets": "Edit onsets"
    },

    "tab_tweaks": {
        "name": "Tweaks",

        "f_seg0_consec": " Segment 0 / Consec. chances ",
        "x_seg0_pause": "Is pause",
        "x_seg0_repeat": "Has repeats",
        "x_seg0_sustain": "Has sustain",
        "x_seg0_muted": "Is muted",

        "x_volume_pause_is_mute": "Pause = Muted segment",
        "l_repeat_consec_chance": "Consecutive repeat chance: ",
        "l_volume_mute_consec_chance": "Consecutive mute chance: ",

        "f_minor": " Minor tweaks ",
        "l_random_start_selection": "Random start selection: ",
        "l_reverse_double_mode": "Double reverse: ",
        "l_pause_apply_effects": "Apply effects to pause: ",
        "l_crossfade_comp_mode": "Crossfade compensation: ",
        "l_fade_in_plus_preroll": "Add crossfade to fade-in: ",
        "l_quan_duration_bpm_mode": "Duration BPM quantization: ",

        "c_no_yes": {
            "no": "No",
            "yes": "Yes"
        },
        "c_random_start_selection": {
            "prior_length": "Prioritize length",
            "prior_start": "Prioritize start"
        },
        "c_reverse_double_mode": {
            "allowed": "Allowed",
            "rev1": "Only reverse-1",
            "rev2": "Only reverse-2"
        },
        "c_crossfade_comp_mode": {
            "shorten": "Shorten",
            "cutoff": "Cut off"
        },
        "c_quan_duration_bpm_mode": {
            "by_end": "By end position",
            "by_length": "By length"
        },

        "f_trim": " Trim source audio ",
        "x_trim_from": "From: ",
        "x_trim_to": "To: ",
        "x_trim_slices": "Shift slice points",
        "x_trim_slices2": "Shift alt. slices",
        "x_trim_loop_start": "Shift loop start",
        "x_trim_avgstart": "Shift AST",

        "f_abpl": " ABPL script ",
        "x_abpl_enabled": "Enabled",
        "b_abpl_edit": "Edit ABPL script",
        "x_abpl_highlight": "Highlight keywords"
    },

    "slice_detection": {
        "methods": {
            "default": "Default",
            "amp_ste": "Amplitude - STE",
            "amp_rms": "Amplitude - RMS",
            "classic": "Classic"
        },

        "slice_types": {
            "slices": "Slices",
            "alt_slices": "Alternative slices"
        },

        "f_slice_detection": " Slice detection ",
        "l_method": "Method: ",
        "l_sens": "Sensitivity: ",

        "b_gen_current": "Generate from current audio",
        "b_gen_other": "Generate from other file",
        "b_get_statistics": "Get statistics",

        "b_file_load": "Apply slices from file",
        "b_file_save": "Save slices to file",
        "b_file_edit": "Manually edit slices",
        "b_file_erase": "Erase slices",

        "msg_onsets_title": "Slices",
        "msg_onsets_detected": "{N_ONS} onsets detected for {SLC_TYPE}.",
        "slice_stats": {
            "total": "Total: {N} slices",
            "mean": "Mean: {L} (RED)",
            "median": "Median: {L} (GREEN)",
            "mode": "Mode: {L} (BLUE)",
            "shortest": "Shortest slice: {L}",
            "longest": "Longest slice: {L}"
        }
    },

    "export_dialog": {
        "title": "Export",
        "l_export_fname": "File name: ",
        "l_export_folder": "Folder: ",
        "l_export_format": "Format: ",
        "l_export_length": "Exported audio length: ",
        "x_export_partial": "Partial generation: ",

        "err_wrong_format": "Wrong audio format!",
        "err_folder_not_exist": "The folder does not exist!",
        "err_overwrite": "The file '{FNAME}' already exists.\nDo you want to overwrite it?"
    },

    "edit_onsets": {
        "m_import": "Import",
        "m_import_slices": "Current slices",
        "m_import_alt_slices": "Current alternative slices",
        "m_import_midi": "External MIDI file",

        "m_tools": "Tools",
        "m_tools_shift": "Shift",
        "l_shift": "Shift by:",
        "m_tools_resample": "Resample",
        "m_tools_override_sr": "Override sample rate",
        "l_new_sample_rate": "New sample rate:",
        "m_tools_divide_long": "Divide long slices",
        "l_division_threshold": "Division threshold (in milliseconds):",
        "m_tools_merge_short": "Merge short slices",
        "l_merge_threshold": "Merge threshold (in milliseconds):",
        "m_tools_random": "Generate random onsets",
        "l_random_length": "Slice length (in milliseconds):",

        "title": "Edit onsets",
        "l_sample_rate": "Sample rate: ",
        "b_apply": "Apply",
        "b_export": "Export",
        "b_sort": "Sort",
        "b_clear": "Clear"
    },

    "audio_information": {
        "title": "Audio information",

        "path": "Path: ",
        "sample_rate": "Sample rate: ",
        "sample_format": "Sample format: ",
        "channels": "Channels: ",
        "ch_mono": " (Mono)",
        "ch_stereo": " (Stereo)",
        "length_sec": "Length: ",
        "length_samp": "Length (in samples): "
    },

    "tooltips": {
        "common": {
            "rand_dist": "A random number is generated based on the given parameters.\n\nAvailable modes include:\n- Uniform: All numbers within the specified range have an equal probability of being selected.\n- Gaussian: Parameters are the mean (average) and standard deviation. This follows the 68-95-99.7 rule.\n- Clipped Gauss: Limits the Gaussian distribution to values within one standard deviation of the mean.\n- Lognormal: Parameters are the mu and sigma of the lognormal distribution.\n- Exponential: Takes a single parameter, 1/lambda of the exponential distribution.",
            "rand_dist_lognorm": "\n\nNote: Lognormal mode does not support seconds, so lengths are always returned in milliseconds.",
            "chance": "Chance for this effect to occur.",
            "space_sep": "Enter them separated by spaces, without commas or other separators."
        },

        "basic": {
            "duration": "Length of the segment body.",
            "reverse1": "Chance that the segment will be reversed.\nReversal is applied before sustain and fades.",
            "reverse2": "Chance that the segment will be reversed.\nReversal is applied after sustain and fades.",
            "pause": "Length of gap between segments.",
            "pause_consec_chance": "Allows pauses to occur one after another with a certain chance.",
            "crossfade": "Length of fades between segments.",

            "fade_in": "The volume increases linearly at the beginning of the segment over the specified time interval.",
            "fade_out": "The volume decreases linearly at the end of the segment over the specified time interval.",
            "fade_prop": "Change fade length to be measured as a percentage of the segment body length.",
            "fade_only_into_pauses": "Chance to disable the fade if it doesn't follow a gap (for fade-in),\nor isn't followed by a gap (for fade-out).",
            "fade_out_from_slice": "Instead of measuring the length as a percentage of the segment (default),\nmeasure the fade-out length as a percentage of the last slice.",

            "repeat": "The segment body is repeated the specified number of times.\nThe value is rounded to the nearest whole number.",
            "repeat_mss": "Measure the number of repeats by duration (in milliseconds or seconds), instead of a fixed count.",
            "reappear": "The number of segments after which the segment will repeat.\nThe value is rounded to the nearest whole number.",
            "reappear_reoccur": "Chance that the segment can reappear again after it has reappeared once."
        },

        "basic_speed": {
            "main_speed": "The base speed at which the segment plays.\nAffects both tempo and pitch.",
            "speed_unit": "The speed's unit of measurement.",
            "speed_alt_chance": "Chance to use a different speed from the list below.",
            "speed_alt_list": "All of the alternative speeds. {SPACE_SEP}\n\nA speed range filler is also supported here.\nSyntax is: RANGE [A B STEP], where A is the first speed and B is the last speed.\nThe range can be either ascending or descending, which is determined automatically.\nSTEP is optional and specifies the step between speeds; the default is 1.\nBoth A and B are always included in the range, even if the step would normally skip them.\nOther speed variants can be listed before and after the range.",
            "speed_alt_weight": "The priority that each speed has over the rest. Leave this field empty for an even distribution.\nFor a speed range, specify a weight for each element.",
            "speed_scale": "Adjust segment lengths based on their speed.\n\nFor example, the main speed is 2x and the current speed is 3x.\nBy default, speed does not affect the final length.\nIn 'relative to main speed' mode, the segment will be 1.5 times shorter.\nIn 'relative to original speed' mode, it will be 3 times shorter."
        },

        "sustain": {
            "sustain_chance": "Chance to sustain a segment by looping its ending forward and backward.",
            "sustain_weight": "Priorities for different sets of sustain parameters.",
            "sus_cross": "Crossfade between sustain grains.",
            "sus_length": "Sustain length.",
            "sus_len_mode": "The mode that will be used to measure the sustain's length.",
            "sus_len_exact": "Use the exact length specified, trimming the last grain if necessary.\nOtherwise, the length will be rounded up.",
            "sus_portion": "The duration of a single grain.",
            "sus_portion_p": "Measure grain length as a percentage of the segment length.\nOtherwise, the length is measured in absolute units (ms/sec).",
            "sus_portion_min": "If a grain is shorter than this value, the sustain is reduced to a single grain.\nUse this to avoid ringing artefacts at the end of the segment.",
            "sus_quantize": "Enable grain length quantization (see more options on the Quantization tab).",
            "sus_shift": "Change to shift the end of the segment.\nFor example, if your segment is 3s long and the grain is 1s, the main body of the segment is reduced to 2s.",
            "sus_reverse": "Additional chance to reverse the segment.\nThis is equivalent to the first reverse; together, this and first reverse cancel each other out.",
            "sus_consec": "Chance for two consecutive segments to possibly have sustain."
        },

        "pattern": {
            "loop_pat": "Chance for the segment to have a random start point.\nOtherwise, it will start roughly where the previous segment ended.\nSuch a segment is called an 'in-loop segment'.",
            "loop_rep": "Chance that the segment will use the same start time and length as the previous segment.\nThis only applies when both segments are in loop.",
            "loop_full": "Consider the segments end point as the moment it actually finishes in the original audio, including repeats and sustain.\nOtherwise, the end point is taken as the end of the segments body.",
            "loop_pause": "Chance to consider gap length when calculating the segment's start time.",
            "loop_count_pat": "Chance to consider the length of a pattern segment (but not its start) when calculating the in-loop segment's start time.",
            "loop_can_break": "Chance that the next in-loop segment's start position\nwill be set to the end of {SEGMENT}.",
            "loop_break_skip_repl": "the segment that skips",
            "loop_break_skip_add": " (See 'skip' for more info).",
            "loop_break_pattern_repl": "the pattern segment",
            "loop_break_ast_repl": "AST segment",
            "loop_break_ast_add": " (See 'average start times' for more info).",
            "loop_begin": "The timestamp in the audio where the loop starts."
        },

        "pattern_skip": {
            "skip": "General skip chance,\ni.e., the probability of shifting the start position of an in-loop segment by a certain distance.\nUsually, skipping does not affect the start position of the next in-loop segment,\nunless explicitly stated otherwise (see 'skipping can break loop').",
            "skip_weight": "The weight of this skip direction variant.",
            "skip_min": "A fixed amount to shift the segment's start position by.",
            "skip_add": "An additional random shift applied to the segment's start position.\nThis value is drawn from a clipped Gaussian distribution."
        },

        "pattern_ast": {
            "ast_main": "Chance for a segment to use one of the 'average start times' (abbr. AST) instead of its default start time.\nAverage start times are custom timestamps that are more likely to be chosen as a segment's start than others.",
            "ast_list": "The list of all the ASTs. {SPACE_SEP}",
            "ast_weights": "The priority each AST has over the rest. Leave this field empty for an even distribution.",
            "ast_dev": "Shift the AST by a small random amount. The shifting amount is drawn from a clipped Gaussian distribution.",
            "ast_dir": "Weights for forward and backward shifts.",
            "ast_force": "ASTs can only be applied to pattern segments. \nThis parameter gives a certain chance to force a segment to become a pattern segment when AST is selected."
        },

        "framing": {
            "framing_main": "Enables the 'framing' mode, which overhauls certain parameters.\nThe main feature of this mode is that the audio is divided into consecutive 'frames' of a fixed length before scrambling starts. \nDuring scrambling, the frames are also processed sequentially, and segment lengths are adjusted to fit the frame by trimming.\nFor in-loop segments, their start time is also adjusted to align with the frame.",
            "frame_dur": "The lengths that frames can range between.",
            "frame_seed": "Optionally, you can use a separate seed for frame length generation.\nThis is useful for when you want to preserve the same set of frames across multiple sessions.",
            "frame_ratio": "Ratio of the frame length in the original audio to the frame length in the scrambled audio.\nFor example, a ratio of 2 halves the frame length, making the final loop twice as short.",
            "frame_ratio_formula": "This field allows not only regular numbers, but also formulas.\nAllowed symbols include: +, -, *, /, (, ).\n\nAdditionally, the following variable keywords can be used:\n[LENGTH] - The original audio file's length (in seconds);\n[LENGTH_SAMP] - The original audio file's length (in samples);\n[SAMPLE_RATE] - The original audio file's sample rate.",
            "frame_alt_rev": "Use an alternative method for trimming reversed segment (second reverse).",
            "frame_force_dur": "Chance to override the segment body's length with the frame's length.",
            "frame_force_pat": "Chance to override the start time and (optionally) the duration of a pattern segment.\nA random frame is selected from all available frames for this.",
            "frame_force_ast": "Chance to override the start time and (optionally) the duration of a AST segment.\nA frame with the start time closest to the current AST is selected for this.",

            "fr_env_attack": "Custom attack duration. If disabled, it defaults to the crossfade length.",
            "fr_env_hold": "Hold duration. If disabled, the entire segment portion not covered by attack and decay will be held.",
            "fr_env_decay": "Decay duration. If disabled, it defaults to 0.\nKEEP IN MIND: Decay has nothing to do with crossfade!",
            "fr_env_crossfade": "Crossfade is a short fading tail of the segment that extends beyond the frame.\nThis option completely disables trimming and fading,\nso the segment plays in full, overlapping with the next one.",

            "fr_length_soft": "Multiply the generated segment's length by the specified percentage.\nThis value can be either less than 100 or greater.",
            "fr_length_hard": "Within the frame, keep only a portion of the segment.\nThe frame length itself remains unchanged.\nThis parameter cannot exceed 100%.",
            "fr_simplify": "Enables simplify.\nThis option splits the audio into equal-length fragments\nand keeps only a part of the frames from each fragment.",
            "fr_simp_step": "The length of a single fragment.",
            "fr_simp_sever": "Specifies which portion of the fragment to keep.\nFor example, with a value of 50%, only frames whose start point lies within the first half of the fragment will be kept."
        },

        "quantization": {
            "quan_mode": "Quantization allows snapping various timestamps to specific points in the original audio.\n\nBy default, quantization is disabled.\nIn Slices mode, timestamps are snapped to onsets, which must be preloaded.\nIn BPM mode, timestamps are quantized to the start of beats.",
            "quan_bpm": "The audio's tempo (in BPM).",
            "quan_chance": "Chance that quantization will be applied to this parameter.",
            "quan_direction": "Determines the direction in which the timestamp will be rounded.",
            "quan_spec_eq": "\nIn the special Equal mode, the segment start will be chosen as a random onset.",
            "quan_spec_auto": "\nIn the special Auto mode, the rounding direction is chosen according to the direction of the deviation.",
            "quan_note_dur": "\nNote that since the segment start and end times cannot coincide,\nthe segment length may be rounded up even if the opposite was specified.",
            "quan_note_sus": "\nNote that for this, quantization must be enabled in the sustain settings.",
            "quan_alt": "Chance to use an alternative set of onsets.\nThis works only in Slices mode, when alternative slices are loaded.\nYou can also specify which parameters the alternative quantization should be applied to."
        },

        "misc": {
            "shift": "Shift the segment's starting point in the scrambled audio by a specified distance.",
            "shift_dir": "Shift direction weights: forward vs backward.",
            "shift_p": "Use a portion (in percent) of the current segment's length as the shift distance.\nOtherwise, an absolute value (in ms/sec) is used.",

            "fade_cut_clip": "\nThis parameter is measured as a percentage of volume (0-100; values above 100 are clipped to 100).",
            "fade_in_cut": "Instead of fading in from complete silence, fade from a different volume level.",
            "fade_out_cut": "Instead of fading out to complete silence, fade to a different volume level.",

            "vol_change": "Change the segment volume by a specified value.\nValues from the distribution are limited to the range 0-100,\nso the final volume can range from 0 to 200%.",
            "vol_direction": "Weight for the direction of volume change: softer (0-100%) or louder (100-200%).",
            "vol_mute": "Chance to mute the segment (sets its volume to 0%).",
            "vol_mute_resize": "Chance that if the segment is muted, its length will be changed to match pause durations.",

            "intro_loop": "Keep only the intro of the segment with the specified length,\nthen repeat it several times to fill the entire original length.\nSetting this value to 0 disables the feature.",

            "pq_main": "Place segments only at specific points in the scrambled audio.\nYou can quantize placement to evenly spaced points or to a custom onset map.",
            "pq_step": "Distance between two evenly spaced points.\n\nYou can also use negative values;\nin that case, the audio is split into the number of parts you specify.",
            "pq_strength": "Quantization strength.\nAt 0%, it does nothing.\nAt 100%, it places the segment exactly on the onset point.\nFor values in between, the segment is positioned somewhere between its original location and the onset.",
            "pq_edit": "Modify the custom onset map.\nThis set of onsets is completely independent from the onsets used in 'regular' quantization."
        },

        "tweaks": {
            "s0_pause": "For the first segment, assume that a pause preceded it.",
            "s0_repeat": "For the first segment, assume that the preceding segment contained repeats.",
            "s0_sustain": "For the first segment, assume that the preceding segment had sustain.",
            "s0_mute": "For the first segment, assume that the preceding segment was muted.",

            "pause_is_mute": "Count muted segments as pauses when calculating the chance of a consecutive pause.",
            "consec_repeat": "Chance that a segment may have repeats if the preceding segment already had them.",
            "consec_mute": "Chance that a segment may be muted if the preceding segment was muted.",
            "abpl": "Modify the ABPL script, which allows creating complex dependencies between different effects.\nThe ABPL guide is available on the AudioButcher GitHub."
        }
    }
}
