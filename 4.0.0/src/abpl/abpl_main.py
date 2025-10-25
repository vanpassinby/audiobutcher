from abpl.core import *
import abpl.core as core


def format_script(script: str):
    def filtered(char):
        if char in "() [] {} ,;:":
            return " "
        else:
            return char

    result = []
    tokens_by_line = []
    text = "".join(filtered(char) for char in script)

    for line in text.split("\n"):
        line = line.split("#")[0].split()

        result.extend(line)
        tokens_by_line.append(len(line))

    return result, tokens_by_line


def exec_function(state: ScriptState, func_name: str):
    from abpl.lib_vars import set_variable
    f_begin, arg_names, function_ = state.functions[func_name]

    for i in range(len(arg_names)):
        set_variable(state, arg_names[i], read_command(state))

    sub_state = ScriptState(function_, state.tokens_by_line, state.segment, state.scr_state, exec_shift=f_begin)
    sub_state.round_samples = state.round_samples
    sub_state.functions = state.functions
    sub_state.variables = state.variables
    sub_state.quan_options = state.quan_options

    result = execute(sub_state, is_sub=True)
    state.round_samples = sub_state.round_samples
    return result


def read_multi(state: ScriptState, amount: int):
    result = []
    for _ in range(amount):
        result.append(read_command(state))
    return result


def read_command(state: ScriptState, move=True):
    from abpl.lib import library
    from abpl.lib_math import number

    command = state.read(move=move)
    return_ = 0

    # Debug
    debug(state.token_pos_str, command)
    pre_cmd_level = core.DEBUG_CMD_LEVEL
    core.DEBUG_CMD_LEVEL += 1

    # Execution

    if command[0] in "1234567890.-+":
        return_ = number(state, command)

    elif command in state.variables:
        return_ = state.variables[command]

    elif command in state.functions:
        return_ = exec_function(state, command)

    elif command in library:
        return_ = library[command](state)

    else:
        state.error(f"'{command}' is not defined")

    # Final
    core.DEBUG_CMD_LEVEL = pre_cmd_level
    debug(command, "returned", return_)
    return float_x(return_)


def execute(state: ScriptState, is_sub=False):
    if not is_sub:
        core.DEBUG_CMD_LEVEL = 0
        debug("*" * 10, "Segment ID =", state.scr_state.segment_idx, "*" * 10)

    try:
        while not state.finished:
            state.jumped = False
            read_command(state)

    except Return:
        pass

    except Break:
        if is_sub:
            raise

    return state.return_
