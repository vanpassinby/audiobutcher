from abpl.core import ScriptState
from abpl.abpl_main import execute as exec_abpl

from ab_tools import *
from scrambler.scr_tools import *
from scrambler.scr_state import *
from scrambler.rand_seg_sp import random_start_pos


def random_volume(state: ScramblerState, segment: SegmentInfo):
    config = state.config

    can_mute = (not state.last_mut) or config.volume_mute_consec_chance.get()
    if can_mute and config.volume_mute_chance.get():
        segment.volume = 0
        return

    if config.volume_alt_chance.get():
        volume = clip_number(config.volume_change.get(), 0, 100)
        segment.volume = 100 + volume * config.volume_direction.get()

    else:
        segment.volume = 100


def random_fades(state: ScramblerState, segment: SegmentInfo):
    qc = state.audio.length_ms_to_samp
    config = state.config

    # Generate initial values
    fadein_flt = rand_by_chance(config.fade_in_chance, config.fade_in_dist)
    fadeout_flt = rand_by_chance(config.fade_out_chance, config.fade_out_dist)
    segment.fadein_cut = rand_by_chance(config.fade_in_cut_chance, config.fade_in_cut_dist)
    segment.fadeout_cut = rand_by_chance(config.fade_out_cut_chance, config.fade_out_cut_dist)

    # Actual lengths
    if config.fade_in_perc:
        segment.fadein = int(fadein_flt * segment.duration / 100)
    else:
        segment.fadein = qc(fadein_flt * segment.k_speed)
    if config.fade_out_perc:
        if config.fade_out_perc_note and state.slices is not None:
            slice_len = find_last_slice(state, segment)
            segment.fadeout = int(fadeout_flt * slice_len / 100)
        else:
            segment.fadeout = int(fadeout_flt * segment.duration / 100)
    else:
        segment.fadeout = qc(fadeout_flt * segment.k_speed)

    # Fade only into pauses
    if config.fade_only_into_pauses.get():
        fadein_bool = state.pause_prev
        fadeout_bool = state.pause_next
        if segment.reverse2:
            fadein_bool, fadeout_bool = fadeout_bool, fadein_bool
        segment.fadein *= fadein_bool
        segment.fadeout *= fadeout_bool


def random_sustain(state: ScramblerState, segment: SegmentInfo):
    qc = state.audio.length_ms_to_samp
    config = state.config
    subconfig_id = state.config.sustain_weights.get()
    subconfig = state.config.sustain_variants[subconfig_id]

    # Consec. checking
    if state.last_sus and not subconfig.consec_chance.get():
        segment.sustain = 0
        return

    # Some simple parameters
    segment.sustain_shift = subconfig.shift_chance.get()
    segment.sustain_exact = subconfig.length_exact
    segment.reverse1 = segment.reverse1 ^ subconfig.reverse_chance.get()

    # Sustain portion
    sustain_portion_flt = subconfig.portion_length.get()
    if subconfig.portion_proportional:
        segment.sustain_portion = round(sustain_portion_flt * segment.duration / 100)
    else:
        segment.sustain_portion = qc(sustain_portion_flt * segment.k_speed)

    # Compensate portion
    base_length = segment.duration
    if segment.sustain_shift:
        base_length //= 2
    segment.sustain_portion = min(segment.sustain_portion, base_length)
    segment.sustain_portion = max(0, segment.sustain_portion)

    # Quantization
    if config.quan_mode != 0 and subconfig.allow_quan and config.quan_sustain.get():
        quan_sustain(state, segment)

    # Crossfade
    segment.sustain_c = max(0, qc(subconfig.crossfade * segment.k_speed))
    fix_sustain_cross(state, segment)

    # Sustain length (finally)
    sustain_flt = subconfig.length.get()
    if subconfig.length_mode == 0:
        segment.sustain = qc(sustain_flt * segment.k_speed)
    elif subconfig.length_mode == 1:
        segment.sustain = round(sustain_flt) * (segment.sustain_portion - segment.sustain_c) + segment.sustain_c
    else:
        coefficients = [segment.sustain_portion, segment.duration, segment.fadeout]
        segment.sustain = int(sustain_flt * coefficients[subconfig.length_mode - 2] / 100)

    # Remove sustain if it's too short
    if segment.sustain > 0:
        if qc(subconfig.portion_minimum) > segment.sustain_portion or segment.sustain_portion == 0:
            segment.sustain = segment.sustain_portion


def random_shift(state: ScramblerState, frame_length: int):
    config = state.config
    qc = state.audio.length_ms_to_samp

    if config.shift_chance.get():
        deviation = config.shift_deviation.get()
        direction = config.shift_dev_direction.get()

        if config.shift_dev_proportional:
            return round(frame_length * deviation / 100) * direction
        else:
            return qc(deviation) * direction

    else:
        return 0


def gen_random_segment(state: ScramblerState) -> SegmentInfo:
    qc = state.audio.length_ms_to_samp
    config = state.config

    # Reappear?
    if not state.pause_curr:
        state.memory.move_on()
        remembered = state.memory.get_segment()

        if remembered:
            remembered.is_in_loop = False
            remembered.from_mem = True
            # WARNING: Next two lines were copy-pasted from another part of this function
            remembered.crossfade = min(int(state.crossfade * remembered.k_speed), remembered.duration // 2)
            remembered.preroll_fadein = config.fade_in_plus_preroll and not config.framing
            return remembered

    # Base
    segment = SegmentInfo()
    segment.speed = rand_by_chance(config.speed_alter_chance, config.speed_variations, config.speed_main)
    segment.k_speed = get_k_speed(config, segment)
    segment.reverse1 = config.reverse1_chance.get()
    segment.reverse2 = config.reverse2_chance.get()
    if segment.reverse1 and segment.reverse2:
        if config.reverse_double_mode == 1:
            segment.reverse2 = False
        if config.reverse_double_mode == 2:
            segment.reverse1 = False

    # Duration & Volume
    random_volume(state, segment)
    if state.pause_curr or (segment.volume == 0 and config.volume_mute_to_pause.get()):
        segment.is_pause = state.pause_curr
        segment.duration = qc(config.pause_dist.get() * segment.k_speed)
        segment.volume = 0
    else:
        segment.duration = qc(config.duration_dist.get() * segment.k_speed)

    # Start position
    random_start_pos(state, segment)

    # Segment duration (Quantize)
    if segment.duration < 0:  # Segments whose length should not be quantized have it negative
        segment.duration = -segment.duration
    elif config.quan_mode in (1, 2) and config.quan_duration.get():
        quantize_length(state, segment)

    # Check segment duration
    fix_length(state, segment)

    # Fades
    random_fades(state, segment)

    # Repeats
    if (not state.last_rep) or config.repeat_consec_chance.get():
        repeats_flt = rand_by_chance(config.repeat_chance, config.repeat_dist)
        if config.repeat_in_mss:
            repeats_flt = qc(repeats_flt) * segment.k_speed / segment.duration
        segment.repeats = round(repeats_flt)
    else:
        segment.repeats = 0

    # Intro loop
    if config.intro_loop_chance.get():
        segment.intro_loop = qc(config.intro_loop_length * segment.k_speed)
    else:
        segment.intro_loop = 0

    # Sustain
    if config.sustain_chance.get():
        random_sustain(state, segment)
    else:
        segment.sustain = 0

    # Misc
    segment.crossfade = min(int(state.crossfade * segment.k_speed), segment.duration//2)
    segment.preroll_fadein = config.fade_in_plus_preroll and not config.framing
    if config.abpl_enabled and len(config.abpl_script) == 2:
        script, tbl = config.abpl_script
        abpl_state = ScriptState(script, tbl, segment, state)
        exec_abpl(abpl_state)

    segment_fixup(state, segment)
    return segment
