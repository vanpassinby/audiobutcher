from abpl.core import *
from abpl.abpl_main import read_command
from scrambler.scr_tools import quantize_length
from slicing import quantize


def quan_config(state: ScriptState):
    op_name = state.read()
    op_value = read_command(state)
    state.quan_options[op_name] = round(op_value)


def quan_config_clear(state: ScriptState):
    state.quan_options.clear()


def cmd_quantize(direction: int):
    def apply_quantization(state: ScriptState):
        value = round(read_command(state))

        if state.scr_state.config.quan_mode == 0:
            return value

        if state.scr_state.config.quan_mode == 1:
            if f2b(state.quan_options.get("use_alt", 0)) and state.scr_state.slices_alt:
                slices = state.scr_state.slices_alt
            else:
                slices = state.scr_state.slices
        else:
            slices = state.scr_state.slices_bpm

        min_pos = state.quan_options.get("min_pos")
        max_pos = state.quan_options.get("max_pos")

        return quantize(value, slices, direction, min_pos, max_pos)

    return apply_quantization


def cmd_len_auto_quan(state: ScriptState):
    quantize_length(state.scr_state, state.segment)


library = {
    "quan_config": quan_config,
    "quan_config_clear": quan_config_clear,

    "quantize": cmd_quantize(direction=0),
    "quantize_forw": cmd_quantize(direction=2),
    "quantize_back": cmd_quantize(direction=1),

    "ab_quantize_length": cmd_len_auto_quan
}
