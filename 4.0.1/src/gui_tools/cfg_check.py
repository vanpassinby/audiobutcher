from state import ABState
from scrambler.scr_state import ScramblerConfig
from ab_random import RandNumber
from common import AB_FLOAT16_AUDIO, AB_DISABLE_PSUTIL
import tkinter.messagebox as mb
from localization import loc

import psutil
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui_main import MainWindow

m_loc = loc["cfg_check"]


def wrong_audio(state: ABState):
    if not state.audio:
        mb.showerror(loc["messages"]["error"], m_loc["msg_import"])
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
        config.quan_duration_bpm_mode, gui.f_tweak.main.c_random_start_selection.current()
    ]

    wrong = (wrong_combo or
        any(obj.check_wrong_mode() for obj in config.sustain_variants) or
        any(obj.check_wrong_mode() for obj in config.__dict__.values() if isinstance(obj, RandNumber))
    )

    if wrong:
        mb.showerror(loc["messages"]["error"], m_loc["msg_dropdowns"])
    return wrong


def wrong_gauss(config: ScramblerConfig):
    wrong = (
        any(obj.check_wrong_gauss() for obj in config.sustain_variants) or
        any(obj.check_wrong_gauss() for obj in config.__dict__.values() if isinstance(obj, RandNumber))
    )

    if wrong:
        mb.showerror(loc["messages"]["error"], m_loc["msg_clipped_gauss"])
    return wrong


def wrong_lognorm(config: ScramblerConfig):
    wrong = (
        any(obj.check_wrong_lognorm() for obj in config.sustain_variants) or
        any(obj.check_wrong_lognorm() for obj in config.__dict__.values() if isinstance(obj, RandNumber))
    )

    if wrong:
        return not mb.askyesno(loc["messages"]["warning"], m_loc["msg_warn_lognorm"], default=mb.NO, icon="warning")
    else:
        return False


def wrong_zero_weights(config: ScramblerConfig):
    cause = None
    m_loc2 = m_loc["msg_zero_weights_params"]

    if config.speed_alter_chance.chance > 0 and config.speed_variations.check_wrong_zero_sum():
        cause = m_loc2["speed"]
    elif config.sustain_chance.chance > 0 and config.sustain_weights.check_wrong_zero_sum():
        cause = m_loc2["sustain"]
    elif config.loop_pattern_chance.chance < 100 and config.skip_chance.chance > 0 and \
            config.skip_weights.check_wrong_zero_sum():
        cause = m_loc2["skip_dir"]
    elif config.avgstart_chance.chance > 0 and config.avgstart_times.check_wrong_zero_sum():
        cause = m_loc2["ast"]
    elif config.avgstart_chance.chance > 0 and config.avgstart_dev_chance.chance > 0 and \
            config.avgstart_dev_direction.check_wrong_zero_sum():
        cause = m_loc2["ast_dev"]
    elif config.shift_chance.chance > 0 and config.shift_dev_direction.check_wrong_zero_sum():
        cause = m_loc2["shift_dir"]
    elif config.volume_alt_chance.chance > 0 and config.volume_direction.check_wrong_zero_sum():
        cause = m_loc2["volume"]

    if cause is not None:
        mb.showerror(loc["messages"]["error"], m_loc["msg_zero_weights"].format(PARAM=cause))
        return True
    else:
        return False


def wrong_zero_seg(config: ScramblerConfig):
    wrong_seg = config.duration_dist.is_zero()
    wrong_frm = config.framing_frame_size.is_zero() and config.framing
    if wrong_seg:
        mb.showerror(loc["messages"]["error"], m_loc["msg_zero_segm_length"])
    elif wrong_frm:
        mb.showerror(loc["messages"]["error"], m_loc["msg_zero_frame_length"])
    return wrong_seg or wrong_frm


def wrong_speeds(config: ScramblerConfig):
    right = all(0 < speed for speed in config.speed_variations.elements)
    wrong = config.speed_main <= 0 or (config.speed_alter_chance.chance > 0 and not right)

    if wrong:
        mb.showerror(loc["messages"]["error"], m_loc["msg_negative_speed"])
    return wrong


def wrong_speed_w(config: ScramblerConfig):
    if config.speed_alter_chance.chance <= 0:
        return False

    a = len(config.speed_variations.elements)
    b = len(config.speed_variations.weights)

    if a!=b:
        mb.showerror(loc["messages"]["error"], m_loc["msg_spd_weight_mismatch"].format(E=a, W=b))
    return a!=b


def wrong_ast_w(config: ScramblerConfig):
    if config.avgstart_chance.chance <= 0:
        return False

    a = len(config.avgstart_times.elements)
    b = len(config.avgstart_times.weights)

    if a!=b:
        mb.showerror(loc["messages"]["error"], m_loc["msg_ast_weight_mismatch"].format(E=a, W=b))
    return a!=b


def wrong_sustain_portion(config: ScramblerConfig):
    if config.sustain_chance.chance <= 0:
        return False

    for i in range(len(config.sustain_weights.elements)):
        if config.sustain_weights.weights[i] > 0:
            if config.sustain_variants[i].portion_length.is_zero():
                mb.showerror(loc["messages"]["error"], m_loc["msg_zero_sustain"].format(N_VAR=i+1))
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
        mb.showerror(loc["messages"]["error"], m_loc["msg_framing_wrong_math"])
    return wrong


def wrong_slices(gui: "MainWindow", state: ABState, config: ScramblerConfig):
    if config.quan_mode == 1 and not state.slices.are_there:
        switch = mb.askyesno(loc["messages"]["error"], m_loc["msg_quan_slice"], icon="error")
        if switch:
            gui.f_tabs.select(gui.f_quantization.root)
        return True

    if config.quan_mode == 2 and config.quan_bpm == 0:
        mb.showerror(loc["messages"]["error"], m_loc["msg_zero_bpm"])
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
        warn_txt = m_loc["msg_warn_performance"].format(REQ=round(mem_demand/1024/1024), PERC=mem_demand/free_mem)
        return not mb.askyesno(loc["messages"]["warning"], warn_txt, icon="warning", default="no")
