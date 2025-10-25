from scrambler.scr_tools import *
from scrambler.scr_state import *
from slicing import get_slices_arr, quantize


def random_sp_ast(state: ScramblerState, segment: SegmentInfo):
    qc = state.audio.length_ms_to_samp
    config = state.config

    avg_start_time = config.avgstart_times.get()
    if config.avgstart_dev_chance.get():
        avg_start_deviation = rand_gauss_deviation(config.avgstart_deviation)
        avg_start_deviation *= config.avgstart_dev_direction.get()
    else:
        avg_start_deviation = 0
    segment.begin = qc(avg_start_time + avg_start_deviation)

    if config.framing and state.loop_frames and config.framing_force_for_ast.get():
        frame_idx = find_closest_frame_idx(state, segment.begin)
        selected_frame = get_frame_info(state, frame_idx)
        segment.begin = selected_frame.begin
        if config.framing_force_duration.get():
            segment.duration = -math.ceil(selected_frame.content_dur * segment.k_speed * config.fr_length_soft/100)

    elif config.quan_mode in [1, 2] and config.quan_ast.get():
        direction = config.quan_ast_dir
        if direction == 3:
            if avg_start_deviation < 0:
                direction = 1
            elif avg_start_deviation > 0:
                direction = 2
            else:
                direction = 0

        if config.quan_mode != 0:
            slices = get_slices_arr(state, config.quan_alt_ast)
            segment.begin = quantize(segment.begin, slices[:-1], direction)


def random_sp_skip(state: ScramblerState, segment: SegmentInfo):
    qc = state.audio.length_ms_to_samp
    config = state.config

    skip_direction = config.skip_weights.get()
    subconfig = [config.skip_forw, config.skip_back, config.skip_rand][skip_direction]

    skip_size = 0
    if subconfig.min_skip_chance.get():
        skip_size += subconfig.min_skip
    if subconfig.add_dev_chance.get():
        skip_size += rand_gauss_deviation(subconfig.add_dev)
    skip_size = qc(skip_size)

    if skip_direction == 1 or (skip_direction == 2 and RandChance(50).get()):
        skip_size *= -1

    segment.begin += skip_size
    segment.begin = min(max(0, segment.begin), state.audio.length-1)

    if config.quan_mode in [1, 2] and config.quan_skip.get():
        direction = config.quan_skip_dir
        if direction == 3:
            if skip_size < 0:
                direction = 1
            elif skip_size > 0:
                direction = 2
            else:
                direction = 0

        if config.quan_mode != 0:
            slices = get_slices_arr(state, config.quan_alt_skip)
            segment.begin = quantize(segment.begin, slices[:-1], direction)


def random_sp_loop(state: ScramblerState, segment: SegmentInfo):
    config = state.config

    state.loop_can_repeat = True
    if config.framing and state.loop_frames:
        selected_frame = get_frame_info(state, state.segment_idx)
        segment.begin = selected_frame.begin
        if config.framing_force_duration.get():
            segment.duration = -math.ceil(selected_frame.content_dur * segment.k_speed * config.fr_length_soft/100)
    else:
        segment.begin = state.loop_position

        if config.quan_mode != 0 and config.quan_loop.get():
            slices = get_slices_arr(state, config.quan_alt_loop)
            segment.begin = quantize(segment.begin, slices[:-1], config.quan_loop_dir)

    if config.skip_chance.get():
        random_sp_skip(state, segment)


def random_sp_pattern(state: ScramblerState, segment: SegmentInfo):
    config = state.config

    if config.framing and state.loop_frames and config.framing_force_for_pattern.get():
        selected_frame: FrameInfo = random.choice(state.loop_frames)
        segment.begin = selected_frame.begin
        if config.framing_force_duration.get():
            segment.duration = -math.ceil(selected_frame.content_dur * segment.k_speed * config.fr_length_soft/100)
    else:
        max_position = state.audio.length - math.ceil(segment.duration * segment.speed)
        segment.begin = random.randint(0, max(0, max_position))

        if config.quan_mode != 0 and config.quan_pattern.get():
            slices = get_slices_arr(state, config.quan_alt_pattern)[:-1]
            if config.quan_pattern_dir == 3:  # Equal
                segment.begin = int(random.choice(slices))
            else:
                segment.begin = quantize(segment.begin, slices, config.quan_pattern_dir)


def random_start_pos(state: ScramblerState, segment: SegmentInfo):
    config = state.config

    # Choose source
    segment.is_in_loop = not config.loop_pattern_chance.get()
    segment.is_avgstart = config.avgstart_chance.get() and len(config.avgstart_times.elements) > 0
    if segment.is_avgstart and segment.is_in_loop:
        if config.avgstart_force_pattern.get():
            segment.is_in_loop = False
        else:
            segment.is_avgstart = False

    if segment.is_avgstart:
        random_sp_ast(state, segment)

    # In loop: Repeat
    elif segment.is_in_loop and (state.loop_rep_begin is not None) and (state.loop_rep_duration is not None):
        segment.begin = state.loop_rep_begin
        segment.duration = -math.ceil(state.loop_rep_duration * segment.k_speed)
        segment.is_in_loop = False
        state.loop_can_repeat = False

    elif segment.is_in_loop:
        random_sp_loop(state, segment)

    else:  # Pattern
        random_sp_pattern(state, segment)

    state.loop_rep_begin = None
    state.loop_rep_duration = None
