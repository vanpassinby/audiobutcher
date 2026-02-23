from abpl.abpl_main import *

PROPS_INT = ("begin", "duration", "repeats", "intro_loop", "fadein", "fadeout",
             "sustain", "sustain_c", "sustain_portion")
PROPS_FLOAT = ("speed", "volume", "fadein_cut", "fadeout_cut", "k_speed")
PROPS_BOOL = ("is_pause", "is_avgstart", "is_in_loop", "from_mem", "preroll_fadein",
              "reverse1", "reverse2", "sustain_exact", "sustain_shift")
PROPS_ALL = PROPS_INT + PROPS_FLOAT + PROPS_BOOL


def set_variable(state: ScriptState, name: str, value):
    state.debug("set", name, value)

    if name in PROPS_ALL:
        if name in PROPS_INT:
            value = round(value)

        elif name in PROPS_BOOL:
            value = bool(value)

        state.segment[name] = value
        state.debug("changed prop", name, "to", value)

    else:
        state.variables[name] = value

    return ABPLObject(value)


def cmd_set(state: ScriptState):
    var_name = state.read()
    state.debug("variable:", var_name)
    return set_variable(state, var_name, read_command(state))


def cmd_var_global(state: ScriptState):
    var_name = state.read()
    state.global_var_list.add(var_name)


def cmd_var_exist(state: ScriptState):
    var_name = state.read()
    return var_name in state.variables or var_name in state.vars_global


def cmd_var_is_global(state: ScriptState):
    var_name = state.read()
    return var_name in state.global_var_list


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
    "var_global":       cmd_var_global,
    "var_exist":        cmd_var_exist,
    "var_is_glob":      cmd_var_is_global,
    "del_var":          cmd_del_var,
    "round_samp_on":    cmd_round_samp_on,
    "round_samp_off":   cmd_round_samp_off
}
