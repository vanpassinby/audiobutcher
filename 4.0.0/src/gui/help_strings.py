### Common ###

rand_dist = """A random number is generated based on the given parameters.

Available modes include:
- Uniform: All numbers within the specified range have an equal probability of being selected.
- Gaussian: Parameters are the mean (average) and standard deviation. This follows the 68-95-99.7 rule.
- Clipped Gauss: Limits the Gaussian distribution to values within one standard deviation of the mean.
- Lognormal: Parameters are the mu and sigma of the lognormal distribution.
- Exponential: Takes a single parameter, 1/lambda of the exponential distribution.

Note: Lognormal mode does not support seconds, so lengths are always returned in milliseconds."""

rand_dist_units = """A random number is generated based on the given parameters.

Available modes include:
- Uniform: All numbers within the specified range have an equal probability of being selected.
- Gaussian: Parameters are the mean (average) and standard deviation. This follows the 68-95-99.7 rule.
- Clipped Gauss: Limits the Gaussian distribution to values within one standard deviation of the mean.
- Lognormal: Parameters are the mu and sigma of the lognormal distribution.
- Exponential: Takes a single parameter, 1/lambda of the exponential distribution."""

chance = "Chance for this effect to occur."
space_sep = "Enter them separated by spaces, without commas or other separators."

### Basic tab ###

duration = "Length of the segment body."
reverse1 = "Chance that the segment will be reversed.\nReversal is applied before sustain and fades."
reverse2 = "Chance that the segment will be reversed.\nReversal is applied after sustain and fades."
pause = "Length of gap between segments."
pause_consec_chance = "Allows pauses to occur one after another with a certain chance."

crossfade = "Length of fades between segments."
fade_in = "The volume increases linearly at the beginning of the segment over the specified time interval."
fade_out = "The volume decreases linearly at the end of the segment over the specified time interval."

fade_prop = "Change fade length to be measured as a percentage of the segment body length."
fade_only_info_pause = "Chance to disable the fade if it doesn't follow a gap (for fade-in),\nor isn't followed by a gap (for fade-out)."
fade_out_from_slice = "Instead of measuring the length as a percentage of the segment (default),\nmeasure the fade-out length as a percentage of the last slice."

repeat = "The segment body is repeated the specified number of times.\nThe value is rounded to the nearest whole number."
repeat_mss = "Measure the number of repeats by duration (in milliseconds or seconds), instead of a fixed count."
reappear = "The number of segments after which the segment will repeat.\nThe value is rounded to the nearest whole number."
reappear_reoccur = "Chance that the segment can reappear again after it has reappeared once."

### Speed change ###

main_speed = "The base speed at which the segment plays.\nAffects both tempo and pitch."
speed_unit = "The speed's unit of measurement."
speed_alt_chance = "Chance to use a different speed from the list below."
speed_alt_list = f"""All of the alternative speeds. {space_sep}

A speed range filler is also supported here.
Syntax is: RANGE [A B STEP], where A is the first speed and B is the last speed.
The range can be either ascending or descending, which is determined automatically.
STEP is optional and specifies the step between speeds; the default is 1.
Both A and B are always included in the range, even if the step would normally skip them.
Other speed variants can be listed before and after the range."""

speed_alt_weight = """The priority that each speed has over the rest. Leave this field empty for an even distribution.
For a speed range, specify a weight for each element."""

speed_scale = """Adjust segment lengths based on their speed.

For example, the main speed is 2x and the current speed is 3x.
By default, speed does not affect the final length.
In 'relative to main speed' mode, the segment will be 1.5 times shorter.
In 'relative to original speed' mode, it will be 3 times shorter."""

### Sustain ###

sustain_chance = "Chance to sustain a segment by looping its ending forward and backward."
sustain_weight = "Priorities for different sets of sustain parameters."
sus_cross = "Crossfade between sustain grains."
sus_length = "Sustain length."
sus_len_mode = "The mode that will be used to measure the sustain's length."
sus_len_exact = "Use the exact length specified, trimming the last grain if necessary.\nOtherwise, the length will be rounded up."
sus_portion = "The duration of a single grain."
sus_portion_p = "Measure grain length as a percentage of the segment length.\nOtherwise, the length is measured in absolute units (ms/sec)."
sus_portion_min = "If a grain is shorter than this value, the sustain is reduced to a single grain.\nUse this to avoid ringing artefacts at the end of the segment."
sus_quantize = "Enable grain length quantization (see more options on the Quantization tab)."
sus_shift = "Change to shift the end of the segment.\nFor example, if your segment is 3s long and the grain is 1s, the main body of the segment is reduced to 2s."
sus_reverse = "Additional chance to reverse the segment.\nThis is equivalent to the first reverse; together, this and first reverse cancel each other out."
sus_consec = "Chance for two consecutive segments to possibly have sustain."

### Pattern ###

loop_pat = "Chance for the segment to have a random start point.\nOtherwise, it will start roughly where the previous segment ended.\nSuch a segment is called an 'in-loop segment'."
loop_rep = "Chance that the segment will use the same start time and length as the previous segment.\nThis only applies when both segments are in loop."
loop_full = "Consider the segments end point as the moment it actually finishes in the original audio, including repeats and sustain.\nOtherwise, the end point is taken as the end of the segments body."
loop_pause = "Chance to consider gap length when calculating the segment's start time."
loop_count_pat = "Chance to consider the length of a pattern segment (but not its start) when calculating the in-loop segment's start time."
loop_can_break = "Chance that the next in-loop segment's start position\nwill be set to the end of {}."
loop_break_skip = loop_can_break.format("the segment that skips") + "\n(See 'skip' for more info)."
loop_break_pattern = loop_can_break.format("the pattern segment")
loop_break_ast = loop_can_break.format("AST segment") + "\n(See 'average start times' for more info)."
loop_begin = "The timestamp in the audio where the loop starts."

### Skipping ###

skip = """General skip chance,
i.e., the probability of shifting the start position of an in-loop segment by a certain distance.
Usually, skipping does not affect the start position of the next in-loop segment,
unless explicitly stated otherwise (see 'skipping can break loop')."""
skip_weight = "The weight of this skip direction variant.\nShift direction is {}."
skip_min = "A fixed amount to shift the segment's start position by."
skip_add = "An additional random shift applied to the segment's start position.\nThis value is drawn from a clipped Gaussian distribution."

### Average start times ###

ast_main = "Chance for a segment to use one of the 'average start times' (abbr. AST) instead of its default start time.\nAverage start times are custom timestamps that are more likely to be chosen as a segment's start than others."
ast_list = f"The list of all the ASTs. {space_sep}"
ast_weights = "The priority each AST has over the rest. Leave this field empty for an even distribution."
ast_dev = "Shift the AST by a small random amount. The shifting amount is drawn from a clipped Gaussian distribution."
ast_dir = "Weights for forward and backward shifts."
ast_force = "ASTs can only be applied to pattern segments. \nThis parameter gives a certain chance to force a segment to become a pattern segment when AST is selected."

### Framing ###
framing_main = """Enables the 'framing' mode, which overhauls certain parameters.
The main feature of this mode is that the audio is divided into consecutive 'frames' of a fixed length before scrambling starts. 
During scrambling, the frames are also processed sequentially, and segment lengths are adjusted to fit the frame by trimming.
For in-loop segments, their start time is also adjusted to align with the frame."""
frame_dur = "The lengths that frames can range between."
frame_seed = "Optionally, you can use a separate seed for frame length generation.\nThis is useful for when you want to preserve the same set of frames across multiple sessions."
frame_ratio = "Ratio of the frame length in the original audio to the frame length in the scrambled audio.\nFor example, a ratio of 2 halves the frame length, making the final loop twice as short."
frame_ratio_formula = """This field allows not only regular numbers, but also formulas.
Allowed symbols include: +, -, *, /, (, ).

Additionally, the following variable keywords can be used:
[LENGTH] - The original audio file's length (in seconds);
[LENGTH_SAMP] - The original audio file's length (in samples);
[SAMPLE_RATE] - The original audio file's sample rate."""

frame_alt_rev = "Use an alternative method for trimming reversed segment (second reverse)."
frame_force_dur = "Chance to override the segment body's length with the frame's length."
frame_force_pat = "Chance to override the start time and (optionally) the duration of a pattern segment.\nA random frame is selected from all available frames for this."
frame_force_ast = "Chance to override the start time and (optionally) the duration of a AST segment.\nA frame with the start time closest to the current AST is selected for this."

### Framing: Envelope ###

fr_env_attack = "Custom attack duration. If disabled, it defaults to the crossfade length."
fr_env_hold = "Hold duration. If disabled, the entire segment portion not covered by attack and decay will be held."
fr_env_decay = "Decay duration. If disabled, it defaults to 0.\nKEEP IN MIND: Decay has nothing to do with crossfade!"
fr_env_crossfade = """Crossfade is a short fading tail of the segment that extends beyond the frame.
This option completely disables trimming and fading,
so the segment plays in full, overlapping with the next one."""

### Framing: Misc ###

fr_length_soft = "Multiply the generated segment's length by the specified percentage.\nThis value can be either less than 100 or greater."
fr_length_hard = "Within the frame, keep only a portion of the segment.\nThe frame length itself remains unchanged.\nThis parameter cannot exceed 100%."

fr_simplify = "Enables simplify.\nThis option splits the audio into equal-length fragments\nand keeps only a part of the frames from each fragment."
fr_simp_step = "The length of a single fragment."
fr_simp_sever = "Specifies which portion of the fragment to keep.\nFor example, with a value of 50%, only frames whose start point lies within the first half of the fragment will be kept."

### Quantization ###

quan_mode = """Quantization allows snapping various timestamps to specific points in the original audio.

By default, quantization is disabled.
In Slices mode, timestamps are snapped to onsets, which must be preloaded.
In BPM mode, timestamps are quantized to the start of beats."""
quan_bpm = "The audio's tempo (in BPM)."
quan_chance = "Chance that quantization will be applied to this parameter."
quan_direction = "Determines the direction in which the timestamp will be rounded."
quan_spec_eq = "\nIn the special Equal mode, the segment start will be chosen as a random onset."
quan_spec_auto = "\nIn the special Auto mode, the rounding direction is chosen according to the direction of the deviation."
quan_note_dur = "\nNote that since the segment start and end times cannot coincide,\nthe segment length may be rounded up even if the opposite was specified."
quan_note_sus = "\nNote that for this, quantization must be enabled in the sustain settings."
quan_alt = """Chance to use an alternative set of onsets.
This works only in Slices mode, when alternative slices are loaded.
You can also specify which parameters the alternative quantization should be applied to."""

### Miscellaneous ###

shift = "Shift the segment's starting point in the scrambled audio by a specified distance."
shift_dir = "Shift direction weights: forward vs backward."
shift_p = "Use a portion (in percent) of the current segment's length as the shift distance.\nOtherwise, an absolute value (in ms/sec) is used."

fade_cut_clip = "\nThis parameter is measured as a percentage of volume (0-100; values above 100 are clipped to 100)."
fade_in_cut = "Instead of fading in from complete silence, fade from a different volume level." + fade_cut_clip
fade_out_cut = "Instead of fading out to complete silence, fade to a different volume level." + fade_cut_clip

vol_change = "Change the segment volume by a specified value.\nValues from the distribution are limited to the range 0-100,\nso the final volume can range from 0 to 200%."
vol_direction = "Weight for the direction of volume change: softer (0-100%) or louder (100-200%)."
vol_mute = "Chance to mute the segment (sets its volume to 0%)."
vol_mute_resize = "Chance that if the segment is muted, its length will be changed to match pause durations."

intro_loop = """Keep only the intro of the segment with the specified length,
then repeat it several times to fill the entire original length.
Setting this value to 0 disables the feature."""

pq_main = "Place segments only at specific points in the scrambled audio.\nYou can quantize placement to evenly spaced points or to a custom onset map."
pq_step = "Distance between two evenly spaced points.\n\nYou can also use negative values;\nin that case, the audio is split into the number of parts you specify."
pq_strength = """Quantization strength.
At 0%, it does nothing.
At 100%, it places the segment exactly on the onset point.
For values in between, the segment is positioned somewhere between its original location and the onset."""
pq_edit = "Modify the custom onset map.\nThis set of onsets is completely independent from the onsets used in 'regular' quantization."

### Tweaks ###

s0_pause = "For the first segment, assume that a pause preceded it."
s0_repeat = "For the first segment, assume that the preceding segment contained repeats."
s0_sustain = "For the first segment, assume that the preceding segment had sustain."
s0_mute = "For the first segment, assume that the preceding segment was muted."

pause_is_mut = "Count muted segments as pauses when calculating the chance of a consecutive pause."
consec_repeat = "Chance that a segment may have repeats if the preceding segment already had them."
consec_mute = "Chance that a segment may be muted if the preceding segment was muted."

abpl = "Modify the ABPL script, which allows creating complex dependencies between different effects.\nThe ABPL guide is available on the AudioButcher GitHub."
