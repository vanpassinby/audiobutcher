from copy import copy, deepcopy
from typing import Optional

from ab_random import *
from audio import Audio
from scrambler.segment import FrameInfo, SegmentInfo
from scrambler.memory import ScrambleMemory

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from slicing import Onsets

THOUSAND = 1000


class ScramblerConfigSubSustain:
    def __init__(self):
        self.crossfade: Optional[float] = None
        self.length: Optional[RandNumber] = None
        self.length_mode: Optional[int] = None
        # ^ Modes: 0 Total, 1 Portion N times, 2 % of portion, 3 % of segment, 4 % of fade-out
        self.length_exact: Optional[bool] = None
        self.portion_length: Optional[RandNumber] = None
        self.portion_proportional: Optional[bool] = None  # Use % of segment
        self.portion_minimum: Optional[float] = None
        # ^- If portion turns out to be < this, sustain length will be shortened
        self.shift_chance: Optional[RandChance] = None
        self.reverse_chance: Optional[RandChance] = None
        self.consec_chance: Optional[RandChance] = None
        self.allow_quan: Optional[bool] = None

    def convert_seconds(self):
        self.crossfade *= THOUSAND

        if self.length_mode == 0:
            self.length.convert_seconds()

        if not self.portion_proportional:
            self.portion_length.convert_seconds()

        self.portion_minimum *= THOUSAND

    def check_wrong_mode(self):
        return (
            self.length.check_wrong_mode() or
            self.length_mode == -1 or
            self.portion_length.check_wrong_mode()
        )

    def check_wrong_gauss(self):
        return self.length.check_wrong_gauss() or self.portion_length.check_wrong_gauss()

    def check_wrong_lognorm(self):
        return self.length.check_wrong_lognorm() or self.portion_length.check_wrong_lognorm()


class ScramblerConfigSubSkip:
    def __init__(self):
        self.min_skip: Optional[float] = None
        self.min_skip_chance: Optional[RandChance] = None
        self.add_dev: Optional[float] = None
        self.add_dev_chance: Optional[RandChance] = None

    def convert_seconds(self):
        self.min_skip *= THOUSAND
        self.add_dev *= THOUSAND


class ScramblerConfig:
    def __init__(self):
        self._overridden = {}

        # Misc
        self.in_seconds: Optional[bool] = None
        self.seed: Optional[str] = None

        # Trim
        self.trim1: Optional[float] = None
        self.trim2: Optional[float] = None
        self.trim_slices: Optional[bool] = None
        self.trim_slices2: Optional[bool] = None
        self.trim_loop_start: Optional[bool] = None
        self.trim_avgstart: Optional[bool] = None

        # Segment 0
        self.seg0_pause: Optional[bool] = None
        self.seg0_repeat: Optional[bool] = None
        self.seg0_sustain: Optional[bool] = None
        self.seg0_muted: Optional[bool] = None

        # Crossfade
        self.crossfade: Optional[RandNumber] = None
        self.crossfade_chance: Optional[RandChance] = None
        self.crossfade_comp_mode: Optional[int] = None  # Compensation: 0 Shorten, 1 Cut off (1 in stylus)

        # Speed
        self.speed_main: Optional[float] = None
        self.speed_alter_chance: Optional[RandChance] = None
        self.speed_variations: Optional[RandChoice] = None
        self.speed_affect_mode: Optional[int] = None
        # Modes: 0 - Don't affect, 1 - From main speed, 2 - From original speed

        # Segment duration
        self.duration_dist: Optional[RandNumber] = None
        self.reverse1_chance: Optional[RandChance] = None
        self.reverse2_chance: Optional[RandChance] = None
        self.reverse_double_mode: Optional[int] = None  # Modes: 0 Allow, 1 Only reverse-1, 2 Only reverse-2

        # Pause
        self.pause_dist: Optional[RandNumber] = None
        self.pause_chance: Optional[RandChance] = None
        self.pause_consec_chance: Optional[RandChance] = None
        self.pause_apply_effects: Optional[bool] = None

        # Segment volume
        self.volume_alt_chance: Optional[RandChance] = None
        self.volume_change: Optional[RandNumber] = None
        self.volume_direction: Optional[RandChoice] = None  # Softer vs Louder
        self.volume_mute_chance: Optional[RandChance] = None
        self.volume_mute_to_pause: Optional[RandChance] = None
        self.volume_mute_consec_chance: Optional[RandChance] = None
        self.volume_pause_is_mute: Optional[bool] = None

        # Fade-in
        self.fade_in_dist: Optional[RandNumber] = None
        self.fade_in_perc: Optional[bool] = None
        self.fade_in_plus_preroll: Optional[bool] = None
        self.fade_in_chance: Optional[RandChance] = None

        # Fade-out
        self.fade_out_dist: Optional[RandNumber] = None
        self.fade_out_perc: Optional[bool] = None
        self.fade_out_perc_note: Optional[bool] = None
        self.fade_out_chance: Optional[RandChance] = None

        # Fades: Misc
        self.fade_only_into_pauses: Optional[RandChance] = None
        self.fade_in_cut_dist: Optional[RandNumber] = None
        self.fade_in_cut_chance: Optional[RandChance] = None
        self.fade_out_cut_dist: Optional[RandNumber] = None
        self.fade_out_cut_chance: Optional[RandChance] = None

        # Segment repeats
        self.repeat_dist: Optional[RandNumber] = None
        self.repeat_chance: Optional[RandChance] = None
        self.repeat_in_mss: Optional[bool] = None
        self.repeat_consec_chance: Optional[RandChance] = None

        # Intro loop
        self.intro_loop_length: Optional[float] = None
        self.intro_loop_chance: Optional[RandChance] = None

        # Sustain
        self.sustain_chance: Optional[RandChance] = None
        self.sustain_weights: Optional[RandChoice] = None
        self.sustain_var1: Optional[ScramblerConfigSubSustain] = None
        self.sustain_var2: Optional[ScramblerConfigSubSustain] = None
        self.sustain_var3: Optional[ScramblerConfigSubSustain] = None
        self.sustain_var4: Optional[ScramblerConfigSubSustain] = None
        self.sustain_var5: Optional[ScramblerConfigSubSustain] = None

        # Average start times
        self.avgstart_chance: Optional[RandChance] = None
        self.avgstart_times: Optional[RandChoice] = None
        self.avgstart_deviation: Optional[float] = None
        self.avgstart_dev_direction: Optional[RandChoice] = None
        self.avgstart_dev_chance: Optional[RandChance] = None
        self.avgstart_force_pattern: Optional[RandChance] = None

        # Loop and pattern
        self.loop_pattern_chance: Optional[RandChance] = None
        self.loop_repeat_chance: Optional[RandChance] = None
        self.loop_begin: Optional[float] = None
        self.loop_count_full_length: Optional[RandChance] = None
        self.loop_count_pause_length: Optional[RandChance] = None
        self.loop_count_pattern_length: Optional[RandChance] = None
        self.loop_break_skips: Optional[RandChance] = None
        self.loop_break_pattern: Optional[RandChance] = None
        self.loop_break_avgstart: Optional[RandChance] = None

        # Skipping
        self.skip_chance: Optional[RandChance] = None
        self.skip_weights: Optional[RandChoice] = None
        self.skip_forw: Optional[ScramblerConfigSubSkip] = None
        self.skip_back: Optional[ScramblerConfigSubSkip] = None
        self.skip_rand: Optional[ScramblerConfigSubSkip] = None

        # Reappear after ... segments
        self.reappear_chance: Optional[RandChance] = None
        self.reappear_after_dist: Optional[RandNumber] = None
        self.reappear_reoccur_chance: Optional[RandChance] = None

        # Framing: Quantization
        self.quan_place_mode: Optional[int] = None
        self.quan_place_step: Optional[float] = None
        self.quan_place_strength: Optional[float] = None
        self.quan_place_onsets: Optional[Onsets] = None

        # Segment shifting
        self.shift_chance: Optional[RandChance] = None
        self.shift_deviation: Optional[RandNumber] = None
        self.shift_dev_proportional: Optional[bool] = None  # % of frame size (only when framing is on)
        self.shift_dev_direction: Optional[RandChoice] = None  # Forwards vs Backwards

        # Framing
        self.framing: Optional[bool] = None
        self.framing_frame_size: Optional[RandNumber] = None
        self.framing_seed: Optional[str] = None
        self.framing_speed_ratio = None
        self.framing_alt_reverse: Optional[bool] = None
        self.framing_force_duration: Optional[RandChance] = None
        self.framing_force_for_pattern: Optional[RandChance] = None
        self.framing_force_for_ast: Optional[RandChance] = None

        # Framing: Simplify
        self.fr_simplify: Optional[bool] = None
        self.fr_simplify_step: Optional[float] = None
        self.fr_simplify_severity: Optional[float] = None

        # Framing: Envelope
        self.fr_env_attack: Optional[bool] = None
        self.fr_env_attack_dist: Optional[RandNumber] = None
        self.fr_env_hold: Optional[bool] = None
        self.fr_env_hold_dist: Optional[RandNumber] = None
        self.fr_env_decay: Optional[bool] = None
        self.fr_env_decay_dist: Optional[RandNumber] = None
        self.fr_env_crossfade_endless: Optional[bool] = None

        # Framing: Length
        self.fr_length_soft: Optional[float] = None
        self.fr_length_hard: Optional[float] = None

        # Quantization
        self.quan_mode: Optional[int] = None  # 0 - None, 1 - Slices, 2 - BPM
        self.quan_bpm: Optional[float] = None
        self.quan_pattern: Optional[RandChance] = None
        self.quan_pattern_dir: Optional[int] = None  # 0 - Closer, 1 - Bigger, 2 - Smaller, 3 - Special* (Here: Equal)
        self.quan_ast: Optional[RandChance] = None
        self.quan_ast_dir: Optional[int] = None  # Spec here: Auto
        self.quan_loop: Optional[RandChance] = None
        self.quan_loop_dir: Optional[int] = None  # Spec here: None
        self.quan_skip: Optional[RandChance] = None
        self.quan_skip_dir: Optional[int] = None  # Spec here: Auto
        self.quan_duration: Optional[RandChance] = None
        self.quan_duration_dir: Optional[int] = None  # Spec here: None
        self.quan_duration_bpm_mode: Optional[int] = None  # 0 - By end position, 1 - By length
        self.quan_sustain: Optional[RandChance] = None
        self.quan_sustain_dir: Optional[int] = None  # Spec here: None
        self.quan_frame: Optional[RandChance] = None
        self.quan_frame_dir: Optional[int] = None  # Spec here: None
        self.quan_alt_slices: Optional[RandChance] = None

        # Quantization - Use alt slices (aka start onsets in AB2/3)
        self.quan_alt_pattern: Optional[bool] = None
        self.quan_alt_ast: Optional[bool] = None
        self.quan_alt_loop: Optional[bool] = None
        self.quan_alt_skip: Optional[bool] = None
        self.quan_alt_duration: Optional[bool] = None
        self.quan_alt_sustain: Optional[bool] = None
        self.quan_alt_frame: Optional[bool] = None

        # AudioButcher Programming Language
        self.abpl_enabled: Optional[bool] = None
        self.abpl_script = []

    def __getattribute__(self, item):
        overridden = object.__getattribute__(self, "_overridden")

        if item in overridden:
            return overridden[item]

        return object.__getattribute__(self, item)

    def override(self, key, value):
        object.__getattribute__(self, "_overridden")[key] = value

    def override_reset(self):
        object.__getattribute__(self, "_overridden").clear()

    @property
    def sustain_variants(self) -> list[Optional[ScramblerConfigSubSustain]]:
        return [self.sustain_var1, self.sustain_var2, self.sustain_var3, self.sustain_var4, self.sustain_var5]

    def convert_seconds(self):
        if not self.in_seconds:
            return

        self.trim1 *= THOUSAND
        self.trim2 *= THOUSAND

        self.crossfade.convert_seconds()
        self.duration_dist.convert_seconds()
        self.pause_dist.convert_seconds()

        if not self.fade_in_perc:
            self.fade_in_dist.convert_seconds()

        if not self.fade_out_perc:
            self.fade_out_dist.convert_seconds()

        if self.repeat_in_mss:
            self.repeat_dist.convert_seconds()

        self.intro_loop_length *= THOUSAND

        for element in self.sustain_variants:
            element.convert_seconds()

        for i in range(len(self.avgstart_times.elements)):
            self.avgstart_times.elements[i] *= THOUSAND
        self.avgstart_deviation *= THOUSAND

        self.loop_begin *= THOUSAND
        self.skip_forw.convert_seconds()
        self.skip_back.convert_seconds()
        self.skip_rand.convert_seconds()

        if self.quan_place_step > 0:
            self.quan_place_step *= THOUSAND

        if not self.shift_dev_proportional:
            self.shift_deviation.convert_seconds()

        self.framing_frame_size.convert_seconds()
        self.fr_simplify_step *= THOUSAND
        self.fr_env_attack_dist.convert_seconds()
        self.fr_env_hold_dist.convert_seconds()
        self.fr_env_decay_dist.convert_seconds()

        self.in_seconds = False


class ScramblerState:
    def __init__(self):
        self.target_length = 0
        self.current_goal = 0
        self.audio: Optional[Audio] = None
        self.config: Optional[ScramblerConfig] = None
        self.trim_zero = 0
        self.warnings = {}
        self.failed = False

        self.slices = []
        self.slices_alt = []
        self.slices_bpm = []
        self.slices_place = []
        self.loop_frames: list[FrameInfo] = []
        self.memory = ScrambleMemory()
        self.slicecr: Optional[Audio] = None
        self.random_state = None

        self.segment_dump: list[SegmentInfo] = []
        self.abpl_marks: dict[int, list[str]] = {}
        self.abpl_constants: dict[str, float] = {}

        self.scr_position_zero = 0
        self.scr_position = 0
        self.segment_idx = 0
        self.loop_position = 0
        self.loop_reset = False

        self.loop_can_repeat = True
        self.loop_rep_begin = None
        self.loop_rep_duration = None

        self.pause_new = True
        self.pause_prev = False
        self.pause_curr = False
        self.pause_next = False

        self.crossfade = 0
        self.crossfade_next = 0
        self.last_segment_length = 0  # Matters when no framing
        self.last_segment_crossfade = 0  # Matters when framing

        self.last_rep = False
        self.last_sus = False
        self.last_mut = False

    def get_copy_for_preview(self, duration):
        prev_copy = copy(self)
        prev_copy.scr_position = 0
        prev_copy.scr_position_zero = self.scr_position
        prev_copy.slicecr = self.slicecr.get_silence(duration)

        prev_copy.memory = deepcopy(self.memory)
        prev_copy.segment_dump = deepcopy(self.segment_dump)
        prev_copy.abpl_marks = deepcopy(self.abpl_marks)
        prev_copy.abpl_constants = deepcopy(self.abpl_constants)

        return prev_copy

    def warn(self, warn_type):
        if warn_type not in self.warnings:
            self.warnings[warn_type] = 0
        self.warnings[warn_type] += 1
