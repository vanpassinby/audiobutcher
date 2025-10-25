import time
import numpy as np

import meta
from state import ABState
from slicing import convert_onsets, get_bpm_array

from scrambler.scr_tools import *
from scrambler.segment import SegmentInfo, precalculate_length, generate_segment_audio
from scrambler.scr_state import ScramblerState
from scrambler.rand_seg import gen_random_segment, random_shift


def add_crossfade(appender: Audio, state: ScramblerState, real_cross1: int):
    config = state.config
    cross1, c1_zero = cross_compensate(config.crossfade_comp_mode, state.crossfade, real_cross1)
    cross2, c2_zero = cross_compensate(config.crossfade_comp_mode, state.crossfade_next, appender.length - cross1)

    appender.fade_in(cross1, zero=c1_zero * 100)
    appender.fade_out(cross2, zero=c2_zero * 100)


def frame_envelope(appender: Audio, state: ScramblerState):
    config = state.config
    qc = state.audio.length_ms_to_samp
    total_length = 0

    attack_dur = qc(config.fr_env_attack_dist.get()) if config.fr_env_attack else state.last_segment_crossfade
    hold_dur = qc(config.fr_env_hold_dist.get()) if config.fr_env_hold else 0
    release_dur = qc(config.fr_env_decay_dist.get()) if config.fr_env_decay else 0

    # Step 1: Attack
    if attack_dur > appender.length:
        if config.crossfade_comp_mode == int(1):
            appender.volume(appender.length / attack_dur * 100)
        attack_dur = appender.length
    appender.fade_in(attack_dur)
    total_length += attack_dur

    # Step 2: Hold
    if total_length >= appender.length:
        return
    if config.fr_env_hold:
        total_length += hold_dur
    else:
        total_length = max(appender.length-release_dur, attack_dur)

    # Step 3: Decay
    appender.crop(0, total_length + release_dur)
    if config.fr_env_decay and total_length < appender.length:
        release_dur, zero = cross_compensate(config.crossfade_comp_mode, release_dur, appender.length - total_length)
        appender.fade_out(release_dur, zero*100)


def frame_cut(appender: Audio, state: ScramblerState, info: SegmentInfo, base_length: int, cross_length: int):
    config = state.config
    og_length = round(appender.length / info.k_speed)

    if config.fr_length_hard < 100:  # Not sure if this is 100% accurate
        base_length = round(base_length * config.fr_length_hard/100)

    if config.framing_alt_reverse and info.reverse2:
        frame_at_speed = round1(base_length * info.k_speed)
        appender.crop(-frame_at_speed, None)

    frame_envelope(appender, state)
    if config.fr_env_crossfade_endless:
        return

    if info.reverse2 and config.framing_alt_reverse:
        base_length = min(base_length, og_length)
    if appender.length > base_length + cross_length:
        frame_end = base_length + cross_length
        if info.reverse2 and not config.framing_alt_reverse:
            appender.crop(-frame_end, None)
        else:
            appender.crop(0, frame_end)

    real_cross2 = max(appender.length - base_length, 0)
    if real_cross2 > 0:
        cross2, c2_zero = cross_compensate(config.crossfade_comp_mode, state.crossfade, real_cross2)
        appender.fade_out(cross2, c2_zero*100)

    if config.crossfade_comp_mode == 0:  # Not sure if this is right
        state.crossfade = real_cross2


def calculate_loop_position(cont_length: int, segment: SegmentInfo, state: ScramblerState):
    config = state.config
    if state.loop_reset:
        state.loop_position = 0
        state.loop_reset = False
        return

    cont_by_begin = False
    cont_by_length = False

    if segment.is_pause:
        if config.loop_count_pause_length.get():
            cont_by_length = True

    elif segment.is_avgstart:
        if config.loop_break_avgstart.get():
            cont_by_begin = True
        elif config.loop_count_pattern_length.get():
            cont_by_length = True

    elif segment.is_in_loop:
        if config.loop_break_skips.get():
            cont_by_begin = True
        else:
            cont_by_length = True

    else:
        if config.loop_break_pattern.get():
            cont_by_begin = True
        elif config.loop_count_pattern_length.get():
            cont_by_length = True

    if cont_by_begin:
        state.loop_position = segment.begin + cont_length
    elif cont_by_length:
        state.loop_position += cont_length


def calc_trim_pos(audio: Audio, trim1, trim2):
    qc = audio.length_ms_to_samp

    t1 = qc(trim1) % audio.length
    t2 = qc(trim2) % audio.length
    if t2 == 0:
        t2 = audio.length

    return t1, t2


def prepare_framing(state: ScramblerState):
    config = state.config
    qc = state.audio.length_ms_to_samp

    # Generate frames
    frames = []
    frame_pos = 0
    if config.quan_mode == 2:
        state.slices_bpm = get_bpm_array(state)

    while frame_pos < state.audio.length:
        frame_length = qc(config.framing_frame_size.get())
        frame_end = frame_pos + frame_length

        if config.quan_mode != 0 and config.quan_frame.get():  # Slices
            slices = get_slices_arr(state, config.quan_alt_frame)
            frame_end = quantize(frame_end, slices, config.quan_frame_dir, min_timestamp=frame_pos + 1)
            frame_length = frame_end - frame_pos

        if frame_end > state.audio.length:
            frame_length = state.audio.length - frame_pos

        frame_info = FrameInfo(frame_pos, frame_length, frame_length)
        frames.append(frame_info)
        frame_pos += frame_length

    # Simplify
    if config.fr_simplify:
        state.loop_frames.append(frames[0])
        grid_step = qc(config.fr_simplify_step)
        grid_start = 0
        threshold = grid_step * (1 - config.fr_simplify_severity / 100)
        for frame in frames[1:]:
            while frame.begin >= grid_start + grid_step:
                grid_start += grid_step
                threshold += grid_step

            if frame.begin < threshold:
                state.loop_frames.append(frame)
            else:
                state.loop_frames[-1].duration += frame.duration
    else:
        state.loop_frames = frames

    # Adjust segment index
    state.segment_idx = find_closest_frame_idx(state, state.loop_position)


def prepare_fix_ast(state: ScramblerState):
    config = state.config

    ast_e, ast_w = [], []
    for i in range(len(config.avgstart_times.elements)):
        ast = config.avgstart_times.elements[i]
        if config.trim_avgstart:
            ast -= state.trim_zero / state.audio.sample_rate * 1000
        if 0 < ast < state.audio.length / state.audio.sample_rate * 1000:
            ast_e.append(ast)
            ast_w.append(config.avgstart_times.weights[i])
    config.avgstart_times = RandChoice(ast_e, ast_w)


def prepare(state: ScramblerState, glob_state: ABState):
    config = state.config
    qc = glob_state.audio.length_ms_to_samp

    # Prepare audio
    state.trim_zero, trim_end = calc_trim_pos(glob_state.audio, config.trim1, config.trim2)
    state.audio = glob_state.audio.get_part(state.trim_zero, trim_end)
    if state.audio.length == 0:
        exc = ValueError("No audio found.")
        raise exc

    # Load onsets / slices
    ons_arg = state.audio.sample_rate, state.audio.length
    if glob_state.slices:
        state.slices = convert_onsets(glob_state.slices, state.trim_zero * config.trim_slices, *ons_arg)
    if glob_state.slices_alt:
        state.slices_alt = convert_onsets(glob_state.slices_alt, state.trim_zero * config.trim_slices2, *ons_arg)

    # Segment 0
    state.last_rep = config.seg0_repeat
    state.last_sus = config.seg0_muted
    state.last_mut = config.seg0_muted

    # Looping stuff
    state.loop_position = state.audio.length_ms_to_samp(config.loop_begin)
    if config.trim_loop_start:
        state.loop_position -= state.trim_zero
    state.loop_position = max(0, state.loop_position)
    state.loop_position %= state.audio.length

    # Framing stuff
    if config.framing:
        if config.framing_seed is not None:
            random.seed(config.framing_seed)
        else:
            random.seed(config.seed)
        prepare_framing(state)

    random.seed(config.seed)

    # Pause stuff
    if (not config.seg0_pause) or config.pause_consec_chance.get():
        state.pause_next = config.pause_chance.get()

    # Crossfade
    state.crossfade_next = qc(rand_by_chance(config.crossfade_chance, config.crossfade, 0))

    # Slicecr
    state.slicecr = state.audio.get_silence(state.target_length)

    # Seed
    state.random_state = random.getstate()


def prepare_ii(state: ScramblerState):
    prepare_fix_ast(state)

    place_onsets = state.config.quan_place_onsets.get(state.audio.sample_rate)
    state.slices_place = np.concatenate(([0], place_onsets[place_onsets > 0]))

    if state.config.quan_mode == 2:
        state.slices_bpm = get_bpm_array(state)

    if state.config.framing:
        get_frame_ratio(state)


def scramble_step(state: ScramblerState, config: ScramblerConfig, qc):
    state.config.override_reset()

    # Calculate pause
    if state.pause_new:
        state.pause_new = False
        state.pause_prev = state.pause_curr
        state.pause_curr = state.pause_next
        state.pause_next = config.pause_chance.get()
        if state.pause_curr and state.pause_next:
            state.pause_next = config.pause_consec_chance.get()

    # Calculate crossfade
    state.last_segment_crossfade = state.crossfade
    state.crossfade = state.crossfade_next
    state.crossfade_next = qc(rand_by_chance(config.crossfade_chance, config.crossfade, 0))
    if not config.framing:
        state.crossfade = min(state.crossfade, state.last_segment_length // 2)

    # New segment & its length
    segment_info = gen_random_segment(state)
    if (not segment_info.is_pause) and ((not segment_info.from_mem) or config.reappear_reoccur_chance.get()):
        if state.loop_can_repeat and segment_info.is_in_loop and config.loop_repeat_chance.get():
            state.loop_rep_begin = segment_info.begin
            state.loop_rep_duration = int(segment_info.duration / segment_info.k_speed)
        if config.reappear_chance.get():
            reappear_after = round(config.reappear_after_dist.get())
            state.memory.remember(segment_info, reappear_after)

    is_real_segment = (not segment_info.is_pause) and segment_info.volume > 0
    crossfade = 0 if config.framing else state.crossfade
    if is_real_segment:
        appender, real_cross1, length_mismatch = generate_segment_audio(state.audio, segment_info, crossfade)
        if length_mismatch:
            state.warn("Pre-calculated length mismatch")
        segment_length = appender.length
    else:
        appender = None
        segment_length, real_cross1 = precalculate_length(segment_info, crossfade, state.audio.length,
                                                          pause_effects=config.pause_apply_effects)
    segment_length -= (0 if config.framing else real_cross1)

    # Calculate frame length
    if config.framing and state.loop_frames:
        frame_length = get_frame_info(state, state.segment_idx).duration
        frame_length = round1(frame_length / config.framing_speed_ratio)
    else:
        frame_length = segment_length

    # Append segment
    if is_real_segment:
        if config.framing and state.loop_frames:
            frame_cut(appender, state, segment_info, frame_length, state.crossfade)
        else:
            add_crossfade(appender, state, real_cross1)

        place_position = quantize_placement_pos(state, state.scr_position)
        place_position += random_shift(state, frame_length) - (0 if config.framing else real_cross1)
        state.slicecr.place(appender, place_position)
    state.last_segment_length = frame_length
    state.scr_position += frame_length
    state.segment_dump.append(segment_info)

    # Looping
    mov_length = segment_length if config.loop_count_full_length.get() else segment_info.duration
    mov_length = round(mov_length * segment_info.speed)
    calculate_loop_position(mov_length, segment_info, state)
    state.pause_new = True
    state.segment_idx += 1

    # Consecutive ...
    if config.pause_apply_effects or not segment_info.is_pause:
        state.last_rep = (segment_info.repeats > 0)
        state.last_sus = (segment_info.sustain > 0)
        state.last_mut = (segment_info.volume <= 0)
    if segment_info.is_pause and config.volume_pause_is_mute:
        state.last_mut = True


def scramble(state: ScramblerState, gui_state, com_progress, com_error):
    config = state.config
    qc = state.audio.length_ms_to_samp

    state.warnings.clear()
    random.setstate(state.random_state)
    state.current_goal = min(state.current_goal, state.slicecr.length)

    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"\n=== Scrambling at {time_str}. Seed: {config.seed} ===")

    while state.scr_position < state.current_goal and not gui_state.force_abort:
        try:
            scramble_step(state, config, qc)

        except Exception as e:
            retry = com_error("Scrambling", meta.def_error.format("scrambling"), e, b_retry=True)
            if not retry:
                break

        # Callback
        com_progress(state.scr_position, state.target_length)

    state.random_state = random.getstate()
