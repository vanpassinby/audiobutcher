from abpl.core import *
from abpl.abpl_main import read_command


PROPS_INT = ("begin", "duration", "repeats", "intro_loop", "fadein", "fadeout",
             "sustain", "sustain_c", "sustain_portion")
PROPS_FLOAT = ("speed", "volume", "fadein_cut", "fadeout_cut", "k_speed")
PROPS_BOOL = ("is_pause", "is_avgstart", "is_in_loop", "from_mem", "preroll_fadein",
              "reverse1", "reverse2", "sustain_exact", "sustain_shift")
PROPS_ALL = PROPS_INT + PROPS_FLOAT + PROPS_BOOL


def set_variable(state: ScriptState, name: str, value: float):
    debug("set", name, value)

    if name in PROPS_ALL:
        if name in PROPS_INT:
            value = round(value)

        elif name in PROPS_BOOL:
            value = f2b(value)

        state.segment[name] = value

    else:
        if name in state.functions:
            del state.functions[name]

        state.variables[name] = value

    return value


def cmd_set(state: ScriptState):
    var_name = state.read()
    var_value = read_command(state)
    return set_variable(state, var_name, var_value)


def cmd_var_exist(state: ScriptState):
    var_name = state.read()
    return var_name in state.variables


def cmd_del_var(state: ScriptState):
    var_name = state.read()
    if var_name in state.variables:
        del state.variables[var_name]
        return 1
    return 0


def cmd_round_samp_on(state: ScriptState):
    state.round_samples = True


def cmd_round_samp_off(state: ScriptState):
    state.round_samples = False


library = {
    "set":              cmd_set,
    "var_exist":        cmd_var_exist,
    "del_var":          cmd_del_var,
    "round_samp_on":    cmd_round_samp_on,
    "round_samp_off":   cmd_round_samp_off
}
