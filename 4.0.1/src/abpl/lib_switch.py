from abpl.abpl_main import *
from abpl.lib_vars import set_variable
from abpl.abpl_function import define_function


def exec_until_if_keyword(state: ScriptState):
    while not state.jumped:
        sub_com = state.read()
        if sub_com in ("else", "end_if"):
            return sub_com
        else:
            read_command(state, move=False)

    return "end_if"


def abpl400(state: ScriptState):
    state.abpl400_mode = True


def seek_if_keyword(state: ScriptState):
    n_nested = 0
    while True:
        sub_com = state.read()

        if sub_com == "if":
            n_nested += 1

        elif sub_com == "else":
            if n_nested == 0:
                return sub_com

        elif sub_com == "end_if":
            if n_nested == 0:
                return sub_com
            n_nested -= 1


def cmd_label(state: ScriptState):
    state.read()


def cmd_goto(state: ScriptState):
    label = state.read()
    state.jump()
    state.seek_label(label)


def cmd_break(_):
    raise Break


def cmd_return(state: ScriptState):
    state.result = read_command(state)
    raise Return


def cmd_stop_loop(state: ScriptState):
    if state.loop_breaks:
        state.loop_breaks[-1] = True
    else:
        raise Error("no loops to stop")


def cmd_skip_loop(state: ScriptState):
    if state.loop_skips:
        state.loop_skips[-1] = True
    else:
        raise Error("no loops to skip")


def if_else(state: ScriptState):
    condition = read_command(state)

    if condition: # Execute if true
        state.debug("condition is true")
        if exec_until_if_keyword(state) == "end_if":
            return condition

    else:
        state.debug("condition is false")
        if seek_if_keyword(state) == "end_if":  # Seek else / end_if
            state.debug("no 'else' found")
            return condition

    if not condition: # Execute if false
        state.debug("skipped 'if' segment")
        exec_until_if_keyword(state)

    else:  # Seek end_if
        state.debug("skipping 'else' segment")
        seek_if_keyword(state)

    return condition


def exec_until_loop_end(state: ScriptState, begin_pos: int, kw_close: str):
    state.loop_breaks[-1] = False
    state.loop_skips[-1] = False

    while not (state.jumped or state.loop_breaks[-1] or state.loop_skips[-1]):
        if state.read() == kw_close:
            break

        read_command(state, move=False)

    if not state.jumped:
        state.set_pos(begin_pos)


def seek_loop_end(state: ScriptState, kw_open: str, kw_close: str):
    state.debug("seeking", kw_open, "-", kw_close)
    state.loop_breaks.pop(-1)
    state.loop_skips.pop(-1)

    nest_level = 0
    while not state.jumped:
        command = state.read()
        if command == kw_open:
            nest_level += 1
        elif command == kw_close:
            if nest_level == 0:
                break
            nest_level -= 1


def loop_while(state: ScriptState):
    condition_pos = state.position
    state.loop_breaks.append(False)
    state.loop_skips.append(False)

    while not (state.jumped or state.loop_breaks[-1]):
        state.debug("while: checking condition")
        if not read_command(state):
            break

        state.debug("while: loop")
        exec_until_loop_end(state, condition_pos, "end_while")

    if not state.jumped:
        state.set_pos(condition_pos)
        seek_loop_end(state, "while", "end_while")


def loop_for(state: ScriptState):
    var_name = state.read()
    left, right, step = read_multi(state, 3)

    if step == 0:
        raise Error("'for' step can't be 0")

    for_begin = state.position
    state.loop_breaks.append(False)
    state.loop_skips.append(False)

    i = 0
    while not (state.jumped or state.loop_breaks[-1]):
        state.debug("for: checking border")
        if (step > 0 and left + step * i >= right) or (step < 0 and left + step * i <= right):
            break

        state.debug("for: loop", i)
        set_variable(state, var_name, left + step * i)
        exec_until_loop_end(state, for_begin, "end_for")
        i += 1

    if not state.jumped:
        state.set_pos(for_begin)
        seek_loop_end(state, "for", "end_for")


def loop_for_each(state: ScriptState):
    from abpl.lib_lists import ABPLList
    var_name = state.read()
    the_list = read_command(state)

    if not isinstance(the_list, ABPLList):
        raise Error("'for_each' requires list")

    for_begin = state.position
    state.loop_breaks.append(False)
    state.loop_skips.append(False)

    i = 0
    values = the_list.contents
    while i < len(values) and not (state.jumped or state.loop_breaks[-1]):
        state.debug("for_each: loop", i)
        set_variable(state, var_name, values[i])
        exec_until_loop_end(state, for_begin, "end_fe")
        i += 1

    if not state.jumped:
        state.set_pos(for_begin)
        seek_loop_end(state, "for", "end_fe")


def obj_envelope(state: ScriptState):
    obj = get_command(state, state.read())
    return ABPLObject(obj)


def obj_envelope1(state: ScriptState):
    times_allowed = read_command(state)
    obj = get_command(state, state.read())

    for _ in range(times_allowed):
        if callable(obj):
            obj = obj(state)
        else:
            break

    if callable(obj):
        return ABPLObject(obj)
    return obj


def unmatched(name: str):
    def unmatched_error(_):
        raise Error(f"unmatched {name}")
    return unmatched_error


library = {
    "!ABPL400": abpl400,

    "env":  obj_envelope,
    "env_": obj_envelope1,

    "label":    cmd_label,
    "goto":     cmd_goto,
    "break":    cmd_break,
    "return":   cmd_return,

    "stop_loop":    cmd_stop_loop,
    "skip_loop":    cmd_skip_loop,

    "if":       if_else,
    "while":    loop_while,
    "for":      loop_for,
    "for_each": loop_for_each,
    "define":   define_function
}

for keyword in ("else", "end_if", "end_while", "end_for", "end_fe", "end_def"):
    library[keyword] = unmatched(keyword)
