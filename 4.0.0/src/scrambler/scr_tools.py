from ab_tools import round1
from scrambler.scr_state import *
from scrambler.segment import FrameInfo
from slicing import get_slices_arr, quantize


def get_frame_info(state: ScramblerState, idx: int) -> FrameInfo:
    index = idx % len(state.loop_frames)
    return state.loop_frames[index]


def find_closest_frame_idx(state: ScramblerState, position: int):
    idx_range = range(len(state.loop_frames))
    return min(idx_range, key=lambda idx: abs(state.loop_frames[idx].begin - position))


def get_k_speed(config, segment: SegmentInfo):
    if config.speed_affect_mode == 1:
        return config.speed_main / segment.speed
    elif config.speed_affect_mode == 2:
        return 1 / segment.speed
    else:
        return 1


def quantize_length(state: ScramblerState, segment: SegmentInfo):
    config = state.config
    segment_end = segment.begin + math.ceil(segment.duration * segment.speed)

    if config.quan_mode == 2 and config.quan_duration_bpm_mode == 1:  # BPM quantization by length
        quan_action = [round, int, math.ceil][config.quan_duration_dir]
        beat_dur_samp = math.ceil(60 / config.quan_bpm * state.audio.sample_rate)
        segment_length = segment_end - segment.begin
        segment_length = quan_action(segment_length / beat_dur_samp) * beat_dur_samp
        segment_end = segment.begin + max(1, segment_length)

    elif config.quan_mode != 0:
        slices = get_slices_arr(state, config.quan_alt_duration)
        segment_end = quantize(segment_end, slices, config.quan_duration_dir, min_timestamp=segment.begin + 1)

    segment.duration = math.ceil((segment_end - segment.begin) / segment.speed)


def fix_length(state: ScramblerState, segment: SegmentInfo):
    if segment.begin + math.ceil(segment.duration * segment.speed) > state.audio.length:
        old_dur = segment.duration
        segment.duration = int((state.audio.length - segment.begin) / segment.speed)
        print("Segment duration shortened from", old_dur, "to", segment.duration)
        if segment.is_in_loop:
            state.loop_reset = True


def find_last_slice(state: ScramblerState, segment: SegmentInfo):
    segment_end = segment.begin + math.ceil(segment.duration * segment.speed)

    if segment.reverse1:
        quantized = quantize(segment.begin+1, state.slices, 2, min_timestamp=segment.begin+1)
        return quantized - segment.begin
    else:
        quantized = quantize(segment_end-1, state.slices, 1, max_timestamp=segment_end-1)
        return segment_end - quantized


def fix_sustain_cross(state: ScramblerState, segment: SegmentInfo):
    if None in (segment.sustain_portion, segment.sustain_c):
        return

    max_cross_length = min(segment.duration, segment.sustain_portion)

    if segment.sustain_shift:
        max_cross_length = min(max_cross_length, segment.duration - segment.sustain_portion)

        if max_cross_length < 0:
            print("Sustain: Negative crossfade length:", max_cross_length)
            state.warn("Negative sustain crossfade length")

    segment.sustain_c = min(segment.sustain_c, max_cross_length // 2)


def quan_sustain(state: ScramblerState, segment: SegmentInfo):
    config = state.config
    seg_end = min(segment.begin + math.ceil(segment.duration * segment.speed), state.audio.length)

    # Calculate bounds
    if segment.sustain_shift:
        if segment.reverse1:
            q_min_pos = segment.begin
            q_max_pos = (segment.begin + seg_end) // 2
        else:
            q_min_pos = (segment.begin + seg_end) // 2
            q_max_pos = seg_end
    else:
        q_min_pos = segment.begin
        q_max_pos = seg_end

    # Calculate where portion begin/end
    if segment.reverse1:
        q_min_pos += 1
        point = min(segment.begin + segment.sustain_portion, state.audio.length)
    else:
        q_max_pos -= 1
        point = max(seg_end - segment.sustain_portion, 0)

    # Direction
    direction = config.quan_sustain_dir
    if not segment.reverse1:
        if direction == 1:
            direction = 2
        elif direction == 2:
            direction = 1

    # Quantize
    if config.quan_mode == 1:  # Slices
        slices = get_slices_arr(state, config.quan_alt_duration)
        point = quantize(point, slices, direction, min_timestamp=q_min_pos, max_timestamp=q_max_pos)

    # FINALLY!
    if segment.reverse1:
        segment.sustain_portion = point - segment.begin
    else:
        segment.sustain_portion = seg_end - point


def segment_fixup(state: ScramblerState, segment: SegmentInfo):
    # Fix negative values
    for key in segment.as_dict:
        value = segment[key]
        if isinstance(value, int) or isinstance(value, float):
            segment[key] = abs(value)

    # Fix length
    fix_length(state, segment)

    # Fix sustain
    available_space = segment.duration
    if segment.sustain_shift:
        available_space //= 2
    segment.sustain_portion = min(segment.sustain_portion or 0, available_space)
    if segment.sustain_portion == 0:
        segment.sustain = 0

    fix_sustain_cross(state, segment)


def cross_compensate(mode: int, desired: int, available: int):
    zero = 0
    if desired > available:
        if mode == 1:
            zero = 1 - available / desired
        desired = available
    return desired, zero


def quantize_placement_pos(state: ScramblerState, position: int):
    config = state.config

    if config.quan_place_mode == 1 and config.quan_place_step != 0:
        if config.quan_place_step > 0:
            step = state.audio.length_ms_to_samp(config.quan_place_step)
        else:
            step = round1(-state.audio.length / config.quan_place_step)

        if step == 0:
            return position

        deviation = (position + state.scr_position_zero) % step

    elif config.quan_place_mode == 2:
        if len(state.slices_place) <= 1:
            return position

        position_loop = (position + state.scr_position_zero) % state.slices_place[-1]
        deviation = position_loop - quantize(position_loop, state.slices_place, direction=1)

    else:
        return position

    return position - round(deviation * config.quan_place_strength / 100)


def get_frame_ratio(state: ScramblerState):
    speed_eq = state.config.framing_speed_ratio.lower() \
        .replace("[length]", str(state.audio.length / state.audio.sample_rate)) \
        .replace("[length_samp]", str(state.audio.length)) \
        .replace("[sample_rate]", str(state.audio.sample_rate))

    state.config.framing_speed_ratio = float(eval(speed_eq))
    if state.config.framing_speed_ratio <= 0:
        exc = ValueError("Frame speed ratio can't be zero or negative!")
        raise exc
