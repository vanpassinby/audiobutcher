import tkinter as tk
import tkinter.ttk as ttk

import gui.help_strings as h

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from state import CurConfig
    from gui.gui_main import MainWindow
    from gui.tab_pattern import LoopSkipVariant


class ToolTip:
    def __init__(self, parent, text, cur_config: "CurConfig"):
        self.root = None
        self.id = None
        self.parent = parent
        self.text = text
        self.cur_config = cur_config

        self.parent.bind("<Enter>", self.schedule_show)
        self.parent.bind("<Leave>", self.cancel)

    def schedule_show(self, event=None):
        self.cancel()
        if self.cur_config.show_hints:
            self.id = self.parent.after(1000, self.show_tip)

    def show_tip(self):
        if self.root or not self.cur_config.show_hints:
            return

        x = self.parent.winfo_rootx()
        y = self.parent.winfo_rooty() + self.parent.winfo_height()

        self.root = tk.Toplevel(self.parent)
        self.root.wm_overrideredirect(True)
        self.root.wm_geometry(f"+{x}+{y}")

        ttk.Label(self.root, text=self.text, relief="solid", anchor="center").pack(ipadx=4, ipady=2)

    def cancel(self, event=None):
        if self.id:
            self.parent.after_cancel(self.id)
            self.id = None
        self.hide_tip()

    def hide_tip(self):
        if self.root:
            self.root.destroy()
            self.root = None


def apply_tooltips(window: "MainWindow"):
    def tt(element, hint):
        if (not hasattr(element, "bind")) and hasattr(element, "root") and hasattr(element.root, "bind"):
            element = element.root
        ToolTip(element, hint, window.state.cur_config)

    def a_basic_tab():
        tab_basic = window.f_basic
        tt(tab_basic.l_duration, h.duration)
        tt(tab_basic.e_duration, h.rand_dist)
        tt(tab_basic.l_reverse1, h.reverse1)
        tt(tab_basic.e_reverse1, h.reverse1)
        tt(tab_basic.l_reverse2, h.reverse2)
        tt(tab_basic.e_reverse2, h.reverse2)

        tt(tab_basic.l_pause, h.pause)
        tt(tab_basic.e_pause, h.rand_dist)
        tt(tab_basic.l_pause_chance, h.chance)
        tt(tab_basic.e_pause_chance, h.chance)
        tt(tab_basic.l_consec_pause_chance, h.pause_consec_chance)
        tt(tab_basic.e_consec_pause_chance, h.pause_consec_chance)

        tt(tab_basic.l_crossfade, h.crossfade)
        tt(tab_basic.e_crossfade, h.rand_dist)
        tt(tab_basic.l_crossfade_chance, h.chance)
        tt(tab_basic.e_crossfade_chance, h.chance)

        tt(tab_basic.l_fadein, h.fade_in)
        tt(tab_basic.x_fadein_perc, h.fade_prop)
        tt(tab_basic.e_fadein, h.rand_dist)
        tt(tab_basic.l_fadein_chance, h.chance)
        tt(tab_basic.e_fadein_chance, h.chance)

        tt(tab_basic.l_fadeout, h.fade_out)
        tt(tab_basic.x_fadeout_perc, h.fade_prop)
        tt(tab_basic.e_fadeout, h.rand_dist)
        tt(tab_basic.l_fadeout_chance, h.chance)
        tt(tab_basic.e_fadeout_chance, h.chance)

        tt(tab_basic.l_fade_only_into_pauses, h.fade_only_info_pause)
        tt(tab_basic.e_fade_only_into_pauses, h.fade_only_info_pause)
        tt(tab_basic.x_fade_out_perc_note, h.fade_out_from_slice)

        tt(tab_basic.l_repeat, h.repeat)
        tt(tab_basic.e_repeat, h.rand_dist)
        tt(tab_basic.l_repeat_chance, h.chance)
        tt(tab_basic.e_repeat_chance, h.chance)
        tt(tab_basic.x_repeat_in_mss, h.repeat_mss)

        tt(tab_basic.l_reappear, h.reappear)
        tt(tab_basic.e_reappear, h.rand_dist_units)
        tt(tab_basic.l_reappear_chance, h.chance)
        tt(tab_basic.e_reappear_chance, h.chance)
        tt(tab_basic.l_reappear_reoccur_chance, h.reappear_reoccur)
        tt(tab_basic.e_reappear_reoccur_chance, h.reappear_reoccur)

        ### Basic > Speed change ###
        fr_speed = tab_basic.f_speed_change
        tt(fr_speed.l_speed_main, h.main_speed)
        tt(fr_speed.e_speed_main, h.main_speed)
        tt(fr_speed.c_speed_measure, h.speed_unit)
        tt(fr_speed.l_speed_alter, h.speed_alt_chance)
        tt(fr_speed.e_speed_alter, h.speed_alt_chance)
        tt(fr_speed.l_speed_variations, h.speed_alt_list)
        tt(fr_speed.e_speed_variations, h.speed_alt_list)
        tt(fr_speed.l_speed_weights, h.speed_alt_weight)
        tt(fr_speed.e_speed_weights, h.speed_alt_weight)
        tt(fr_speed.l_speed_affect_mode, h.speed_scale)
        tt(fr_speed.c_speed_affect_mode, h.speed_scale)

    def a_sustain():
        tab_sustain = window.f_sustain
        tt(tab_sustain.l_chance, h.sustain_chance)
        tt(tab_sustain.e_chance, h.sustain_chance)
        tt(tab_sustain.l_weights, h.sustain_weight)
        tt(tab_sustain.e_weights, h.sustain_weight)
        for sus_var in (tab_sustain.f_var1, tab_sustain.f_var2, tab_sustain.f_var3, tab_sustain.f_var4,
                        tab_sustain.f_var5):
            tt(sus_var.l_crossfade, h.sus_cross)
            tt(sus_var.e_crossfade, h.sus_cross)
            tt(sus_var.l_length, h.sus_length)
            tt(sus_var.e_length, h.rand_dist)
            tt(sus_var.l_length_mode, h.sus_len_mode)
            tt(sus_var.c_length_mode, h.sus_len_mode)
            tt(sus_var.x_length_exact, h.sus_len_exact)
            tt(sus_var.l_portion_length, h.sus_portion)
            tt(sus_var.e_portion_length, h.rand_dist)
            tt(sus_var.x_portion_proportional, h.sus_portion_p)
            tt(sus_var.l_portion_minimum, h.sus_portion_min)
            tt(sus_var.e_portion_minimum, h.sus_portion_min)

            tt(sus_var.x_allow_quan, h.sus_quantize)
            tt(sus_var.l_shift_chance, h.sus_shift)
            tt(sus_var.e_shift_chance, h.sus_shift)
            tt(sus_var.l_reverse_chance, h.sus_reverse)
            tt(sus_var.e_reverse_chance, h.sus_reverse)
            tt(sus_var.l_consec_chance, h.sus_consec)
            tt(sus_var.e_consec_chance, h.sus_consec)

    def a_pattern():
        # Loop
        sub_pattern = window.f_pattern.pattern.f_chances
        tt(sub_pattern.l_pattern, h.loop_pat)
        tt(sub_pattern.e_pattern, h.loop_pat)
        tt(sub_pattern.l_repeat, h.loop_rep)
        tt(sub_pattern.e_repeat, h.loop_rep)

        tt(sub_pattern.l_count_full_length, h.loop_full)
        tt(sub_pattern.e_count_full_length, h.loop_full)
        tt(sub_pattern.l_count_pause_length, h.loop_pause)
        tt(sub_pattern.e_count_pause_length, h.loop_pause)
        tt(sub_pattern.l_count_pattern_length, h.loop_count_pat)
        tt(sub_pattern.e_count_pattern_length, h.loop_count_pat)
        tt(sub_pattern.l_break_skips, h.loop_break_skip)
        tt(sub_pattern.e_break_skips, h.loop_break_skip)
        tt(sub_pattern.l_break_pattern, h.loop_break_pattern)
        tt(sub_pattern.e_break_pattern, h.loop_break_pattern)
        tt(sub_pattern.l_break_avgstart, h.loop_break_ast)
        tt(sub_pattern.e_break_avgstart, h.loop_break_ast)
        tt(window.f_pattern.pattern.l_loop_begin, h.loop_begin)
        tt(window.f_pattern.pattern.e_loop_begin, h.loop_begin)

        # Skipping
        sub_skip = window.f_pattern.pattern.f_skipping
        tt(sub_skip.l_chance, h.skip)
        tt(sub_skip.e_chance, h.skip)

        skip_var: "LoopSkipVariant"
        for skip_var, name in ((sub_skip.f_forw, "forwards"),
                               (sub_skip.f_back, "backwards"),
                               (sub_skip.f_rand, "chosen randomly")):
            tt(skip_var.l_weight, h.skip_weight.format(name))
            tt(skip_var.e_weight, h.skip_weight.format(name))
            tt(skip_var.l_min_skip, h.skip_min)
            tt(skip_var.e_min_skip, h.skip_min)
            tt(skip_var.l_min_skip_chance, h.chance)
            tt(skip_var.e_min_skip_chance, h.chance)
            tt(skip_var.l_add_dev, h.skip_add)
            tt(skip_var.e_add_dev, h.skip_add)
            tt(skip_var.l_add_dev_chance, h.chance)
            tt(skip_var.e_add_dev_chance, h.chance)

        # AST
        sub_ast = window.f_pattern.avg_st_times
        tt(sub_ast.l_chance, h.ast_main)
        tt(sub_ast.e_chance, h.ast_main)
        tt(sub_ast.l_times, h.ast_list)
        tt(sub_ast.e_times, h.ast_list)
        tt(sub_ast.l_weights, h.ast_weights)
        tt(sub_ast.e_weights, h.ast_weights)
        tt(sub_ast.l_deviation, h.ast_dev)
        tt(sub_ast.e_deviation, h.ast_dev)
        tt(sub_ast.l_dev_chance, h.chance)
        tt(sub_ast.e_dev_chance, h.chance)
        tt(sub_ast.l_dev_direction, h.ast_dir)
        tt(sub_ast.e_dev_direction, h.ast_dir)
        tt(sub_ast.l_force_pattern, h.ast_force)
        tt(sub_ast.e_force_pattern, h.ast_force)

    def a_framing():
        tab_framing = window.f_framing.general
        tt(tab_framing.x_enabled, h.framing_main)
        tt(tab_framing.l_frame_size, h.frame_dur)
        tt(tab_framing.e_frame_size, h.rand_dist)
        tt(tab_framing.x_use_seed, h.frame_seed)
        tt(tab_framing.e_seed, h.frame_seed)
        tt(tab_framing.l_speed_ratio, h.frame_ratio)
        tt(tab_framing.e_speed_ratio, h.frame_ratio_formula)
        tt(tab_framing.x_alt_reverse, h.frame_alt_rev)
        tt(tab_framing.l_force_duration, h.frame_force_dur)
        tt(tab_framing.e_force_duration, h.frame_force_dur)
        tt(tab_framing.l_force_for_pattern, h.frame_force_pat)
        tt(tab_framing.e_force_for_pattern, h.frame_force_pat)
        tt(tab_framing.l_force_for_ast, h.frame_force_ast)
        tt(tab_framing.e_force_for_ast, h.frame_force_ast)

        # Envelope
        sub_env = window.f_framing.envelope
        tt(sub_env.x_attack, h.fr_env_attack)
        tt(sub_env.e_attack_dist, h.rand_dist)
        tt(sub_env.x_hold, h.fr_env_hold)
        tt(sub_env.e_hold_dist, h.rand_dist)
        tt(sub_env.x_decay, h.fr_env_decay)
        tt(sub_env.e_decay_dist, h.rand_dist)
        tt(sub_env.x_crossfade_endless, h.fr_env_crossfade)

        # Alt length
        sub_fr_len = window.f_framing.alt_length
        tt(sub_fr_len.l_soft, h.fr_length_soft)
        tt(sub_fr_len.e_soft, h.fr_length_soft)
        tt(sub_fr_len.l_hard, h.fr_length_hard)
        tt(sub_fr_len.e_hard, h.fr_length_hard)

        # Simplify
        sub_fr_simp = window.f_framing.simplify
        tt(sub_fr_simp.x_enable, h.fr_simplify)
        tt(sub_fr_simp.l_step, h.fr_simp_step)
        tt(sub_fr_simp.e_step, h.fr_simp_step)
        tt(sub_fr_simp.l_severity, h.fr_simp_sever)
        tt(sub_fr_simp.e_severity, h.fr_simp_sever)

    def a_quantization():
        tab_quan = window.f_quantization.f_main
        tt(tab_quan.l_quan_mode, h.quan_mode)
        tt(tab_quan.c_quan_mode, h.quan_mode)
        tt(tab_quan.l_quan_bpm, h.quan_bpm)
        tt(tab_quan.e_quan_bpm, h.quan_bpm)

        tt(tab_quan.l_quan_pattern, h.quan_chance)
        tt(tab_quan.e_quan_pattern, h.quan_chance)
        tt(tab_quan.c_quan_pattern_dir, h.quan_direction+h.quan_spec_eq)

        tt(tab_quan.l_quan_ast, h.quan_chance)
        tt(tab_quan.e_quan_ast, h.quan_chance)
        tt(tab_quan.c_quan_ast_dir, h.quan_direction + h.quan_spec_auto)

        tt(tab_quan.l_quan_loop, h.quan_chance)
        tt(tab_quan.e_quan_loop, h.quan_chance)
        tt(tab_quan.c_quan_loop_dir, h.quan_direction)

        tt(tab_quan.l_quan_skip, h.quan_chance)
        tt(tab_quan.e_quan_skip, h.quan_chance)
        tt(tab_quan.c_quan_skip_dir, h.quan_direction + h.quan_spec_auto)

        tt(tab_quan.l_quan_duration, h.quan_chance)
        tt(tab_quan.e_quan_duration, h.quan_chance)
        tt(tab_quan.c_quan_duration_dir, h.quan_direction + h.quan_note_dur)

        tt(tab_quan.l_quan_sustain, h.quan_chance + h.quan_note_sus)
        tt(tab_quan.e_quan_sustain, h.quan_chance + h.quan_note_sus)
        tt(tab_quan.c_quan_sustain_dir, h.quan_direction)

        tt(tab_quan.l_quan_frame, h.quan_chance)
        tt(tab_quan.e_quan_frame, h.quan_chance)
        tt(tab_quan.c_quan_frame_dir, h.quan_direction + h.quan_note_dur)

        tt(tab_quan.l_quan_alt_slices, h.quan_alt)
        tt(tab_quan.e_quan_alt_slices, h.quan_alt)

    def a_misc():
        # Shifting
        sub_shift = window.f_misc.shift
        tt(sub_shift.l_deviation, h.shift)
        tt(sub_shift.e_deviation, h.rand_dist)
        tt(sub_shift.l_chance, h.chance)
        tt(sub_shift.e_chance, h.chance)
        tt(sub_shift.l_dev_direction, h.shift_dir)
        tt(sub_shift.e_dev_direction, h.shift_dir)
        tt(sub_shift.x_dev_proportional, h.shift_p)

        # Fade cutoff
        sub_cut = window.f_misc.cutoff
        tt(sub_cut.l_fade_in_cut_dist, h.fade_in_cut)
        tt(sub_cut.e_fade_in_cut_dist, h.rand_dist_units)
        tt(sub_cut.l_fade_in_cut_chance, h.chance)
        tt(sub_cut.e_fade_in_cut_chance, h.chance)
        tt(sub_cut.l_fade_out_cut_dist, h.fade_out_cut)
        tt(sub_cut.e_fade_out_cut_dist, h.rand_dist_units)
        tt(sub_cut.l_fade_out_cut_chance, h.chance)
        tt(sub_cut.e_fade_out_cut_chance, h.chance)

        # Volume
        sub_vol = window.f_misc.volume
        tt(sub_vol.l_alt_chance, h.chance)
        tt(sub_vol.e_alt_chance, h.chance)
        tt(sub_vol.l_change, h.vol_change)
        tt(sub_vol.e_change, h.rand_dist_units)
        tt(sub_vol.l_direction, h.vol_direction)
        tt(sub_vol.e_direction, h.vol_direction)
        tt(sub_vol.l_direction_hint, h.vol_direction)
        tt(sub_vol.f_mute.l_mute_chance, h.vol_mute)
        tt(sub_vol.f_mute.e_mute_chance, h.vol_mute)
        tt(sub_vol.f_mute.l_mute_to_pause, h.vol_mute_resize)
        tt(sub_vol.f_mute.e_mute_to_pause, h.vol_mute_resize)

        # Intro loop
        sub_intro = window.f_misc.intro_loop
        tt(sub_intro.l_intro_loop_length, h.intro_loop)
        tt(sub_intro.e_intro_loop_length, h.intro_loop)
        tt(sub_intro.l_intro_loop_chance, h.chance)
        tt(sub_intro.e_intro_loop_chance, h.chance)

        # Placement quantization
        sub_pq = window.f_misc.place_quan
        tt(sub_pq.c_mode, h.pq_main)
        tt(sub_pq.l_step, h.pq_step)
        tt(sub_pq.e_step, h.pq_step)
        tt(sub_pq.l_strength, h.pq_strength)
        tt(sub_pq.e_strength, h.pq_strength)
        tt(sub_pq.b_edit_onsets, h.pq_edit)

    def a_tweak():
        sub_consec = window.f_tweak.cons
        tt(sub_consec.x_seg0_pause, h.s0_pause)
        tt(sub_consec.x_seg0_repeat, h.s0_repeat)
        tt(sub_consec.x_seg0_sustain, h.s0_sustain)
        tt(sub_consec.x_seg0_muted, h.s0_mute)

        tt(sub_consec.x_volume_pause_is_mute, h.pause_is_mut)
        tt(sub_consec.l_repeat_consec_chance, h.consec_repeat)
        tt(sub_consec.e_repeat_consec_chance, h.consec_repeat)
        tt(sub_consec.l_volume_mute_consec_chance, h.consec_mute)
        tt(sub_consec.e_volume_mute_consec_chance, h.consec_mute)

        tt(window.f_tweak.abpl.root, h.abpl)

    a_basic_tab()
    a_sustain()
    a_pattern()
    a_framing()
    a_quantization()
    a_misc()
    a_tweak()
