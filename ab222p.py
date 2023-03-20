# -*- coding: utf-8 -*-

AB_DEBUG_BUTTON = False
AB_FORCE_CUSTOM_OS = False
AB_DISABLE_LIBROSA = False
AB_DISABLE_SOUNDFILE = False
AB_DISABLE_SIMPLEAUDIO = False
AB_DONT_USE_B64_ICON = False
AB_RESIZABLE_WINDOWS = False
AB_BYPASS_BACKCOM_WARN = False

import os, sys, random, webbrowser
from time import *
from os.path import *
from platform import system
from threading import Thread
from traceback import format_exc
from subprocess import call
from configparser import RawConfigParser

from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter.simpledialog as sd

from pydub import AudioSegment
from pydub.playback import play

import numpy as np

# Comment out next line when compiling with AB_DISABLE_LIBROSA
if not AB_DISABLE_LIBROSA: from librosa.onset import *

# Comment out next line when compiling with AB_DISABLE_SOUNDFILE
if not AB_DISABLE_SOUNDFILE: import soundfile as sf

# Comment out next line when compiling with AB_DISABLE_SIMPLEAUDIO
if not AB_DISABLE_SIMPLEAUDIO: import simpleaudio

# Names
abVersion = "AudioButcher v2.2.2-p"
abVersionShort = "2.2.2.00"
abKnownVersions = ["2.1.0", "2.1.1", "2.2.0", "2.2.1.00", "2.2.2.00"]
abDescription = """AudioButcher ver. 2.2.2 (Public Release), March 2023

Brought to you by the AudioButcher Team:
MightInvisible, osdwa, Shriki, vanpassinby, Zach Man

Runs in Python {}
"""
abDiscordLink = "https://discord.gg/gNHxMmfTy4"
abLicenceLink = "https://www.gnu.org/licenses/gpl-3.0.txt"
abIconB64 = "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADqUExURQAAALy8vLq6up6enr6+vpaWlmlp3L29vaenp7S0tFVV4rW1tbi4uAAA/wQE/by8vbm5ub+/v7e3t6ioqKCgoLGxsbi4wXZ21oaG0jg47IeH0h0d9YCA1AIC/gEB/6+vxKurq6iox1ZW4jMz7gcH/RMT+KWlpQ0N+5qamru7u0xM5lJS47a2tpGRzn5+1XNz2Lu7wKmpxo6Ojmpq2L29vxwc9jQ07TQ07kVF6LGxvgMD/oOD0xAQ+rW1wwsL+7KyxD096goK+39/1KSkyKOjowQE/rKysrCwsK6urmpqzQwM+0ZG6Hh41wAAAJ0U8VQAAABOdFJOU///////////////////////////////////////////////////////////////////////////////////////////////////////AKxN+84AAAAJcEhZcwAADsQAAA7EAZUrDhsAAAeqSURBVHhexZoLQxNHFIVjSo1YBokWSqWk+EQrtVaKFgUUqKCi///v9J57z+zM7s5mH9mQT9idOXNnztlNDEl2B98bMOgIp0+lqohL9AgXLpLSOaOGG9y3gQYxJY2l07khsNkW2mQUBZbVggDdUtDIk++zpn+GQ/zKVvYFS+6B1c4DeBPt0xBEbR2aGz8I2lhakg0thdDU0bkBfw/6NI0CaNk1QtssAOVrxBtztwDozN0CoLNtF4JZ23YhmPXi/C0BNuwugOsP8GMA3SYBbt68yVbMaMRGc27ZjtaGBWAnj/imrZWRwV4TbgG2I6oD1NA6gQa4VZrlAywvL5sQuM19W34S2BRWVthIHD3IzkAhwW3CbiuC/4qH/QQIIN4GNeG2JXDyI6yCO3fucLDE2mBtLX57JqeAxuPx3ZWV0egukFO/pAy0S89lCWBdTsZCS4Ml+MasrnIY2AN579498SbRe+SfhfX1dWmpUYaNZthzYmNDAuBBAxwxfhFoHuBYPeovpL0zNgQJwF7G5uZArOgZg/qNDVbNjK2WCkC7JCzphV+VcgBaJWFJn5QC0Arcv3+fLYMVfbG1tSXbxEMA1FAC/BYIA9aaEbHf2nJuK3UGtrfxuy3+9ylCNu+e7CeTyXg8xopTn4QUAr09CpOJOUxSAfzRitvvAsUsF7t9IOchGUCBt8J+ODHs9wBWSweYTLAN5oq6C/6BsFd2/aTXBa4W28sZ8VDJwyk4B/KzQ7UbXEmgEHgAJIPuH1AMcM5oBwFmCeEePnzoHj16xK6iiZz8/xhXuGfIuxr5g7ijKTpgRnB6/JhSfFKce/LkCSTbFoA1m13At0t0sWOlblAXKMRwZDSSH0C5O6UAdBAoFOAgoNIaTB0Oh0/xXY3bFca7HKnHnDOoduGp4XZlmd0ogC2sSIdiDhuU13D2u/FMgbdCtXiAAgcCpqXHmqAzHe2N8BygYGjPRBvNg1EUsdsGmxqTCkCpEpYJz58/p9YQvHRzrocj0bLs16DurQLoH47gLytwwKAsUEjDmoYpK7AF/Bp/eHThGBbkefHiBWNQaI9+6NL5urF3RgGtqaV5ZRkGUKSLl0OXC2FlNexx343YCQGQofER7bm9Pf1tneFPQTc5KwZomECDe6i1BDNfvmRHMHd7DChNRQsFdlvD6WEBDSCoFulVoM4N/hIotEZXcK9esUt/QXWq9Wg1YL8F+WnBW4DQcMkuziByMigEqXZl1nZMYGbRZGlRUqhOwRc1qy6BaYBdwf9hdX8b2mlCcaFpWG2EXkB7LbCgKZiAaTrPllI9A5fleG0ujU2yALpeCKE61nv9eig/Jhos0m1WjwlsRZ62cBmNDQsDAayS61F2TspsUEDbhnV65kxsDojmeH+pjicEbyzEIl1SNhwRMF/Hc0gpdijHP8D6DJYFpNgjIxge7u9rVxNYkUzRMS4iy6iawabW5tHqfwAaFMvI3P39fbSwce7gQGp9uS0+jI6FA01R/wyKUzg4ONjcZDuG7vDnro43utViIfdVUgIpYYtT3r5ll8hfZ4P9BryJoFQNVw9Qz8D7A9P/BVRrce7wcDw+PBwcUqiFLiXevXuXHpiOzDn0UErCldVdsX6EBEACQrEe1hvUEtigVQkm5vEy9tOWKqErKhTKyIiumkE9R+VAA3Rew+n4VO0cvt2gENHRv01y+1LFoOTpfPgR8gZxahoceoCiBzNnyeBqzIF6EEoBVd6/13Yn0svmODrSmnShc+8JhTZgyQiqCY6OjtgqUTOzFp3voVbk+PhYthURpk+tR2efnJxUryDux8fVwzO5n3j7EwpptKrqfzuGdKe9Dujq6dly6uXYnT4H9XmYSqE6YL8d8QstpRiO5OBQBmVCsRWcmp7MoQy7ZhxfzP8gKpszMnWdMFhM8MFgryUfP9qvUumfu/ZeYhZ/w84toBCgvrqqG4rzwZxKD4OK1hrML4B6R1AW8r3eyN+UcHrqTuHEboH5JChwqttqqzPu01RcOa2lcGuG2J+fpxOcCdpI3U1Teem2MeeAe1NAdDbgf3aGm2pSEWYIUPiqXoMggveOX6WrnweznwHlnD4CldgdUC3RLcB/3JdRp0++TcJZKdPTGQCfAujS3OzZSNBXAKxvNsQ0a8RENxMqxQAX3LfG3GK25de+gQZ2F6WgvUAhwIXCTh3hktX6OoxitgH21i2ch8tLNooBzJ4JcK+bNgJ4DQbs2nUzSSGbUgQgIUajceGj0KXCDgLkbHLHbwk+C6PR58/0F0U8zTpjXTDP7Htvwz6MfRkMvvBeg8v48AUNsLzsr7/sXVys6WmQGNAlAPwlgA4DSXCXtgZ1w2y/2g6Ez4I7gO1AeAhwEQj4GwQDdhRgwMWs0loqZFxdXQ2+wv+q9PxPIwH6+X9IxN92tq8lu6e0T759Y6MBcwjwzWgYYy5noA0aYIYEyS+SW9Dk3vJK7KvmluD2iWdsCzMF6AMGWFgC9cZmQQnM2rYLwax1u5AEdOZuAdDZdgtI4I25v/YEtA0BWibAfYFsdoKmcYD2CfLvbVpBSyFqXuOjQEMQt68rAs2MfO86ItDIU+zPPQFtMkqCwNI5QIOYlAY4o0e4cJEqPQeXaA2nT+H79/8BNeXyRCNnMNMAAAAASUVORK5CYII="

if AB_FORCE_CUSTOM_OS: osname = None
else: osname = system()
if osname=="Windows":
    homepath = os.environ["USERPROFILE"]
    temppath = os.environ["TEMP"]
    def openf(file): os.startfile(file)
elif osname=="Darwin":
    homepath = os.environ["HOME"]
    temppath = "/tmp"
    def openf(file): call(("open", file))
elif osname=="Linux":
    homepath = os.environ["HOME"]
    temppath = "/tmp"
    def openf(file): call(("xdg-open", file))
else: #Custom OS
    homepath = "."
    temppath = "."
    def openf(file): ...


def run(target, *args):
    Thread(target=target, args=args, daemon=True).start()

def validPath(path):
    return path!="" and path!=()

def getNoExt(name):
    return basename(splitext(name)[0])

def newFileName():
    if useunixfilename.get()==1: return f"untitled_{int(time())}"
    else: return "untitled"

def defOnsPath(ons2):
    if ons2: return "dir_onsets2"
    else: return "dir_onsets"

def binBool(b):
    try: return int(bool(int(b)))
    except ValueError: return 0

def openFile(file):
    try: openf(file)
    except Exception as e: abError("AudioButcher", f"Can't open file:\n{e}")

def updSecImpAudLen():
    abConfig.set("secimpaudlen")
    updateWindow()

def updShowMoreFormats(init=False):
    global import_types
    if not init: abConfig.set("showmoreformats")
    if showmoreformats.get() == 1:
        import_types = import_types_2
    else:
        import_types = import_types_1

def updBackupPresets(init=False, ask=True):
    proposed = backuppresets.get()
    if proposed==1 and not isdir(abConfig.get("backuppresetsdir")) and ask: updBackupPresetsDir()
    if not isdir(abConfig.get("backuppresetsdir")): proposed = 0
    if not init: abConfig.set("backuppresets", value=proposed)
    backuppresets.set(proposed)

def updBackupPresetsDir():
    selfile = fd.askdirectory(initialdir=abConfig.get("backuppresetsdir"))
    if validPath(selfile):
        abConfig.set("backuppresetsdir", path=selfile)

def openBackupPresetsDir():
    path = abConfig.get("backuppresetsdir")
    if isdir(path): openFile(path)

def restoreLastSeed():
    if lastSeed!=None:
        x_fromseed.set(1)
        updateSymbols()
        e_seed.delete(0, END)
        e_seed.insert(0, lastSeed)

def sec2ms(sec):
    try:
        ms = str(float(sec)*1000)
        if ms[-2:]==".0": ms=ms[:-2]
        return ms
    except ValueError:
        return sec

def text2list(_type, text):
    return [_type(x) for x in text.split()]

def convOns(_onsets):
    try:
        return [int(o) for o in _onsets]
    except Exception as e:
        abError("Onsets", e)
        return None

def checkVersion(version):
    if version in abKnownVersions or AB_BYPASS_BACKCOM_WARN:
        return True
    else:
        return mb.askyesno("Warning", f"This preset has been created using an unknown version of AudioButcher ({version}), and is likely won't work as intended.\n\nDo you want to continue opening this preset anyway?", icon="warning")

def getExportLength():
    if not generating:
        return sd.askfloat("Export", "Exported audio length (in seconds):", initialvalue=abConfig.get("ste"), parent=window)
    else:
        return None

def cboxSel(cbox, val):
    try:
        cbox.current(int(val))
    except Exception:
        cbox.configure(state="normal")
        cbox.delete(0, END)
        cbox.insert(0, "<Error>")
        cbox.configure(state="readonly")


def importstate(state):
    global importState
    importState = state
    if importState=="wait":
        progress.configure(mode="indeterminate")
        progress.start()
    else:
        progress.configure(mode="determinate")
        progress.stop()

def updateWindow():
    title = abVersion
    if importState=="good":
        audlen = round(audio.duration_seconds)
        if secimpaudlen.get()==0:
            audlen = f"{audlen//60}:{str(audlen%60).zfill(2)}"
        else:
            audlen = f"{audlen} sec"
        title+=f" - {basename(lastSrcPath)} ({audlen})"
    if onsets!=[]:  title+=" - Onsets loaded"
    if onsets2!=[]: title+=" - Start onsets loaded"
    if previewing:  title+=" - Previewing"
    window.title(title)

    if not AB_DISABLE_SIMPLEAUDIO:
        if previewing: menu_prev.entryconfig(1, state="normal")
        else: menu_prev.entryconfig(1, state="disabled")

def updateSymbols(dum=None):
    mode2sym = ["-", "±", "±", ",", "?"]
    mode2sym2 = ["-", "±", "±", "?"]

    s_Size.config(text=mode2sym[c_methDur.current()])
    s_PL.config(text=mode2sym[c_methPause.current()])
    s_FadeIn.config(text=mode2sym[c_methFdIn.current()])
    s_FadeOut.config(text=mode2sym[c_methFdOut.current()])
    s_crossfade.config(text=mode2sym[c_methCrsfd.current()])
    s_repeat.config(text=mode2sym[c_methrep.current()])
    s_segs.config(text=mode2sym[c_remembertype.current()])
    s_cutFdIn.config(text=mode2sym2[c_methCutFdIn.current()])
    s_cutFdOut.config(text=mode2sym2[c_methCutFdOut.current()])

    if c_methrepmsk.current() == 0:
        l_minMaskRepeat.config(text="Minimum: ")
        l_maxMaskRepeat.config(text="Maximum: ")
    elif c_methrepmsk.current() in (1, 2):
        l_minMaskRepeat.config(text="Average: ")
        l_maxMaskRepeat.config(text="Deviation: ")
    elif c_methrepmsk.current() == 3:
        l_minMaskRepeat.config(text="Mu (µ): ")
        l_maxMaskRepeat.config(text="Sigma (σ): ")

    if x_propfadeout.get() == 0:
        c_notepropfd.config(state="disabled")
        x_notepropfd.set(0)
    else:
        c_notepropfd.config(state="normal")

    if x_repmode.get() == 0:
        l_repeat.configure(text="Repeat segment ... times: ")
    else:
        l_repeat.configure(text="Repeat segment for: ")

    if x_fromseed.get() == 0:
        e_seed.configure(state="disabled")
    else:
        e_seed.configure(state="normal")

    if c_quantizeMode.current() == 0:
        e_quanavgstrt.configure(state="disabled")
        e_quanstrt.configure(state="disabled")
        e_quanseglgth.configure(state="disabled")
        e_quanrep.configure(state="disabled")
        e_quanmask.configure(state="disabled")
        e_bpm.configure(state="disabled")
    else:
        e_quanavgstrt.configure(state="normal")
        e_quanstrt.configure(state="normal")
        e_quanseglgth.configure(state="normal")
        e_quanrep.configure(state="normal")
        e_quanmask.configure(state="normal")
        if c_quantizeMode.current() == 2:
            e_bpm.configure(state="normal")
        else:
            e_bpm.configure(state="disabled")

    if c_quantizeMode.current() == 1:
        e_usestartonsets.configure(state="normal")
    else:
        e_usestartonsets.configure(state="disabled")

    if x_trimfile.get() == 0:
        e_trimmin.configure(state="disabled")
        e_trimmax.configure(state="disabled")
        c_shiftons.configure(state="disabled")
    else:
        e_trimmin.configure(state="normal")
        e_trimmax.configure(state="normal")
        c_shiftons.configure(state="normal")

def applyWindowStyle(obj):
    if not AB_RESIZABLE_WINDOWS: obj.resizable(AB_RESIZABLE_WINDOWS, AB_RESIZABLE_WINDOWS)
    if not AB_DONT_USE_B64_ICON: obj.iconphoto(True, PhotoImage(data=abIconB64, format="png"))

def loadAudio(path):
    try:
        return AudioSegment.from_file(path)
    except Exception:
        if AB_DISABLE_SOUNDFILE or not isfile(path): raise
        else:
            y, sr = sf.read(path)
            wavpath = join(temppath, f"ab_convert_{int(time())}.wav")
            sf.write(wavpath, y, sr)
            audio = AudioSegment.from_wav(wavpath)
            try: os.remove(wavpath)
            except Exception: print("Exception caught: loadAudio")
            return audio

def apply210CompMethod(CompMethod):
    if CompMethod=="0":
        e_fdmode_lc.delete(0, END)
        e_fdmode_lc.insert(0, "1")
    elif CompMethod=="1":
        e_fdmode_sf.delete(0, END)
        e_fdmode_sf.insert(0, "1")
    elif CompMethod=="2":
        e_fdmode_en.delete(0, END)
        e_fdmode_en.insert(0, "1")

def apply220StumMethod(methStumble):
    if methStumble=="0":
        e_methStumbleNorm.delete(0, END)
        e_methStumbleNorm.insert(0, "1")
    elif methStumble=="1":
        e_methStumbleForw.delete(0, END)
        e_methStumbleForw.insert(0, "1")
    elif methStumble=="2":
        e_methStumbleBack.delete(0, END)
        e_methStumbleBack.insert(0, "1")


def speedChange(sound, speed=1):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)})
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def findNearest(array, value, mode, direction = 0):
    #mode 0 returns timestamp, mode 1 returns array index
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()

    if direction == 1:
        if array[idx] > value and idx > 0:
            idx -= 1
    if direction == 2:
        if array[idx] < value and idx < array.size - 1:
            idx += 1

    if mode == 0: return array[idx]
    else: return idx

def generateOnsets(source):
    sr = 22050
    y = np.array(source.set_frame_rate(sr).set_channels(1).get_array_of_samples()).astype(np.float32)
    onset_function = onset_strength(y=y, sr=sr, aggregate=np.median, n_fft=1024, fmax=1500)
    backtrack_function = onset_strength(y=y, sr=sr)
    onset_times = onset_detect(y=y, sr=sr, onset_envelope = onset_function, backtrack=1, energy=backtrack_function, units="time")
    return [round(element * 1000) for element in onset_times]

def processOnsets(mode, _onsets, ons2=False, source=None, parent=None):
    global onsets, onsets2
    if _onsets!=None:
        _onsets = sorted(np.unique(_onsets))
        if mode in [0, 1]:
            try:
                if ons2: initialfile=""
                else: initialfile = getNoExt(source)+" [onsets]"
                selfile = fd.asksaveasfilename(filetypes=onset_types, defaultextension=onset_types, initialdir=abConfig.get("dir_onsets"), initialfile=initialfile, parent=parent)
                if validPath(selfile):
                    abConfig.set("dir_onsets", path=selfile)
                    abofile = open(selfile, "w")
                    for onset in _onsets: abofile.write("%s " % onset)
                    abofile.close()
            except Exception as e:
                abError("Onsets", e)
        if mode in [0, 2]:
            if not ons2: onsets = _onsets
            else: onsets2 = _onsets
    updateWindow()

def openOnsets(parent, ons2=False):
    selfile = fd.askopenfilename(filetypes=onset_types, initialdir=abConfig.get(defOnsPath(ons2)), parent=parent)
    if validPath(selfile):
        try:
            abConfig.set(defOnsPath(ons2), path=selfile)
            abofile = open(selfile, "r")
            processOnsets(2, text2list(int, abofile.read()), ons2)
            abofile.close()
        except Exception as e:
            abError("Onsets", e)
        else:
            updateWindow()
            mb.showinfo("Onsets", "Applied successfully.")
            if closeonsets.get()==1: parent.destroy()

def getOnsets(parent, mode, ons2=False, fromCurrent=False, source=None, window=True):
    global audio
    if fromCurrent:
        source = lastSrcPath
    elif source==None:
        source = fd.askopenfilename(filetypes=import_types, initialdir=abConfig.get("dir_srcaud"), parent=parent)
    if validPath(source):
        try:
            if window: parent.title("Manage onsets - Busy")
            if fromCurrent: _onsets = generateOnsets(audio)
            else: _onsets = generateOnsets(loadAudio(source))
            if window: parent.title("Manage onsets - Ready")
            mb.showinfo("Onsets", "All onsets detected.")
            processOnsets(mode, _onsets, ons2, source, parent)
        except Exception as e:
            if window: parent.title("Onsets - Ready")
            abError("Onsets", e)
        else:
            if closeonsets.get()==1 and window: parent.destroy()

def eoImportOnsets(parent, entry, ons2):
    selfile = fd.askopenfilename(filetypes=onset_types, initialdir=abConfig.get(defOnsPath(ons2)), parent=parent)
    if validPath(selfile):
        try:
            entry.delete("1.0", END)
            abConfig.set("dir_onsets", path=selfile)
            abofile = open(selfile, "r")
            entry.insert(END, abofile.read())
            abofile.close()
        except Exception as e:
            abError("Onsets", e)

def eoCurrentOnsets(entry, ons2):
    global onsets, onsets2
    if not ons2: _onsets = onsets
    else: _onsets = onsets2
    try:
        entry.delete("1.0", END)
        for o in _onsets: entry.insert(END, "%s " % o)
    except Exception as e:
        abError("Onsets", e)


class abConfigure:
    def __init__(self, file, section):
        self.config = RawConfigParser()
        self.file = file
        self.section = section
    def get(self, what):
        try: self.config.read(self.file, encoding="utf-8")
        except Exception:
            print("Exception caught: abConfigure")
        fallbacks = {
            "dir_srcaud":       homepath,
            "dir_resaud":       homepath,
            "dir_presets":      homepath,
            "dir_onsets":       homepath,
            "dir_onsets2":      homepath,
            "lastdebcom":       "",
            "ste":              120,
            "stp":              10,
            "useunixfilename":  1,
            "secimpaudlen":     0,
            "showmoreformats":  0,
            "shadderrinf":      0,
            "backuppresets":    0,
            "backuppresetsdir": "",
            "autoonsdet":       0,
            "resetonsets":      1,
            "closeonsets":      0,
            "onsetsdropdown":   2,
        }
        if not self.config.has_section(self.section): self.config[self.section] = {}
        return self.config.get(self.section, what, fallback=fallbacks[what])
    def set(self, what, value=0, path=""):
        values = {
            "dir_srcaud":       dirname(path),
            "dir_resaud":       dirname(path),
            "dir_presets":      dirname(path),
            "dir_onsets":       dirname(path),
            "dir_onsets2":      dirname(path),
            "lastdebcom":       value,
            "ste":              value,
            "stp":              stp.get(),
            "useunixfilename":  useunixfilename.get(),
            "secimpaudlen":     secimpaudlen.get(),
            "showmoreformats":  showmoreformats.get(),
            "shadderrinf":      shadderrinf.get(),
            "backuppresets":    value,
            "backuppresetsdir": path,
            "autoonsdet":       autoonsdet.get(),
            "resetonsets":      resetonsets.get(),
            "closeonsets":      closeonsets.get(),
            "onsetsdropdown":   value,
        }
        self.config[self.section][what] = str(values[what])
        cfgfile = open(self.file, "w", encoding="utf-8")
        self.config.write(cfgfile)
        cfgfile.close()

def abDefaultConfig():
    cfgEmpty()
    cfgDefault()
    updateSymbols()

def abDebug(result):
    com = sd.askstring("Debug", "Execute python command:", initialvalue=abConfig.get("lastdebcom"), parent=window)
    if com!=None:
        abConfig.set("lastdebcom", com)
        try:
            if result: r = eval(com)
            else: exec(com)
        except Exception as e:
            abError("Debug", e)
        else:
            if result: mb.showinfo(com, str(r))

def abOnsetsWindow():
    onswin = Toplevel(window)
    onswin.title("Manage onsets - Ready")
    face = Frame(onswin, padding=3); face.pack(fill="both", expand=True)
    group = Frame(face); group.grid(row=0, column=0, columnspan=3, sticky="w")

    Separator(group, orient=VERTICAL).grid(row=0, column=1, rowspan=3, padx=3, ipady=30)

    b_ons1_file = Button(group, text="Apply onset list from file", command=lambda: openOnsets(onswin))
    b_ons1_edit = Button(group, text="Manually edit onsets", command=lambda: abEditOnsets(onswin))
    b_ons1_eras = Button(group, text="Erase onsets", command=lambda: processOnsets(2, []))
    b_ons2_file = Button(group, text="Apply start onset list from file", command=lambda: openOnsets(onswin, ons2=True))
    b_ons2_edit = Button(group, text="Manually edit start onsets", command=lambda: abEditOnsets(onswin, ons2=True))
    b_ons2_eras = Button(group, text="Erase start onsets", command=lambda: processOnsets(2, [], True))
    b_geno_curr = Button(face,  text="Generate onset list from current audio", command=lambda: run(getOnsets, onswin, c_andthen.current(), False, True))
    b_geno_oaud = Button(face,  text="Generate onset list from other file", command=lambda: run(getOnsets, onswin, c_andthen.current()))
    l_andthen = Label(face, text="And then,")
    c_andthen = Combobox(face, values=("Save to file and apply", "Save to file only", "Apply only"), width=20, state="readonly")

    b_ons1_file.grid(row=0, column=0, sticky="w")
    b_ons1_edit.grid(row=1, column=0, sticky="w")
    b_ons1_eras.grid(row=2, column=0, sticky="w")
    b_ons2_file.grid(row=0, column=3, sticky="w")
    b_ons2_edit.grid(row=1, column=3, sticky="w")
    b_ons2_eras.grid(row=2, column=3, sticky="w")
    b_geno_curr.grid(row=2, column=0, sticky="w")
    b_geno_oaud.grid(row=3, column=0, sticky="w")
    l_andthen.grid(row=2, column=1, rowspan=2, padx=2)
    c_andthen.grid(row=2, column=2, rowspan=2)

    if importState != "good":
        b_geno_curr.configure(state="disabled")

    if AB_DISABLE_LIBROSA:
        b_geno_curr.configure(state="disabled")
        b_geno_oaud.configure(state="disabled")

    cboxSel(c_andthen, abConfig.get("onsetsdropdown"))
    c_andthen.bind("<<ComboboxSelected>>", lambda event: abConfig.set("onsetsdropdown", c_andthen.current()))

    applyWindowStyle(onswin)
    onswin.grab_set()

def abEditOnsets(parent, ons2=False):
    parent.destroy()
    edonsw = Toplevel(window)
    if not ons2: edonsw.title("Edit onsets")
    else: edonsw.title("Edit start onsets")

    menu_upper = Menu(edonsw, tearoff=False)
    menu_import = Menu(menu_upper, tearoff=False)
    menu_upper.add_cascade(label="Import", menu=menu_import)
    menu_import.add_command(label="Open onsets file", command=lambda: eoImportOnsets(edonsw, t_onsets, ons2))
    menu_import.add_command(label="Import current onsets", command=lambda: eoCurrentOnsets(t_onsets, ons2))
    if ons2: menu_import.add_command(label="Import current usual onsets", command=lambda: eoCurrentOnsets(t_onsets, False))

    menu_lower = Frame(edonsw, padding=1)
    b_apply = Button(menu_lower, text="Apply", command=lambda: processOnsets(2, convOns(t_onsets.get("1.0", END).split()), ons2))
    b_export = Button(menu_lower, text="Export", command=lambda: processOnsets(1, convOns(t_onsets.get("1.0", END).split()), ons2, "Custom", edonsw))
    b_clear = Button(menu_lower, text="Clear", command=lambda: t_onsets.delete("1.0", END))

    t_onsets = ScrolledText(edonsw, wrap=WORD)
    t_onsets.pack(expand=1, fill="both")
    t_onsets.focus()

    menu_lower.pack(fill="x", expand=False)
    b_apply.pack(side="left")
    b_export.pack(side="left")
    b_clear.pack(side="right")

    edonsw.config(menu=menu_upper)
    applyWindowStyle(edonsw)
    edonsw.grab_set()

def abError(title, exception):
    if shadderrinf.get()==1:
        mb.showerror(title, format_exc())
    else:
        mb.showerror(title, exception)


def cfgUnlockAll():
    e_seed.configure(state="normal")
    e_bpm.configure(state="normal")
    e_quanavgstrt.configure(state="normal")
    e_quanstrt.configure(state="normal")
    e_quanseglgth.configure(state="normal")
    e_quanrep.configure(state="normal")
    e_quanmask.configure(state="normal")
    e_usestartonsets.configure(state="normal")
    e_trimmin.configure(state="normal")
    e_trimmax.configure(state="normal")

def cfgEmpty():
    cfgUnlockAll()
    e_minSize.delete(0, END)
    e_maxSize.delete(0, END)
    e_reverseChance.delete(0, END)
    e_minPL.delete(0, END)
    e_maxPL.delete(0, END)
    e_stopChance.delete(0, END)
    e_conspause.delete(0, END)
    e_minFadeIn.delete(0, END)
    e_maxFadeIn.delete(0, END)
    e_fadeInChance.delete(0, END)
    e_minFadeOut.delete(0, END)
    e_maxFadeOut.delete(0, END)
    e_fadeOutChance.delete(0, END)
    e_fdprior.delete(0, END)
    e_faderestrict.delete(0, END)
    e_mincrossfade.delete(0, END)
    e_maxcrossfade.delete(0, END)
    e_crossfadechance.delete(0, END)
    e_repeatMin.delete(0, END)
    e_repeatMax.delete(0, END)
    e_repeatchance.delete(0, END)
    e_consrep.delete(0, END)
    e_minsegs.delete(0, END)
    e_maxsegs.delete(0, END)
    e_rememberchance.delete(0, END)
    e_avgstrt.delete(0, END)
    e_strtdev.delete(0, END)
    e_strtweights.delete(0, END)
    e_normStrtChance.delete(0, END)
    e_speeds.delete(0, END)
    e_speedweights.delete(0, END)
    e_fdmode_lc.delete(0, END)
    e_fdmode_sf.delete(0, END)
    e_fdmode_en.delete(0, END)
    e_minfdmsk.delete(0, END)
    e_BackmaskCrossfade.delete(0, END)
    e_BackmaskChance.delete(0, END)
    e_asymmetricalBackmaskChance.delete(0, END)
    e_reverseMaskChance.delete(0, END)
    e_doublesize.delete(0, END)
    e_consecbackmask.delete(0, END)
    e_minMaskRepeat.delete(0, END)
    e_maxMaskRepeat.delete(0, END)
    e_maskRepeatChance.delete(0, END)
    e_seed.delete(0, END)
    e_stumblechance.delete(0, END)
    e_stumbledeviation.delete(0, END)
    e_stumbdeviate.delete(0, END)
    e_methStumbleNorm.delete(0, END)
    e_methStumbleForw.delete(0, END)
    e_methStumbleBack.delete(0, END)
    e_stumavgstrt.delete(0, END)
    e_countstumblepauses.delete(0, END)
    e_minCutFdIn.delete(0, END)
    e_maxCutFdIn.delete(0, END)
    e_cutFdInChance.delete(0, END)
    e_minCutFdOut.delete(0, END)
    e_maxCutFdOut.delete(0, END)
    e_cutFdOutChance.delete(0, END)
    e_bpm.delete(0, END)
    e_quanavgstrt.delete(0, END)
    e_quanstrt.delete(0, END)
    e_quanseglgth.delete(0, END)
    e_quanrep.delete(0, END)
    e_quanmask.delete(0, END)
    e_usestartonsets.delete(0, END)
    e_trimmin.delete(0, END)
    e_trimmax.delete(0, END)

def cfgDefault():
    e_minSize.insert(0, "0")
    e_maxSize.insert(0, "0")
    c_methDur.current(0)
    e_reverseChance.insert(0, "0")
    e_minPL.insert(0, "0")
    e_maxPL.insert(0, "0")
    c_methPause.current(0)
    e_stopChance.insert(0, "0")
    e_conspause.insert(0, "0")
    x_propfadein.set(0)
    e_minFadeIn.insert(0, "0")
    e_maxFadeIn.insert(0, "0")
    c_methFdIn.current(0)
    e_fadeInChance.insert(0, "100")
    x_propfadeout.set(0)
    e_minFadeOut.insert(0, "0")
    e_maxFadeOut.insert(0, "0")
    c_methFdOut.current(0)
    e_fadeOutChance.insert(0, "100")
    e_fdprior.insert(0, "0")
    e_faderestrict.insert(0, "0")
    e_mincrossfade.insert(0, "0")
    e_maxcrossfade.insert(0, "0")
    c_methCrsfd.current(0)
    e_crossfadechance.insert(0, "100")
    e_repeatMin.insert(0, "0")
    e_repeatMax.insert(0, "0")
    e_repeatchance.insert(0,"0")
    c_methrep.current(0)
    e_consrep.insert(0, "0")
    e_minsegs.insert(0,"0")
    e_maxsegs.insert(0,"0")
    c_remembertype.current(0)
    e_rememberchance.insert(0,"0")
    e_avgstrt.insert(0, "0")
    e_strtweights.insert(0, "1")
    e_strtdev.insert(0, "0")
    e_normStrtChance.insert(0, "0")
    e_speeds.insert(0, "0")
    c_speedmeasure.current(0)
    e_speedweights.insert(0, "1")
    c_TimeMeasure.current(0)
    e_fdmode_lc.insert(0, "1")
    e_fdmode_sf.insert(0, "0")
    e_fdmode_en.insert(0, "0")
    e_minfdmsk.insert(0, "0")
    e_BackmaskCrossfade.insert(0, "0")
    e_BackmaskChance.insert(0, "0")
    e_asymmetricalBackmaskChance.insert(0, "0")
    e_reverseMaskChance.insert(0, "0")
    e_doublesize.insert(0, "0")
    e_consecbackmask.insert(0, "100")
    e_minMaskRepeat.insert(0, "0")
    e_maxMaskRepeat.insert(0, "0")
    c_methrepmsk.current(0)
    c_maskmode.current(0)
    e_maskRepeatChance.insert(0, "0")
    x_fromseed.set(0)
    e_stumblechance.insert(0, "0")
    e_stumbledeviation.insert(0, "0")
    e_stumbdeviate.insert(0, "100")
    e_methStumbleNorm.insert(0, "1")
    e_methStumbleForw.insert(0, "0")
    e_methStumbleBack.insert(0, "0")
    e_stumavgstrt.insert(0, "0")
    e_countstumblepauses.insert(0, "0")
    x_repmode.set(0)
    x_notepropfd.set(0)
    e_minCutFdIn.insert(0, "0")
    e_maxCutFdIn.insert(0, "0")
    c_methCutFdIn.current(0)
    e_cutFdInChance.insert(0, "100")
    e_minCutFdOut.insert(0, "0")
    e_maxCutFdOut.insert(0, "0")
    c_methCutFdOut.current(0)
    e_cutFdOutChance.insert(0, "100")
    c_quantizeMode.current(0)
    e_bpm.insert(0, "120")
    e_quanavgstrt.insert(0, "100")
    e_quanstrt.insert(0, "100")
    e_quanseglgth.insert(0, "100")
    e_quanrep.insert(0, "100")
    e_quanmask.insert(0, "100")
    e_usestartonsets.insert(0, "100")
    x_trimfile.set(0)
    e_trimmin.insert(0, "0")
    e_trimmax.insert(0, "0")
    x_shiftons.set(1)

def cfgImport(path=None, rempath=True):
    if path==None: path = fd.askopenfilename(filetypes=preset_types, initialdir=abConfig.get("dir_presets"))
    if validPath(path):
        try:
            if rempath: abConfig.set("dir_presets", path=path)
            preset = RawConfigParser()
            preset.read(path, encoding="utf-8")
            ab = "AudioButcher"
            version = preset.get(ab, "version", fallback="2.1.0")
            _avgstrt = preset.get(ab, "avgstrt", fallback="0")
            _speeds = preset.get(ab, "speeds", fallback="0")
            if checkVersion(version):
                cfgEmpty()
                e_minSize.insert(0, preset.get(ab, "minSize", fallback="0"))
                e_maxSize.insert(0, preset.get(ab, "maxSize", fallback="0"))
                cboxSel(c_methDur, preset.get(ab, "methDur", fallback="0"))
                e_reverseChance.insert(0, preset.get(ab, "reverseChance", fallback="0"))
                e_minPL.insert(0, preset.get(ab, "minPL", fallback="0"))
                e_maxPL.insert(0, preset.get(ab, "maxPL", fallback="0"))
                cboxSel(c_methPause, preset.get(ab, "methPause", fallback="0"))
                e_stopChance.insert(0, preset.get(ab, "stopChance", fallback="0"))
                e_conspause.insert(0, preset.get(ab, "conspause", fallback="0"))
                x_propfadein.set(binBool(preset.get(ab, "propfadein", fallback="0")))
                e_minFadeIn.insert(0, preset.get(ab, "minFadeIn", fallback="0"))
                e_maxFadeIn.insert(0, preset.get(ab, "maxFadeIn", fallback="0"))
                cboxSel(c_methFdIn, preset.get(ab, "methFdIn", fallback="0"))
                e_fadeInChance.insert(0, preset.get(ab, "fadeInChance", fallback="100"))
                x_propfadeout.set(binBool(preset.get(ab, "propfadeout", fallback="0")))
                e_minFadeOut.insert(0, preset.get(ab, "minFadeOut", fallback="0"))
                e_maxFadeOut.insert(0, preset.get(ab, "maxFadeOut", fallback="0"))
                cboxSel(c_methFdOut, preset.get(ab, "methFdOut", fallback="0"))
                e_fadeOutChance.insert(0, preset.get(ab, "fadeOutChance", fallback="100"))
                e_fdprior.insert(0, preset.get(ab, "fdprior", fallback="0"))
                e_faderestrict.insert(0, preset.get(ab, "faderestrict", fallback="0"))
                e_mincrossfade.insert(0, preset.get(ab, "mincrossfade", fallback="0"))
                e_maxcrossfade.insert(0, preset.get(ab, "maxcrossfade", fallback="0"))
                cboxSel(c_methCrsfd, preset.get(ab, "methCrsfd", fallback="0"))
                e_crossfadechance.insert(0, preset.get(ab, "crossfadechance", fallback="100"))
                e_repeatMin.insert(0, preset.get(ab, "repeatMin", fallback="0"))
                e_repeatMax.insert(0, preset.get(ab, "repeatMax", fallback="0"))
                cboxSel(c_methrep, preset.get(ab, "methrep", fallback="0"))
                e_repeatchance.insert(0, preset.get(ab, "repeatchance", fallback="0"))
                e_consrep.insert(0, preset.get(ab, "consrep", fallback="0"))
                e_minsegs.insert(0, preset.get(ab, "minsegs", fallback="0"))
                e_maxsegs.insert(0, preset.get(ab, "maxsegs", fallback="0"))
                cboxSel(c_remembertype, preset.get(ab, "remembertype", fallback="0"))
                e_rememberchance.insert(0, preset.get(ab, "rememberchance", fallback="0"))
                e_avgstrt.insert(0, _avgstrt)
                e_strtdev.insert(0, preset.get(ab, "strtdev", fallback="0"))
                e_strtweights.insert(0, preset.get(ab, "strtweights", fallback="1 "*len(_avgstrt.split())))
                e_normStrtChance.insert(0, preset.get(ab, "normStrtChance", fallback="0"))
                e_speeds.insert(0, _speeds)
                cboxSel(c_speedmeasure, preset.get(ab, "speedmeasure", fallback="0"))
                e_speedweights.insert(0, preset.get(ab, "speedweights", fallback="1 "*len(_speeds.split())))
                cboxSel(c_TimeMeasure, preset.get(ab, "TimeMeasure", fallback="0"))
                e_fdmode_lc.insert(0, preset.get(ab, "fdmode_lc", fallback="0"))
                e_fdmode_sf.insert(0, preset.get(ab, "fdmode_sf", fallback="0"))
                e_fdmode_en.insert(0, preset.get(ab, "fdmode_en", fallback="0"))
                e_minfdmsk.insert(0, preset.get(ab, "minfdmsk", fallback="0"))
                e_BackmaskCrossfade.insert(0, preset.get(ab, "BackmaskCrossfade", fallback="0"))
                e_BackmaskChance.insert(0, preset.get(ab, "BackmaskChance", fallback="0"))
                e_asymmetricalBackmaskChance.insert(0, preset.get(ab, "asymmetricalBackmaskChance", fallback="0"))
                e_reverseMaskChance.insert(0, preset.get(ab, "reverseMaskChance", fallback="0"))
                e_doublesize.insert(0, preset.get(ab, "doublesize", fallback="0"))
                e_consecbackmask.insert(0, preset.get(ab, "consecbackmask", fallback="100"))
                e_minMaskRepeat.insert(0, preset.get(ab, "minMaskRepeat", fallback="0"))
                e_maxMaskRepeat.insert(0, preset.get(ab, "maxMaskRepeat", fallback="0"))
                cboxSel(c_methrepmsk, preset.get(ab, "methrepmsk", fallback="0"))
                cboxSel(c_maskmode, preset.get(ab, "maskmode", fallback="0"))
                e_maskRepeatChance.insert(0, preset.get(ab, "maskRepeatChance", fallback="0"))
                x_fromseed.set(binBool(preset.get(ab, "fromseed", fallback="0")))
                e_seed.insert(0, preset.get(ab, "seed", fallback=""))
                e_stumblechance.insert(0, preset.get(ab, "stumblechance", fallback="0"))
                e_stumbledeviation.insert(0, preset.get(ab, "stumbledeviation", fallback="0"))
                e_stumbdeviate.insert(0, preset.get(ab, "stumbdeviate", fallback="100"))
                e_methStumbleNorm.insert(0, preset.get(ab, "methStumbleNorm", fallback="0"))
                e_methStumbleForw.insert(0, preset.get(ab, "methStumbleForw", fallback="0"))
                e_methStumbleBack.insert(0, preset.get(ab, "methStumbleBack", fallback="0"))
                e_stumavgstrt.insert(0, preset.get(ab, "stumavgstrt", fallback="0"))
                e_countstumblepauses.insert(0, preset.get(ab, "countstumblepauses", fallback="0"))
                x_repmode.set(binBool(preset.get(ab, "repmode", fallback="0")))
                x_notepropfd.set(binBool(preset.get(ab, "notepropfd", fallback="0")))
                e_minCutFdIn.insert(0, preset.get(ab, "minCutFdIn", fallback="0"))
                e_maxCutFdIn.insert(0, preset.get(ab, "maxCutFdIn", fallback="0"))
                cboxSel(c_methCutFdIn, preset.get(ab, "methCutFdIn", fallback="0"))
                e_cutFdInChance.insert(0, preset.get(ab, "cutFdInChance", fallback="100"))
                e_minCutFdOut.insert(0, preset.get(ab, "minCutFdOut", fallback="0"))
                e_maxCutFdOut.insert(0, preset.get(ab, "maxCutFdOut", fallback="0"))
                cboxSel(c_methCutFdOut, preset.get(ab, "methCutFdOut", fallback="0"))
                e_cutFdOutChance.insert(0, preset.get(ab, "cutFdOutChance", fallback="100"))
                cboxSel(c_quantizeMode, preset.get(ab, "quantizeMode", fallback="0"))
                e_bpm.insert(0, preset.get(ab, "bpm", fallback="120"))
                e_quanavgstrt.insert(0, preset.get(ab, "quanavgstrt", fallback="100"))
                e_quanstrt.insert(0, preset.get(ab, "quanstrt", fallback="100"))
                e_quanseglgth.insert(0, preset.get(ab, "quanseglgth", fallback="100"))
                e_quanrep.insert(0, preset.get(ab, "quanrep", fallback="100"))
                e_quanmask.insert(0, preset.get(ab, "quanmask", fallback="100"))
                e_usestartonsets.insert(0, preset.get(ab, "usestartonsets", fallback="100"))
                x_trimfile.set(binBool(preset.get(ab, "trimfile", fallback="0")))
                e_trimmin.insert(0, preset.get(ab, "trimmin", fallback="0"))
                e_trimmax.insert(0, preset.get(ab, "trimmax", fallback="0"))
                x_shiftons.set(binBool(preset.get(ab, "shiftons", fallback="1")))
                apply210CompMethod(preset.get(ab, "CompMethod", fallback=None))
                apply220StumMethod(preset.get(ab, "methStumble", fallback=None))
                cfgBackcom(version)
                updateSymbols()
        except Exception as e:
            abError("Preset", e)

def cfgApply():
    global minSize, maxSize, methDur, reverseChance
    global minPL, maxPL, methPause, stopChance, conspause
    global propfadein, minFadeIn, maxFadeIn, methFdIn, fadeInChance
    global propfadeout, minFadeOut, maxFadeOut, methFdOut, fadeOutChance
    global fdprior, faderestrict
    global mincrossfade, maxcrossfade, methCrsfd, crossfadechance
    global repeatMin, repeatMax, methrep, repeatchance, consrep
    global minsegs, maxsegs, remembertype, rememberchance
    global avgstrt, strtweights, strtdev, normStrtChance, speeds, speedweights
    global fdmode_lc, fdmode_sf, fdmode_en, minfdmsk
    global BackmaskCrossfade, BackmaskChance, asymmetricalBackmaskChance, reverseMaskChance, doublesize, consecbackmask
    global minMaskRepeat, maxMaskRepeat, methrepmsk, maskmode, maskRepeatChance
    global stumblechance, stumbledeviation, stumbdeviate, methStumbleNorm, methStumbleForw, methStumbleBack, stumavgstrt, countstumblepauses
    global seed, repmode, notepropfd
    global minCutFdIn, maxCutFdIn, methCutFdIn, cutFdInChance
    global minCutFdOut, maxCutFdOut, methCutFdOut, cutFdOutChance
    global quantizeMode, bpm, quanavgstrt, quanstrt, quanseglgth, quanrep, quanmask, usestartonsets
    global trimfile, trimmin, trimmax, shiftons
    minSize = float(e_minSize.get())
    maxSize = float(e_maxSize.get())
    methDur = c_methDur.current()
    reverseChance = float(e_reverseChance.get())
    minPL = float(e_minPL.get())
    maxPL = float(e_maxPL.get())
    methPause = c_methPause.current()
    stopChance = float(e_stopChance.get())
    conspause = float(e_conspause.get())
    propfadein = x_propfadein.get()
    minFadeIn = float(e_minFadeIn.get())
    maxFadeIn = float(e_maxFadeIn.get())
    methFdIn = c_methFdIn.current()
    fadeInChance = float(e_fadeInChance.get())
    propfadeout = x_propfadeout.get()
    minFadeOut = float(e_minFadeOut.get())
    maxFadeOut = float(e_maxFadeOut.get())
    methFdOut = c_methFdOut.current()
    fadeOutChance = float(e_fadeOutChance.get())
    fdprior = float(e_fdprior.get())
    faderestrict = float(e_faderestrict.get())
    mincrossfade = float(e_mincrossfade.get())
    maxcrossfade = float(e_maxcrossfade.get())
    methCrsfd = c_methCrsfd.current()
    crossfadechance = float(e_crossfadechance.get())
    repeatMin = float(e_repeatMin.get())
    repeatMax = float(e_repeatMax.get())
    methrep = c_methrep.current()
    repeatchance = float(e_repeatchance.get())
    consrep = float(e_consrep.get())
    minsegs = float(e_minsegs.get())
    maxsegs = float(e_maxsegs.get())
    remembertype = c_remembertype.current()
    rememberchance = float(e_rememberchance.get())
    avgstrt = text2list(float, e_avgstrt.get())
    strtweights = text2list(int, e_strtweights.get())
    strtdev = float(e_strtdev.get())
    normStrtChance = float(e_normStrtChance.get())
    speeds = text2list(float, e_speeds.get())
    speedweights = text2list(int, e_speedweights.get())
    TimeMeasure = c_TimeMeasure.current()
    fdmode_lc = int(e_fdmode_lc.get())
    fdmode_sf = int(e_fdmode_sf.get())
    fdmode_en = int(e_fdmode_en.get())
    minfdmsk = float(e_minfdmsk.get())
    BackmaskCrossfade = float(e_BackmaskCrossfade.get())
    BackmaskChance = float(e_BackmaskChance.get())
    asymmetricalBackmaskChance = float(e_asymmetricalBackmaskChance.get())
    reverseMaskChance = float(e_reverseMaskChance.get())
    doublesize = float(e_doublesize.get())
    consecbackmask = float(e_consecbackmask.get())
    minMaskRepeat = float(e_minMaskRepeat.get())
    maxMaskRepeat = float(e_maxMaskRepeat.get())
    methrepmsk = c_methrepmsk.current()
    maskmode = c_maskmode.current()
    maskRepeatChance = float(e_maskRepeatChance.get())
    stumblechance = float(e_stumblechance.get())
    stumbledeviation = float(e_stumbledeviation.get())
    stumbdeviate = float(e_stumbdeviate.get())
    methStumbleNorm = int(e_methStumbleNorm.get())
    methStumbleForw = int(e_methStumbleForw.get())
    methStumbleBack = int(e_methStumbleBack.get())
    stumavgstrt = float(e_stumavgstrt.get())
    countstumblepauses = float(e_countstumblepauses.get())
    repmode = x_repmode.get()
    notepropfd = x_notepropfd.get()
    minCutFdIn = float(e_minCutFdIn.get())
    maxCutFdIn = float(e_maxCutFdIn.get())
    methCutFdIn = c_methCutFdIn.current()
    cutFdInChance = float(e_cutFdInChance.get())
    minCutFdOut = float(e_minCutFdOut.get())
    maxCutFdOut = float(e_maxCutFdOut.get())
    methCutFdOut = c_methCutFdOut.current()
    cutFdOutChance = float(e_cutFdOutChance.get())
    quantizeMode = c_quantizeMode.current()
    bpm = float(e_bpm.get())
    quanavgstrt = float(e_quanavgstrt.get())
    quanstrt = float(e_quanstrt.get())
    quanseglgth = float(e_quanseglgth.get())
    quanrep = float(e_quanrep.get())
    quanmask = float(e_quanmask.get())
    usestartonsets = float(e_usestartonsets.get())
    trimfile = x_trimfile.get()
    trimmin = float(e_trimmin.get())
    trimmax = float(e_trimmax.get())
    shiftons = x_shiftons.get()

    speedmeasure = c_speedmeasure.current()
    if speedmeasure==0: speeds = [2**(speed/12) for speed in speeds]
    elif speedmeasure==1: speeds = [1 + speed/100 for speed in speeds]

    if x_fromseed.get()==1: seed = e_seed.get()
    else: seed = None

    if TimeMeasure == 1:
        avgstrt = [s*1000 for s in avgstrt]
        strtdev*=1000
        minfdmsk*=1000
        BackmaskCrossfade*=1000
        stumbledeviation*=1000
        trimmin*=1000
        trimmax*=1000
        if methDur!=3:
            minSize*=1000
            maxSize*=1000
        if methPause!=3:
            minPL*=1000
            maxPL*=1000
        if methFdIn!=3 and propfadein!=1:
            minFadeIn*=1000
            maxFadeIn*=1000
        if methFdOut!=3 and propfadeout!=1:
            minFadeOut*=1000
            maxFadeOut*=1000
        if methCrsfd!=3:
            mincrossfade*=1000
            maxcrossfade*=1000
        if methrep!=3 and repmode==1:
            minsegs*=1000
            maxsegs*=1000
        if methrepmsk!=3 and maskmode==1:
            minMaskRepeat*=1000
            maxMaskRepeat*=1000

def cfgBackcom(version):
    if version == "2.1.0":
        if e_doublesize.get()=="1":
            e_doublesize.delete(0, END)
            e_doublesize.insert(0, "100")
        version = "2.1.1"
    if version == "2.1.1":
        if e_conspause.get()=="1":
            e_conspause.delete(0, END)
            e_conspause.insert(0, "100")
        if e_consrep.get()=="1":
            e_consrep.delete(0, END)
            e_consrep.insert(0, "100")
        if c_methDur.current()==2: c_methDur.current(3)
        if c_methPause.current()==2: c_methPause.current(3)
        if c_methFdIn.current()==2: c_methFdOut.current(3)
        if c_methFdOut.current()==2: c_methFdOut.current(3)
        if c_methCrsfd.current()==2: c_methCrsfd.current(3)
        if c_methrep.current()==2: c_methrep.current(3)
        if c_methDur.current()==1: c_methDur.current(2)
        if c_methPause.current()==1: c_methPause.current(2)
        if c_methFdIn.current()==1: c_methFdIn.current(2)
        if c_methFdOut.current()==1: c_methFdOut.current(2)
        if c_methCrsfd.current()==1: c_methCrsfd.current(2)
        if c_methrep.current()==1: c_methrep.current(2)
        if c_methrepmsk.current()==1: c_methrepmsk.current(2)
        if c_TimeMeasure.current() != 1:
            _avgstrt = e_avgstrt.get()
            _strtdev = e_strtdev.get()
            e_avgstrt.delete(0, END)
            e_strtdev.delete(0, END)
            for t in _avgstrt.split():
                e_avgstrt.insert(END, sec2ms(t)+" ")
            e_strtdev.insert(0, sec2ms(_strtdev))

def cfgExport(path=None, rempath=True):
    if path==None:
        defname = getNoExt(lastSrcPath)
        if defname!="": defname+=" preset"
        path = fd.asksaveasfilename(filetypes=preset_types, defaultextension=preset_types, initialfile=defname, initialdir=abConfig.get("dir_presets"))
    if validPath(path):
        try:
            if rempath: abConfig.set("dir_presets", path=path)
            summary = f"""[AudioButcher]
version = {abVersionShort}
minSize = {e_minSize.get()}
maxSize = {e_maxSize.get()}
methDur = {c_methDur.current()}
reverseChance = {e_reverseChance.get()}
minPL = {e_minPL.get()}
maxPL = {e_maxPL.get()}
methPause = {c_methPause.current()}
stopChance = {e_stopChance.get()}
conspause = {e_conspause.get()}
propfadein = {x_propfadein.get()}
minFadeIn = {e_minFadeIn.get()}
maxFadeIn = {e_maxFadeIn.get()}
methFdIn = {c_methFdIn.current()}
fadeInChance = {e_fadeInChance.get()}
propfadeout = {x_propfadeout.get()}
minFadeOut = {e_minFadeOut.get()}
maxFadeOut = {e_maxFadeOut.get()}
methFdOut = {c_methFdOut.current()}
fadeOutChance = {e_fadeOutChance.get()}
fdprior = {e_fdprior.get()}
faderestrict = {e_faderestrict.get()}
mincrossfade = {e_mincrossfade.get()}
maxcrossfade = {e_maxcrossfade.get()}
methCrsfd = {c_methCrsfd.current()}
crossfadechance = {e_crossfadechance.get()}
repeatMin = {e_repeatMin.get()}
repeatMax = {e_repeatMax.get()}
methrep = {c_methrep.current()}
repeatchance = {e_repeatchance.get()}
consrep = {e_consrep.get()}
minsegs = {e_minsegs.get()}
maxsegs = {e_maxsegs.get()}
remembertype = {c_remembertype.current()}
rememberchance = {e_rememberchance.get()}
avgstrt = {e_avgstrt.get()}
strtdev = {e_strtdev.get()}
strtweights = {e_strtweights.get()}
normStrtChance = {e_normStrtChance.get()}
speeds = {e_speeds.get()}
speedmeasure = {c_speedmeasure.current()}
speedweights = {e_speedweights.get()}
TimeMeasure = {c_TimeMeasure.current()}
fdmode_lc = {e_fdmode_lc.get()}
fdmode_sf = {e_fdmode_sf.get()}
fdmode_en = {e_fdmode_en.get()}
minfdmsk = {e_minfdmsk.get()}
BackmaskCrossfade = {e_BackmaskCrossfade.get()}
BackmaskChance = {e_BackmaskChance.get()}
asymmetricalBackmaskChance = {e_asymmetricalBackmaskChance.get()}
reverseMaskChance = {e_reverseMaskChance.get()}
doublesize = {e_doublesize.get()}
consecbackmask = {e_consecbackmask.get()}
minMaskRepeat = {e_minMaskRepeat.get()}
maxMaskRepeat = {e_maxMaskRepeat.get()}
methrepmsk = {c_methrepmsk.current()}
maskmode = {c_maskmode.current()}
maskRepeatChance = {e_maskRepeatChance.get()}
fromseed = {x_fromseed.get()}
seed = {e_seed.get()}
stumblechance = {e_stumblechance.get()}
stumbledeviation = {e_stumbledeviation.get()}
stumbdeviate = {e_stumbdeviate.get()}
methStumbleNorm = {e_methStumbleNorm.get()}
methStumbleForw = {e_methStumbleForw.get()}
methStumbleBack = {e_methStumbleBack.get()}
stumavgstrt = {e_stumavgstrt.get()}
countstumblepauses = {e_countstumblepauses.get()}
repmode = {x_repmode.get()}
notepropfd = {x_notepropfd.get()}
minCutFdIn = {e_minCutFdIn.get()}
maxCutFdIn = {e_maxCutFdIn.get()}
methCutFdIn = {c_methCutFdIn.current()}
cutFdInChance = {e_cutFdInChance.get()}
minCutFdOut = {e_minCutFdOut.get()}
maxCutFdOut = {e_maxCutFdOut.get()}
methCutFdOut = {c_methCutFdOut.current()}
cutFdOutChance = {e_cutFdOutChance.get()}
quantizeMode = {c_quantizeMode.current()}
bpm = {e_bpm.get()}
quanavgstrt = {e_quanavgstrt.get()}
quanstrt = {e_quanstrt.get()}
quanseglgth = {e_quanseglgth.get()}
quanrep = {e_quanrep.get()}
quanmask = {e_quanmask.get()}
usestartonsets = {e_usestartonsets.get()}
trimfile = {x_trimfile.get()}
trimmin = {e_trimmin.get()}
trimmax = {e_trimmax.get()}
shiftons = {x_shiftons.get()}
"""
            preset = open(path, "w", encoding="utf-8")
            preset.write(summary)
            preset.close()
        except Exception as e:
            abError("Preset", e)


def checkImportedFile():
    if importState=="none":
        mb.showerror("Error", "You have to first import an audio file!")
        return False
    elif importState=="wait":
        mb.showerror("Error", "Please wait while importing!")
        return False
    elif importState=="good":
        return True

def checkComboboxes():
    wrong = -1 in [methDur, methPause, methFdIn, methFdOut, methCrsfd, methrep, remembertype, c_speedmeasure.current(), c_TimeMeasure.current(), methrepmsk, maskmode, quantizeMode]
    if wrong: mb.showerror("Error", "Please check all checkboxes!")
    return not wrong

def checkZeroSegment():
    wrong = minSize==0 and maxSize==0
    if wrong: mb.showerror("Error", "Segment length can't be zero!")
    return not wrong

def checkWrongRandom():
    wrong = False
    if methDur==0 and minSize > maxSize: wrong = True
    elif methPause==0 and minPL > maxPL: wrong = True
    elif methrepmsk==0 and minMaskRepeat > maxMaskRepeat: wrong = True
    elif methrep==0 and repeatMin > repeatMax: wrong = True
    elif methCrsfd==0 and mincrossfade > maxcrossfade: wrong = True
    elif methFdIn==0 and minFadeIn > maxFadeIn: wrong = True
    elif methFdOut==0 and minFadeOut > maxFadeOut: wrong = True
    elif remembertype==0 and minsegs > maxsegs: wrong = True
    elif methCutFdIn==0 and minCutFdIn > maxCutFdIn: wrong = True
    elif methCutFdOut==0 and minCutFdOut > maxCutFdOut: wrong = True
    if wrong: mb.showerror("Error", "In UNIFORM random mode, the first value should be less than the second!")
    return not wrong

def checkWrongLognorm():
    wrong = False
    if methDur==3 and (minSize > 10 or maxSize > 10): wrong = True
    elif methPause==3 and (minPL > 10 or maxPL > 10): wrong = True
    elif methFdIn==3 and (minFadeIn > 10 or maxFadeIn > 10): wrong = True
    elif methFdOut==3 and (minFadeOut > 10 or maxFadeOut > 10): wrong = True
    elif methCrsfd==3 and (mincrossfade > 10 or maxcrossfade > 10): wrong = True
    elif methrep==3 and (repeatMin > 10 or repeatMax > 10): wrong = True
    elif methrepmsk==3 and (minMaskRepeat > 10 or maxMaskRepeat > 10): wrong = True
    elif remembertype==3 and (minsegs > 10 or maxsegs > 10): wrong = True
    if wrong: return mb.askyesno("Warning", "In LOGNORMAL random mode, parameters greater than 10 are not recommended! Continue anyway?", icon="warning")
    else: return True

def checkWrongStarts():
    a = len(avgstrt)
    b = len(strtweights)
    if a!=b: mb.showerror("Error", f"The number of average start times and their weights must match! ({a} vs {b})")
    return a==b

def checkWrongSpeeds():
    a = len(speeds)
    b = len(speedweights)
    if a!=b: mb.showerror("Error", f"The number of speeds and their weights must match! ({a} vs {b})")
    return a==b

def checkNegativeSpeeds():
    wrong = False in [0<speed for speed in speeds]
    if wrong: mb.showerror("Error", "Speed ​​cannot be zero or negative!")
    return not wrong

def checkZeroFdModes():
    wrong = fdmode_lc==0 and fdmode_sf==0 and fdmode_en==0
    if wrong: mb.showerror("Error", "You must activate at least one fade mode!")
    return not wrong

def checkZeroStumMethods():
    wrong = methStumbleNorm==0 and methStumbleForw==0 and methStumbleBack==0
    if wrong: mb.showerror("Error", "You must activate at least one stumbling method!")
    return not wrong

def checkOnsets():
    if quantizeMode==1:
        if onsets==[]:
            if mb.askyesno("Error", "You can't use ONSET quantize mode without onsets detected.\nDo you want to detect onsets?", icon="error"): abOnsetsWindow()
            return False
        else:
            return True
    else:
        return True

def checkTrim():
    if trimfile==1 and trimmax<=trimmin:
        return mb.askyesno("Error", "Trim 'From' is bigger than 'To'. 'To' will be defaulted to length of audio. Continue?", icon="warning")
    else:
        return True

def checkConfig():
    return checkImportedFile() and checkComboboxes() and checkZeroSegment() and checkWrongRandom() and checkWrongLognorm() and checkWrongStarts() and checkWrongSpeeds() and checkNegativeSpeeds() and checkZeroFdModes() and checkZeroStumMethods() and checkOnsets() and checkTrim()


def genImportAudio(path=None):
    global audio, lastSrcPath
    if path==None: path = fd.askopenfilename(filetypes=import_types, initialdir=abConfig.get("dir_srcaud"))
    if validPath(path):
        importstate("wait")
        lastSrcPath = path
        abConfig.set("dir_srcaud", path=path)
        try:
            audio = loadAudio(path)
        except Exception as e:
            importstate("none"); updateWindow()
            abError("Import", e)
        else:
            if resetonsets.get()==1:
                processOnsets(2, [])
                processOnsets(2, [], True)
            if autoonsdet.get()==1: getOnsets(None, 2, fromCurrent=True, window=False)
            importstate("good"); updateWindow()
            mb.showinfo("Import", "Audio imported successfully.")

def genSeed(length):
    random.seed()
    symbols = "-AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    proposed = ""
    for i in range(0, length):
        proposed += random.choice(symbols)
    return proposed

def genScramble(export, segTime):
    global generating, genTime, lastSeed
    def pbname():
        pb_time = strftime("%Y-%m-%d_%H-%M-%S", localtime())
        pb_srcp = getNoExt(lastSrcPath).replace(" ", "_")
        if export: pb_tarp = getNoExt(selfile).replace(" ", "_")
        else: pb_tarp = "preview"
        pb_name = f"{pb_time} {pb_srcp} {pb_tarp}"
        if x_fromseed.get()==0: pb_name += f" {lastSeed}"
        return join(abConfig.get("backuppresetsdir"), pb_name+".abp")
    good = segTime!=None and (not previewing or export) and not generating
    try:
        if good: cfgApply()
        if good and checkConfig():
            if export: selfile = fd.asksaveasfilename(filetypes=export_types, defaultextension=export_types, initialfile=newFileName(), initialdir=abConfig.get("dir_resaud"))
            else: selfile = None
            if validPath(selfile):
                genTime = segTime
                lastSeed = seed
                if lastSeed==None: lastSeed = genSeed(8)
                if export:
                    abConfig.set("dir_resaud", path=selfile)
                    abConfig.set("ste", round(segTime))
                if backuppresets.get()==1: cfgExport(pbname(), False)
                generating = True; abort.configure(state="normal")
                slicecr = genMain(audio, segTime, lastSeed, onsets, onsets2)
                if export:
                    slicecr.export(selfile, format="wav")
                    if mb.askyesno("Complete!", "Scrambling complete.\nDo you want to open your file now?", icon="info"): openFile(selfile)
                else: run(genPreview, slicecr, segTime)
    except Exception as e:
        abError("Scrambling", e)
    if good:
        generating = False; abort.configure(state="disabled")
        progress["value"]=0

def genPreview(audio, time):
    global previewing
    try:
        previewing = True; updateWindow()
        supportedFrs = [8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000]
        if time > audio.duration_seconds: time = audio.duration_seconds
        if audio.sample_width > 2: audio = audio.set_sample_width(2)
        if not audio.frame_rate in supportedFrs: audio = audio.set_frame_rate(findNearest(supportedFrs, audio.frame_rate, 0))
        if audio.channels > 2: audio = audio.set_channels(1)
        play(audio[0:time*1000])
    except Exception as e:
        abError("Preview", e)
    finally:
        previewing = False; updateWindow()

def genStopPreview():
    simpleaudio.stop_all()

def genAbort():
    global generating
    generating = not mb.askyesno("Abort", f"Are you sure you want to abort scrambling?\nThe current rendered length is {round(genReady, 3)} seconds out of {genTime} ({round(genReady/genTime*100, 2)}%).\nAudio will be exported/previewed anyway.", icon="warning")

def genRandNum(val1, val2, mode):
    if mode == 0: return random.uniform(val1, val2)
    elif mode == 1:
        fval = -1
        while fval < 0:
            fval = random.gauss(val1,val2)
        return fval
    elif mode == 2: return abs(random.gauss(val1,val2))
    elif mode == 3: return random.lognormvariate(val1,val2)

def genMain(audio, segTime, seed, onsets, onsets2):
    global genReady
    global minfdmsk, trimmin, trimmax

    random.seed(seed)

    lengthOfAudio = audio.duration_seconds*1000
    if trimfile==1:
        if trimmin < 0: trimmin = 0
        if trimmax > lengthOfAudio or trimmax<=trimmin: trimmax = lengthOfAudio
        audio = audio[trimmin:trimmax]
        if shiftons==1:
            onsets = [o-trimmin for o in onsets if trimmin<=o<=trimmax]
            onsets2 = [o-trimmin for o in onsets2 if trimmin<=o<=trimmax]
        lengthOfAudio = audio.duration_seconds*1000


    onsets3 = []

    if quantizeMode != 1:
        onsets2 = []

    if quantizeMode == 2:
        i = 1
        onsets3 = onsets.copy()
        onsets = [0]
        while (i * 60/bpm * 1000) <= audio.duration_seconds*1000:
            onsets.append(i * 60/bpm * 1000)
            i += 1

    slicecr = AudioSegment.silent(duration = 1) #make slicecr audio that we can work with

    counter = 0
    firstTime = 1
    stumblestrt = 0

    print("\nnewgen\n")

    if stumblechance > 0:
        audio += audio[0:0.1*lengthOfAudio]  #1.1x audio length to help prevent stumbling over file end
        newaudlgth = audio.duration_seconds*1000

    if quantizeMode != 0:
        lengthOfAudio = findNearest(onsets, lengthOfAudio, 0)

    paused = 0
    stumbpause = 0
    chance = 0
    fadepause = 0
    repeated = 0
    rembintialized = 0
    backmasked = 0

    #check if minfademask is needed
    if propfadeout == 1 and notepropfd == 1:
        minfdmsk = 0

    def appFadeIn(appender, fdin):
        cutFdIn = genRandNum(minCutFdIn, maxCutFdIn, methCutFdIn)
        if cutFdIn>=100: return appender
        else:
            if cutFdIn!=0 and cutfdinchnce < cutFdInChance:
                cutFdIn = genRandNum(minCutFdIn, maxCutFdIn, methCutFdIn)
                cutFdInLength = fdin * cutFdIn/100
                empty = AudioSegment.silent(duration=cutFdInLength)
                appender = empty + appender
                return appender.fade_in(fdin + int(cutFdInLength))[cutFdInLength:]
            else:
                return appender.fade_in(fdin)

    def appFadeOut(appender, fdout):
        cutFdOut = genRandNum(minCutFdOut, maxCutFdOut, methCutFdOut)
        if cutFdOut>=100: return appender
        else:
            if cutFdOut!=0 and cutfdoutchnce < cutFdOutChance:
                cutFdOutLength = fdout * cutFdOut/100
                empty = AudioSegment.silent(duration=cutFdOutLength)
                appender = appender + empty
                return appender.fade_out(fdout + int(cutFdOutLength))[:-cutFdOutLength]
            else:
                return appender.fade_out(fdout)

    def reverse(audio):
        return AudioSegment.from_mono_audiosegments(*(channel.reverse() for channel in audio.split_to_mono()))

    class processonsets:
        placecross = -1

        @classmethod
        def shift(cls, Onsets):
            if firstTime == 1: cls.placecross = -1
            if Onsets == []:
                Placeonsets = 0
            else:
                Placeonsets = Onsets.copy()
                cls.placecross = spedcross
                for x in range(len(Placeonsets)):
                    Placeonsets[x] -= spedcross
                    if Placeonsets[x] < 0: Placeonsets[x] = 0
            return Placeonsets


    genReady = 0
    while slicecr.duration_seconds < segTime and generating:
        firstchance = random.uniform(0,100)
        inchance = random.uniform(0,100)
        outchance = random.uniform(0,100)
        crosschance = random.uniform(0,100)
        revchance = random.uniform(0,100)
        bkmskchance = random.uniform(0,100)
        repchance = random.uniform(0,100)
        nrmSrtChnce = random.uniform(0,100)
        stumbchnce = random.uniform(0,100)
        asymmaskchnce = random.uniform(0,100)
        doublsize = random.uniform(0,100)
        quanstrtchnce = random.uniform(0,100)
        quanseglgthchnce = random.uniform(0,100)
        quanavgstrtchnce = random.uniform(0,100)
        remberchnce = random.uniform(0,100)
        conspausechce = random.uniform(0,100)
        consrepchce = random.uniform(0,100)
        consbckmskchce = random.uniform(0,100)
        fdpriorchce = random.uniform(0,100)
        quanrepchce = random.uniform(0,100)
        quanmaskchce = random.uniform(0,100)
        faderestrictchce = random.uniform(0,100)
        stumavgstrtchce = random.uniform(0,100)
        countstumblepauseschce = random.uniform(0,100)
        usestartonsetschce = random.uniform(0,100)
        cutfdinchnce = random.uniform(0,100)
        cutfdoutchnce = random.uniform(0,100)
        stumbdeviatechce = random.uniform(0,100)

        if not(firstchance < (100 - stopChance)):
            fadepause = 1
        else:
            fadepause = 0

        averagestart = random.choices(avgstrt, weights=strtweights)[0]
        speed = random.choices(speeds, weights=speedweights)[0]
        CompMethod = random.choices([0, 1, 2], weights=[fdmode_lc, fdmode_sf, fdmode_en])[0]
        methStumble = random.choices([0, 1, 2], weights=[methStumbleNorm, methStumbleForw, methStumbleBack])[0]

        if crosschance < crossfadechance:
            crossfade = genRandNum(mincrossfade, maxcrossfade, methCrsfd)
            if crossfade < 1 and crossfade > 0: crossfade = 1
            crossfade = int(crossfade)
        else:
            crossfade = 0

        if firstTime == 1:                                      #check if it's first loop
            slicecr = AudioSegment.silent(duration = crossfade) #make silence length equal crossfade
            slicecr = slicecr.set_frame_rate(audio.frame_rate)  #defaults to 11025 for some reason. set to track rate.
            firstTime = 0


        spedcross = int(crossfade * speed)
            
        if processonsets.placecross != spedcross:
            placeonsets = processonsets.shift(onsets)
            placeonsets2 = processonsets.shift(onsets2)
            placeonsets3 = processonsets.shift(onsets3)

        if stumbchnce < stumblechance and (not nrmSrtChnce < normStrtChance) and methStumble == 0 and placeonsets != 0:
            placeonsets.insert(0,0)

        spedcross2 = int(crossfade * speed)
        if onsets2 == []:
            placeonsets2 = 0
        elif placecross2 != spedcross2:
            placeonsets2 = onsets2.copy()
            placecross2 = spedcross2
            for x in range(len(placeonsets2)):
                placeonsets2[x] -= spedcross2
                if placeonsets2[x] < 0: placeonsets2[x] = 0


        if nrmSrtChnce < normStrtChance:
            startPosition = -1
            nrmstrtcounter = 0
            while (startPosition < 0 or startPosition >= lengthOfAudio) and nrmstrtcounter < 1000:
                startPosition = random.gauss(averagestart,strtdev)
                nrmstrtcounter += 1
            if nrmstrtcounter == 1000:
                startPosition = random.gauss(averagestart,strtdev)%lengthOfAudio
        elif quanstrtchnce < quanstrt and quantizeMode > 0:
                if placeonsets2 != 0 and usestartonsetschce < usestartonsets and not(stumbchnce < stumblechance and  methStumble == 0):
                    startPosition = random.choice(placeonsets2)
                else:
                    startPosition = random.choice(placeonsets)
        else:
            startPosition = random.uniform(0,lengthOfAudio)

        def quantstart(startPosition, direction = 0):
            if quanstrtchnce < quanstrt and quantizeMode > 0 and (not(nrmSrtChnce < normStrtChance) or quanavgstrtchnce < quanavgstrt):
                if direction == 0 and stumbchnce < stumblechance and (not nrmSrtChnce < normStrtChance) and  methStumble == 1: direction = 2
                if placeonsets2 != 0 and usestartonsetschce < usestartonsets and not(stumbchnce < stumblechance and  methStumble == 0):
                    startIndex = findNearest(placeonsets2, startPosition, 1, direction)
                    if startIndex == (len(placeonsets2)-1): startIndex = 0
                    startPosition = placeonsets2[startIndex]
                else:
                    startIndex = findNearest(placeonsets, startPosition, 1, direction)
                    if startIndex == (len(placeonsets)-1): startIndex = 0
                    startPosition = placeonsets[startIndex]
            return startPosition

        startPosition = quantstart(startPosition)


        randdur = genRandNum(minSize, maxSize, methDur)
        if bkmskchance < BackmaskChance and doublsize < doublesize:
            randdur *= 2
        randdur += spedcross
        while randdur <= spedcross*2: randdur += spedcross

        if lengthOfAudio - startPosition < randdur and not(stumbchnce < stumblechance):
            startPosition = lengthOfAudio - randdur

        pause = genRandNum(minPL, maxPL, methPause)
        pause += spedcross

        fadein = 0
        if inchance < fadeInChance and propfadein == 0:
            fadein = int(genRandNum(minFadeIn, maxFadeIn, methFdIn))

        fadeout = 0
        if outchance < fadeOutChance and propfadeout == 0:
            fadeout = int(genRandNum(minFadeOut, maxFadeOut, methFdOut))


        if randdur < fadein + fadeout: #if possible fade times are longer than duration, increase duration to fade times
            if CompMethod == 0 or (CompMethod == 2 and bkmskchance < BackmaskChance):
                randdur = fadein + fadeout + spedcross
            elif CompMethod == 1:
                if fadein > randdur/2:
                    fadein = int(randdur/2)
                if fadeout > randdur/2:
                    fadeout = int(randdur/2)

        repeatcounter = genRandNum(repeatMin, repeatMax, methrep)
        if repmode == 0:
            if repeatcounter < 1 and repeatcounter > 0:
                repeatcounter = 1
        else: repeatcounter += spedcross
        repeatcounter = int(repeatcounter)

        maskrepeatcounter = genRandNum(minMaskRepeat, maxMaskRepeat, methrepmsk)
        if maskmode == 0:
            if maskrepeatcounter < 1 and maskrepeatcounter > 0:
                maskrepeatcounter = 1
            maskrepeatcounter = int(maskrepeatcounter)


        if stumbdeviate < stumbdeviatechce: tempstumbledeviation = 0
        else: tempstumbledeviation = stumbledeviation

        if stumbchnce < stumblechance and (not nrmSrtChnce < normStrtChance):
            if methStumble == 0:
                startPosition = abs(random.gauss(stumblestrt,tempstumbledeviation))
            elif methStumble == 1:
                startPosition = stumblestrt + abs(random.gauss(0,tempstumbledeviation))
            elif methStumble == 2:
                startPosition = stumblestrt - abs(random.gauss(0,tempstumbledeviation))
            if stumbledeviation > 0 or methStumble != 1:
                if methStumble == 2: startPosition = quantstart(startPosition, 1)
                else:  startPosition = quantstart(startPosition)



        if stumblechance > 0:
            if newaudlgth - startPosition < randdur:
                startPosition = newaudlgth - randdur


        if quanseglgthchnce < quanseglgth and quantizeMode > 0 and (nrmSrtChnce < normStrtChance or (not(stumbchnce < stumblechance) or stumbledeviation > 0 or methStumble != 1)):
            segIndex = findNearest(placeonsets, startPosition + randdur * speed, 1)
            randdur = placeonsets[segIndex] - startPosition + spedcross
            while randdur <= spedcross + 0.1:
                segIndex += 1
                if segIndex < len(placeonsets): randdur = placeonsets[segIndex] - startPosition + spedcross
                else: break
            endPosition = startPosition + randdur
        else: endPosition = startPosition + randdur * speed

        randdurpremask = randdur
        if bkmskchance < BackmaskChance and backmasked == 0: randdur += round(BackmaskCrossfade/2 + .5) * 2
        #fixes offsets in stage three distortions

        if quanrepchce < quanrep and quantizeMode > 0 and repmode == 1:
            repIndex = findNearest(placeonsets, startPosition + randdur + repeatcounter * speed, 1)
            repeatcounter = placeonsets[repIndex] - (startPosition + randdur) + spedcross
            while repeatcounter <= spedcross:
                repIndex += 1
                if repIndex < len(placeonsets): repeatcounter = placeonsets[repIndex] - (startPosition + randdur) + crossfade
                else: break

        if quanmaskchce < quanmask and quantizeMode > 0 and maskmode == 1:
            maskIndex = findNearest(placeonsets, startPosition + randdurpremask + maskrepeatcounter * speed, 1)
            maskrepeatcounter = placeonsets[maskIndex] - (startPosition + randdurpremask) + BackmaskCrossfade*2
            while maskrepeatcounter <= BackmaskCrossfade*2:
                maskIndex += 1
                if maskIndex < len(placeonsets): maskrepeatcounter = placeonsets[maskIndex] - (startPosition + randdurpremask) + BackmaskCrossfade*2
                else: break


        #rember
        rembseg = 0
        if remberchnce < rememberchance and rembintialized == 0:
            rembstartPosition = startPosition
            rembranddur = randdurpremask
            rembendPosition = endPosition
            rembcountdown = genRandNum(minsegs, maxsegs, remembertype)
            if rembcountdown < 1 and rembcountdown > 0:
                rembcountdown = 1
            rembcountdown = int(rembcountdown)
            rembintialized = 1
        elif rembintialized == 1 and rembcountdown > 0: rembcountdown -= 1
        elif rembintialized == 1 and  rembcountdown <= 0:
            startPosition = rembstartPosition
            randdur = rembranddur
            endPosition = rembendPosition
            rembintialized = 0
            rembseg = 1

        #create appender segment

        if chance < (100 - stopChance) or paused == 1:

            if quanseglgthchnce < quanseglgth and quantizeMode > 0: appender = audio[startPosition:startPosition + randdur]
            else: appender = audio[startPosition:startPosition + randdur * speed]    #get audio segment, apply speed change if neccesary

            #apply speed change
            appender = speedChange(appender,speed)


            #trim segment to nearest ms (unless non-forwards stumble)
            if not(stumbchnce < stumblechance) or (methStumble == 1) or nrmSrtChnce < normStrtChance:
              appender = appender[0:int(1000*appender.duration_seconds)]


            #little crossfade shortener for fadecomp2
            def apcrsfd(audio, audio1 = audio):
                apfd = crossfade
                mintime = min(int(1000*audio.duration_seconds),int(1000*audio1.duration_seconds))
                if apfd > mintime:
                    apfd = mintime/2
                    #print("fade crossfade shortened")
                return apfd


            #calculate fades for proportional fade modes using appender length
            fadaplength = 1000*appender.duration_seconds + crossfade
            if inchance < fadeInChance and propfadein == 1:
                fadein = round(genRandNum(minFadeIn, maxFadeIn, methFdIn) * fadaplength/100)
                if fadein > fadaplength and CompMethod != 2: fadein = round(fadaplength)

            if outchance < fadeOutChance and propfadeout == 1:
                fadeout = round(genRandNum(minFadeOut, maxFadeOut, methFdOut) * fadaplength/100)
                if fadeout > fadaplength and CompMethod != 2: fadeout = round(fadaplength)

            #extend segment/note via backmasking for fade compensation 2
            if placeonsets == 0: fadeonsets = 0
            elif placeonsets3 == 0: fadeonsets = placeonsets.copy()
            else:  fadeonsets = placeonsets3.copy()

            if CompMethod == 2 and not(bkmskchance < BackmaskChance):
                appenderlength = 1000*appender.duration_seconds
                if faderestrictchce > faderestrict or ((fadepause == 1 and not(revchance < reverseChance)) or (paused == 1 and revchance < reverseChance)):
                    if fadeout > 0:
                        if fadeonsets != 0:

                            fdsegIndex = findNearest(fadeonsets, startPosition + randdur * speed, 1)
                            shitdur = fadeonsets[fdsegIndex] - startPosition + spedcross
                            while shitdur < randdur and fdsegIndex < len(fadeonsets)-1:
                                fdsegIndex += 1
                                shitdur = fadeonsets[fdsegIndex] - startPosition + spedcross
                            if fdsegIndex > 0:
                                while (endPosition - fadeonsets[fdsegIndex - 1] + spedcross <= minfdmsk) or (fadeonsets[fdsegIndex - 1] >= int(endPosition)):
                                    fdsegIndex -= 1
                                    if fdsegIndex == 0: break

                            if fdsegIndex > 0: fademask1 = audio[fadeonsets[fdsegIndex - 1]:endPosition]
                            else: fademask1 = audio[0:endPosition]


                            fademask1 = speedChange(fademask1,speed)
                            fademask1 = fademask1[0:int(1000*fademask1.duration_seconds)]

                            #change fade to percent of note length if proportional to notes is checked
                            if propfadeout == 1 and notepropfd == 1:
                                fadeout = round(genRandNum(minFadeOut, maxFadeOut, methFdOut) * int(1000*fademask1.duration_seconds)/100)


                            #check if fadeout is 0 again due to it now possibly being a fraction of last note
                            if fadeout > 0:
                                fademask2 = reverse(fademask1)

                                fademask = fademask2.append(fademask1, crossfade=apcrsfd(fademask1))

                                while 1000*fademask.duration_seconds < fadeout:
                                    #print("loop 2 ",1000*fademask.duration_seconds)
                                    fademask = fademask.append(fademask, crossfade=apcrsfd(fademask))


                                appender = appender.append(fademask, crossfade=apcrsfd(fademask,appender))
                                appender = appender[0:appenderlength+fadeout]
                                appender = appFadeOut(appender, fadeout)
                        else:

                            fademask1 = appender
                            fademask2 = reverse(fademask1)

                            fademask = fademask2.append(fademask1, crossfade=apcrsfd(fademask1))
                            while 1000*fademask.duration_seconds < fadeout:
                                fademask = fademask.append(fademask, crossfade=apcrsfd(fademask))
                                print("loop 2 ",1000*fademask.duration_seconds)

                            appender = appender.append(fademask, crossfade=apcrsfd(appender))
                            appender = appender[0:appenderlength+fadeout]
                            appender = appFadeOut(appender, fadeout)

                #fade in + regular compensation for compmethod 2 mode
                if faderestrictchce > faderestrict or ((paused == 1 and not(revchance < reverseChance)) or (fadepause == 1 and revchance < reverseChance)):
                    if fadein > 1000*appender.duration_seconds: fadein = round(1000*appender.duration_seconds)
                    if fadein > 0 and not(bkmskchance < BackmaskChance): appender = appFadeIn(appender, fadein)

            #repeating
            if repchance <= repeatchance and repeated == 0 and (not(bkmskchance < BackmaskChance and asymmaskchnce >= asymmetricalBackmaskChance)):
                appendercopy = appender
                if repmode == 0:
                    while repeatcounter > 0:
                        appender = appender.append(appendercopy, crossfade=crossfade)
                        repeatcounter -= 1
                else:
                    while appender.duration_seconds*1000 < randdur + repeatcounter - crossfade:
                        appender = appender.append(appendercopy, crossfade=crossfade)
                    appender = appender[0:randdur + repeatcounter - crossfade]
                if consrepchce > consrep: repeated = 1
            else:
                repeated = 0

            #backmasking
            if bkmskchance < BackmaskChance and backmasked == 0:
                bckmskfde = BackmaskCrossfade
                if asymmaskchnce >= asymmetricalBackmaskChance:

                    appender = appender[0:randdur/2]

                    if revchance < reverseMaskChance:
                        appender = reverse(appender)

                    revpender = reverse(appender)

                    if bckmskfde > appender.duration_seconds*1000:
                        bckmskfde = int(appender.duration_seconds*1000)

                    appender = appender.append(revpender, crossfade=bckmskfde)

                    if repchance <= maskRepeatChance:
                        temppender = appender
                        if maskmode == 0:
                            randdurmult = maskrepeatcounter
                            while maskrepeatcounter > 0:
                                appender = appender.append(temppender, crossfade=bckmskfde)
                                maskrepeatcounter -= 1
                            appender = appender[0:randdurpremask*randdurmult] #requantizes segment
                        else:
                            while appender.duration_seconds*1000 < randdurpremask + maskrepeatcounter:
                                appender = appender.append(temppender, crossfade=bckmskfde)
                            appender = appender[0:randdurpremask + maskrepeatcounter - bckmskfde*2]
                    else:
                        appender = appender[0:randdurpremask] #requantizes segment
                else:
                    appendlength = appender.duration_seconds*1000

                    if revchance < reverseMaskChance:
                        appender = reverse(appender)

                    revpender = reverse(appender)

                    if bckmskfde > appender.duration_seconds*1000:
                        bckmskfde = int(appender.duration_seconds*1000)

                    appender = appender.append(revpender, crossfade=bckmskfde)
                    tempstrt = random.uniform(0,appendlength)
                    appender = appender[tempstrt:tempstrt + appendlength]
                if consbckmskchce > consecbackmask: backmasked = 1
            else: backmasked = 0


            def applyfades(appender):
                if CompMethod != 2 or bkmskchance < BackmaskChance:
                    if faderestrictchce > faderestrict or paused == 1:
                        if fadein > 0: appender = appFadeIn(appender, fadein)
                    if faderestrictchce > faderestrict or fadepause == 1:
                        if fadeout > 0: appender = appFadeOut(appender, fadeout)
                return appender

            if fdpriorchce < fdprior: appender = applyfades(appender)

            #apply reverse if applicable
            if revchance < reverseChance and not(bkmskchance < BackmaskChance):
                appender = reverse(appender)

            if not(fdpriorchce < fdprior): appender = applyfades(appender)


            paused = 0
            stumbpause = 0
            fadepause = 0
            chance = firstchance
        else:
            #add silence to file
            appender = AudioSegment.silent(duration=pause)
            if conspausechce > conspause: paused = 1
            stumbpause = 1
            chance = firstchance

        if (not nrmSrtChnce < normStrtChance) or (not stumavgstrtchce < stumavgstrt):
            if methStumble == 0:
                stumblestrt += (appender.duration_seconds*1000 - crossfade) * speed
            elif methStumble == 1 and (stumbpause == 0 or countstumblepauseschce < countstumblepauses) and rembseg == 0:
                stumblestrt = startPosition + (appender.duration_seconds*1000 - crossfade) * speed
            elif methStumble == 2 and (stumbpause == 0 or countstumblepauseschce < countstumblepauses) and rembseg == 0:
                stumblestrt = startPosition - (appender.duration_seconds*1000 - crossfade) * speed


        stumblestrt = stumblestrt % lengthOfAudio

        if crossfade > appender.duration_seconds*1000:
            crossfade = int(appender.duration_seconds*1000)
            print("crossfade shortened to ", crossfade)
        if crossfade > slicecr.duration_seconds*1000:
            crossfade = int(slicecr.duration_seconds*1000)
            print("crossfade shortened to ", crossfade)

        #append segment to final variable
        slicecr = slicecr.append(appender, crossfade=crossfade)

        #debug second/segment counter
        counter +=1
        genReady = slicecr.duration_seconds
        progress["value"]=genReady/segTime*100

    return slicecr

if True:
    importState = "none"
    lastSrcPath = ""
    onsets = []
    onsets2 = []
    generating = False
    previewing = False
    lastSeed = None
    genReady = 0

    randmodes = ["Uniform", "Normal", "Folded normal", "Lognorm (µ, σ)"]
    randmodes2 = ["Uniform", "Normal", "F. normal"]
    speedmodes = ["Semitones", "Percent change", "Speed multiplier"]
    timemodes = ["Milliseconds", "Seconds"]
    repmeasmodes = ["Times", "Length"]
    quantmodes = ["None", "Onsets", "BPM"]

    import_types_1 = [["Popular formats", "*.wav *.mp3 *.ogg *.flac"],
                      ["Wave", "*.wav"],
                      ["MPEG Layer-3", "*.mp3"],
                      ["Ogg Vorbis", "*.ogg"],
                      ["FLAC", "*.flac"],
                      ["All files", "*.*"]]

    import_types_2 = [["Popular formats", "*.wav *.mp3 *.wma *.ogg *.opus *.flac *.aac *.m4a"],
                      ["Wave", "*.wav"],
                      ["MPEG Layer-3", "*.mp3"],
                      ["Windows Media Audio", "*.wma"],
                      ["Ogg Vorbis", "*.ogg"],
                      ["Opus", "*.opus"],
                      ["FLAC", "*.flac"],
                      ["AAC", "*.aac"],
                      ["MPEG-4 Audio", "*.m4a"],
                      ["All files", "*.*"]]

    export_types = [["Wave", "*.wav"],
                    ["All files", "*.*"]]

    preset_types = [["AudioButcher Preset", "*.abp"],
                    ["All files", "*.*"]]

    onset_types = [["AudioButcher Onset List", "*.abo"],
                   ["Text files", "*.txt"],
                   ["All files", "*.*"]]

    abConfig = abConfigure(join(homepath, ".audiobutcher"), "AudioButcher_Config")

    # Window
    window = Tk()
    tabs = Notebook(window)
    tab1 = Frame(tabs, padding=10)
    tab2 = Frame(tabs, padding=10)
    tabs.pack(side="top", fill="both", expand=True)
    tabs.add(tab1, text="Main")
    tabs.add(tab2, text="Advanced")

    # Menus
    menu = Menu(window)
    window.config(menu=menu)
    menu_file = Menu(menu, tearoff=False)
    smenu_pbu = Menu(menu_file, tearoff=False)
    menu_prev = Menu(menu, tearoff=False)
    smenu_stp = Menu(menu_prev, tearoff=False)
    menu_pref = Menu(menu, tearoff=False)
    menu_debg = Menu(menu, tearoff=False)
    menu_help = Menu(menu, tearoff=False)
    menu.add_cascade(label="File", menu=menu_file)
    menu.add_cascade(label="Preview", menu=menu_prev)
    menu.add_cascade(label="Preferences", menu=menu_pref)
    if AB_DEBUG_BUTTON: menu.add_cascade(label="Debug", menu=menu_debg)
    menu.add_cascade(label="Help", menu=menu_help)

    # File menu
    menu_file.add_command(label="Import audio file...", accelerator="Ctrl+I", command=lambda: run(genImportAudio))
    menu_file.add_command(label="Export audio...", accelerator="Ctrl+E", command=lambda: run(genScramble, True, getExportLength()))
    menu_file.add_command(label="Refresh file", accelerator="Ctrl+R", command=lambda: run(genImportAudio, lastSrcPath))
    menu_file.add_separator()
    menu_file.add_command(label="Open preset...", accelerator="Ctrl+O", command=lambda: cfgImport())
    menu_file.add_command(label="Save preset...", accelerator="Ctrl+S", command=lambda: cfgExport())
    menu_file.add_command(label="Clear all settings", accelerator="Ctrl+N", command=lambda: abDefaultConfig())
    menu_file.add_separator()
    menu_file.add_command(label="Restore the last seed", command=lambda: restoreLastSeed())
    menu_file.add_cascade(label="Presets backup", menu=smenu_pbu)
    menu_file.add_separator()
    menu_file.add_command(label="Quit", command=lambda: sys.exit())

    # File menu / Presets backup
    backuppresets = IntVar()
    smenu_pbu.add_checkbutton(label="Backup presets", var=backuppresets, command=lambda: updBackupPresets())
    smenu_pbu.add_command(label="Choose presets backup directory", command=lambda: updBackupPresetsDir())
    smenu_pbu.add_command(label="Open presets backup directory", command=lambda: openBackupPresetsDir())

    # Preview menu
    menu_prev.add_command(label="Preview", accelerator="Ctrl+P", command=lambda: run(genScramble, False, stp.get()))
    if not AB_DISABLE_SIMPLEAUDIO: menu_prev.add_command(label="Stop preview", accelerator="Ctrl+Alt+P", command=lambda: genStopPreview())
    menu_prev.add_cascade(label="Preview length", menu=smenu_stp)

    # Preview length submenu
    stp = IntVar()
    smenu_stp.add_radiobutton(label="5 seconds",  var=stp, value=5,  command=lambda: abConfig.set("stp"))
    smenu_stp.add_radiobutton(label="10 seconds", var=stp, value=10, command=lambda: abConfig.set("stp"))
    smenu_stp.add_radiobutton(label="20 seconds", var=stp, value=20, command=lambda: abConfig.set("stp"))
    smenu_stp.add_radiobutton(label="30 seconds", var=stp, value=30, command=lambda: abConfig.set("stp"))
    smenu_stp.add_radiobutton(label="40 seconds", var=stp, value=40, command=lambda: abConfig.set("stp"))
    smenu_stp.add_radiobutton(label="50 seconds", var=stp, value=50, command=lambda: abConfig.set("stp"))
    smenu_stp.add_radiobutton(label="60 seconds", var=stp, value=60, command=lambda: abConfig.set("stp"))
    stp.set(int(abConfig.get("stp")))

    # Preferences menu (variables)
    useunixfilename = IntVar()
    secimpaudlen = IntVar()
    showmoreformats = IntVar()
    shadderrinf = IntVar()
    autoonsdet = IntVar()
    resetonsets = IntVar()
    closeonsets = IntVar()

    # Preferences menu
    menu_pref.add_checkbutton(label="Generate unique filenames", var=useunixfilename, command=lambda: abConfig.set("useunixfilename"))
    menu_pref.add_checkbutton(label="Imported audio length in seconds", var=secimpaudlen, command=lambda: updSecImpAudLen())
    menu_pref.add_checkbutton(label="Show more import formats", var=showmoreformats, command=lambda: updShowMoreFormats())
    menu_pref.add_checkbutton(label="Show additional error information", var=shadderrinf, command=lambda: abConfig.set("shadderrinf"))
    menu_pref.add_separator()
    menu_pref.add_checkbutton(label="Automatically detect onsets", var=autoonsdet, command=lambda: abConfig.set("autoonsdet"))
    menu_pref.add_checkbutton(label="Reset onsets after new file imported", var=resetonsets, command=lambda: abConfig.set("resetonsets"))
    menu_pref.add_checkbutton(label="Automatically close onsets window", var=closeonsets, command=lambda: abConfig.set("closeonsets"))
    if AB_DISABLE_LIBROSA: menu_pref.entryconfig(5, state="disabled")

    #Debug menu
    menu_debg.add_command(label="exec", command=lambda: abDebug(False))
    menu_debg.add_command(label="eval", command=lambda: abDebug(True))

    #Help menu
    menu_help.add_command(label="Join our Discord server", command=lambda: webbrowser.open(abDiscordLink))
    menu_help.add_separator()
    menu_help.add_command(label="License...", command=lambda: webbrowser.open(abLicenceLink))
    menu_help.add_command(label="About...", command=lambda: mb.showinfo(abVersion, abDescription.format(sys.version)))

    # Hotkey binds
    window.bind("<Control-i>", lambda event: run(genImportAudio))
    window.bind("<Control-e>", lambda event: run(genScramble, True, getExportLength()))
    window.bind("<Control-r>", lambda event: run(genImportAudio, lastSrcPath))
    window.bind("<Control-o>", lambda event: cfgImport())
    window.bind("<Control-s>", lambda event: cfgExport())
    window.bind("<Control-n>", lambda event: abDefaultConfig())
    window.bind("<Control-p>", lambda event: run(genScramble, False, stp.get()))
    if not AB_DISABLE_SIMPLEAUDIO: window.bind("<Control-Alt-p>", lambda event: genStopPreview())

    # Main tab
    Label(tab1).grid(row=0, column=6)
    Label(tab1).grid(row=0, column=10)
    Label(tab1).grid(row=11, column=0)
    
    l_Size = Label(tab1, text="Segment length: ")
    e_minSize = Entry(tab1, width=5)
    s_Size = Label(tab1, text="-", width=1)
    e_maxSize = Entry(tab1, width=5)
    s_methDur = Label(tab1, text="/", width=1)
    c_methDur = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_reverseChance = Label(tab1, text="Reverse chance: ")
    e_reverseChance = Entry(tab1, width=3)
    p_reverseChance = Label(tab1, text="%", width=2)

    l_Size.grid(row=0, column=0, sticky="w")
    e_minSize.grid(row=0, column=1)
    s_Size.grid(row=0, column=2)
    e_maxSize.grid(row=0, column=3)
    s_methDur.grid(row=0, column=4)
    c_methDur.grid(row=0, column=5)
    l_reverseChance.grid(row=0, column=7, sticky="w")
    e_reverseChance.grid(row=0, column=8)
    p_reverseChance.grid(row=0, column=9)

    l_PL = Label(tab1, text="Gap length: ")
    e_minPL = Entry(tab1, width=5)
    s_PL = Label(tab1, text="-", width=1)
    e_maxPL = Entry(tab1, width=5)
    s_methPause = Label(tab1, text="/", width=1)
    c_methPause = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_stopChance = Label(tab1, text="Chance to stop: ")
    e_stopChance = Entry(tab1, width=3)
    p_stopChance = Label(tab1, text="%", width=2)
    l_conspause = Label(tab1, text="Chance of consecutive pausing: ")
    e_conspause = Entry(tab1, width=3)
    p_conspause = Label(tab1, text="%", width=2)

    l_PL.grid(row=1, column=0, sticky="w")
    e_minPL.grid(row=1, column=1)
    s_PL.grid(row=1, column=2)
    e_maxPL.grid(row=1, column=3)
    s_methPause.grid(row=1, column=4)
    c_methPause.grid(row=1, column=5)
    l_stopChance.grid(row=1, column=7, sticky="w")
    e_stopChance.grid(row=1, column=8)
    p_stopChance.grid(row=1, column=9)
    l_conspause.grid(row=1, column=12, sticky="w")
    e_conspause.grid(row=1, column=13)
    p_conspause.grid(row=1, column=14)

    x_propfadein = IntVar()
    l_FadeIn = Label(tab1, text="Fade-in length: ")
    c_propfadein = Checkbutton(tab1, text="% ", variable=x_propfadein)
    e_minFadeIn = Entry(tab1, width=5)
    s_FadeIn = Label(tab1, text="-", width=1)
    e_maxFadeIn = Entry(tab1, width=5)
    s_methFdIn = Label(tab1, text="/", width=1)
    c_methFdIn = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_fadeInChance = Label(tab1, text="Chance to fade-in: ")
    e_fadeInChance = Entry(tab1, width=3)
    p_fadeInChance = Label(tab1, text="%", width=2)

    l_FadeIn.grid(row=2, column=0, sticky="w")
    c_propfadein.grid(row=2, column=0, sticky="e")
    e_minFadeIn.grid(row=2, column=1)
    s_FadeIn.grid(row=2, column=2)
    e_maxFadeIn.grid(row=2, column=3)
    s_methFdIn.grid(row=2, column=4)
    c_methFdIn.grid(row=2, column=5)
    l_fadeInChance.grid(row=2, column=7, sticky="w")
    e_fadeInChance.grid(row=2, column=8)
    p_fadeInChance.grid(row=2, column=9)

    x_propfadeout = IntVar()
    l_FadeOut = Label(tab1, text="Fade-out length: ")
    c_propfadeout = Checkbutton(tab1, text="% ", variable=x_propfadeout, command=lambda: updateSymbols())
    e_minFadeOut = Entry(tab1, width=5)
    s_FadeOut = Label(tab1, text="-", width=1)
    e_maxFadeOut = Entry(tab1, width=5)
    s_methFdOut = Label(tab1, text="/", width=1)
    c_methFdOut = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_fadeOutChance = Label(tab1, text="Chance to fade-out: ")
    e_fadeOutChance = Entry(tab1, width=3)
    p_fadeOutChance = Label(tab1, text="%", width=2)

    l_FadeOut.grid(row=3, column=0, sticky="w")
    c_propfadeout.grid(row=3, column=0, sticky="e")
    e_minFadeOut.grid(row=3, column=1)
    s_FadeOut.grid(row=3, column=2)
    e_maxFadeOut.grid(row=3, column=3)
    s_methFdOut.grid(row=3, column=4)
    c_methFdOut.grid(row=3, column=5)
    l_fadeOutChance.grid(row=3, column=7, sticky="w")
    e_fadeOutChance.grid(row=3, column=8)
    p_fadeOutChance.grid(row=3, column=9)

    l_fdprior = Label(tab1, text="Apply fades before reversal (chance): ")
    e_fdprior = Entry(tab1, width=3)
    p_fdprior = Label(tab1, text="%", width=2)
    l_faderestrict = Label(tab1, text="Fade only into pauses (chance): ")
    e_faderestrict = Entry(tab1, width=3)
    p_faderestrict = Label(tab1, text="%", width=2)

    l_fdprior.grid(row=2, column=12, sticky="w")
    e_fdprior.grid(row=2, column=13)
    p_fdprior.grid(row=2, column=14)
    l_faderestrict.grid(row=3, column=12, sticky="w")
    e_faderestrict.grid(row=3, column=13)
    p_faderestrict.grid(row=3, column=14)

    l_crossfade = Label(tab1, text="Crossfade length: ")
    e_mincrossfade = Entry(tab1, width=5)
    s_crossfade = Label(tab1, text="-", width=1)
    e_maxcrossfade = Entry(tab1, width=5)
    s_methCrsfd = Label(tab1, text="/", width=1)
    c_methCrsfd = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_crossfadechance = Label(tab1, text="Chance to crossfade: ")
    e_crossfadechance = Entry(tab1, width=3)
    p_crossfadechance = Label(tab1, text="%", width=2)

    l_crossfade.grid(row=4, column=0, sticky="w")
    e_mincrossfade.grid(row=4, column=1)
    s_crossfade.grid(row=4, column=2)
    e_maxcrossfade.grid(row=4, column=3)
    s_methCrsfd.grid(row=4, column=4)
    c_methCrsfd.grid(row=4, column=5)
    l_crossfadechance.grid(row=4, column=7, sticky="w")
    e_crossfadechance.grid(row=4, column=8)
    p_crossfadechance.grid(row=4, column=9)

    l_repeat = Label(tab1, text="Repeat segment ... times: ")
    e_repeatMin = Entry(tab1, width=5)
    s_repeat = Label(tab1, text="-", width=1)
    e_repeatMax = Entry(tab1, width=5)
    s_methrep = Label(tab1, text="/", width=1)
    c_methrep = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_repeatchance = Label(tab1, text="Chance to repeat: ")
    e_repeatchance = Entry(tab1, width=3)
    p_repeatchance = Label(tab1, text="%", width=2)
    l_consrep = Label(tab1, text="Chance of consecutive repeating: ")
    e_consrep = Entry(tab1, width=3)
    p_consrep = Label(tab1, text="%", width=2)

    l_repeat.grid(row=5, column=0, sticky="w")
    e_repeatMin.grid(row=5, column=1)
    s_repeat.grid(row=5, column=2)
    e_repeatMax.grid(row=5, column=3)
    s_methrep.grid(row=5, column=4)
    c_methrep.grid(row=5, column=5)
    l_repeatchance.grid(row=5, column=7, sticky="w")
    e_repeatchance.grid(row=5, column=8)
    p_repeatchance.grid(row=5, column=9)
    l_consrep.grid(row=5, column=12, sticky="w")
    e_consrep.grid(row=5, column=13)
    p_consrep.grid(row=5, column=14)

    l_remember = Label(tab1, text="Repeat after ... segments: ")
    e_minsegs = Entry(tab1, width=5)
    s_segs = Label(tab1, text="-", width=1)
    e_maxsegs = Entry(tab1, width=5)
    s_remembertype = Label(tab1, text="/", width=1)
    c_remembertype = Combobox(tab1, values=randmodes, width=14, state="readonly")
    l_rememberchance = Label(tab1, text="Chance to reappear: ")
    e_rememberchance = Entry(tab1, width=3)
    p_rememberchance = Label(tab1, text="%", width=2)

    l_remember.grid(row=6, column=0, sticky="w")
    e_minsegs.grid(row=6, column=1)
    s_segs.grid(row=6, column=2)
    e_maxsegs.grid(row=6, column=3)
    s_remembertype.grid(row=6, column=4)
    c_remembertype.grid(row=6, column=5)
    l_rememberchance.grid(row=6, column=7, sticky="w")
    e_rememberchance.grid(row=6, column=8)
    p_rememberchance.grid(row=6, column=9)

    l_avgstrt = Label(tab1, text="Average start times: ")
    e_avgstrt = Entry(tab1, width=33)
    l_strtdev = Label(tab1, text="Average start deviation: ")
    e_strtdev = Entry(tab1, width=6)
    l_strtweights = Label(tab1, text="Start time weights: ")
    e_strtweights = Entry(tab1, width=33)
    l_normStrtChance = Label(tab1, text="Average start chance: ")
    e_normStrtChance = Entry(tab1, width=3)
    p_normStrtChance = Label(tab1, text="%", width=2)

    l_avgstrt.grid(row=7, column=0, sticky="w")
    e_avgstrt.grid(row=7, column=1, columnspan=5)
    l_strtdev.grid(row=7, column=7, sticky="w")
    e_strtdev.grid(row=7, column=8, columnspan=2)
    l_strtweights.grid(row=8, column=0, sticky="w")
    e_strtweights.grid(row=8, column=1, columnspan=5)
    l_normStrtChance.grid(row=8, column=7, sticky="w")
    e_normStrtChance.grid(row=8, column=8)
    p_normStrtChance.grid(row=8, column=9)

    l_speeds = Label(tab1, text="Speed variations: ")
    e_speeds = Entry(tab1, width=63)
    c_speedmeasure = Combobox(tab1, values=speedmodes, width=36, state="readonly")
    l_speedweights = Label(tab1, text="Variation weights: ")
    e_speedweights = Entry(tab1, width=63)

    l_speeds.grid(row=9, column=0, sticky="w")
    e_speeds.grid(row=9, column=1, columnspan=9)
    c_speedmeasure.grid(row=9, column=12, columnspan=3)
    l_speedweights.grid(row=10, column=0, sticky="w")
    e_speedweights.grid(row=10, column=1, columnspan=9)

    l_TimeMeasure = Label(tab1, text="Time measure: ")
    c_TimeMeasure = Combobox(tab1, values=timemodes, width=60, state="readonly")
    l_fdmode = Label(tab1, text="Fade mode weights: ")
    l_fdmode_lc = Label(tab1, text="Lengthen chunks: ")
    e_fdmode_lc = Entry(tab1, width=6)
    l_fdmode_sf = Label(tab1, text="Shorten fades: ")
    e_fdmode_sf = Entry(tab1, width=6)
    l_fdmode_en = Label(tab1, text="Extend notes: ")
    e_fdmode_en = Entry(tab1, width=6)
    l_minfdmsk = Label(tab1, text="Minimum fade backmask: ")
    e_minfdmsk = Entry(tab1, width=5)

    l_TimeMeasure.grid(row=12, column=0, sticky="w")
    c_TimeMeasure.grid(row=12, column=1, columnspan=9)
    l_fdmode.grid(row=13, column=0, sticky="w")
    l_fdmode_lc.grid(row=13, column=1, columnspan=7, sticky="w")
    e_fdmode_lc.grid(row=13, column=8, columnspan=2)
    l_fdmode_sf.grid(row=14, column=1, columnspan=7, sticky="w")
    e_fdmode_sf.grid(row=14, column=8, columnspan=2)
    l_fdmode_en.grid(row=15, column=1, columnspan=7, sticky="w")
    e_fdmode_en.grid(row=15, column=8, columnspan=2)
    l_minfdmsk.grid(row=15, column=12, sticky="w")
    e_minfdmsk.grid(row=15, column=13, columnspan=2)

    # Advanced tab
    lf_Backmask = LabelFrame(tab2, text="Backmasking: ", padding=2)
    l_BackmaskCrossfade = Label(lf_Backmask, text="Crossfade: ")
    e_BackmaskCrossfade = Entry(lf_Backmask, width=5)
    lf_MaskChances = LabelFrame(lf_Backmask, text="Chances: ", padding=2)
    l_BackmaskChance = Label(lf_MaskChances, text="Backmask (General): ")
    e_BackmaskChance = Entry(lf_MaskChances, width=3)
    p_BackmaskChance = Label(lf_MaskChances, text="%", width=2)
    l_asymmetricalBackmaskChance = Label(lf_MaskChances, text="Asymmetrical backmask: ")
    e_asymmetricalBackmaskChance = Entry(lf_MaskChances, width=3)
    p_asymmetricalBackmaskChance = Label(lf_MaskChances, text="%", width=2)
    l_reverseMaskChance = Label(lf_MaskChances, text="Reverse backmask: ")
    e_reverseMaskChance = Entry(lf_MaskChances, width=3)
    p_reverseMaskChance = Label(lf_MaskChances, text="%", width=2)
    l_doublesize = Label(lf_MaskChances, text="Double segment size: ")
    e_doublesize = Entry(lf_MaskChances, width=3)
    p_doublesize = Label(lf_MaskChances, text="%", width=2)
    l_consecbackmask = Label(lf_MaskChances, text="Consecutive backmasking: ")
    e_consecbackmask = Entry(lf_MaskChances, width=3)
    p_consecbackmask = Label(lf_MaskChances, text="%", width=2)
    lf_MaskRepeat = LabelFrame(lf_Backmask, text="Repeats: ", padding=2)
    l_minMaskRepeat = Label(lf_MaskRepeat, text="Minimum: ")
    e_minMaskRepeat = Entry(lf_MaskRepeat, width=4)
    l_maxMaskRepeat = Label(lf_MaskRepeat, text="Maximum: ")
    e_maxMaskRepeat = Entry(lf_MaskRepeat, width=4)
    l_methrepmsk = Label(lf_MaskRepeat, text="Method: ")
    c_methrepmsk = Combobox(lf_MaskRepeat, values=randmodes, width=14, state="readonly")
    l_maskmode = Label(lf_MaskRepeat, text="Measure: ")
    c_maskmode = Combobox(lf_MaskRepeat, values=repmeasmodes, width=14, state="readonly")
    l_maskRepeatChance = Label(lf_MaskRepeat, text="Chance: ")
    e_maskRepeatChance = Entry(lf_MaskRepeat, width=3)
    p_maskRepeatChance = Label(lf_MaskRepeat, text="%", width=2)

    lf_Backmask.grid(row=0, column=0, rowspan=3, padx=3, sticky="n")
    l_BackmaskCrossfade.grid(row=0, column=0, sticky="w")
    e_BackmaskCrossfade.grid(row=0, column=1, sticky="e")
    lf_MaskChances.grid(row=1, column=0, columnspan=2)
    l_BackmaskChance.grid(row=0, column=0, sticky="w")
    e_BackmaskChance.grid(row=0, column=1)
    p_BackmaskChance.grid(row=0, column=2)
    l_asymmetricalBackmaskChance.grid(row=1, column=0, sticky="w")
    e_asymmetricalBackmaskChance.grid(row=1, column=1)
    p_asymmetricalBackmaskChance.grid(row=1, column=2)
    l_reverseMaskChance.grid(row=2, column=0, sticky="w")
    e_reverseMaskChance.grid(row=2, column=1)
    p_reverseMaskChance.grid(row=2, column=2)
    l_doublesize.grid(row=3, column=0, sticky="w")
    e_doublesize.grid(row=3, column=1)
    p_doublesize.grid(row=3, column=2)
    l_consecbackmask.grid(row=4, column=0, sticky="w")
    e_consecbackmask.grid(row=4, column=1)
    p_consecbackmask.grid(row=4, column=2)
    lf_MaskRepeat.grid(row=2, column=0, columnspan=2)
    l_minMaskRepeat.grid(row=0, column=0, sticky="w")
    e_minMaskRepeat.grid(row=0, column=1, sticky="e")
    l_maxMaskRepeat.grid(row=1, column=0, sticky="w")
    e_maxMaskRepeat.grid(row=1, column=1, sticky="e")
    l_methrepmsk.grid(row=2, column=0, sticky="w")
    c_methrepmsk.grid(row=2, column=1)
    l_maskmode.grid(row=3, column=0, sticky="w")
    c_maskmode.grid(row=3, column=1)
    l_maskRepeatChance.grid(row=4, column=0, sticky="w")
    e_maskRepeatChance.grid(row=4, column=1, sticky="e")
    p_maskRepeatChance.grid(row=4, column=2)

    f_Seed = Frame(tab2)
    x_fromseed = IntVar()
    c_fromseed = Checkbutton(f_Seed, text="Generate from seed: ", variable=x_fromseed, command=lambda: updateSymbols())
    e_seed = Entry(f_Seed, width=10)

    f_Seed.grid(row=3, column=0)
    c_fromseed.grid(row=0, column=0, sticky="w")
    e_seed.grid(row=0, column=1, sticky="e")

    lf_Stumbling = LabelFrame(tab2, text="Stumbling: ", padding=2)
    f_StumbChance = Frame(lf_Stumbling)
    l_stumblechance = Label(f_StumbChance, text="Stumble chance: ")
    f_stumblechance = Frame(f_StumbChance)
    e_stumblechance = Entry(f_stumblechance, width=3)
    p_stumblechance = Label(f_stumblechance, text="%")
    lf_StumbDev = LabelFrame(lf_Stumbling, text="Deviation: ", padding=2)
    f_StumbDev1 = Frame(lf_StumbDev)
    f_StumbDev2 = Frame(lf_StumbDev)
    l_stumbledeviation = Label(f_StumbDev1, text="Deviation: ")
    e_stumbledeviation = Entry(f_StumbDev2, width=5)
    l_stumbdeviate = Label(f_StumbDev1, text="Chance to deviate: ")
    e_stumbdeviate = Entry(f_StumbDev2, width=5)
    p_stumbdeviate = Label(f_StumbDev2, text="%")
    lf_MethStumble = LabelFrame(lf_Stumbling, text="Stumbling method weights: ", padding=2)
    f_MethStumble1 = Frame(lf_MethStumble)
    f_MethStumble2 = Frame(lf_MethStumble)
    l_methStumbleNorm = Label(f_MethStumble1, text="Normal: ")
    e_methStumbleNorm = Entry(f_MethStumble2, width=3)
    l_methStumbleForw = Label(f_MethStumble1, text="Forwards: ")
    e_methStumbleForw = Entry(f_MethStumble2, width=3)
    l_methStumbleBack = Label(f_MethStumble1, text="Backwards: ")
    e_methStumbleBack = Entry(f_MethStumble2, width=3)
    lf_StumbleMisc = LabelFrame(lf_Stumbling, text="Misc chances: ", padding=2)
    l_stumavgstrt = Label(lf_StumbleMisc, text="Ignore average start times: ")
    e_stumavgstrt = Entry(lf_StumbleMisc, width=3)
    p_stumavgstrt = Label(lf_StumbleMisc, text="%")
    l_countstumblepauses = Label(lf_StumbleMisc, text="Count pauses: ")
    e_countstumblepauses = Entry(lf_StumbleMisc, width=3)
    p_countstumblepauses = Label(lf_StumbleMisc, text="%")

    lf_Stumbling.grid(row=0, column=1, rowspan=2, padx=3, sticky="n")
    f_StumbChance.pack(side="top", fill="x", expand=True)
    l_stumblechance.pack(side="left")
    f_stumblechance.pack(side="right")
    e_stumblechance.grid(row=0, column=0)
    p_stumblechance.grid(row=0, column=1)
    lf_StumbDev.pack(side="top", fill="x", expand=True)
    f_StumbDev1.pack(side="left")
    f_StumbDev2.pack(side="right")
    l_stumbledeviation.grid(row=0, column=0, sticky="w")
    e_stumbledeviation.grid(row=0, column=0)
    l_stumbdeviate.grid(row=1, column=0, sticky="w")
    e_stumbdeviate.grid(row=1, column=0)
    p_stumbdeviate.grid(row=1, column=1)
    lf_MethStumble.pack(side="top", fill="x", expand=True)
    f_MethStumble1.pack(side="left")
    f_MethStumble2.pack(side="right")
    l_methStumbleNorm.grid(row=0, column=0, sticky="w")
    e_methStumbleNorm.grid(row=0, column=1)
    l_methStumbleForw.grid(row=1, column=0, sticky="w")
    e_methStumbleForw.grid(row=1, column=1)
    l_methStumbleBack.grid(row=2, column=0, sticky="w")
    e_methStumbleBack.grid(row=2, column=1)
    lf_StumbleMisc.pack(side="top", fill="x", expand=True)
    l_stumavgstrt.grid(row=0, column=0, sticky="w")
    e_stumavgstrt.grid(row=0, column=1)
    p_stumavgstrt.grid(row=0, column=2)
    l_countstumblepauses.grid(row=1, column=0, sticky="w")
    e_countstumblepauses.grid(row=1, column=1)
    p_countstumblepauses.grid(row=1, column=2)

    x_repmode = IntVar()
    x_notepropfd = IntVar()

    lf_Misc = LabelFrame(tab2, text="Misc: ", padding=2)
    c_repmode = Checkbutton(lf_Misc, text="Measure segment repeats in ms/sec", variable=x_repmode, command=lambda: updateSymbols())
    c_notepropfd = Checkbutton(lf_Misc, text="Measure backmask fade from last note", variable=x_notepropfd)

    lf_Misc.grid(row=2, column=1, rowspan=2, padx=3, sticky="n")
    c_repmode.grid(row=0, column=0, columnspan=2, sticky="w")
    c_notepropfd.grid(row=1, column=0, columnspan=2, sticky="w")

    lf_CutFades = LabelFrame(tab2, text="Fade cutoffs (%): ", padding=2)
    l_cutFdIn = Label(lf_CutFades, text="Fade-in: ")
    e_minCutFdIn = Entry(lf_CutFades, width=3)
    s_cutFdIn = Label(lf_CutFades, text="-", width=1)
    e_maxCutFdIn = Entry(lf_CutFades, width=3)
    s_methCutFdIn = Label(lf_CutFades, text="/", width=1)
    c_methCutFdIn = Combobox(lf_CutFades, values=randmodes2, width=9, state="readonly")
    l_cutFdInChance = Label(lf_CutFades, text="Chance: ")
    e_cutFdInChance = Entry(lf_CutFades, width=3)
    p_cutFdInChance = Label(lf_CutFades, text="%", width=2)
    l_cutFdOut = Label(lf_CutFades, text="Fade-out: ")
    e_minCutFdOut = Entry(lf_CutFades, width=3)
    s_cutFdOut = Label(lf_CutFades, text="-", width=1)
    e_maxCutFdOut = Entry(lf_CutFades, width=3)
    s_methCutFdOut = Label(lf_CutFades, text="/", width=1)
    c_methCutFdOut = Combobox(lf_CutFades, values=randmodes2, width=9, state="readonly")
    l_cutFdOutChance = Label(lf_CutFades, text="Chance: ")
    e_cutFdOutChance = Entry(lf_CutFades, width=3)
    p_cutFdOutChance = Label(lf_CutFades, text="%", width=2)

    lf_CutFades.grid(row=0, column=2, columnspan=2, padx=3, sticky="n")
    Label(lf_CutFades).grid(row=0, column=6)
    l_cutFdIn.grid(row=0, column=0, sticky="w")
    e_minCutFdIn.grid(row=0, column=1)
    s_cutFdIn.grid(row=0, column=2)
    e_maxCutFdIn.grid(row=0, column=3)
    s_methCutFdIn.grid(row=0, column=4)
    c_methCutFdIn.grid(row=0, column=5)
    l_cutFdInChance.grid(row=0, column=7, sticky="w")
    e_cutFdInChance.grid(row=0, column=8)
    p_cutFdInChance.grid(row=0, column=9)
    l_cutFdOut.grid(row=1, column=0, sticky="w")
    e_minCutFdOut.grid(row=1, column=1)
    s_cutFdOut.grid(row=1, column=2)
    e_maxCutFdOut.grid(row=1, column=3)
    s_methCutFdOut.grid(row=1, column=4)
    c_methCutFdOut.grid(row=1, column=5)
    l_cutFdOutChance.grid(row=1, column=7, sticky="w")
    e_cutFdOutChance.grid(row=1, column=8)
    p_cutFdOutChance.grid(row=1, column=9)

    lf_Quantization = LabelFrame(tab2, text="Quantization: ", padding=2)
    l_quantizeMode = Label(lf_Quantization, text="Mode: ")
    c_quantizeMode = Combobox(lf_Quantization, values=quantmodes, width=13, state="readonly")
    l_bpm = Label(lf_Quantization, text="BPM: ")
    e_bpm = Entry(lf_Quantization, width=16)
    lf_QuantizationChances = LabelFrame(lf_Quantization, text="Chances: ", padding=2)
    l_quanavgstrt = Label(lf_QuantizationChances, text="Average start times: ")
    e_quanavgstrt = Entry(lf_QuantizationChances, width=3)
    p_quanavgstrt = Label(lf_QuantizationChances, text="%")
    l_quanstrt = Label(lf_QuantizationChances, text="Start time: ")
    e_quanstrt = Entry(lf_QuantizationChances, width=3)
    p_quanstrt = Label(lf_QuantizationChances, text="%")
    l_quanseglgth = Label(lf_QuantizationChances, text="Segment length: ")
    e_quanseglgth = Entry(lf_QuantizationChances, width=3)
    p_quanseglgth = Label(lf_QuantizationChances, text="%")
    l_quanrep = Label(lf_QuantizationChances, text="Segment repeats: ")
    e_quanrep = Entry(lf_QuantizationChances, width=3)
    p_quanrep = Label(lf_QuantizationChances, text="%")
    l_quanmask = Label(lf_QuantizationChances, text="Mask repeats: ")
    e_quanmask = Entry(lf_QuantizationChances, width=3)
    p_quanmask = Label(lf_QuantizationChances, text="%")
    l_usestartonsets = Label(lf_QuantizationChances, text="Use start onsets: ")
    e_usestartonsets = Entry(lf_QuantizationChances, width=3)
    p_usestartonsets = Label(lf_QuantizationChances, text="%")
    b_onsets = Button(lf_Quantization, text="Manage onsets", command=lambda: run(abOnsetsWindow))

    lf_Quantization.grid(row=1, column=2, rowspan=3, padx=3, sticky="n")
    l_quantizeMode.grid(row=0, column=0, sticky="w")
    c_quantizeMode.grid(row=0, column=1)
    l_bpm.grid(row=1, column=0, sticky="w")
    e_bpm.grid(row=1, column=1)
    lf_QuantizationChances.grid(row=2, column=0, columnspan=2)
    l_quanavgstrt.grid(row=0, column=0, sticky="w")
    e_quanavgstrt.grid(row=0, column=1)
    p_quanavgstrt.grid(row=0, column=2)
    l_quanstrt.grid(row=1, column=0, sticky="w")
    e_quanstrt.grid(row=1, column=1)
    p_quanstrt.grid(row=1, column=2)
    l_quanseglgth.grid(row=2, column=0, sticky="w")
    e_quanseglgth.grid(row=2, column=1)
    p_quanseglgth.grid(row=2, column=2)
    l_quanrep.grid(row=3, column=0, sticky="w")
    e_quanrep.grid(row=3, column=1)
    p_quanrep.grid(row=3, column=2)
    l_quanmask.grid(row=4, column=0, sticky="w")
    e_quanmask.grid(row=4, column=1)
    p_quanmask.grid(row=4, column=2)
    l_usestartonsets.grid(row=5, column=0, sticky="w")
    e_usestartonsets.grid(row=5, column=1)
    p_usestartonsets.grid(row=5, column=2)
    b_onsets.grid(row=3, column=0, columnspan=2)

    x_trimfile = IntVar()
    x_shiftons = IntVar()

    lf_Trim = LabelFrame(tab2, text="Trim: ", padding=2)
    c_trimfile = Checkbutton(lf_Trim, text="Trim audio file", variable=x_trimfile, command=lambda: updateSymbols())
    l_trimmin = Label(lf_Trim, text="From: ")
    e_trimmin = Entry(lf_Trim, width=7)
    l_trimmax = Label(lf_Trim, text="To: ")
    e_trimmax = Entry(lf_Trim, width=7)
    c_shiftons = Checkbutton(lf_Trim, text="Shift onset times", variable=x_shiftons)

    lf_Trim.grid(row=1, column=3, rowspan=3, padx=3, sticky="n")
    c_trimfile.grid(row=0, column=0, columnspan=2, sticky="w")
    l_trimmin.grid(row=1, column=0, sticky="w")
    e_trimmin.grid(row=1, column=1, sticky="e")
    l_trimmax.grid(row=2, column=0, sticky="w")
    e_trimmax.grid(row=2, column=1, sticky="e")
    c_shiftons.grid(row=3, column=0, columnspan=2, sticky="w")

    # Progress bar
    pbar = Frame(window)
    progress = Progressbar(pbar, orient="horizontal")
    abort = Button(pbar, text="Abort", state="disabled", command=lambda: genAbort())
    pbar.pack(side="bottom", fill="x", expand=False)
    progress.pack(side="left", fill="x", expand=True)
    abort.pack(side="right")

    # Combobox binds
    c_methDur.bind("<<ComboboxSelected>>", updateSymbols)
    c_methPause.bind("<<ComboboxSelected>>", updateSymbols)
    c_methFdIn.bind("<<ComboboxSelected>>", updateSymbols)
    c_methFdOut.bind("<<ComboboxSelected>>", updateSymbols)
    c_methCrsfd.bind("<<ComboboxSelected>>", updateSymbols)
    c_methrep.bind("<<ComboboxSelected>>", updateSymbols)
    c_remembertype.bind("<<ComboboxSelected>>", updateSymbols)
    c_methrepmsk.bind("<<ComboboxSelected>>", updateSymbols)
    c_propfadein.bind("<<ComboboxSelected>>", updateSymbols)
    c_propfadeout.bind("<<ComboboxSelected>>", updateSymbols)
    c_repmode.bind("<<ComboboxSelected>>", updateSymbols)
    c_methCutFdIn.bind("<<ComboboxSelected>>", updateSymbols)
    c_methCutFdOut.bind("<<ComboboxSelected>>", updateSymbols)
    c_quantizeMode.bind("<<ComboboxSelected>>", updateSymbols)

    # Configure
    backuppresets.set(binBool(abConfig.get("backuppresets")))
    useunixfilename.set(binBool(abConfig.get("useunixfilename")))
    secimpaudlen.set(binBool(abConfig.get("secimpaudlen")))
    showmoreformats.set(binBool(abConfig.get("showmoreformats")))
    shadderrinf.set(binBool(abConfig.get("shadderrinf")))
    autoonsdet.set(binBool(abConfig.get("autoonsdet")))
    resetonsets.set(binBool(abConfig.get("resetonsets")))
    closeonsets.set(binBool(abConfig.get("closeonsets")))
    if AB_DISABLE_LIBROSA: autoonsdet.set(0)

    updateWindow()
    applyWindowStyle(window)
    updShowMoreFormats(init=True)
    updBackupPresets(init=True, ask=False)
    abDefaultConfig()
    if len(sys.argv)>=2: run(cfgImport, sys.argv[1], False)
    window.mainloop()
    sys.exit()
