import os
import platform
import subprocess
from ab_tools import x_bool, int1

# Variables

AB_FORCE_CUSTOM_OS = False
AB_ANDROID_MODE = False

AB_DISABLE_ICON = x_bool(os.getenv("AB_DISABLE_ICON", ""))
AB_RESIZABLE_WINDOWS = x_bool(os.getenv("AB_RESIZABLE_WINDOWS", ""))
AB_VISUAL_ONSETS_ALL = x_bool(os.getenv("AB_VISUAL_ONSETS_ALL", ""))
AB_HIDE_TOOLTIPS = x_bool(os.getenv("AB_HIDE_TOOLTIPS", ""))

AB_FLOAT16_AUDIO = x_bool(os.getenv("AB_FLOAT16_AUDIO", ""))
AB_NO_INTERPOLATION = x_bool(os.getenv("AB_NO_INTERPOLATION", ""))
AB_ABPL_DEBUG = x_bool(os.getenv("AB_ABPL_DEBUG", ""))

AB_DISABLE_TKDND2 = x_bool(os.getenv("AB_DISABLE_TKDND2", ""))
AB_DISABLE_FFMPEG = x_bool(os.getenv("AB_DISABLE_FFMPEG", ""))
AB_DISABLE_SOUNDFILE = x_bool(os.getenv("AB_DISABLE_SOUNDFILE", ""))
AB_DISABLE_SIMPLEAUDIO = x_bool(os.getenv("AB_DISABLE_SIMPLEAUDIO", ""))
AB_DISABLE_PSUTIL = x_bool(os.getenv("AB_DISABLE_PSUTIL", ""))
AB_DISABLE_LIBROSA = x_bool(os.getenv("AB_DISABLE_LIBROSA", ""))
AB_DISABLE_PRETTY_MIDI = x_bool(os.getenv("AB_DISABLE_PRETTY_MIDI", ""))

AB_LIBROSA_SR = int1(os.getenv("AB_LIBROSA_PROCESS_SR", "22050"))
AB_LIBROSA_N_FFT = int1(os.getenv("AB_LIBROSA_N_FFT", "1024"))
AB_AMP_ONSET_SR = int1(os.getenv("AB_AMP_ONSET_SR", "44100"))
AB_AMP_ONSET_HOP = int1(os.getenv("AB_AMP_ONSET_HOP", "512"))
AB_AMP_ONSET_WINDOW = int1(os.getenv("AB_AMP_ONSET_WINDOW", "1024"))

if AB_ANDROID_MODE:
    AB_FORCE_CUSTOM_OS = True
    AB_DISABLE_TKDND2 = True
    AB_DISABLE_FFMPEG = True
    AB_DISABLE_SOUNDFILE = True
    AB_DISABLE_SIMPLEAUDIO = True
    AB_DISABLE_LIBROSA = True


# Extra libraries

if not AB_DISABLE_TKDND2:
    try:
        from TkinterDnD2 import TkinterDnD
    except ModuleNotFoundError:
        from tkinterdnd2 import TkinterDnD

if not AB_DISABLE_SOUNDFILE:
    import soundfile as sf

if not AB_DISABLE_SIMPLEAUDIO:
    import simpleaudio

if not AB_DISABLE_PSUTIL:
    import psutil

if not AB_DISABLE_LIBROSA:
    import librosa.onset as lb_onset

if not AB_DISABLE_PRETTY_MIDI:
    from pretty_midi import PrettyMIDI


# OS Specifics

os_name = None if AB_FORCE_CUSTOM_OS else platform.system()
OS_IS_WINDOWS = os_name == "Windows"
OS_IS_MACOS = os_name == "Darwin"
OS_IS_UNIX = os_name in ("Linux", "FreeBSD", "OpenBSD", "NetBSD", "SunOS")
OS_IS_OTHER = not (OS_IS_WINDOWS or OS_IS_MACOS or OS_IS_UNIX)

if OS_IS_WINDOWS:
    import winsound
    HOME_PATH = os.environ["USERPROFILE"]
elif OS_IS_MACOS:
    HOME_PATH = os.environ["HOME"]
elif OS_IS_UNIX:
    HOME_PATH = os.environ["HOME"]
else:
    HOME_PATH = os.path.abspath(".")


def open_f(path):
    if OS_IS_WINDOWS:
        os.startfile(path)
    elif OS_IS_MACOS:
        subprocess.call(["open", path])
    elif OS_IS_UNIX:
        subprocess.call(["xdg-open", path])
    else:
        raise OSError


def open_d(path):
    if OS_IS_WINDOWS:
        subprocess.call(["explorer.exe", "/select,", path.replace("/", "\\")])
    elif OS_IS_MACOS:
        subprocess.call(["open", "-R", path])
    else:
        raise OSError
