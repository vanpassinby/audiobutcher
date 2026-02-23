from abpl.abpl_main import *
from scrambler.scr_state import ScramblerConfig, ScramblerConfigSubSustain, ScramblerConfigSubSkip


def fake_random(result_type):

    class FakeRandom:
        def __init__(self, value):
            self.value = result_type(value)

        def get(self):
            return self.value

    return FakeRandom


def get_parameter(config, option_name: str):
    got = config.__dict__.get(option_name)

    if hasattr(got, "get") and callable(got.get):
        return got.get()

    elif got is None:
        return 0

    return got


def from_config(state: ScriptState):
    option_name = state.read()
    return get_parameter(state.scr_state.config, option_name)


def from_config_sub(sub_type: str):
    def recv(state: ScriptState):
        sub_id = read_command(state)
        option_name = state.read()

        if sub_type == "skip":
            skip_id = {
                0: state.scr_state.config.skip_forw,
                1: state.scr_state.config.skip_back,
                2: state.scr_state.config.skip_rand,
            }
            config = skip_id[sub_id]

        elif sub_type == "sustain":
            config = state.scr_state.config.sustain_variants[sub_id]

        else:
            return 0

        return get_parameter(config, option_name)

    return recv


def cmd_force(state: ScriptState):
    name = state.read()
    value = read_command(state)

    def fallback_one(num):
        if num <= 0:
            return 1.0
        return num

    key, type_ = {
        "reappear":         ("reappear_chance", fake_random(bool)),
        "reappear_after":   ("reappear_after_dist", fake_random(abs)),
        "reappear_reoccur": ("reappear_reoccur_chance", fake_random(bool)),
        "loop_repeat":      ("loop_repeat_chance", fake_random(bool)),

        "framing_speed_ratio":  ("framing_speed_ratio", fallback_one),
        "framing_alt_reverse":  ("framing_alt_reverse", bool),
        "fr_length_hard":       ("fr_length_hard", abs),

        "fr_env_attack":    ("fr_env_attack", bool),
        "fr_env_hold":      ("fr_env_attack", bool),
        "fr_env_decay":     ("fr_env_attack", bool),
        "fr_env_crossfade_endless": ("fr_env_crossfade_endless", bool),

        "fr_env_attack_dur":    ("fr_env_attack_dist", fake_random(bool)),
        "fr_env_hold_dur":      ("fr_env_hold_dist", fake_random(bool)),
        "fr_env_decay_dur":     ("fr_env_decay_dist", fake_random(bool)),

        "shift":        ("shift_chance", fake_random(bool)),
        "shift_prop":   ("shift_dev_proportional", bool),
        "shift_dur":    ("shift_deviation", fake_random(abs)),
        "shift_direct": ("shift_dev_direction", fake_random(int)),

        "loop_count_full_length":       ("loop_count_full_length", fake_random(bool)),
        "loop_count_pause_length":      ("loop_count_pause_length", fake_random(bool)),
        "loop_count_pattern_length":    ("loop_count_pattern_length", fake_random(bool)),

        "loop_break_skips":     ("loop_break_skips", fake_random(bool)),
        "loop_break_pattern":   ("loop_break_pattern", fake_random(bool)),
        "loop_break_avgstart":  ("loop_break_avgstart", fake_random(bool))

    }[name]

    value_fmt = type_(value)
    state.scr_state.config.override(key, value_fmt)


library = {
    "from_config": from_config,
    "from_config_skip": from_config_sub("skip"),
    "from_config_sustain": from_config_sub("sustain"),
    "force": cmd_force,
}

misc_kw = (
    ScramblerConfig().__dict__.keys() |
    ScramblerConfigSubSustain().__dict__.keys() |
    ScramblerConfigSubSkip().__dict__.keys()
)
misc_kw.discard("_overridden")
