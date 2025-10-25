from abpl.core import *
from abpl.abpl_main import read_command
from abpl.lib_vars import PROPS_ALL
from scrambler.scr_tools import get_k_speed, get_frame_info


def get_segment(state: ScriptState, idx: int):
    if idx < 0 or idx > state.scr_state.segment_idx:
        return SegmentInfo()

    elif idx == state.scr_state.segment_idx:
        return state.segment

    else:
        return state.scr_state.segment_dump[idx]


def get_seg_prop(segment: SegmentInfo, prop_name: str):
    return getattr(segment, prop_name)


def prop_by_idx(state: ScriptState):
    seg_idx = round(read_command(state))
    prop_name = state.read()

    segment = get_segment(state, seg_idx)
    return get_seg_prop(segment, prop_name)


def onset_by_idx(state: ScriptState, alt=False):
    ons_idx = round(read_command(state))
    if alt and state.scr_state.slices_alt:
        return state.scr_state.slices_alt[ons_idx]
    else:
        return state.scr_state.slices[ons_idx]


def frame_by_idx(state: ScriptState):
    frame_idx = round(read_command(state))
    parameter = state.read()

    frame = get_frame_info(state.scr_state, frame_idx)
    return getattr(frame, parameter)


def seg_prop(prop_name: str):
    def get_prop(state: ScriptState):
        segment = get_segment(state, state.scr_state.segment_idx)
        return get_seg_prop(segment, prop_name)
    return get_prop


library = {
    "k_speed_now":  lambda s: get_k_speed(s.scr_state.config, s.segment),

    "segment_idx":          lambda s: s.scr_state.segment_idx,
    "audio_sample_rate":    lambda s: s.scr_state.audio.sample_rate,

    "audio_length":     lambda s: s.scr_state.audio.length,
    "rendered_length":  lambda s: s.scr_state.scr_position + s.scr_state.scr_position_zero,
    "target_length":    lambda s: s.scr_state.target_length,
    "loop_position":    lambda s: s.scr_state.loop_position,

    "amt_frames":       lambda s: len(s.scr_state.loop_frames),
    "amt_onsets":       lambda s: len(s.scr_state.slices),
    "amt_onsets_alt":   lambda s: len(s.scr_state.slices_alt),

    "prop_by_idx":      lambda s: prop_by_idx(s),
    "onset_by_idx":     lambda s: onset_by_idx(s),
    "onset_by_idx_alt": lambda s: onset_by_idx(s, True),
    "frame_by_idx":     lambda s: frame_by_idx(s)
}

for prop in PROPS_ALL:
    library[prop] = seg_prop(prop)
