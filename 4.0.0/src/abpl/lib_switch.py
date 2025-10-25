from abpl.core import *
from abpl.abpl_main import read_command, read_multi
from abpl.lib_vars import set_variable


def exec_until_if_keyword(state: ScriptState):
    while not state.jumped:
        sub_com = state.read()
        if sub_com in ("else", "end_if"):
            return sub_com
        else:
            read_command(state, move=False)

    return "end_if"


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
    state.return_ = read_command(state)
    raise Return


def cmd_stop_loop(state: ScriptState):
    if state.loop_breaks:
        state.loop_breaks[-1] = True
    else:
        state.error("no loops to stop")


def cmd_skip_loop(state: ScriptState):
    if state.loop_skips:
        state.loop_skips[-1] = True
    else:
        state.error("no loops to skip")


def if_else(state: ScriptState):
    condition = f2b(read_command(state))

    if condition: # Execute if true
        debug("condition is true")
        if exec_until_if_keyword(state) == "end_if":
            return condition

    else:
        debug("condition is false")
        if seek_if_keyword(state) == "end_if":  # Seek else / end_if
            debug("no 'else' found")
            return condition

    if not condition: # Execute if false
        debug("skipped 'if' segment")
        exec_until_if_keyword(state)

    else:  # Seek end_if
        debug("skipping 'else' segment")
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
    debug("seeking", kw_open, "-", kw_close)
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
        debug("while: checking condition")
        if not f2b(read_command(state)):
            break

        debug("while: loop")
        exec_until_loop_end(state, condition_pos, "end_while")

    if not state.jumped:
        state.set_pos(condition_pos)
        seek_loop_end(state, "while", "end_while")


def loop_for(state: ScriptState):
    var_name = state.read()
    left, right, step = read_multi(state, 3)

    for_begin = state.position
    state.loop_breaks.append(False)
    state.loop_skips.append(False)

    i = 0
    while not (state.jumped or state.loop_breaks[-1]):
        debug("for: checking border")
        if left + step * i >= right:
            break

        debug("for: loop", i)
        set_variable(state, var_name, left + step * i)
        exec_until_loop_end(state, for_begin, "end_for")
        i += 1

    if not state.jumped:
        state.set_pos(for_begin)
        seek_loop_end(state, "for", "end_for")


def define_function(state: ScriptState):
    func_name = state.read()
    n_args = int(state.read())
    arg_names = [state.read() for _ in range(n_args)]

    debug("defining", func_name, "(", *arg_names, ")")

    function_ = []
    func_begin = state.position + 1

    n_nest = 0
    while True:
        sub = state.read()
        if sub == "define":
            n_nest += 1
        elif sub == "end_def":
            if n_nest == 0:
                break
            else:
                n_nest -= 1

        function_.append(sub)

    if func_name in state.variables:
        del state.variables[func_name]
    state.functions[func_name] = (func_begin, arg_names, function_)


def unmatched(name: str):
    def unmatched_error(state: ScriptState):
        state.error(f"unmatched {name}")
    return unmatched_error


library = {
    "label":    cmd_label,
    "goto":     cmd_goto,
    "break":    cmd_break,
    "return":   cmd_return,

    "stop_loop":    cmd_stop_loop,
    "skip_loop":    cmd_skip_loop,

    "if":       if_else,
    "while":    loop_while,
    "for":      loop_for,
    "define":   define_function,
}

for keyword in ("else", "end_if", "end_while", "end_for", "end_def"):
    library[keyword] = unmatched(keyword)
