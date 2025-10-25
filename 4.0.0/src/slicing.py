from common import *
import numpy as np
from audio import Audio
from scrambler.scr_state import ScramblerState


class Onsets:
    def __init__(self, onsets, sample_rate: int):
        self.onsets = np.array(onsets, dtype=np.int64)
        self.onsets = np.unique(self.onsets)
        self.sample_rate = sample_rate

    @property
    def amount(self):
        return len(self.onsets)

    @property
    def are_there(self):
        return len(self.onsets) > 0

    @property
    def as_str(self):
        return " ".join(str(int(o)) for o in self.onsets)

    def get(self, target_sr):
        return (self.onsets / self.sample_rate * target_sr).astype(np.int64)

    def erase(self):
        self.onsets = np.array([], dtype=self.onsets.dtype)

    def override(self, new_onsets):
        self.onsets = new_onsets.onsets
        self.sample_rate = new_onsets.sample_rate


def strip_onsets(onsets: np.array, audio_length: int):
    onsets_f = onsets[(onsets > 0) & (onsets < audio_length)]
    onsets_f = np.append(onsets_f, [0, audio_length])
    return np.unique(onsets_f).astype(np.int64)


def convert_onsets(onsets: Onsets, shift: int, sample_rate: int, audio_length: int):
    slices = onsets.get(sample_rate) - shift
    return strip_onsets(slices, audio_length)


def audio_as_array(audio: Audio, sr: int) -> (np.array, int):
    if sr <= 0:
        sr = audio.sample_rate

    fixed_audio = audio.refactored(mono=True, sample_rate=sr)
    return fixed_audio.data.flatten(), sr


def import_midi(path: str, sample_rate: int):
    def conv(stamp_s):
        return round(stamp_s * sample_rate)

    onsets = set()
    midi_data = PrettyMIDI(path)

    onsets.add(conv(midi_data.get_end_time()))
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            onsets.add(conv(note.start))

    return sorted(onsets)


def detect_onsets_classic(audio: Audio):
    y, sr = audio_as_array(audio, 22050)

    onset_function = lb_onset.onset_strength(y=y, sr=sr, aggregate=np.median, n_fft=1024, fmax=1500)
    backtrack_function = lb_onset.onset_strength(y=y, sr=sr)
    onset_times = lb_onset.onset_detect(y=y, sr=sr, backtrack=True, units="time",
                                        onset_envelope=onset_function, energy=backtrack_function)

    return Onsets(onset_times * 1000, 1000)


def detect_onsets_envelope(onset_env: np.array, sample_rate: int, hop_size: int, sens: float):
    def find_peaks(data, threshold):
        look_l = data[:-2]
        look_c = data[1:-1]
        look_r = data[2:]
        return np.where(
            (look_l < look_c) &
            (look_c < look_r) &
            (look_c > threshold)
        )[0] + 1

    k_sens = 1 - sens / 100
    onsets = find_peaks(onset_env, onset_env.max() * k_sens)
    return Onsets(onsets * hop_size, sample_rate)


def detect_onsets_spectro(audio: Audio, sens: float):
    y, sr = audio_as_array(audio, AB_LIBROSA_SR)
    onset_env = lb_onset.onset_strength(y=y, sr=sr, center=False, n_fft=AB_LIBROSA_N_FFT)
    return detect_onsets_envelope(onset_env, sr, 512, sens)


def detect_onsets_amp(formula):
    def detect(audio: Audio, sens: float):
        y, sr = audio_as_array(audio, AB_AMP_ONSET_SR)
        window_size, hop_size = AB_AMP_ONSET_WINDOW, AB_AMP_ONSET_HOP

        energy = []
        for i in range(0, len(y) - window_size, hop_size):
            frame = y[i:i + window_size]
            energy.append(formula(frame))

        onset_env = np.maximum(0, np.diff(energy, prepend=0))
        return detect_onsets_envelope(onset_env, sr, hop_size, sens)
    return detect


def get_bpm_array(state: ScramblerState):
    beat_length_sec = 60 / state.config.quan_bpm
    audio_length_sec = state.audio.length/state.audio.sample_rate
    bpm_array = np.arange(0, audio_length_sec, beat_length_sec)
    bpm_array = np.floor(bpm_array * state.audio.sample_rate)
    bpm_array = np.concatenate((bpm_array, [state.audio.length]))
    return np.unique(bpm_array).astype(np.int64)


def get_slices_arr(state: ScramblerState, use_alt: bool):
    if state.config.quan_mode == 2:
        return state.slices_bpm

    elif use_alt and len(state.slices_alt) > 0 and state.config.quan_alt_slices.get():
        return state.slices_alt

    else:
        return state.slices


def quantize(timestamp: int, onsets: np.array, direction: int,
                    min_timestamp: int | None = None, max_timestamp: int | None = None):
    if min_timestamp is not None:
        onsets = onsets[onsets >= min_timestamp]
    if max_timestamp is not None:
        onsets = onsets[onsets <= max_timestamp]

    if len(onsets) == 0:
        return timestamp

    idx = (np.abs(onsets - timestamp)).argmin()

    if direction == 1 and onsets[idx] > timestamp and idx > 0:  # Direction = Back
        idx -= 1

    if direction == 2 and onsets[idx] < timestamp and idx < len(onsets) - 1:  # Direction = Forward
        idx += 1

    return int(onsets[idx])


detect_onsets_amp_ste = detect_onsets_amp(lambda frame: np.sum(frame ** 2))
detect_onsets_amp_rms = detect_onsets_amp(lambda frame: np.sqrt(np.mean(frame ** 2)))
