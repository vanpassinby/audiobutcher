# ABPL: AudioButcher Programming Language - The Guide
**Warning: This guide is not finished.**

<details>
<summary><b>Table of сontents</b></summary>

* [Intro](#intro)
* [Basic syntax](#basic-syntax)
* [Numbers and variables](#numbers-and-variables)
  * [Numbers](#numbers)
  * [Units](#units)
  * [Variables](#variables)
  * [Two types of variables](#two-types-of-variables)
* [Command list](#command-list)
    - [Variables](#variables-1)
    - [Math](#math)
    - [Random](#random)
    - [Properties](#properties)
    - [Config reading](#config-reading)
    - [Inter-sessional](#inter-sessional)
    - [Quantization](#quantization)
* [Advanced syntax](#advanced-syntax)
  * [If statement](#if-statement)
  * [While loop](#while-loop)
  * [For loop](#for-loop)
  * [Loop breaking](#loop-breaking)
  * [Functions](#functions)
  * [Labels and jumping](#labels-and-jumping)
* [Appendix: Scrambler config options](#appendix-scrambler-config-options)
  * [Sustain](#sustain-variants-1-5)
  * [Skip](#skip-forwards-backwards-random)
  * [`force` options](#force-options)
</details>

## Intro
* This is *AudioButcher Programming Language*, a simple domain language made specifically for *AudioButcher v4.0*.
* AB runs the script written in this langauge after having already generated random segment, so its parameters can be slightly changed, with additional logic behind it.\
  For expample, you can make all segments long enough to be guaranteedly reversed.\
  However, it allows much more complicated behaviours as well.
* **WARNING!** There's no safeguard against infinite loops in ABPL; once an infinite loop is entered, AB gets softlocked.

## Basic syntax
* ABPL is a prefix language. It looks somehow similar to LISP, however the main difference is that there's no any brackets present.
* The commands read exactly as many arguments as they need, and each argument can itself be another command.\
  **Here's an example of ABPL syntax and its explanation:**\
  The line is `mul 2 add 3 4`.\
  The first command here is `mul`, which is responsible for multiplication. It needs to get two arguments;\
  First it reads `2`, and it gets interpreted as number *2*;\
  Then it reads `add`, which is another command responsible for adding two numbers.\
  So now it's `add` time to run. It reads `3` and `4` as numbers, and returns *7* to `mul`.\
  After `mul` has got its two arguments (*2* and *7*), it multiplies them, returning *14* to whatever called it.\
  **Also**, notice how adding got executed first, despite in math multiplication has higher priority.
* ABPL is case-sensitive;
* ABPL supports comments. Comment starts with `#`. It can be placed both at the start of line and in the middle of it.
  Anything that goes after `#` is being ignored. The only way to end a comment is starting a new line.
* Any type of bracket (`()[]{}`) and `,;:` are ignored and get read as space.\
  For readability, you can place brackets manually.\
  You can also make your ABPL code look like LISP or C-styled language, even Python, if that makes you comfortable.
* Using newline isn't different from using usual space.

## Numbers and variables
### Numbers
* Anything that starts with `1234567890-.` is interpreted as number.
* All numbers are stored as *float*.
* Some functions require *integer* numbers. In that case, the number is being rounded using math rules.
* Some functions require *boolean*. In that case, number first is rounded, then 0 turns to *false*, other numbers to *true*.
* Functions that are supposeddly boolean (for example, comparison ones) return *1* when the condition is true, and *0* if it's false.
* ABPL numbers support mathematical expressions, unless they don't contain separating symbols.\
  Unlike commands in ABPL, these mathematical expression follow the math rules, eg. `1+1/2` = *1.5*.

### Units
* ABPL has some sort of standard measurement units:
  * **Durations** are measured in *samples*,
  * **Angles** are measured in *radians*,
  * **Speed change** is measured in *speed multiplier*.
* For simpler usage, ABPL allows *unit suffixes* and *unit prefixes* to convert number in other units to default ones.
* There's also inverse functions to convert measures in default unit to the custom one.
* Here they are:
  | Unit | Converts to | Suffix | Prefix | Inverse |
  |---|---|---|---|---|
  | Milliseconds | Samples | `ms` | `ms` | `in_ms` |
  | Seconds | Samples | `sec` | `sec` | `in_sec` |
  | Minutes | Samples | `min` | `minutes` | `in_minutes` |
  | Percentages | Number | `%` | `perc` | `in_perc` |
  | Semitones | Speed multiplier | `st` | `semitones` | `in_semitones` |
  | Degrees | Radians | `deg` | `degrees` | `in_degrees` |
* For example, you want to know how many samples 100 milliseconds is.\
  You should use `200ms` or `ms 200`. If your audio sample rate is *44100*, both of these return *8820*.\
  Prefixes are useful when you take your number from variable, since you can't add suffix to the end of variable name.\
  If you want to know how many milliseconds 8820 samples are, you should use `in_ms 4410`, which returns *200* (if SR=44100).
* **Note:** volumes are measured in %, however you shouldn't use `%` suffixes for them. For example, the volume is 100, but what `100%` returns is just *1*.\
  The `%` is usable for finding a portion (eg. 60% of 500 = `mul 500 60%` = 300), but not for volume.

### Variables
* Variable value can be accessed by entering its name as command. 
* Variable can be changed using `set [var_name] [value]` command.
* When trying to access unitialised variable, it throws an error.
* Variables are erased for each new segment.
* All variables use the same namespace, so there's no local and global ones, despite ABPL does support functions.

### Two types of variables
There are two types of variables in ABPL:
* The first type is **temporary variable**. It gets created during the code execution, and doesn't affect anything by itself. However, it can be used in other part of program.
* The second type is **current segment property**. These are available from the very start of the script, and they directly affect the segment.\
  Here's all the properties:
  | Name | Description | Unit |
  |---|---|---|
  | `is_pause` | Is segment pause or not. | Boolean |
  | `is_avgstart` | Is segment start taken from AST list. | Boolean |
  | `is_in_loop` | Is segment start taken from current loop position. | Boolean |
  | `from_mem` | Was segment taken from memory (e.g. using AB's *Reappear after* feature) | Boolean |
  | `begin` | Segment start. | Samples (Integer) |
  | `duration` | Segment duration, before slowdown/repeats/sustain. | Samples (Integer) |
  | `speed` | Segment speed. | Speed multiplier (Floating) |
  | `repeats` | Number of segment repeats. | Integer |
  | `intro_loop` | Intro loop length. 0 means disabled. | Samples (Integer) |
  | `volume` | Segment volume. | % (Floating) |
  | `reverse1` | Segment is reversed (first reverse). | Boolean |
  | `reverse2` | Segment is reversed (second reverse). | Boolean |
  | `sustain` | Sustain length. | Samples (Integer) |
  | `sustain_exact` | Use exact sustain length. | Boolean |
  | `sustain_c` | Sustain crossfade. | Samples (Integer) |
  | `sustain_shift` | Sustain portion is shifted. | Boolean |
  | `sustain_portion` | Sustain portion length. | Samples (Integer) |
  | `fadein`, `fadeout` | Fade-in/out length. | Samples (Integer) |
  | `fadein_cut`, `fadeout_cut` | Fade-in/out "zero" volume. | % (Floating) |
  | `preroll_fadein` | Tweak: Add crossfade to fade-in | Boolean |
  | `k_speed` | Speed coefficent, which matters a lot in *loop repeat*. | Floating |

## Command list
### Variables
* `set [var_name] [value]`: Set variable `var_name` value to `value`.
  * If using `set` on segment property, the assigned value gets converted into what type segment property is.
* `var_exists [var_name]`: Returns if variable exists. This is only works for temp variables.
* `del_var [var_name]`: Delete the variable. This only works for temp variables.
* `round_samp_on` and `round_samp_off`: These are related to unit prefixes and suffixes.
  * The length in samples can't have a fractional part, so when converting time (ms/sec) to samples, the final value should be rounded. For example, if SR=44100, 1ms equals to 44.1 samples, but it can't have the fraction, so it gets rounded.
  * Ininially sample rounding is enabled, but you can disable it for some internal logic. However, when assigning any sample-based segment property, the value gets rounded anyway.

### Math
* Constants:
  * `_e`: Returns *e* constant, eg. 2.71828...
  * `pi`: Returns *pi* constant, eg. 3.14159...
* `abs`, `neg`, `round`, `floor`, `ceil`, `factorial`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`: Self-explanatory. The syntax is `command [n]`.
* `add`, `sub`, `mul`, `div`, `mod`, `min`, `max`: Self-explanatory. The syntax is `command [a] [b]`.\
  These return the result of on operation, but don't change the variable.
* `pow [a] [b]`: Returns the number *a* raised to the power *b*.
  * Square root can be calculated as `pow [number] 1/2`, cube root as `pow [number] 1/3`, etc.
  * Exponent (exp) can be calculated as `pow _e [number]`.
* `log [a] [b]`: Returns the logarithm of *a* to the base *b*.
  * Natural logarithm (ln) can be calculated as `log [number] _e`.
* `not [a]`, `and [a] [b]`, `or [a] [b]`, `xor [a] [b]`: Boolean operations, self-explanatory.
* `equal`, `unequal`, `close`, `more`, `less`, `more_or_eq`, `less_or_eq`: Comparisons, self-explanatory. The syntax is `command [a] [b]`. For example, `more [a] [b]` = `[a] > [b]`.
  * Among these, `close` is quite unusual. It determines if values are *approximately* the same, e.g. the difference is millionth etc.. This is handy when comparing floating numbers calculated using other functions.
* `in_range`, `in_range_strict`, `in_range_str_left`, `in_range_str_right`: Double comparison, the syntax is `command [value] [left_border] [right_border]`.
  * `in_range` = [left, right],
  * `..._strict` = (left, right),
  * `..._str_left` = (left, right],
  * `..._str_right` = [left, right).
* `ms`, `sec`, `minutes`, `perc`, `semitones`, `degrees`: See *Units* chapter.
* `in_ms`, `in_sec`, `in_minutes`, `in_perc`, `in_semitones`, `in_degrees`: The opposite of the previous ones.

### Random
* `rand_chance [chance]`: Returns `1` with a certain *chance*, else returns `0`. Chance is measured in %.
* `rand_int [a] [b]`: Returns random integer from between `a` and `b`, including these.
* `rand_uniform`, `rand_gauss`, `rand_gauss_clip`, `rand_lognorm`: Their syntax is `rand_... [value1] [value2]`. Returns values using given distribution. Since these functions are pulled from AB random module, they never return negative values.
* `rand_exp [value]`: Another command from AB random module. Is no different from other ones, besides only taking one argument.
* `ab_random_sp [mode]`: Generate new segment start position using the default AB algorithms, and instantly apply it. The modes include `auto` (generate based on current segment parameters), `in_loop`, `avgstart`, `pattern`.

### Properties
* Return current segment's property values. See *two types of variables* chapter for more.
  * Integer-based: `begin`, `duration`, `repeats`, `intro_loop`, `fadein`, `fadeout`, `sustain`, `sustain_c`, `sustain_portion`.
  * Floating-based: `speed`, `volume`, `fadein_cut`, `fadeout_cut`, `k_speed`.
  * Boolean-based: `is_pause`, `is_avgstart`, `is_in_loop`, `from_mem`, `preroll_fadein`, `reverse1`, `reverse2`, `sustain_exact`, `sustain_shift`.
* Get some information about the current scrambling:
  * `k_speed_now`: Calculates the current *speed coefficent*, based on current *segment speed* and *length scaling mode* 
  * `segment_idx`: Ordinal number of the current segment. Counting starts from 0.
  * `audio_sample_rate`: Audio sample rate.
  * `audio_length`: Audio length (in samples).
  * `rendered_length`: Currently rendered length (in samples).
  * `target_length`: Target scrambled audio length (in samples).
  * `loop_position`: Position in the audio loop (in samples).
  * `amt_frames`: Amount of frames. If *Framing* is disabled, returns 0.
  * `amt_onsets`, `amt_onsets_alt`: Amount of onsets for slices (ref AB *Slicing*).
    * `..._alt` is for alternative slices.
  * `prop_by_idx [segment_index] [prop_name]`: Get information about other segment property by its index.
    * The first segment has index 0.
    * The set of `prop_name` values is exactly the same as set of current segment properties.
    * You can get info about the previous segment by using `prob_by_idx (sub current_segment_idx 1) [prop_name]`.
    * If segment with such index does not exist, it returns 0.
  * `onset_by_idx [idx]`, `onset_by_idx_alt[idx]`: Get the onset position (in sampled) based on its index.
    * `..._alt` is for alternative slices onsets.
  * `frame_by_idx [idx] [paramter]`: Get information about the frame by its index (ref AB *Framing*).
    * Parameter can be `begin`, `duration` and `content_dur`. Names are self-explationary, all are measured in samples.
    * Be careful: Don't use this when `Framing` is disabled, with non-existent frame indexes, or non-existent parameters.
  * `segment_end_pos [idx]`. Get segment body end position in original audio. This includes speed change.
    * For current segment, you can use `segment_end_pos segment_idx`.
    * This is unavailable in original AB 4.0 October Release.

### Config reading
* `from_config`, `from_config_skip`, `from_config_sustain`: These have similar usage and particular qualities.
  * They allow you to get values directly from scrambler parameters. The list of parameters/options is at the end of this doc.
  * Some parameters are random numbers or chances. In that case, it returns one of random values within the random pattern specified in config.
  * It doesn't return values in their default measures.
    * For example, lengths are returned in milliseconds. But never in seconds, even if *seconds mode* is enabled in AB.
    * Some parameters responsinble for the same thing can be in differnt measures at differnt times. For example, fade-in/out length can be either in milliseconds or in % of segment body, depending on other paraters.
  * `from_config [option_name]` is responsible for the most of scrambling parametes.
  * `from_config_skip [skip_id] [option]` is responsible for *Skipping* parameters (*Pattern > Loop > Skipping*).
    * `skip_id` = 0 for *forwards* one, 1 for *backwards*, 2 for *random*.
  * `from_config_sustain [var_id] [option]` is responsible for *Sustain* parameters.
    * `var_id` = 0 for *Variant 1*, 1 for *Variant 2*, etc.
* `force [option_name] [value]`: ABPL processing isn't the last thing is done during random segment generation. This command allows you to predefine random generation result or temporarily override some parameter. The list of parameters is at the end of this guide.

### Inter-sessional
* **Constants**. Constant works as a variable, however it's available during the entire process of scrambling.
  * `const [name]`: Access a constant.
  * `const_set [name] [value]`: Assign constant value.
* **Marks**. Segments can be marked with a special keyword, visible during the entire scrambling process.
  * `has_mark [seg_idx] [mark_name]`: Does segment at index `seg_idx` has mark `mark_name`.
  * `mark_add [seg_idx] [mark_name]`: Mark segment with this.
  * `mark_remove [seg_idx] [mark_name]`: Remove this mark from segment.

### Quantization
You can apply quantization as well. It quantizes only using current scrambler parameters. So, if quantization is disabled, this won't do anything.
* `quan_config [op_name] [op_value]`: Since quantization has some optional parameters, it's impossible to use it quickly with ABPL syntax. So you can configure it first using this command. The options inclide:
  * `use_alt`: Use alternative slices (if possible). Values are 0/1.
  * `min_pos` and `max_pos`: Boundaries for quantized number. Measured in samples.
* `quan_config_clear`: Clear the config.
* `quantize`, `quantize_forw`, `quantize_back`. Return the quantized number. Syntax is `quantize... [number]`, argument and result are both in samples.
  * "Usual" quantize quantizes to the closest point, `..._forw` always round up, `..._back` always rounds down.
* `ab_quantize_length`. Quantize current segment length using the default AB algorithm, and instantly apply it.

## Advanced syntax
### If statement
* ABPL supports *if statements*. Here's the syntax:
  ```
  if [condition]
     [do_something]
  end_if
  ```
* It also supports *if-else* statements:
  ```
  if [condition]
     [do_something]
  else
    [do_something_else]
  end_if
  ```
* ABPL does **not** support *elif* constructions.

### While loop
* ABPL supports *while loop*. Here's the syntax:
  ```
  while [condition]
     [do_something]
  end_while
  ```
* It checks the condition before executing loop body.

### For loop
* ABPL supports *for loop*. Here's the syntax:
  ```
  for [variable] [from] [to] [step]
     [do_something]
  end_for
  ```
* `variable` is variable name, and `from`, `to` and `step` are numbers.
* The range always includes `from` and always excludes `to` values.
* In the loop, you can effectively change the key variable value.\
  However, when the new loop instance begins, this variable gets to its next value as if it wasn't changed.
* Remember there's no global and local variables, so at the end of the loop, this variable remains at its last value.

### Loop breaking
* In ABPL, loops can be broken.
* `stop_loop` fully aborts the loop;
* `skip_loop` skips all loop body code that goes after it, and loop continues.

### Functions
* ABPL supports functions.
* Functions are declated like this:
  ```
  define [func_name] [N_args] [arg1 arg2 ... argN]
    [function_body]
  end_def
  ```
* `N_args` is the amount of arguments your function takes, and is followed by list of argument names.
* If your function has no arguments, `N_args` is 0, and 0 is followed by function body.
* To return something or stop the function, use `return [value]` command. If no return used, function returns 0 after it finishes.
* Function is called by using its name as command, followed by arguments if present.
* Function can't be called before assignment;
* Be careful and avoid using outer variable names as arguments, unless you know what you're doing.\
  Since there's no local variables, when calling a function, variables with the name of argument are being set to the value you specified when calling a function.
* ABPL supports nested function. After function defined inside the other function, it gets visible everywhere.

### Labels and jumping
* ABPL supports labels and jumping.
* `label`:
  * To specify the jump point, use `label [lab_name]`.
  * Specifying labels inside ifs and loops isn't recommended.
* `goto`:
  * To jump, use the `goto [lab_name]` command.
  * After jumping, all loops and ifs get aborted.
  * You can jump both forwards and backwards.
* `break`:
  * This command aborts your whole script.
  * It's very strong, killing the script even if called inside a function.
* An example:
  ```
  set a 0
  label point1

  if equal a 1
     set duration 3000ms
     break
  end_if

  set a 1
  goto point1
  ```
  This one sets `a` to 0, thus skipping the `if` part. Then it sets `a`=1, jumps back to `if` part, and executes it. The `break` kills the script to avoid infinite loop.

## Appendix: Scrambler config options
Here's all the possible option names. Currently, they are uncategorised:\
`trim1`, `trim2`, `trim_slices`, `trim_slices2`, `trim_loop_start`, `trim_avgstart`,\
`seg0_pause`, `seg0_repeat`, `seg0_sustain`, `seg0_muted`,\
`crossfade`, `crossfade_chance`, `crossfade_comp_mode`,\
`speed_main`, `speed_alter_chance`, `speed_variations`, `speed_affect_mode`,\
`duration_dist`, `reverse1_chance`, `reverse2_chance`, `reverse_double_mode`,\
`pause_dist`, `pause_chance`, `pause_consec_chance`, `pause_apply_effects`,\
`volume_alt_chance`, `volume_change`, `volume_direction`, `volume_mute_chance`, `volume_mute_to_pause`, `volume_mute_consec_chance`, `volume_pause_is_mute`,\
`fade_in_dist`, `fade_in_perc`, `fade_in_plus_preroll`, `fade_in_chance`,\
`fade_out_dist`, `fade_out_perc`, `fade_out_perc_note`, `fade_out_chance`, `fade_only_into_pauses`,\
`fade_in_cut_dist`, `fade_in_cut_chance`, `fade_out_cut_dist`, `fade_out_cut_chance`,\
`repeat_dist`, `repeat_chance`, `repeat_in_mss`, `repeat_consec_chance`,\
`intro_loop_length`, `intro_loop_chance`,\
`sustain_chance`, `sustain_weights`,\
`avgstart_chance`, `avgstart_times`, `avgstart_deviation`, `avgstart_dev_direction`, `avgstart_dev_chance`, `avgstart_force_pattern`,\
`loop_pattern_chance`, `loop_repeat_chance`, `loop_begin`, `loop_count_full_length`, `loop_count_pause_length`, `loop_count_pattern_length`, `loop_break_skips`, `loop_break_pattern`, `loop_break_avgstart`,\
`skip_chance`, `skip_weights`,\
`reappear_chance`, `reappear_after_dist`, `reappear_reoccur_chance`,\
`quan_place_mode`, `quan_place_step`, `quan_place_strength`,\
`shift_chance`, `shift_deviation`, `shift_dev_proportional`, `shift_dev_direction`,\
`framing`, `framing_frame_size`, `framing_seed`, `framing_speed_ratio`, `framing_alt_reverse`, `framing_force_duration`, `framing_force_for_pattern`, `framing_force_for_ast`,\
`fr_simplify`, `fr_simplify_step`, `fr_simplify_severity`,\
`fr_env_attack`, `fr_env_attack_dist`, `fr_env_hold`, `fr_env_hold_dist`, `fr_env_decay`, `fr_env_decay_dist`, `fr_env_crossfade_endless`, `fr_length_soft`, `fr_length_hard`,\
`quan_mode`, `quan_bpm`, `quan_pattern`, `quan_pattern_dir`, `quan_ast`, `quan_ast_dir`, `quan_loop`, `quan_loop_dir`, `quan_skip`, `quan_skip_dir`, `quan_duration`, `quan_duration_dir`, `quan_duration_bpm_mode`, `quan_sustain`, `quan_sustain_dir`, `quan_frame`, `quan_frame_dir`,\
`quan_alt_slices`, `quan_alt_pattern`, `quan_alt_ast`, `quan_alt_loop`, `quan_alt_skip`, `quan_alt_duration`, `quan_alt_sustain`, `quan_alt_frame`.

### Sustain (Variants 1-5)
| Option | Full name | Data type |
|---|---|---|
| `crossfade` | Sustain crossfade | Milliseconds |
| `length` | Sustain length | Random, Milliseconds **OR** Floating |
| `length_mode` | Sustain length measure | 0 - Total length,<br>1 - Portion [N] times,<br>2 - % of portion,<br>3 - % of segment,<br>4 - % of fade-out. |
| `length_exact` | Sustain length: exact | Boolean |
| `portion_length` | Sustain portion length | Random, Milliseconds **OR** % ratio |
| `portion_proportional` | Sustain portion: proportinal to segment length | Boolean |
| `portion_minimum` | Minimal required portion | Milliseconds |
| `shift_chance` | Sustain: Portion shift [chance] | Random, Boolean |
| `reverse_chance` | Sustain: Reverse [chance] | Random, Boolean |
| `consec_chance` | Sustain: Consecutiveness [chance] | Random, Boolean |
| `allow_quan` | Sustain: Allow portion quantization | Boolean |

### Skip (Forwards, Backwards, Random)
| Option | Full name | Data type |
|---|---|---|
| `min_skip` | Minimum skip | Milliseconds |
| `min_skip_chance` | Minimum skip [chance] | Random, Boolean |
| `add_dev` | Additional deviation | Milliseconds<br>[Use random manually] |
| `add_dev_chance` | Additional deviation [chance] | Random, Boolean |

### `force` options
| option_name | Full name | Possible values |
|---|---|---|
| `reappear` | Reappear | 0/1 |
| `reappear_after` | Reappear interval | Positive integer |
| `reappear_reoccur` | Allow reocurrence | 0/1 |
| `loop_repeat` | Loop: Repeat | 0/1 |
| `framing_speed_ratio` | Framing: Speed ratio | Floating, <=0 defaults to 1 |
| `framing_alt_reverse` | Framing: Alternative reverse mode | 0/1 |
| `fr_length_hard` | Framing: Hard cutoff | Floating, %, >100 defaults to 100 |
| `fr_env_attack` | Framing envelope: Custom attack | 0/1 |
| `fr_env_hold` | Framing evnelope: Custom hold | 0/1 |
| `fr_env_decay` | Framing envelope: Custom decay | 0/1 |
| `fr_env_crossfade_endless` | Framing envelope: Endless crossfade | 0/1 |
| `fr_env_attack_dur` | Framing envelope: Custom attack - duration | Floating, length in ms |
| `fr_env_hold_dur` | Framing envelope: Custom hold - duration | Floating, length in ms |
| `fr_env_decay_dur` | Framing envelope: Custom decay - duration | Floating, length in ms |
| `shift` | Segment shift | 0/1 |
| `shift_prop` | Segment shift: Proportional to frame length | 0/1 |
| `shift_dur` | Segment shift: Distance | Floating, length in ms **OR** % ratio |
| `shift_direct` | Segment shift: Direction | 0 - Backwards, 1 - Forwards |
| `loop_count_full_length` | Looping: Count full length | 0/1 |
| `loop_count_pause_length` | Looping: Count pause length | 0/1 |
| `loop_count_pattern_length` | Looping: Count pattern length | 0/1 |
| `loop_break_skips` | Looping: Skips can break loop | 0/1 |
| `loop_break_pattern` | Looping: Pattern can break loop | 0/1 |
| `loop_break_avgstart` | Looping: AST can break loop | 0/1 |
