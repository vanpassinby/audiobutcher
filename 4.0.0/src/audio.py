import math
import json
import wave
import shutil
import tempfile

import numpy as np
from common import *

FFMPEG_PATH = None
PLAY_SUPPORTED = [8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000]


def ff_exe(name):
    if full_path := shutil.which(name, path=FFMPEG_PATH):
        return full_path
    else:
        return name


def delete_file(path):
    try:
        os.remove(path)
    except:
        print("Failed to delete", path)


def abs_max(array: np.array):
    min_val = np.min(array)
    max_val = np.max(array)
    return max(abs(min_val), abs(max_val))


class FFmpegError(Exception):
    pass


class Audio:
    def __init__(self, data: np.array, sample_rate: int):
        self.data = data
        self.sample_rate = sample_rate

    def length_ms_to_samp(self, length_ms, round_mode=round):
        return round_mode(self.sample_rate * length_ms / 1000)

    # Properties

    @property
    def length(self):
        return self.data.shape[0]

    @property
    def channels(self):
        return self.data.shape[1]

    @property
    def _dtype(self):
        return self.data.dtype

    # Misc

    def _fade_ramp(self, begin, end, duration):
        return np.linspace(begin, end, duration, dtype=self._dtype)[:, np.newaxis]

    @staticmethod
    def _ffprobe_get_info(path):
        command = [ff_exe("ffprobe"), "-hide_banner", "-show_streams", "-select_streams", "a", "-of", "json", path]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            info = json.loads(stdout)["streams"]

            if len(info) != 0 and "sample_rate" in info[0] and "channels" in info[0]:
                return info[0]

            else:
                exc = "This file does not contain the required audio data!"
                raise FFmpegError(exc)

        else:
            exc = "Unable to process this file! FFprobe output:\n{}"
            raise FFmpegError(exc.format(stderr.decode("utf-8", "ignore")))

    @staticmethod
    def _ffmpeg(*args):
        command = [ff_exe("ffmpeg"), "-hide_banner", "-y"] + list(args)

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            exc = "Unable to process this file! FFmpeg output:\n{}"
            raise FFmpegError(exc.format(stderr.decode("utf-8", "ignore")))

    # Read

    @staticmethod
    def _load_array(raw_data, dtype, n_channels):
        return np.frombuffer(raw_data, dtype=dtype).reshape(-1, n_channels)

    @classmethod
    def _load_wave(cls, path):
        with wave.open(path, "rb") as file:
            info = file.getparams()
            raw_data = file.readframes(info.nframes)

        dtypes = {1: np.uint8, 2: np.int16, 4: np.int32}
        if info.sampwidth not in dtypes:
            exc = RuntimeError("This format isn't supported by the WAVE library!")
            raise exc

        data = cls._load_array(raw_data, dtypes[info.sampwidth], info.nchannels)
        del raw_data

        threshold = 2**(8*info.sampwidth-1)
        data = (data / threshold).astype(np.float16 if AB_FLOAT16_AUDIO else np.float32)

        if info.sampwidth == 1:
            data -= 1

        return cls(data, info.framerate)

    @classmethod
    def _load_soundfile(cls, path):
        y, sr = sf.read(path, always_2d=True, dtype=np.float32)
        if AB_FLOAT16_AUDIO:
            y = y.astype(np.float16)
        return cls(y, sr)

    @classmethod
    def _load_ffmpeg(cls, path):
        info = cls._ffprobe_get_info(path)
        file = tempfile.NamedTemporaryFile(mode="rb", suffix=".raw", delete=False)

        try:
            cls._ffmpeg("-vn", "-i", path, "-f", "f32le", file.name)
            raw_data = file.read()
            file.close()
            delete_file(file.name)

            array = cls._load_array(raw_data, np.float32, int(info["channels"]))
            if AB_FLOAT16_AUDIO:
                array = array.astype(np.float16)
            return cls(array, int(info["sample_rate"]))

        except:
            file.close()
            delete_file(file.name)
            raise

    @classmethod
    def load(cls, path):
        try:
            if AB_DISABLE_SOUNDFILE:
                return cls._load_wave(path)
            else:
                return cls._load_soundfile(path)

        except Exception as e:
            error_lib = e
            if AB_DISABLE_FFMPEG:
                raise

        try:
            return cls._load_ffmpeg(path)
        except FFmpegError:
            raise
        except:
            raise error_lib from None

    # Write

    def _write_wave(self, path, export_format):
        if export_format == "wav16":
            sw, mult, dtype = 2, 2**15, np.int16
        elif export_format == "wav32":
            sw, mult, dtype = 4, 2**31, np.int32
        else:
            exc = RuntimeError("This format isn't supported by the WAVE library!")
            raise exc

        with wave.open(path, "wb") as file:
            file.setnchannels(self.channels)
            file.setframerate(self.sample_rate)
            file.setsampwidth(sw)
            file.setnframes(self.length)

            for i in range(0, self.length, self.sample_rate):
                data_part = self.data[i:i+self.sample_rate]
                data_fix = (data_part * mult).astype(dtype)
                file.writeframes(data_fix.tobytes())

    def _write_soundfile(self, path, export_format):
        format_, subtype = {
            "wav16":  ("WAV", "PCM_16"),
            "wav24":  ("WAV", "PCM_24"),
            "wav32":  ("WAV", "PCM_32"),
            "wav32f": ("WAV", "FLOAT"),
            "flac16": ("FLAC", "PCM_16"),
            "flac24": ("FLAC", "PCM_24"),
            "mp3":    ("MP3", "MPEG_LAYER_III"),
        }[export_format]

        with sf.SoundFile(path, mode="w", samplerate=self.sample_rate, channels=self.channels,
                          format=format_, subtype=subtype) as file:
            for i in range(0, self.length, self.sample_rate):
                data_part = self.data[i:i+self.sample_rate]
                file.write(data_part.astype(np.float32))

    def _write_ffmpeg(self, path, export_format):
        fmt_args = {
            "wav16":  ("pcm_s16le",),
            "wav24":  ("pcm_s24le",),
            "wav32":  ("pcm_s32le",),
            "wav32f": ("pcm_f32le",),
            "flac16": ("flac", "-sample_fmt", "s16"),
            "flac24": ("flac", "-sample_fmt", "s32"),
            "mp3":    ("libmp3lame",)
        }[export_format]

        file = tempfile.NamedTemporaryFile("wb", suffix=".raw", delete=False)

        try:
            for i in range(0, self.length, self.sample_rate):
                data_part = self.data[i:i+self.sample_rate]
                file.write(data_part.astype(np.float32).tobytes())

            input_args = ["-f", "f32le", "-ar", str(self.sample_rate), "-ac", str(self.channels), "-i", file.name]
            self._ffmpeg(*input_args, "-c:a", *fmt_args, path)

            file.close()
            delete_file(file.name)

        except:
            file.close()
            delete_file(file.name)
            raise

    def write(self, path, export_format):
        try:
            if AB_DISABLE_SOUNDFILE:
                self._write_wave(path, export_format)
            else:
                self._write_soundfile(path, export_format)
            return

        except Exception as e:
            error_lib = e
            if AB_DISABLE_FFMPEG or not AB_DISABLE_SOUNDFILE:
                raise

        try:
            self._write_ffmpeg(path, export_format)
        except FFmpegError:
            raise
        except:
            raise error_lib from None

    def play(self):
        y = (self.data * 32767).astype(np.int16).copy()
        play_buffer = simpleaudio.play_buffer(y, self.channels, 2, self.sample_rate)
        return play_buffer

    # Generate new

    def get_copy(self):
        return self.__class__(np.copy(self.data), self.sample_rate)

    def get_part(self, begin, end):
        return self.__class__(self.data[begin:end], self.sample_rate)

    def get_silence(self, duration):
        ndata = np.zeros((duration, self.channels), dtype=self._dtype)
        return Audio(ndata, self.sample_rate)

    def refactored(self, mono: bool, sample_rate: int):
        if mono and self.channels > 1:
            ndata = self.data.mean(axis=1)[:, np.newaxis]
        else:
            ndata = self.data.copy()

        new_length = math.ceil(self.length / self.sample_rate * sample_rate)
        new_audio = self.__class__(ndata, self.sample_rate)
        new_audio.interpolate(new_length)
        new_audio.sample_rate = sample_rate

        return new_audio

    # Effects

    def reverse(self):
        self.data = np.flip(self.data, axis=0)

    def volume(self, volume):
        if volume <= 0:
            self.data = np.zeros(self.data.shape, dtype=self._dtype)
        elif volume != 100:
            self.data *= (volume / 100)

    def _no_interp(self, target_length):
        new_x = np.linspace(0, self.length-1, num=target_length)
        new_x = np.round(new_x).astype(np.uint64)
        self.data = self.data[new_x]

    def interpolate(self, target_length):
        if self.length == target_length:
            return

        if AB_NO_INTERPOLATION:
            self._no_interp(target_length)
            return

        old_x = np.arange(self.length)
        new_x = np.linspace(0, self.length-1, num=target_length)

        channels = []
        for channel in self.data.T:
            channels.append(
                np.interp(new_x, old_x, channel).astype(self._dtype)
            )

        self.data = np.array(channels).T

    def fade_in(self, length=0, zero=0):
        if length <= 0 or zero >= 100:
            return

        length = min(length, self.length)
        self.data[:length] *= self._fade_ramp(zero / 100, 1, length)

    def fade_out(self, length=0, zero=0):
        if length <= 0 or zero >= 100:
            return

        length = min(length, self.length)
        position = self.length - length
        self.data[position:] *= self._fade_ramp(1, zero / 100, length)

    # Mixing

    def fix_range(self):
        threshold = abs_max(self.data)
        if threshold > 1:
            self.data /= threshold

    def crop(self, begin, end):
        self.data = self.data[begin:end]

    def tile(self, n_repeats: int):
        if n_repeats <= 1:
            return

        self.data = np.tile(self.data, (n_repeats, 1))

    def extend(self, target_length, fade_out):
        self.fade_out(min(fade_out, self.length))

        silence = self.get_silence(target_length)
        silence.place(self, 0)

        self.data = silence.data

    def place(self, audio2, position):
        if position > self.length:
            return

        aud2_data = audio2.data
        if position < 0:
            if position + audio2.length < 0:
                return
            else:
                aud2_data = aud2_data[:position + audio2.length]
                position = 0
        elif position + audio2.length > self.length:
            aud2_data = aud2_data[:self.length - position]

        self.data[position:position+aud2_data.shape[0]] += aud2_data
