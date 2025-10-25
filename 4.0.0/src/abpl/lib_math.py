import math
from abpl.core import *
from abpl.abpl_main import read_multi, read_command


consts = {
    "_e": math.e,
    "pi": math.pi
}

one_op = {
    "abs": lambda x: abs(x),
    "neg": lambda x: -x,

    "round":    lambda x: round(x),
    "floor":    lambda x: math.floor(x),
    "ceil":     lambda x: math.ceil(x),

    "factorial": lambda x: math.factorial(round(x)),

    "sin": lambda x: math.sin(x),
    "cos": lambda x: math.cos(x),
    "tan": lambda x: math.tan(x),

    "asin": lambda x: math.asin(x),
    "acos": lambda x: math.acos(x),
    "atan": lambda x: math.atan(x),

    "not": lambda x: not x
}

two_op = {
    "add": lambda x, y: x + y,
    "sub": lambda x, y: x - y,
    "mul": lambda x, y: x * y,
    "div": lambda x, y: x / y,
    "mod": lambda x, y: x % y,
    "pow": lambda x, y: x ** y,
    "log": lambda x, y: math.log(x, y),

    "and":  lambda x, y: f2b(x) and f2b(y),
    "or":   lambda x, y: f2b(x) and f2b(y),
    "xor":  lambda x, y: f2b(x) ^ f2b(y),

    "min": lambda x, y: min(x, y),
    "max": lambda x, y: max(x, y),

    "equal":    lambda x, y: x == y,
    "unequal":  lambda x, y: x != y,
    "more":     lambda x, y: x > y,
    "less":     lambda x, y: x < y,
    "close":    lambda x, y: math.isclose(x, y),

    "more_or_eq": lambda x, y: x >= y,
    "less_or_eq": lambda x, y: x <= y
}

in_range = {
    "in_range":             lambda left, value, right: left <= value <= right,
    "in_range_strict":      lambda left, value, right: left < value < right,
    "in_range_str_left":    lambda left, value, right: left < value <= right,
    "in_range_str_right":   lambda left, value, right: left <= value < right
}

units1 = ("ms", "sec", "minutes", "perc", "semitones", "degrees")
units2 = ("in_ms", "in_sec", "in_minutes", "in_perc", "in_semitones", "in_degrees")


def conv_ms_length(state: ScriptState, length: float):
    round_method = round if state.round_samples else float
    return state.scr_state.audio.length_ms_to_samp(length, round_method)


def measured_unit(state: ScriptState, unit_name: str, value: float):
    return {
        "ms":           lambda: conv_ms_length(state, value),
        "sec":          lambda: conv_ms_length(state, value*1000),
        "minutes":      lambda: conv_ms_length(state, value*60_000),
        "perc":         lambda: value / 100,
        "semitones":    lambda: 2 ** (value / 12),
        "degrees":      lambda: math.radians(value)
    }.get(unit_name, lambda: value)()


def conv_back(state: ScriptState, measure: str, value: float):
    return {
        "in_ms":        lambda: value / state.scr_state.audio.sample_rate * 1000,
        "in_sec":       lambda: value / state.scr_state.audio.sample_rate,
        "in_minutes":   lambda: value / state.scr_state.audio.sample_rate / 60,
        "in_perc":      lambda: value * 100,
        "in_semitones": lambda: 12 * math.log2(value),
        "in_degrees":   lambda: math.degrees(value)
    }.get(measure)()


def number(state: ScriptState, string: str):
    suffix_map = {
        "ms": "ms",
        "sec": "sec",
        "min": "minutes",
        "%": "perc",
        "st": "semitones",
        "deg": "degrees",
    }

    for suffix, unit in suffix_map.items():
        if string.endswith(suffix):
            suffix_len = len(suffix)
            return measured_unit(state, unit, eval(string[:-suffix_len]))

    return eval(string)


def math_const(command: str):
    return lambda _: consts[command]


def math_one_op(command: str):
    def op(state: ScriptState):
        x = read_command(state)
        return one_op[command](x)
    return op


def math_two_op(command: str):
    def op(state: ScriptState):
        x, y = read_multi(state, 2)
        return two_op[command](x, y)
    return op


def math_three_op(command: str):
    def op(state: ScriptState):
        x, y, z = read_multi(state, 3)
        return in_range[command](x, y, z)
    return op


def math_unit(command: str, invert=False):
    def unit(state: ScriptState):
        value = read_command(state)
        if invert:
            return conv_back(state, command, value)
        return measured_unit(state, command, value)
    return unit


library = {}
for cmd in consts:
    library[cmd] = math_const(cmd)
for cmd in one_op:
    library[cmd] = math_one_op(cmd)
for cmd in two_op:
    library[cmd] = math_two_op(cmd)
for cmd in in_range:
    library[cmd] = math_three_op(cmd)
for cmd in units1:
    library[cmd] = math_unit(cmd)
for cmd in units2:
    library[cmd] = math_unit(cmd, invert=True)
