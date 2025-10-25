import math
from audio import Audio


class FrameInfo:
    def __init__(self, begin: int, duration: int, content_dur: int):
        self.begin = begin
        self.duration = duration
        self.content_dur = content_dur


class SegmentInfo:
    is_pause, is_avgstart, is_in_loop, from_mem = [False] * 4
    begin, duration, speed, repeats, intro_loop = [None] * 5
    volume, reverse1, reverse2 = [None] * 3
    sustain, sustain_exact, sustain_c, sustain_shift, sustain_portion = [None] * 5
    fadein, fadein_cut, fadeout, fadeout_cut = [None] * 4
    preroll_fadein, crossfade, k_speed = [None] * 3

    @property
    def as_dict(self):
        return self.__dict__

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value


def calculate_begin_end(info: SegmentInfo, crossfade: int, audio_length: int):
    segment_begin = info.begin
    segment_end = segment_begin + math.ceil(info.duration * info.speed)
    max_crossfade = max(crossfade, info.crossfade * (info.repeats > 0))
    cross_shift = math.ceil(max_crossfade * info.speed)

    if info.reverse1:
        segment_end += cross_shift
        segment_end = min(segment_end, audio_length)
    else:
        segment_begin -= cross_shift
        segment_begin = max(segment_begin, 0)

    cross_available = int((segment_end - segment_begin) / info.speed - info.duration)
    crossfade_internal = min(info.crossfade * (info.repeats > 0), cross_available)
    crossfade_external = min(crossfade, cross_available)

    return segment_begin, segment_end, crossfade_external, crossfade_internal


def calculate_real_sustain(desired_length: int, portion_length: int, crossfade: int):
    portion_shift = portion_length - crossfade
    return portion_length + math.ceil((desired_length - portion_length) / portion_shift) * portion_shift


def precalculate_length(info: SegmentInfo, crossfade: int, audio_length: int, pause_effects=True):
    count_effects = pause_effects or not info.is_pause

    crossfade = calculate_begin_end(info, crossfade, audio_length)[2]
    length = info.duration
    length += length * (info.repeats if count_effects else 0)
    length += crossfade

    if count_effects and info.sustain > 0:
        if info.sustain_exact:
            length += info.sustain - info.sustain_c
        else:
            length += calculate_real_sustain(info.sustain, info.sustain_portion, info.sustain_c)
            length -= info.sustain_c
        length -= info.sustain_portion * info.sustain_shift

    return length, crossfade


def compensate_fades(fadein: int, fadeout: int, segment_length: int):
    fade_sum = fadein + fadeout
    if fade_sum > segment_length:
        fadein = int(fadein * segment_length / fade_sum)
        fadeout = int(fadeout * segment_length / fade_sum)

    return fadein, fadeout


def add_repeats(segment: Audio, info: SegmentInfo, crossfade_in: int):
    base_segment = segment.get_part(-info.duration - crossfade_in, None)
    segment_length = segment.length
    base_length = base_segment.length
    final_length = segment_length + (base_segment.length - crossfade_in) * info.repeats

    segment_fadein = base_segment.get_copy()
    segment_fadein.fade_in(crossfade_in)
    segment_2fades = segment_fadein.get_copy()
    segment_2fades.fade_out(crossfade_in)

    segment.extend(final_length, crossfade_in)
    position = segment_length - crossfade_in
    for i in range(info.repeats-1):
        segment.place(segment_2fades, position)
        position += base_length - crossfade_in

    segment.place(segment_fadein, position)


def add_sustain(segment: Audio, info: SegmentInfo):
    # Get one "granule"
    if info.sustain_shift:
        tail_part = segment.get_part(-info.sustain_portion * 2, -info.sustain_portion)
        segment.crop(0, -info.sustain_portion)
    else:
        tail_part = segment.get_part(-info.sustain_portion, None)

    # Calculate length after adding sustain
    final_length = segment.length - info.sustain_c
    if info.sustain_exact:
        final_length += info.sustain
    else:
        final_length += calculate_real_sustain(info.sustain, info.sustain_portion, info.sustain_c)

    # Create sub-granules
    tail_normal = tail_part.get_copy()
    tail_normal.fade_in(info.sustain_c)
    tail_normal.fade_out(info.sustain_c)
    tail_reversed = tail_normal.get_copy()
    tail_reversed.reverse()

    # Finally, create a tail
    is_reversed = True
    position = segment.length - info.sustain_c
    segment.extend(final_length, info.sustain_c)
    while position < final_length:
        segment.place(tail_reversed if is_reversed else tail_normal, position)
        position += info.sustain_portion - info.sustain_c
        is_reversed = not is_reversed

    # filtered = dict(sorted((k, v) for k, v in info.__dict__.items() if "sustain" in k))
    # print("DEBUG. Sustain:", segment.length_ms, filtered)


def generate_segment_audio(audio: Audio, info: SegmentInfo, crossfade: int) -> (Audio, int, bool):
    est_length = precalculate_length(info, crossfade, audio.length)[0]

    # Get base audio
    segment_begin, segment_end, crossfade, crossfade_in = calculate_begin_end(info, crossfade, audio.length)
    base_audio = audio.get_part(segment_begin, segment_end)
    base_audio.interpolate(info.duration+max(crossfade, crossfade_in))
    if info.reverse1:
        base_audio.reverse()

    # Segment audio
    segment = base_audio.get_copy()
    if info.repeats > 0:  # Repeats
        add_repeats(segment, info, crossfade_in)
    if info.sustain > 0:  # Sustain
        add_sustain(segment, info)
    if crossfade_in > crossfade:
        segment = segment.get_part(crossfade_in-crossfade, None)

    # Fades + Volume
    fadein, fadeout = compensate_fades(info.fadein + (crossfade * info.preroll_fadein), info.fadeout, segment.length)
    segment.fade_in(fadein, info.fadein_cut)
    segment.fade_out(fadeout, info.fadeout_cut)
    segment.volume(info.volume)

    # Intro loop
    if info.intro_loop > 0:
        og_length = segment.length
        segment.crop(0, info.intro_loop)

        segment.tile(math.ceil(og_length/info.intro_loop))
        segment.crop(0, og_length)

    # Second reverse
    if info.reverse2:
        segment.reverse()

    # Warning
    length_mismatch = False
    if est_length != segment.length:
        print(f"Segment length: Estimated {est_length}, got {segment.length}!", info.__dict__)
        length_mismatch = True

    return segment, crossfade, length_mismatch
