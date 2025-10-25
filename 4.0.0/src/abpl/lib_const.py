from abpl.core import *
from abpl.abpl_main import read_command


def const_get(state: ScriptState):
    cons_name = state.read()
    return state.scr_state.abpl_constants.get(cons_name, 0)


def const_set(state: ScriptState):
    cons_name = state.read()
    cons_value = read_command(state)

    state.scr_state.abpl_constants[cons_name] = cons_value
    return cons_value


def mark_props(state: ScriptState):
    seg = round(read_command(state))
    mark = state.read()
    return seg, mark


def has_mark(state: ScriptState):
    seg, mark = mark_props(state)
    return mark in state.scr_state.abpl_marks.get(seg, [])


def mark_add(state: ScriptState):
    seg, mark = mark_props(state)
    if seg not in state.scr_state.abpl_marks:
        state.scr_state.abpl_marks[seg] = []
    if mark not in state.scr_state.abpl_marks[seg]:
        state.scr_state.abpl_marks[seg].append(mark)


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
