from abpl.abpl_main import *


def const_get(state: ScriptState):
    cons_name = state.read()
    cons_value = state.scr_state.abpl_constants.get(cons_name, 0)
    return cons_value


def const_set(state: ScriptState):
    cons_name = state.read()
    cons_value = read_command(state)

    state.debug("const set", cons_name, cons_value)
    state.scr_state.abpl_constants[cons_name] = cons_value
    return ABPLObject(cons_value)


def mark_props(state: ScriptState):
    seg = read_command(state)
    mark = state.read()
    return seg, mark


def has_mark(state: ScriptState):
    seg, mark = mark_props(state)
    return mark in state.scr_state.abpl_marks.get(seg, [])


def mark_add(state: ScriptState):
    seg, mark = mark_props(state)
    if seg not in state.scr_state.abpl_marks:
        state.scr_state.abpl_marks[seg] = set()
    if mark not in state.scr_state.abpl_marks[seg]:
        state.scr_state.abpl_marks[seg].add(mark)


def mark_remove(state: ScriptState):
    seg, mark = mark_props(state)
    if seg in state.scr_state.abpl_marks:
        if mark in state.scr_state.abpl_marks[seg]:
            state.scr_state.abpl_marks[seg].remove(mark)


library = {
    "const": const_get,
    "const_set": const_set,
    "has_mark": has_mark,
    "mark_add": mark_add,
    "mark_remove":  mark_remove,
}
