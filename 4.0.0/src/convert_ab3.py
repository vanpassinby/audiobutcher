import math
from ab_tools import *
from typing import Any
from preset import PresetOpen


def quick_recv(preset):
    def recv(option_name: str, fallback: Any=0, action: Any=str, act_fb: Any=0):
        option = preset.get(option_name, str(fallback))
        try:
            return action(option)
        except:
            return act_fb
    return recv


def old_rdist(string):
    items = string.split() + ["?", "?", "?"]
    method = {0:0, 1:1, 2:3, 3:4}.get(int1(items[2]))
    return f"{method} {items[0]} {items[1]}"


def old_rdist_plus_one(string):
    items = old_rdist(string).split()
    method = int1(items[0])
    v1 = items[1]
    v2 = items[2]

    if method == 0:
        v1 = float1(v1) + 1
        v2 = float1(v2) + 1
    if method in (1, 2):
        v1 = float1(v1) + 1
    if method == 3:
        v1 = math.log(math.exp(float1(v1))+1)

    return f"{method} {v1} {v2}"

def minus_one_is_zero(string):
    if int1(string) == -1:
        return "0"
    return string


def opposite_chance(string):
    return 100 - float1(string)


def ab3_locked_mode(string):
    if int1(string) == 1:
        return 0
    else:
        return 100


def ab3_pattern_quan(string):
    idx = int1(string) - 1

    if idx < 0:
        return 3
    else:
        return idx


def convert_ab3(preset_ab3):
    qr = quick_recv(preset_ab3)

    # Pre-calculate sustain weights
    bm_chance = float1(qr("backmaskChance")) / 100
    ne_chance = qr("extnoteChance", 0, float1) * qr("fadeOutChance", 0, float1) / (100 ** 2)
    as_chance = qr("backmaskAsymChance", 0, float1) / 100
    bm_rep_in_mss = float1(qr("bmaskRepeatInMss")) == 1

    if bool(qr("extnotePriority", 0, int1)):
        bm_chance *= (1 - ne_chance)
    else:
        ne_chance *= (1 - bm_chance)

    bm_repeat_chance = qr("bmaskRepeatChance", 0, float1) / 100
    bm_chance_single = bm_chance * (1 - bm_repeat_chance) * (1-as_chance)
    bm_chance_single_a = bm_chance * (1 - bm_repeat_chance) * as_chance
    bm_chance_multi = bm_chance * bm_repeat_chance * (1-as_chance)
    bm_chance_multi_a = bm_chance * bm_repeat_chance * as_chance

    max_chance = max(bm_chance_single, bm_chance_single_a, bm_chance_multi, bm_chance_multi_a, ne_chance)
    if max_chance != 0:
        str_w1 = bm_chance_single / max_chance * 1000
        str_w2 = bm_chance_single_a / max_chance * 1000
        str_w3 = bm_chance_multi / max_chance * 1000
        str_w4 = bm_chance_multi_a / max_chance * 1000
        str_w5 = ne_chance / max_chance * 1000
    else:
        str_w1, str_w2, str_w3, str_w4, str_w5 = 0, 0, 0, 0, 0

    # Convert
    preset_text = f"""[AudioButcher]
version = 4.0.0
conv2sec = {qr("convert2sec")}
use_seed = {qr("fromseed")}
seed = {qr("seed", "")}

; Main tab
duration_dist = {qr("seg", "0 0 0", old_rdist)}
reverse1_chance = {qr("segReverseChance1")}
reverse2_chance = {qr("segReverseChance2")}

pause_dist = {qr("pause", "0 0 0", old_rdist)}
pause_chance = {qr("pauseChance")}
pause_consec_chance = {qr("consPauseChance")}

crossfade = {qr("crossFd", "0 0 0", old_rdist)}
crossfade_chance = {qr("crossFdChance", 100)}

fade_in_dist = {qr("fadeIn", "0 0 0", old_rdist)}
fade_in_perc = {qr("fadeInPerc")}
fade_in_chance = {qr("fadeInChance", 100)}

fade_out_dist = {qr("fadeOut", "0 0 0", old_rdist)}
fade_out_perc = {qr("fadeOutPerc")}
fade_out_chance = {qr("fadeOutChance", 100)}

fade_only_into_pauses = {qr("fadeOnlyIntoPauses")}
fade_out_perc_note = {qr("fadeOutPercNote")}

repeat_dist = {qr("repeat", "0 0 0", old_rdist)}
repeat_chance = {qr("repeatChance")}
repeat_in_mss = {qr("repeatInMss")}

reappear_after_dist = {qr("rememb", "0 0 0", old_rdist)}
reappear_chance = {qr("remembChance")}
reappear_reoccur_chance = 0

; Speed change
speed_main = 0
speed_measure = {qr("speedm")}
speed_alter_chance = 100
speed_variations = {qr("speeds")}
speed_weights = {qr("speedw", "")}
speed_affect_mode = 0

; Sustain
sustain_chance = {(bm_chance+ne_chance)*100}
sustain_weights = {str_w1:.0f} {str_w2:.0f} {str_w3:.0f} {str_w4:.0f} {str_w5:.0f}

; Sustain V1 - Single back mask
sustain1_crossfade = {qr("backmaskCrossfd", 0, minus_one_is_zero)}
sustain1_length = 0 1 1
sustain1_length_mode = 1
sustain1_length_exact = 0
sustain1_portion_length = 0 100 100
sustain1_portion_proportional = 1
sustain1_portion_minimum = 0
sustain1_shift_chance = {qr("backmaskFullChance", 0, opposite_chance)}
sustain1_reverse_chance = {qr("backmaskRevChance")}
sustain1_consec_chance = {qr("consecBmaskChance", 100)}

; Sustain V2 - Single back mask + A
sustain2_crossfade = {qr("backmaskCrossfd", 0, minus_one_is_zero)}
sustain2_length = 0 1 1
sustain2_length_mode = 1
sustain2_length_exact = 0
sustain2_portion_length = {qr("backmaskAsymPortion", "0 100 0", old_rdist)}
sustain2_portion_proportional = 1
sustain2_portion_minimum = 0
sustain2_shift_chance = {qr("backmaskFullChance", 0, opposite_chance)}
sustain2_reverse_chance = {qr("backmaskRevChance")}
sustain2_consec_chance = {qr("consecBmaskChance", 100)}

; Sustain V3 - Repeated back mask
sustain3_crossfade = {qr("backmaskCrossfd", 0, minus_one_is_zero)}
sustain3_length = {qr("bmaskRepeatNum", "0 0 0", old_rdist if bm_rep_in_mss else old_rdist_plus_one)}
sustain3_length_mode = {0 if bm_rep_in_mss else 1}
sustain3_length_exact = 0
sustain3_portion_length = 0 100 100
sustain3_portion_proportional = 1
sustain3_portion_minimum = 0
sustain3_shift_chance = {qr("backmaskFullChance", 0, opposite_chance)}
sustain3_reverse_chance = {qr("backmaskRevChance")}
sustain3_consec_chance = {qr("consecBmaskChance", 100)}

; Sustain V4 - Repeated back mask + A
sustain4_crossfade = {qr("backmaskCrossfd", 0, minus_one_is_zero)}
sustain4_length = {qr("bmaskRepeatNum", "0 0 0", old_rdist if bm_rep_in_mss else old_rdist_plus_one)}
sustain4_length_mode = {0 if bm_rep_in_mss else 1}
sustain4_length_exact = 0
sustain4_portion_length = {qr("backmaskAsymPortion", "0 100 0", old_rdist)}
sustain4_portion_proportional = 1
sustain4_portion_minimum = 0
sustain4_shift_chance = {qr("backmaskFullChance", 0, opposite_chance)}
sustain4_reverse_chance = {qr("backmaskRevChance")}
sustain4_consec_chance = {qr("consecBmaskChance", 100)}

; Sustain V5 - Note extension
sustain5_crossfade = {qr("extnoteCrossfd", 0, minus_one_is_zero)}
sustain5_length = 0 100 100
sustain5_length_mode = 4
sustain5_length_exact = 1
sustain5_portion_length = 0 250 250
sustain5_portion_proportional = 0
sustain5_portion_minimum = {qr("extnoteMinNoteLen")}
sustain5_shift_chance = 0
sustain5_reverse_chance = 0
sustain5_consec_chance = 100

; Loop
loop_begin = {qr("stumbBegin")}
loop_pattern_chance = {qr("stumbleChance", 0, opposite_chance)}
loop_repeat_chance = 0
loop_count_full_length = 100
loop_count_pause_length = {qr("stumbleCountPauses")}
loop_count_pattern_length = {qr("stumbleOnlyStumbled", 100)}
loop_break_skips = {qr("stumbleLockedMode", 0, ab3_locked_mode)}
loop_break_pattern = {qr("stumbleOnlyStumbled", 100, opposite_chance) * qr("stumbleLockedMode", 0, ab3_locked_mode) / 100}
loop_break_avgstart = {qr("stumbleOnlyStumbled", 100, opposite_chance) * qr("stumbleLockedMode", 0, ab3_locked_mode) / 100}
skip_chance = {qr("skipChance", 100)}

; Skipping
skip_forw_weight = {qr("skipForwWeight")}
skip_forw_min_skip = {qr("skipForwMin")}
skip_forw_min_skip_chance = {qr("skipForwMinChance", 100)}
skip_forw_add_dev = {qr("skipForwAddDev")}
skip_forw_add_dev_chance = {qr("skipForwAddDevChance", 100)}

skip_back_weight = {qr("skipBackWeight")}
skip_back_min_skip = {qr("skipBackMin")}
skip_back_min_skip_chance = {qr("skipBackMinChance", 100)}
skip_back_add_dev = {qr("skipBackAddDev")}
skip_back_add_dev_chance = {qr("skipBackAddDevChance", 100)}

skip_rand_weight = {qr("skipRandWeight")}
skip_rand_min_skip = {qr("skipRandMin")}
skip_rand_min_skip_chance = {qr("skipRandMinChance", 100)}
skip_rand_add_dev = {qr("skipRandAddDev")}
skip_rand_add_dev_chance = {qr("skipRandAddDevChance", 100)}

; Average start times
avgstart_chance = {qr("avgstrtChance")}
avgstart_times = {qr("avgstrtTimes")}
avgstart_weights = {qr("avgstrtWeights", "")}
avgstart_deviation = {qr("avgstrtDev")}
avgstart_dev_chance = 100
avgstart_dev_direction = 1 1
avgstart_force_pattern = {qr("stumbleIgnoreAvgSt", 0, opposite_chance)}

; Looping -> Framing (kinda)
framing = {qr("looping")}
framing_frame_size = {qr("seg", "0 0 0", old_rdist)}
framing_speed_ratio = 1/1

; Quantization
quan_mode = {qr("quanMode")}
quan_bpm = {qr("quanBPM", "120.000")}
quan_pattern = {qr("quanBegin", 100)}
quan_pattern_dir = {qr("quanBeginDir", 0, ab3_pattern_quan)}
quan_ast = {qr("quanAvgStart", 100)}
quan_ast_dir = {qr("quanAvgStartDir", 3)}
quan_loop = {qr("quanStumbBegin", 100)}
quan_loop_dir = {qr("quanStumbBeginDir", 0)}
quan_skip = {qr("quanStumbleSkip", 100)}
quan_skip_dir = {qr("quanStumbleSkipDir", 3)}
quan_duration = {qr("quanDuration", 100)}
quan_duration_dir = {qr("quanDurationDir", 2)}
quan_alt_slices = {qr("quanUseStOnsets", 100)}
quan_alt_pattern = 1

; Fade cutoff
fade_in_cut_dist = {qr("fadeInCut", "0 0 0", old_rdist)}
fade_in_cut_chance = {qr("fadeInCutChance", 100)}
fade_out_cut_dist = {qr("fadeOutCut", "0 0 0", old_rdist)}
fade_out_cut_chance = {qr("fadeOutCutChance", 100)}

; Mute
volume_mute_chance = {qr("muteChance")}
volume_mute_to_pause = {qr("muteToPauseChance")}

; Trim
trim1 = {qr("trimVal1")}
trim1_x = {qr("trim")}
trim2 = {qr("trimVal2")}
trim2_x = {qr("trim")}
trim_slices = {qr("trimShiftOns", 1)}
trim_slices2 = {qr("trimShiftOns", 1)}
trim_loop_start = 0
trim_avgstart = 0

; Segment 0
seg0_pause = {qr("consecPauseFirst")}
seg0_repeat = {qr("consecRepeatFirst")}
seg0_sustain = {qr("consecBmaskFirst")}
seg0_muted = {qr("consecMutedFirst")}
volume_pause_is_mute = {qr("muteCountPauses")}
repeat_consec_chance = {qr("consecRepeatChance", 100)}
volume_mute_consec_chance = {qr("consecMutedChance", 100)}

; Misc
reverse_double_mode = 0
pause_apply_effects = 0
crossfade_comp_mode = 0
fade_in_plus_preroll = 0
quan_duration_bpm_mode = 0
"""

    return PresetOpen(data=preset_text)
