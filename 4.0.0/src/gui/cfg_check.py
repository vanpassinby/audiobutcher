from state import ABState
from scrambler.scr_state import ScramblerConfig
from ab_random import RandNumber
from common import AB_FLOAT16_AUDIO, AB_DISABLE_PSUTIL

import psutil
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui_main import MainWindow
import tkinter.messagebox as mb


def wrong_audio(state: ABState):
    if not state.audio:
        mb.showerror("Error", "You have to first import an audio file!")
        return True
    else:
        return False


def wrong_combobox(gui: "MainWindow", config: ScramblerConfig):
    wrong_combo = -1 in [
        gui.f_basic.f_speed_change.c_speed_measure.current(), config.speed_affect_mode, config.quan_mode,
        config.quan_pattern_dir, config.quan_ast_dir, config.quan_loop_dir, config.quan_skip_dir,
        config.quan_duration_dir, config.quan_sustain_dir, config.quan_frame_dir,
        config.reverse_double_mode, gui.f_tweak.main.c_pause_apply_effects.current(),
        config.crossfade_comp_mode, gui.f_tweak.main.c_fade_in_plus_preroll.current(), config.quan_place_mode,
        config.quan_duration_bpm_mode, gui.f_tweak.main.c_allow_abpl.current()
    ]

    wrong = (wrong_combo or
        any(obj.check_wrong_mode() for obj in config.sustain_variants) or
        any(obj.check_wrong_mode() for obj in config.__dict__.values() if isinstance(obj, RandNumber))
    )

    if wrong:
        mb.showerror("Error", "Please check all dropdowns!")
    return wrong


def wrong_gauss(config: ScramblerConfig):
    wrong = (
        any(obj.check_wrong_gauss() for obj in config.sustain_variants) or
        any(obj.check_wrong_gauss() for obj in config.__dict__.values() if isinstance(obj, RandNumber))
    )

    if wrong:
        mb.showerror("Error", "In CLIPPED GAUSS random mode, the sum of the parameters must be greater than 0!")
    return wrong


def wrong_lognorm(config: ScramblerConfig):
    wrong = (
        any(obj.check_wrong_lognorm() for obj in config.sustain_variants) or
        any(obj.check_wrong_lognorm() for obj in config.__dict__.values() if isinstance(obj, RandNumber))
    )

    if wrong:
        return not mb.askyesno("Warning",
                               "In LOGNORMAL random mode, parameters with sum greater than 10 are not recommended! Continue anyway?",
                               default=mb.NO, icon="warning")
    else:
        return False


def wrong_zero_weights(config: ScramblerConfig):
    cause = None
    if config.speed_alter_chance.chance > 0 and config.speed_variations.check_wrong_zero_sum():
        cause = "speed variation"
    elif config.sustain_chance.chance > 0 and config.sustain_weights.check_wrong_zero_sum():
        cause = "sustain variation"
    elif config.loop_pattern_chance.chance < 100 and config.skip_chance.chance > 0 and \
            config.skip_weights.check_wrong_zero_sum():
        cause = "skip direction"
    elif config.avgstart_chance.chance > 0 and config.avgstart_times.check_wrong_zero_sum():
        cause = "average start time"
    elif config.avgstart_chance.chance > 0 and config.avgstart_dev_chance.chance > 0 and \
            config.avgstart_dev_direction.check_wrong_zero_sum():
        cause = "average start time deviation"
    elif config.shift_chance.chance > 0 and config.shift_dev_direction.check_wrong_zero_sum():
        cause = "segment shift direction"
    elif config.volume_alt_chance.chance > 0 and config.volume_direction.check_wrong_zero_sum():
        cause = "volume change direction"

    if cause:
        mb.showerror("Error", "Total of {} weights must be greater than zero!".format(cause))
        return True
    else:
        return False


def wrong_zero_seg(config: ScramblerConfig):
    wrong_seg = config.duration_dist.is_zero()
    wrong_frm = config.framing_frame_size.is_zero() and config.framing
    if wrong_seg:
        mb.showerror("Error", "Segment length can't be zero!")
    elif wrong_frm:
        mb.showerror("Error", "Frame length can't be zero!")
    return wrong_seg or wrong_frm


def wrong_speeds(config: ScramblerConfig):
    right = all(0 < speed for speed in config.speed_variations.elements)
    wrong = config.speed_main <= 0 or (config.speed_alter_chance.chance > 0 and not right)

    if wrong:
        mb.showerror("Error", "Speed cannot be zero or negative!")
    return wrong


def wrong_speed_w(config: ScramblerConfig):
    if config.speed_alter_chance.chance <= 0:
        return False

    a = len(config.speed_variations.elements)
    b = len(config.speed_variations.weights)

    if a!=b:
        mb.showerror("Error",
                     f"The number of speeds and their weights must match! ({a} vs {b})\n"
                     "You can leave the weights field blank for equal weighting.")
    return a!=b


def wrong_ast_w(config: ScramblerConfig):
    if config.avgstart_chance.chance <= 0:
        return False

    a = len(config.avgstart_times.elements)
    b = len(config.avgstart_times.weights)

    if a!=b:
        mb.showerror("Error",
                     f"The number of average start times and their weights must match! ({a} vs {b})\n"
                     "You can leave the weights field blank for equal weighting.")
    return a!=b


def wrong_sustain_portion(config: ScramblerConfig):
    if config.sustain_chance.chance <= 0:
        return False

    for i in range(len(config.sustain_weights.elements)):
        if config.sustain_weights.weights[i] > 0:
            if config.sustain_variants[i].portion_length.is_zero():
                mb.showerror("Error", f"Sustain portion can't be zero! (Variant #{i+1})")
                return True

    return False


def wrong_math(config: ScramblerConfig):
    if not config.framing:
        return False

    allowed = set("0123456789.+-*/()_ ")
    string = config.framing_speed_ratio.lower() \
        .replace("[length]", "_") \
        .replace("[length_samp]", "_") \
        .replace("[sample_rate]", "_")

    wrong = not set(string).issubset(allowed)

    if wrong:
        mb.showerror("Error", "Framing: Speed ratio. Math equations can only include numbers, operators (. + - * /), parentheses, special words ([length], [length_samp], [sample_rate]) and spaces!")
    return wrong


def wrong_slices(gui: "MainWindow", state: ABState, config: ScramblerConfig):
    if config.quan_mode == 1 and not state.slices.are_there:
        switch = mb.askyesno("Error", "You can't use SLICES quantization mode without slices detected.\nDo you want to detect slices now?", icon="error")
        if switch:
            gui.f_tabs.select(gui.f_quantization.root)
        return True

    if config.quan_mode == 2 and config.quan_bpm == 0:
        mb.showerror("Error", "Quantization BPM can't be zero!")
        return True

    return False


def check_wrong_config(gui: "MainWindow", state: ABState, config: ScramblerConfig):
    return (
        wrong_audio(state) or
        wrong_combobox(gui, config) or
        wrong_gauss(config) or
        wrong_lognorm(config) or
        wrong_zero_weights(config) or
        wrong_zero_seg(config) or
        wrong_speeds(config) or
        wrong_speed_w(config) or
        wrong_ast_w(config) or
        wrong_sustain_portion(config) or
        wrong_math(config) or
        wrong_slices(gui, state, config)
    )


def check_ram_overflow(target_length, n_channels):
    if AB_DISABLE_PSUTIL:
        return False

    free_mem = psutil.virtual_memory().available
    mem_demand = target_length * n_channels * (2 if AB_FLOAT16_AUDIO else 4)

    if mem_demand / free_mem < 0.9:
        return False

    else:
        warn = "This operation will require at least {:.0f} MB of RAM, amounting to {:.1%} of your currently available memory. Continuing may affect your device's performance.\nWould you like to proceed?"
        return not mb.askyesno("Warning", warn.format(mem_demand / (1024**2), mem_demand / free_mem), icon="warning", default="no")
