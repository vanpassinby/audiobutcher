from abpl.core import *


def read_multi(state: ScriptState, amount):
    return [read_command(state) for _ in range(amount)]


def extract_env(state: ScriptState, obj):
    while True:
        if isinstance(obj, ABPLObject):
            return obj.obj
        elif callable(obj):
            obj = obj(state)
        else:
            return obj


def get_command(state: ScriptState, command: str):
    from abpl.lib import library
    from abpl.lib_math import number

    if command[0] in "1234567890.-+":
        return number(state, command)

    elif command in state.variables:
        return state.variables[command]

    elif command in state.vars_global:
        return state.vars_global[command]

    elif command in library:
        return library[command]

    else:
        raise Error(f"'{command}' is not defined")


def read_command(state: ScriptState, move=True):
    # Read
    command = state.read(move=move)

    state.debug(state.token_pos_str, command)
    state.call_stack_add(command)

    result = get_command(state, command)
    result = extract_env(state, result)

    state.call_stack.pop(-1)
    state.debug(command, "returned", result)

    return result


def execute(state: ScriptState, is_sub=False):
    if not is_sub:
        state.debug("*" * 10, "Segment ID =", state.scr_state.segment_idx, "*" * 10)

    try:
        while not state.finished:
            state.jumped = False
            read_command(state)

    except Return:
        pass

    except Break:
        if is_sub:
            raise

    except Exception as e:
        if is_sub:
            raise
        state.error(e)

    return state.result
