# -*- coding: utf-8 -*-

AB_FORCE_CUSTOM_OS = False
AB_DONT_USE_B64_ICON = False
AB_RESIZABLE_WINDOWS = False
AB_SHOW_LIVE_PREVIEW = False
AB_DISABLE_TKDND2 = False
AB_DISABLE_LIBROSA = False
AB_ALT_USE_AUBIO = False
AB_DISABLE_SOUNDFILE = False
AB_DISABLE_SIMPLEAUDIO = False

import os, sys, random, webbrowser
from time import *
from copy import copy
from math import ceil, log10
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

# Comment out next 3 lines when compiling with AB_DISABLE_TKDND2
if not AB_DISABLE_TKDND2:
    try: from TkinterDnD2 import TkinterDnD
    except ModuleNotFoundError: from tkinterdnd2 import TkinterDnD

# Comment out next 3 lines when compiling with AB_DISABLE_LIBROSA or AB_ALT_USE_AUBIO
if not (AB_DISABLE_LIBROSA or AB_ALT_USE_AUBIO):
    from numpy import array, float32, median
    from librosa.onset import onset_strength, onset_detect

# Comment out next line when compiling without AB_ALT_USE_AUBIO
if AB_ALT_USE_AUBIO: import aubio

# Comment out next line when compiling with AB_DISABLE_SOUNDFILE
if not AB_DISABLE_SOUNDFILE: import soundfile as sf

# Comment out next line when compiling with AB_DISABLE_SIMPLEAUDIO
if not AB_DISABLE_SIMPLEAUDIO: import simpleaudio

# Names
abVersion = "AudioButcher v3.0.0-p"
abVersionShort = "3.0.0"
abKnownVersions = ["3.0.0"]
abDescription = """AudioButcher ver. 3.0.0 (Public Release), September 2023

Brought to you by the AudioButcher Team:
MightInvisible, osdwa, Shriki, vanpassinby, Zach Man

Runs in Python {}
"""
abDiscordLink = "https://discord.gg/gNHxMmfTy4"
abLicenceLink = "https://www.gnu.org/licenses/gpl-3.0.txt"
abIconB64 = "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADqUExURQAAALy8vLq6up6enr6+vpaWlmlp3L29vaenp7S0tFVV4rW1tbi4uAAA/wQE/by8vbm5ub+/v7e3t6ioqKCgoLGxsbi4wXZ21oaG0jg47IeH0h0d9YCA1AIC/gEB/6+vxKurq6iox1ZW4jMz7gcH/RMT+KWlpQ0N+5qamru7u0xM5lJS47a2tpGRzn5+1XNz2Lu7wKmpxo6Ojmpq2L29vxwc9jQ07TQ07kVF6LGxvgMD/oOD0xAQ+rW1wwsL+7KyxD096goK+39/1KSkyKOjowQE/rKysrCwsK6urmpqzQwM+0ZG6Hh41wAAAJ0U8VQAAABOdFJOU///////////////////////////////////////////////////////////////////////////////////////////////////////AKxN+84AAAAJcEhZcwAADsQAAA7EAZUrDhsAAAeqSURBVHhexZoLQxNHFIVjSo1YBokWSqWk+EQrtVaKFgUUqKCi///v9J57z+zM7s5mH9mQT9idOXNnztlNDEl2B98bMOgIp0+lqohL9AgXLpLSOaOGG9y3gQYxJY2l07khsNkW2mQUBZbVggDdUtDIk++zpn+GQ/zKVvYFS+6B1c4DeBPt0xBEbR2aGz8I2lhakg0thdDU0bkBfw/6NI0CaNk1QtssAOVrxBtztwDozN0CoLNtF4JZ23YhmPXi/C0BNuwugOsP8GMA3SYBbt68yVbMaMRGc27ZjtaGBWAnj/imrZWRwV4TbgG2I6oD1NA6gQa4VZrlAywvL5sQuM19W34S2BRWVthIHD3IzkAhwW3CbiuC/4qH/QQIIN4GNeG2JXDyI6yCO3fucLDE2mBtLX57JqeAxuPx3ZWV0egukFO/pAy0S89lCWBdTsZCS4Ml+MasrnIY2AN579498SbRe+SfhfX1dWmpUYaNZthzYmNDAuBBAxwxfhFoHuBYPeovpL0zNgQJwF7G5uZArOgZg/qNDVbNjK2WCkC7JCzphV+VcgBaJWFJn5QC0Arcv3+fLYMVfbG1tSXbxEMA1FAC/BYIA9aaEbHf2nJuK3UGtrfxuy3+9ylCNu+e7CeTyXg8xopTn4QUAr09CpOJOUxSAfzRitvvAsUsF7t9IOchGUCBt8J+ODHs9wBWSweYTLAN5oq6C/6BsFd2/aTXBa4W28sZ8VDJwyk4B/KzQ7UbXEmgEHgAJIPuH1AMcM5oBwFmCeEePnzoHj16xK6iiZz8/xhXuGfIuxr5g7ijKTpgRnB6/JhSfFKce/LkCSTbFoA1m13At0t0sWOlblAXKMRwZDSSH0C5O6UAdBAoFOAgoNIaTB0Oh0/xXY3bFca7HKnHnDOoduGp4XZlmd0ogC2sSIdiDhuU13D2u/FMgbdCtXiAAgcCpqXHmqAzHe2N8BygYGjPRBvNg1EUsdsGmxqTCkCpEpYJz58/p9YQvHRzrocj0bLs16DurQLoH47gLytwwKAsUEjDmoYpK7AF/Bp/eHThGBbkefHiBWNQaI9+6NL5urF3RgGtqaV5ZRkGUKSLl0OXC2FlNexx343YCQGQofER7bm9Pf1tneFPQTc5KwZomECDe6i1BDNfvmRHMHd7DChNRQsFdlvD6WEBDSCoFulVoM4N/hIotEZXcK9esUt/QXWq9Wg1YL8F+WnBW4DQcMkuziByMigEqXZl1nZMYGbRZGlRUqhOwRc1qy6BaYBdwf9hdX8b2mlCcaFpWG2EXkB7LbCgKZiAaTrPllI9A5fleG0ujU2yALpeCKE61nv9eig/Jhos0m1WjwlsRZ62cBmNDQsDAayS61F2TspsUEDbhnV65kxsDojmeH+pjicEbyzEIl1SNhwRMF/Hc0gpdijHP8D6DJYFpNgjIxge7u9rVxNYkUzRMS4iy6iawabW5tHqfwAaFMvI3P39fbSwce7gQGp9uS0+jI6FA01R/wyKUzg4ONjcZDuG7vDnro43utViIfdVUgIpYYtT3r5ll8hfZ4P9BryJoFQNVw9Qz8D7A9P/BVRrce7wcDw+PBwcUqiFLiXevXuXHpiOzDn0UErCldVdsX6EBEACQrEe1hvUEtigVQkm5vEy9tOWKqErKhTKyIiumkE9R+VAA3Rew+n4VO0cvt2gENHRv01y+1LFoOTpfPgR8gZxahoceoCiBzNnyeBqzIF6EEoBVd6/13Yn0svmODrSmnShc+8JhTZgyQiqCY6OjtgqUTOzFp3voVbk+PhYthURpk+tR2efnJxUryDux8fVwzO5n3j7EwpptKrqfzuGdKe9Dujq6dly6uXYnT4H9XmYSqE6YL8d8QstpRiO5OBQBmVCsRWcmp7MoQy7ZhxfzP8gKpszMnWdMFhM8MFgryUfP9qvUumfu/ZeYhZ/w84toBCgvrqqG4rzwZxKD4OK1hrML4B6R1AW8r3eyN+UcHrqTuHEboH5JChwqttqqzPu01RcOa2lcGuG2J+fpxOcCdpI3U1Teem2MeeAe1NAdDbgf3aGm2pSEWYIUPiqXoMggveOX6WrnweznwHlnD4CldgdUC3RLcB/3JdRp0++TcJZKdPTGQCfAujS3OzZSNBXAKxvNsQ0a8RENxMqxQAX3LfG3GK25de+gQZ2F6WgvUAhwIXCTh3hktX6OoxitgH21i2ch8tLNooBzJ4JcK+bNgJ4DQbs2nUzSSGbUgQgIUajceGj0KXCDgLkbHLHbwk+C6PR58/0F0U8zTpjXTDP7Htvwz6MfRkMvvBeg8v48AUNsLzsr7/sXVys6WmQGNAlAPwlgA4DSXCXtgZ1w2y/2g6Ez4I7gO1AeAhwEQj4GwQDdhRgwMWs0loqZFxdXQ2+wv+q9PxPIwH6+X9IxN92tq8lu6e0T759Y6MBcwjwzWgYYy5noA0aYIYEyS+SW9Dk3vJK7KvmluD2iWdsCzMF6AMGWFgC9cZmQQnM2rYLwax1u5AEdOZuAdDZdgtI4I25v/YEtA0BWibAfYFsdoKmcYD2CfLvbVpBSyFqXuOjQEMQt68rAs2MfO86ItDIU+zPPQFtMkqCwNI5QIOYlAY4o0e4cJEqPQeXaA2nT+H79/8BNeXyRCNnMNMAAAAASUVORK5CYII="
abPresets = {
    "Default": "[AudioButcher3]\nversion = 3.0.0\nseg = 0 1000 0\ncrossFd = 5 5 0\nskipForwWeight = 1\n",
    "_1": None,
    "Basic scrambling": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 0\nfromseed = 0\nseed = \n\nseg = 500 1000 0\nsegReverseChance1 = 30\nsegReverseChance2 = 0\npause = 0 250 0\npauseChance = 45\nconsPauseChance = 0\ncrossFd = 5 5 0\ncrossFdChance = 100\nfadeInPerc = 0\nfadeIn = 0 0 0\nfadeInChance = 100\nfadeOnlyIntoPauses = 0\nfadeOutPerc = 0\nfadeOut = 0 0 0\nfadeOutChance = 100\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 0\navgstrtDev = 0\navgstrtWeights = \navgstrtChance = 0\nspeeds = 0\nspeedm = 0\nspeedw = \n\nbackmaskCrossfd = -1\nbackmaskChance = 0\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 0\nbmaskRepeatNum = 0 0 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 0\nextnoteAltPortion = 0 100 0\nextnoteMinNoteLen = 100\nextnoteCrossfd = -1\n\nquanMode = 0\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 0\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 0\nloopDuration = 0\nloopStrictly = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 1\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
    "Basic scrambling II": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 0\nfromseed = 0\nseed = \n\nseg = 750 250 1\nsegReverseChance1 = 30\nsegReverseChance2 = 0\npause = 100 200 1\npauseChance = 45\nconsPauseChance = 15\ncrossFd = 5 5 0\ncrossFdChance = 100\nfadeInPerc = 0\nfadeIn = 50 150 0\nfadeInChance = 100\nfadeOnlyIntoPauses = 0\nfadeOutPerc = 0\nfadeOut = 50 150 0\nfadeOutChance = 100\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 0\navgstrtDev = 0\navgstrtWeights = \navgstrtChance = 0\nspeeds = 0\nspeedm = 0\nspeedw = \n\nbackmaskCrossfd = -1\nbackmaskChance = 0\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 0\nbmaskRepeatNum = 0 0 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 0\nextnoteAltPortion = 0 100 0\nextnoteMinNoteLen = 100\nextnoteCrossfd = -1\n\nquanMode = 0\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 0\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 0\nloopDuration = 0\nloopStrictly = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 1\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
    "Basic scrambling III": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 0\nfromseed = 0\nseed = \n\nseg = 7 0.9 2\nsegReverseChance1 = 30\nsegReverseChance2 = 0\npause = 6 1 2\npauseChance = 45\nconsPauseChance = 15\ncrossFd = 5 5 0\ncrossFdChance = 100\nfadeInPerc = 1\nfadeIn = 0 20 0\nfadeInChance = 80\nfadeOnlyIntoPauses = 100\nfadeOutPerc = 1\nfadeOut = 0 20 0\nfadeOutChance = 80\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 0\navgstrtDev = 0\navgstrtWeights = \navgstrtChance = 0\nspeeds = 0 -4 -12\nspeedm = 0\nspeedw = 10 5 1\n\nbackmaskCrossfd = -1\nbackmaskChance = 0\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 0\nbmaskRepeatNum = 0 0 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 0\nextnoteAltPortion = 0 100 0\nextnoteMinNoteLen = 100\nextnoteCrossfd = -1\n\nquanMode = 0\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 0\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 0\nloopDuration = 0\nloopStrictly = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 1\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
    "_2": None,
    "Repeats demo": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 0\nfromseed = 0\nseed = \n\nseg = 6.6 0.8 2\nsegReverseChance1 = 0\nsegReverseChance2 = 0\npause = 6.6 0.9 2\npauseChance = 70\nconsPauseChance = 0\ncrossFd = 5 5 0\ncrossFdChance = 100\nfadeInPerc = 0\nfadeIn = 0 0 0\nfadeInChance = 100\nfadeOnlyIntoPauses = 0\nfadeOutPerc = 1\nfadeOut = 40 70 0\nfadeOutChance = 100\nfadeOutPercNote = 0\nrepeat = 1 2 1\nrepeatChance = 70\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 0\navgstrtDev = 0\navgstrtWeights = \navgstrtChance = 0\nspeeds = 0\nspeedm = 0\nspeedw = \n\nbackmaskCrossfd = -1\nbackmaskChance = 0\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 0\nbmaskRepeatNum = 0 0 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 0\nextnoteAltPortion = 0 100 0\nextnoteMinNoteLen = 100\nextnoteCrossfd = -1\n\nquanMode = 0\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 0\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 0\nloopDuration = 0\nloopStrictly = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 1\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
    "Reappearance demo": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 0\nfromseed = 0\nseed = \n\nseg = 6.5 1 2\nsegReverseChance1 = 40\nsegReverseChance2 = 0\npause = 0 200 1\npauseChance = 75\nconsPauseChance = 0\ncrossFd = 5 5 0\ncrossFdChance = 100\nfadeInPerc = 1\nfadeIn = 0 10 0\nfadeInChance = 100\nfadeOnlyIntoPauses = 0\nfadeOutPerc = 1\nfadeOut = 0 10 0\nfadeOutChance = 100\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 1 3 0\nremembChance = 80\navgstrtTimes = 0\navgstrtDev = 0\navgstrtWeights = \navgstrtChance = 0\nspeeds = 0 -2 -4 -6\nspeedm = 0\nspeedw = \n\nbackmaskCrossfd = -1\nbackmaskChance = 0\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 0\nbmaskRepeatNum = 0 0 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 0\nextnoteAltPortion = 0 100 0\nextnoteMinNoteLen = 100\nextnoteCrossfd = -1\n\nquanMode = 0\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 0\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 0\nloopDuration = 0\nloopStrictly = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 1\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
    "Average start times demo": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 0\nfromseed = 0\nseed = \n\nseg = 6 1 2\nsegReverseChance1 = 0\nsegReverseChance2 = 0\npause = 6 1 2\npauseChance = 50\nconsPauseChance = 0\ncrossFd = 5 5 0\ncrossFdChance = 100\nfadeInPerc = 1\nfadeIn = 0 10 0\nfadeInChance = 100\nfadeOnlyIntoPauses = 0\nfadeOutPerc = 1\nfadeOut = 0 10 0\nfadeOutChance = 100\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 5000 10000\navgstrtDev = 100\navgstrtWeights = \navgstrtChance = 90\nspeeds = 0\nspeedm = 0\nspeedw = \n\nbackmaskCrossfd = -1\nbackmaskChance = 0\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 0\nbmaskRepeatNum = 0 0 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 0\nextnoteAltPortion = 0 100 0\nextnoteMinNoteLen = 100\nextnoteCrossfd = -1\n\nquanMode = 0\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 0\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 0\nloopDuration = 0\nloopStrictly = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 1\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
    "_3": None,
    "Backmasking demo": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 0\nfromseed = 0\nseed = \n\nseg = 3000 1000 1\nsegReverseChance1 = 0\nsegReverseChance2 = 0\npause = 0 600 1\npauseChance = 60\nconsPauseChance = 0\ncrossFd = 5 5 0\ncrossFdChance = 100\nfadeInPerc = 0\nfadeIn = 0 0 0\nfadeInChance = 100\nfadeOnlyIntoPauses = 0\nfadeOutPerc = 0\nfadeOut = 0 0 0\nfadeOutChance = 100\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 0\navgstrtDev = 0\navgstrtWeights = \navgstrtChance = 0\nspeeds = 0\nspeedm = 0\nspeedw = \n\nbackmaskCrossfd = -1\nbackmaskChance = 100\nbackmaskRevChance = 50\nbackmaskFullChance = 40\nbackmaskAsymChance = 30\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 20\nbmaskRepeatNum = 0 2 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 0\nextnoteAltPortion = 0 100 0\nextnoteMinNoteLen = 100\nextnoteCrossfd = -1\n\nquanMode = 0\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 0\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 0\nloopDuration = 0\nloopStrictly = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 1\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
    "Quantization demo": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 0\nfromseed = 0\nseed = \n\nseg = 6.7 0.9 2\nsegReverseChance1 = 0\nsegReverseChance2 = 0\npause = 200 200 1\npauseChance = 50\nconsPauseChance = 0\ncrossFd = 5 5 0\ncrossFdChance = 100\nfadeInPerc = 1\nfadeIn = 5 10 0\nfadeInChance = 100\nfadeOnlyIntoPauses = 0\nfadeOutPerc = 1\nfadeOut = 5 10 0\nfadeOutChance = 100\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 5000 10000 15000\navgstrtDev = 1000\navgstrtWeights = \navgstrtChance = 50\nspeeds = 0 -4 -8 -12\nspeedm = 0\nspeedw = \n\nbackmaskCrossfd = -1\nbackmaskChance = 0\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 0\nbmaskRepeatNum = 0 0 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 0\nextnoteAltPortion = 0 100 0\nextnoteMinNoteLen = 100\nextnoteCrossfd = -1\n\nquanMode = 1\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 0\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 0\nloopDuration = 0\nloopStrictly = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 1\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
    "Note extension demo": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 0\nfromseed = 0\nseed = \n\nseg = 1000 4000 1\nsegReverseChance1 = 10\nsegReverseChance2 = 40\npause = 0 1000 1\npauseChance = 80\nconsPauseChance = 0\ncrossFd = 5 5 0\ncrossFdChance = 100\nfadeInPerc = 1\nfadeIn = 5 5 0\nfadeInChance = 100\nfadeOnlyIntoPauses = 100\nfadeOutPerc = 1\nfadeOut = 60 20 1\nfadeOutChance = 100\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 0\navgstrtDev = 0\navgstrtWeights = \navgstrtChance = 0\nspeeds = 0\nspeedm = 0\nspeedw = \n\nbackmaskCrossfd = -1\nbackmaskChance = 0\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 0\nbmaskRepeatNum = 0 0 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 100\nextnoteUseAltPortion = 40\nextnoteAltPortion = 100 20 1\nextnoteAltFadeOut = 0\nextnoteMinNoteLen = 60\nextnoteCrossfd = -1\n\nquanMode = 1\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 0\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 0\nloopDuration = 0\nloopStrictly = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 1\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
    "_4": None,
    "Stumbling demo": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 0\nfromseed = 0\nseed = \n\nseg = 6 1 2\nsegReverseChance1 = 0\nsegReverseChance2 = 0\npause = 6 1 2\npauseChance = 15\nconsPauseChance = 0\ncrossFd = 5 5 0\ncrossFdChance = 100\nfadeInPerc = 1\nfadeIn = 10 0 1\nfadeInChance = 100\nfadeOnlyIntoPauses = 100\nfadeOutPerc = 1\nfadeOut = 10 0 1\nfadeOutChance = 100\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 0\navgstrtDev = 0\navgstrtWeights = \navgstrtChance = 0\nspeeds = 0\nspeedm = 0\nspeedw = \n\nbackmaskCrossfd = -1\nbackmaskChance = 0\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 0\nbmaskRepeatNum = 0 0 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 0\nextnoteAltPortion = 0 100 0\nextnoteMinNoteLen = 100\nextnoteCrossfd = -1\n\nquanMode = 0\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 80\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 0\nloopDuration = 0\nloopStrictly = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 1\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
    "Stumbling demo II": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 0\nfromseed = 0\nseed = \n\nseg = 6.8 0.9 2\nsegReverseChance1 = 0\nsegReverseChance2 = 0\npause = 0 0 0\npauseChance = 0\nconsPauseChance = 0\ncrossFd = 5 5 0\ncrossFdChance = 100\nfadeInPerc = 0\nfadeIn = 0 0 0\nfadeInChance = 100\nfadeOnlyIntoPauses = 0\nfadeOutPerc = 0\nfadeOut = 0 0 0\nfadeOutChance = 100\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 0\navgstrtDev = 0\navgstrtWeights = \navgstrtChance = 0\nspeeds = 0 -8\nspeedm = 0\nspeedw = 10 1\n\nbackmaskCrossfd = -1\nbackmaskChance = 50\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 0\nbmaskRepeatNum = 0 0 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 0\nextnotePriority = 0\nextnoteUseAltPortion = 0\nextnoteAltPortion = 0 100 0\nextnoteAltFadeOut = 0\nextnoteMinNoteLen = 100\nextnoteCrossfd = -1\n\nquanMode = 0\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 100\nstumbleLockedMode = 0\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nstumbleCountMuted = 100\nskipChance = 100\n\nskipForwWeight = 5\nskipForwMin = 1000\nskipForwMinChance = 20\nskipForwAddDev = 2000\nskipForwAddDevChance = 100\n\nskipBackWeight = 1\nskipBackMin = 1500\nskipBackMinChance = 100\nskipBackAddDev = 1500\nskipBackAddDevChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nlooping = 0\nloopDuration = 0\nloopStrictly = 1\nloopVarNumber = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopAltSpeed = 100\nloopAltSource = 0\nloopAltBegin = 0\nloopAltRandBegin = 0\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltRepeats = 0\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\nconsecMutedFirst = 0\nconsecMutedChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n\nstumbPrior = 0\nmuteChance = 0\nmuteToPauseChance = 0\nmuteCountPauses = 0\n",
    "Looping demo": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 1\nfromseed = 0\nseed = \n\nseg = 6.5 1 2\nsegReverseChance1 = 0\nsegReverseChance2 = 0\npause = 5.6 1 2\npauseChance = 45\nconsPauseChance = 15\ncrossFd = 0.005 0.005 0\ncrossFdChance = 100\nfadeInPerc = 1\nfadeIn = 0 20 0\nfadeInChance = 80\nfadeOnlyIntoPauses = 100\nfadeOutPerc = 1\nfadeOut = 0 20 0\nfadeOutChance = 80\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 0\navgstrtDev = 0\navgstrtWeights = \navgstrtChance = 0\nspeeds = 0 -4 -8\nspeedm = 0\nspeedw = 10 1 1\n\nbackmaskCrossfd = -1\nbackmaskChance = 0\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 0\nbmaskRepeatNum = 0 0 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 0\nextnoteAltPortion = 0 100 0\nextnoteMinNoteLen = 0.1\nextnoteCrossfd = -1\n\nquanMode = 0\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 0\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 1\nloopDuration = 11\nloopStrictly = 0\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 1\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
    "Looping demo II (Less obvious)": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 1\nfromseed = 0\nseed = \n\nseg = 6.5 1 2\nsegReverseChance1 = 30\nsegReverseChance2 = 0\npause = 6 1 2\npauseChance = 45\nconsPauseChance = 15\ncrossFd = 0.005 0.005 0\ncrossFdChance = 100\nfadeInPerc = 1\nfadeIn = 0 20 0\nfadeInChance = 80\nfadeOnlyIntoPauses = 100\nfadeOutPerc = 1\nfadeOut = 0 20 0\nfadeOutChance = 80\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 0\navgstrtDev = 0\navgstrtWeights = \navgstrtChance = 0\nspeeds = 0 -4 -8\nspeedm = 0\nspeedw = \n\nbackmaskCrossfd = -1\nbackmaskChance = 0\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 0\nbmaskRepeatNum = 0 0 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 0\nextnoteAltPortion = 0 100 0\nextnoteMinNoteLen = 0.1\nextnoteCrossfd = -1\n\nquanMode = 0\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 0\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 1\nloopDuration = 30\nloopStrictly = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 3\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
    "_5": None,
    "General demo": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 0\nfromseed = 0\nseed = \n\nseg = 6.4 0.9 2\nsegReverseChance1 = 0\nsegReverseChance2 = 15\npause = 6 1 2\npauseChance = 35\nconsPauseChance = 0\ncrossFd = 5 5 0\ncrossFdChance = 100\nfadeInPerc = 1\nfadeIn = 10 1 1\nfadeInChance = 70\nfadeOnlyIntoPauses = 80\nfadeOutPerc = 1\nfadeOut = 15 1 1\nfadeOutChance = 70\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 500\navgstrtDev = 100\navgstrtWeights = \navgstrtChance = 3\nspeeds = 0 -2 -4 -12\nspeedm = 0\nspeedw = 20 2 2 1\n\nbackmaskCrossfd = -1\nbackmaskChance = 10\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 70\nbmaskRepeatNum = 0 1 1\nbmaskRepeatInMss = 0\n\nextnoteChance = 7\nextnoteAltPortion = 0 100 0\nextnoteMinNoteLen = 100\nextnoteCrossfd = -1\n\nquanMode = 1\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 50\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 25\nstumbleOnlyStumbled = 25\nstumbleIgnoreAvgSt = 50\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 300\nskipRandAddDevChance = 70\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 0\nloopDuration = 0\nloopStrictly = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 1\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
    "Reverse each note": "[AudioButcher3]\nversion = 3.0.0\n\nconvert2sec = 0\nfromseed = 0\nseed = \n\nseg = 1 1 0\nsegReverseChance1 = 100\nsegReverseChance2 = 0\npause = 0 0 0\npauseChance = 0\nconsPauseChance = 0\ncrossFd = 5 5 0\ncrossFdChance = 100\nfadeInPerc = 0\nfadeIn = 0 0 0\nfadeInChance = 100\nfadeOnlyIntoPauses = 0\nfadeOutPerc = 0\nfadeOut = 0 0 0\nfadeOutChance = 100\nfadeOutPercNote = 0\nrepeat = 0 0 0\nrepeatChance = 0\nrepeatInMss = 0\nrememb = 0 0 0\nremembChance = 0\navgstrtTimes = 0\navgstrtDev = 0\navgstrtWeights = \navgstrtChance = 0\nspeeds = 0\nspeedm = 0\nspeedw = \n\nbackmaskCrossfd = -1\nbackmaskChance = 0\nbackmaskRevChance = 0\nbackmaskFullChance = 0\nbackmaskAsymChance = 0\nbackmaskAsymPortion = 0 100 0\nbmaskRepeatChance = 0\nbmaskRepeatNum = 0 0 0\nbmaskRepeatInMss = 0\n\nextnoteChance = 0\nextnoteAltPortion = 0 100 0\nextnoteMinNoteLen = 100\nextnoteCrossfd = -1\n\nquanMode = 1\nquanBPM = 120.000\nquanAvgStart = 100\nquanAvgStartDir = 3\nquanStumbBegin = 100\nquanStumbBeginDir = 0\nquanStumbleSkip = 100\nquanStumbleSkipDir = 3\nquanBegin = 100\nquanBeginDir = 0\nquanDuration = 100\nquanDurationDir = 2\nquanUseStOnsets = 100\nquanUseStOnsetsDir = 0\n\nstumbleChance = 100\nstumbleOnlyStumbled = 100\nstumbleIgnoreAvgSt = 0\nstumbleCountPauses = 100\nskipChance = 100\n\nskipRandWeight = 0\nskipRandMin = 0\nskipRandMinChance = 100\nskipRandAddDev = 0\nskipRandAddDevChance = 100\n\nskipForwWeight = 1\nskipForwMin = 0\nskipForwMinChance = 100\nskipForwAddDev = 0\nskipForwAddDevChance = 100\n\nskipBackWeight = 0\nskipBackMin = 0\nskipBackMinChance = 100\nskipBackAddDev = 0\nskipBackAddDevChance = 100\n\nlooping = 0\nloopDuration = 0\nloopStrictly = 1\nloopKeepSize = 1\nloopFillWithSilence = 50\nloopVarNumber = 1\nloopAltSpeed = 100\nloopAltAvgBegin = 100\nloopAltStumBegin = 100\nloopAltBegin = 0\nloopAltDuration = 0\nloopAltReQnDur = 100\nloopAltRepeats = 0\nloopAltRev1 = 100\nloopAltRev2 = 100\nloopAltBmask = 0\nloopAltBmRep = 0\nloopAltFadeIn = 0\nloopAltFadeOut = 0\nloopAltNoteExt = 0\n\nfadeInCut = 0 0 0\nfadeInCutChance = 100\nfadeOutCut = 0 0 0\nfadeOutCutChance = 100\n\nconsecPauseFirst = 0\nconsecRepeatFirst = 0\nconsecRepeatChance = 100\nconsecBmaskFirst = 0\nconsecBmaskChance = 100\n\ntrim = 0\ntrimVal1 = 0\ntrimVal2 = 0\ntrimShiftOns = 1\n",
}


if AB_FORCE_CUSTOM_OS: osname = None
else: osname = system()
if osname=="Windows":
    homepath = os.environ["USERPROFILE"]
    temppath = os.environ["TEMP"]
    def openf(file): os.startfile(file)
    def opend(file): call(("explorer.exe", "/select,", file.replace("/", "\\")))
elif osname=="Darwin":
    homepath = os.environ["HOME"]
    temppath = "/tmp"
    def openf(file): call(("open", file))
    def opend(file): pass
elif osname=="Linux":
    homepath = os.environ["HOME"]
    temppath = "/tmp"
    def openf(file): call(("xdg-open", file))
    def opend(file): pass
else: #Custom OS
    homepath = "."
    temppath = "."
    def openf(file): pass
    def opend(file): pass


def run(target, *args):
    Thread(target=target, args=args, daemon=True).start()

def cut2gain(cut):
    if cut <= 0:
        return -120
    elif cut >= 100:
        return 0
    else:
        return log10(cut/100) * 20

def popup(event):
    menu.tk_popup(event.x_root, event.y_root)
    menu.grab_release()

def openFile(file):
    try:
        if abCurrCfg.openscrfolder.get() == 0: openf(file)
        else: opend(file)
    except Exception as e:
        abError("AudioButcher", f"Can't open file:\n{e}")

def delFile(file):
    try: os.remove(file)
    except Exception: pass

def tempWavPath():
    return join(temppath, f"ab_convert_{int(time())}.wav")

def validPath(path):
    return path!="" and path!=()

def getNoExt(name):
    return basename(splitext(name)[0])

def defOnsPath(ons2):
    if ons2: return "dir_onsets2"
    else: return "dir_onsets"

def binBool(b):
    try: return int(bool(int(float(b))))
    except ValueError: return 0

def getBufferSize():
    size = sd.askinteger("Live preview", "Live preview buffer size (in seconds):", initialvalue=abSavCfg.get("livepr_buff"), parent=root)
    if size!=None:
        abSavCfg.set("livepr_buff", size)

def convOns(_onsets):
    try:
        return [float(o) for o in _onsets]
    except Exception as e:
        abError("Onsets", e)
        return None

def checkVersion(version, known=abKnownVersions):
    if version in known:
        return True
    else:
        return mb.askyesno("Warning", f"This preset has been created using an unknown version of AudioButcher ({version}), and is likely not to work as intended.\n\nDo you want to continue opening this preset anyway?", icon="warning")

def applyWindowStyle(obj):
    if not AB_RESIZABLE_WINDOWS: obj.resizable(False, False)
    if not AB_DONT_USE_B64_ICON: obj.iconphoto(True, PhotoImage(data=abIconB64, format="png"))

def loadAudio(path):
    try:
        return AudioSegment.from_file(path)
    except Exception:
        if AB_DISABLE_SOUNDFILE or not isfile(path): raise
        else:
            y, sr = sf.read(path)
            wavpath = tempWavPath()
            sf.write(wavpath, y, sr)
            audio = AudioSegment.from_wav(wavpath)
            delFile(wavpath)
            return audio

def getFormat(path):
    ext = path.split(".")[-1]
    if ext in ["wav", "mp3", "ogg", "flac"]:
        return ext
    else:
        return "wav"

def exportAudio(audio, path):
    try:
        fmt = getFormat(path)
        audio.export(path, format=fmt)
    except Exception:
        if AB_DISABLE_SOUNDFILE: raise
        else:
            wavpath = tempWavPath()
            audio.export(wavpath, format="wav")
            y, sr = sf.read(wavpath)
            delFile(wavpath)
            sf.write(path, y, sr, format=fmt)

def makePlayable(audio):
    supportedFrs = [8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000]
    if audio.sample_width > 2: audio = audio.set_sample_width(2)
    if not audio.frame_rate in supportedFrs:
        idx = findNearestIdx(audio.frame_rate, supportedFrs)
        audio = audio.set_frame_rate(supportedFrs[idx])
    if audio.channels > 2: audio = audio.set_channels(1)
    return audio

def dndGotFile(event):
    path = event.data
    if path[0]+path[-1]=="{}": path = path[1:-1]
    path = path.replace("\{", "{")
    path = path.replace("\}", "}")
    path = path.replace("\ ", " ")
    dndAnalyzeFile(path)

def dndAnalyzeFile(path):
    rempath = bool(abCurrCfg.remdndpath.get())
    ext = splitext(path)[-1].lower()
    if isdir(path) or not exists(path): pass
    elif ext==".abo": onsOpen(root, False, path, rempath, False)
    elif ext==".sto": onsOpen(root, True,  path, rempath, False)
    elif ext==".ab3": run(cfgImport, path, None, rempath)
    elif ext==".abp": run(cfgImportAB2, path, rempath)
    else: run(usrLoadAudio, path, rempath)


def cfgImport(path=None, data=None, rempath=True):
    global presetPath
    if path==None and data==None:
        path = fd.askopenfilename(filetypes=types_preset, initialdir=abSavCfg.get("dir_presets"))
    def get(config, variable, fallback, ident="AudioButcher3"):
        return config.get(ident, variable, fallback=fallback)
    if not(validPath(path)) and data==None: return
    if data != None: presetPath = ""
    else: presetPath = path
    if data==None and rempath: abSavCfg.set("dir_presets", path=path)
    try:
        p = RawConfigParser()
        if data != None: p.read_string(data)
        else: p.read(path, encoding="utf-8")
    except Exception as e:
        abError("Preset", e)
        return
    version = get(p, "version", "unknown")
    if not checkVersion(version): return
    cfgUnlockAll()
    b_convert2sec.set(get(p, "convert2sec", "0"))
    b_fromseed.set(get(p, "fromseed", "0"))
    uiSetText(i_seed, get(p, "seed", ""))
    ir_seg.set(*get(p, "seg", "0 0 0").split())
    ic_segReverseChance1.set(get(p, "segReverseChance1", "0"))
    ic_segReverseChance2.set(get(p, "segReverseChance2", "0"))
    ir_pause.set(*get(p, "pause", "0 0 0").split())
    ic_pause.set(get(p, "pauseChance", "0"))
    ic_consPause.set(get(p, "consPauseChance", "0"))
    ir_crossFd.set(*get(p, "crossFd", "0 0 0").split())
    ic_crossFd.set(get(p, "crossFdChance", "100"))
    ib_fadeInPerc.set(get(p, "fadeInPerc", "0"))
    ir_fadeIn.set(*get(p, "fadeIn", "0 0 0").split())
    ic_fadeIn.set(get(p, "fadeInChance", "100"))
    ic_fadeOnlyIntoPauses.set(get(p, "fadeOnlyIntoPauses", "0"))
    ib_fadeOutPerc.set(get(p, "fadeOutPerc", "0"))
    ir_fadeOut.set(*get(p, "fadeOut", "0 0 0").split())
    ic_fadeOut.set(get(p, "fadeOutChance", "100"))
    ib_fadeOutPercNote.set(get(p, "fadeOutPercNote", "0"))
    ir_repeat.set(*get(p, "repeat", "0 0 0").split())
    ic_repeat.set(get(p, "repeatChance", "0"))
    ib_repeatInMss.set(get(p, "repeatInMss", "0"))
    ir_rememb.set(*get(p, "rememb", "0 0 0").split())
    ic_rememb.set(get(p, "remembChance", "0"))
    uiSetText(i_avgstrtTimes, get(p, "avgstrtTimes", "0"))
    uiSetText(i_avgstrtDev, get(p, "avgstrtDev", "0"))
    uiSetText(i_avgstrtWeights, get(p, "avgstrtWeights", ""))
    i_avgstrtChance.set(get(p, "avgstrtChance", "0"))
    uiSetText(i_speeds, get(p, "speeds", "0"))
    uiSelCbox(x_speedm, get(p, "speedm", "0"))
    uiSetText(i_speedw, get(p, "speedw", ""))
    uiSetText(i_backmaskCrossfd, get(p, "backmaskCrossfd", "-1"))
    i_backmaskChance.set(get(p, "backmaskChance", "0"))
    i_backmaskRevChance.set(get(p, "backmaskRevChance", "0"))
    i_backmaskFullChance.set(get(p, "backmaskFullChance", "0"))
    i_backmaskAsymChance.set(get(p, "backmaskAsymChance", "0"))
    i_backmaskAsymPortion.set(*get(p, "backmaskAsymPortion", "0 100 0").split())
    i_bmaskRepeatChance.set(get(p, "bmaskRepeatChance", "0"))
    i_bmaskRepeatNum.set(*get(p, "bmaskRepeatNum", "0 0 0").split())
    b_bmaskRepeatInMss.set(get(p, "bmaskRepeatInMss", "0"))
    i_extnoteChance.set(get(p, "extnoteChance", "0"))
    b_extnotePriority.set(get(p, "extnotePriority", "0"))
    i_extnoteUseAltPortion.set(get(p, "extnoteUseAltPortion", "0"))
    i_extnoteAltPortion.set(*get(p, "extnoteAltPortion", "0 100 0").split())
    b_extnoteAltFadeOut.set(get(p, "extnoteAltFadeOut", "0"))
    uiSetText(i_extnoteMinNoteLen, get(p, "extnoteMinNoteLen", "100"))
    uiSetText(i_extnoteCrossfd, get(p, "extnoteCrossfd", "-1"))
    uiSelCbox(x_quanMode, get(p, "quanMode", "0"))
    uiSetText(i_quanBPM, get(p, "quanBPM", "120.000"))
    i_quanAvgStart.set(get(p, "quanAvgStart", "100"))
    uiSelCbox(x_quanAvgStartDir, get(p, "quanAvgStartDir", "3"))
    i_quanStumbBegin.set(get(p, "quanStumbBegin", "100"))
    uiSelCbox(x_quanStumbBeginDir, get(p, "quanStumbBeginDir", "0"))
    i_quanStumbleSkip.set(get(p, "quanStumbleSkip", "100"))
    uiSelCbox(x_quanStumbleSkipDir, get(p, "quanStumbleSkipDir", "3"))
    i_quanBegin.set(get(p, "quanBegin", "100"))
    uiSelCbox(x_quanBeginDir, get(p, "quanBeginDir", "0"))
    i_quanDuration.set(get(p, "quanDuration", "100"))
    uiSelCbox(x_quanDurationDir, get(p, "quanDurationDir", "2"))
    i_quanUseStOnsets.set(get(p, "quanUseStOnsets", "100"))
    uiSelCbox(x_quanUseStOnsetsDir, get(p, "quanUseStOnsetsDir", "0"))
    i_stumbleChance.set(get(p, "stumbleChance", "0"))
    b_stumbleLockedMode.set(get(p, "stumbleLockedMode", "0"))
    i_stumbleOnlyStumbled.set(get(p, "stumbleOnlyStumbled", "100"))
    i_stumbleIgnoreAvgSt.set(get(p, "stumbleIgnoreAvgSt", "0"))
    i_stumbleCountPauses.set(get(p, "stumbleCountPauses", "100"))
    i_stumbleCountMuted.set(get(p, "stumbleCountMuted", "100"))
    i_skipChance.set(get(p, "skipChance", "100"))
    uiSetText(i_skipForwWeight, get(p, "skipForwWeight", "0"))
    uiSetText(i_skipForwMin, get(p, "skipForwMin", "0"))
    i_skipForwMinChance.set(get(p, "skipForwMinChance", "100"))
    uiSetText(i_skipForwAddDev, get(p, "skipForwAddDev", "0"))
    i_skipForwAddDevChance.set(get(p, "skipForwAddDevChance", "100"))
    uiSetText(i_skipBackWeight, get(p, "skipBackWeight", "0"))
    uiSetText(i_skipBackMin, get(p, "skipBackMin", "0"))
    i_skipBackMinChance.set(get(p, "skipBackMinChance", "100"))
    uiSetText(i_skipBackAddDev, get(p, "skipBackAddDev", "0"))
    i_skipBackAddDevChance.set(get(p, "skipBackAddDevChance", "100"))
    uiSetText(i_skipRandWeight, get(p, "skipRandWeight", "0"))
    uiSetText(i_skipRandMin, get(p, "skipRandMin", "0"))
    i_skipRandMinChance.set(get(p, "skipRandMinChance", "100"))
    uiSetText(i_skipRandAddDev, get(p, "skipRandAddDev", "0"))
    i_skipRandAddDevChance.set(get(p, "skipRandAddDevChance", "100"))
    b_looping.set(get(p, "looping", "0"))
    uiSetText(i_loopDuration, get(p, "loopDuration", "0"))
    b_loopStrictly.set(get(p, "loopStrictly", "1"))
    uiSetText(i_loopVarNumber, get(p, "loopVarNumber", "1"))
    b_loopKeepSize.set(get(p, "loopKeepSize", "1"))
    i_loopFillWithSilence.set(get(p, "loopFillWithSilence", "50"))
    i_loopAltSpeed.set(get(p, "loopAltSpeed", "100"))
    i_loopAltSource.set(get(p, "loopAltSource", "0"))
    i_loopAltBegin.set(get(p, "loopAltBegin", "0"))
    i_loopAltRandBegin.set(get(p, "loopAltRandBegin", "0"))
    i_loopAltAvgBegin.set(get(p, "loopAltAvgBegin", "100"))
    i_loopAltStumBegin.set(get(p, "loopAltStumBegin", "100"))
    i_loopAltDuration.set(get(p, "loopAltDuration", "0"))
    i_loopAltReQnDur.set(get(p, "loopAltReQnDur", "100"))
    i_loopAltRev1.set(get(p, "loopAltRev1", "100"))
    i_loopAltRev2.set(get(p, "loopAltRev2", "100"))
    i_loopAltRepeats.set(get(p, "loopAltRepeats", "0"))
    i_loopAltBmask.set(get(p, "loopAltBmask", "0"))
    i_loopAltBmRep.set(get(p, "loopAltBmRep", "0"))
    i_loopAltFadeIn.set(get(p, "loopAltFadeIn", "0"))
    i_loopAltFadeOut.set(get(p, "loopAltFadeOut", "0"))
    i_loopAltNoteExt.set(get(p, "loopAltNoteExt", "0"))
    ir_fadeInCut.set(*get(p, "fadeInCut", "0 0 0").split())
    ic_fadeInCut.set(get(p, "fadeInCutChance", "100"))
    ir_fadeOutCut.set(*get(p, "fadeOutCut", "0 0 0").split())
    ic_fadeOutCut.set(get(p, "fadeOutCutChance", "100"))
    b_consecPauseFirst.set(get(p, "consecPauseFirst", "0"))
    b_consecRepeatFirst.set(get(p, "consecRepeatFirst", "0"))
    i_consecRepeatChance.set(get(p, "consecRepeatChance", "100"))
    b_consecBmaskFirst.set(get(p, "consecBmaskFirst", "0"))
    i_consecBmaskChance.set(get(p, "consecBmaskChance", "100"))
    b_consecMutedFirst.set(get(p, "consecMutedFirst", "0"))
    i_consecMutedChance.set(get(p, "consecMutedChance", "100"))
    b_trim.set(get(p, "trim", "0"))
    uiSetText(i_trimVal1, get(p, "trimVal1", "0"))
    uiSetText(i_trimVal2, get(p, "trimVal2", "0"))
    b_trimShiftOns.set(get(p, "trimShiftOns", "1"))
    i_stumbPrior.set(get(p, "stumbPrior", "0"))
    i_muteChance.set(get(p, "muteChance", "0"))
    i_muteToPauseChance.set(get(p, "muteToPauseChance", "0"))
    b_muteCountPauses.set(get(p, "muteCountPauses", "0"))
    cfgUpdate()

def cfgImportAB2(path=None, rempath=True):
    if path==None:
        path = fd.askopenfilename(filetypes=types_preset_ab2, initialdir=abSavCfg.get("dir_presets"))
    def get(config, variable, fallback, ident="AudioButcher"):
        return config.get(ident, variable, fallback=fallback)
    def m2d(meth):
        try:
            return [0, 1, 1, 2][int(meth)]
        except Exception:
            return -1
    def try2flt(a):
        try:
            return float(a)
        except Exception:
            return 0
    def mulsp(a, b, opposite):
        a = try2flt(a)
        b = try2flt(b)
        if opposite: b = 100 - b
        return round(a * b / 100, 1)
    def w2p(a, ws):
        try:
            ws = [int(w) for w in ws]
            return round(int(a) / sum(ws) * 100, 1)
        except Exception:
            return 0
    def strsum(*strs):
        try:
            strs = [int(s) for s in strs]
            return sum(strs)
        except Exception:
            return 0
    if not validPath(path): return
    if rempath: abSavCfg.set("dir_presets", path=path)
    try:
        p = RawConfigParser()
        p.read(path, encoding="utf-8")
    except Exception as e:
        abError("Preset", e)
        return
    version = get(p, "version", "2.1.0")
    if not checkVersion(version, ["2.1.0", "2.1.1", "2.2.0", "2.2.1.00", "2.2.2.00", "2.2.3.00"]): return
    minSize = get(p, "minSize", "0")
    maxSize = get(p, "maxSize", "0")
    methDur = get(p, "methDur", "0")
    reverseChance = get(p, "reverseChance", "0")
    minPL = get(p, "minPL", "0")
    maxPL = get(p, "maxPL", "0")
    methPause = get(p, "methPause", "0")
    stopChance = get(p, "stopChance", "0")
    conspause = get(p, "conspause", "0")
    propfadein = get(p, "propfadein", "0")
    minFadeIn = get(p, "minFadeIn", "0")
    maxFadeIn = get(p, "maxFadeIn", "0")
    methFdIn = get(p, "methFdIn", "0")
    fadeInChance = get(p, "fadeInChance", "100")
    propfadeout = get(p, "propfadeout", "0")
    minFadeOut = get(p, "minFadeOut", "0")
    maxFadeOut = get(p, "maxFadeOut", "0")
    methFdOut = get(p, "methFdOut", "0")
    fadeOutChance = get(p, "fadeOutChance", "100")
    fdprior = get(p, "fdprior", "0")
    faderestrict = get(p, "faderestrict", "0")
    mincrossfade = get(p, "mincrossfade", "0")
    maxcrossfade = get(p, "maxcrossfade", "0")
    methCrsfd = get(p, "methCrsfd", "0")
    crossfadechance = get(p, "crossfadechance", "100")
    repeatMin = get(p, "repeatMin", "0")
    repeatMax = get(p, "repeatMax", "0")
    methrep = get(p, "methrep", "0")
    repeatchance = get(p, "repeatchance", "0")
    consrep = get(p, "consrep", "0")
    minsegs = get(p, "minsegs", "0")
    maxsegs = get(p, "maxsegs", "0")
    remembertype = get(p, "remembertype", "0")
    rememberchance = get(p, "rememberchance", "0")
    avgstrt = get(p, "avgstrt", "0")
    strtdev = get(p, "strtdev", "0")
    strtweights = get(p, "strtweights", "")
    normStrtChance = get(p, "normStrtChance", "0")
    speeds = get(p, "speeds", "0")
    speedmeasure = get(p, "speedmeasure", "0")
    speedweights = get(p, "speedweights", "")
    TimeMeasure = get(p, "TimeMeasure", "0")
    fdmode_lc = get(p, "fdmode_lc", "0")
    fdmode_sf = get(p, "fdmode_sf", "0")
    fdmode_en = get(p, "fdmode_en", "0")
    backmaskFadeCrossfade = get(p, "backmaskFadeCrossfade", "-1")
    minfdmsk = get(p, "minfdmsk", "0")
    BackmaskCrossfade = get(p, "BackmaskCrossfade", "0")
    BackmaskChance = get(p, "BackmaskChance", "0")
    asymmetricalBackmaskChance = get(p, "asymmetricalBackmaskChance", "0")
    reverseMaskChance = get(p, "reverseMaskChance", "0")
    doublesize = get(p, "doublesize", "0")
    consecbackmask = get(p, "consecbackmask", "100")
    minMaskRepeat = get(p, "minMaskRepeat", "0")
    maxMaskRepeat = get(p, "maxMaskRepeat", "0")
    methrepmsk = get(p, "methrepmsk", "0")
    maskmode = get(p, "maskmode", "0")
    maskRepeatChance = get(p, "maskRepeatChance", "0")
    fromseed = get(p, "fromseed", "0")
    seed = get(p, "seed", "")
    stumblechance = get(p, "stumblechance", "0")
    stumbledeviation = get(p, "stumbledeviation", "0")
    stumbdeviate = get(p, "stumbdeviate", "100")
    methStumbleNorm = get(p, "methStumbleNorm", "0")
    methStumbleForw = get(p, "methStumbleForw", "0")
    methStumbleBack = get(p, "methStumbleBack", "0")
    stumavgstrt = get(p, "stumavgstrt", "0")
    countstumblepauses = get(p, "countstumblepauses", "0")
    repmode = get(p, "repmode", "0")
    notepropfd = get(p, "notepropfd", "0")
    minCutFdIn = get(p, "minCutFdIn", "0")
    maxCutFdIn = get(p, "maxCutFdIn", "0")
    methCutFdIn = get(p, "methCutFdIn", "0")
    cutFdInChance = get(p, "cutFdInChance", "100")
    minCutFdOut = get(p, "minCutFdOut", "0")
    maxCutFdOut = get(p, "maxCutFdOut", "0")
    methCutFdOut = get(p, "methCutFdOut", "0")
    cutFdOutChance = get(p, "cutFdOutChance", "100")
    quantizeMode = get(p, "quantizeMode", "0")
    bpm = get(p, "bpm", "120")
    quanavgstrt = get(p, "quanavgstrt", "100")
    quanstrt = get(p, "quanstrt", "100")
    quanseglgth = get(p, "quanseglgth", "100")
    quanrep = get(p, "quanrep", "100")
    quanmask = get(p, "quanmask", "100")
    usestartonsets = get(p, "usestartonsets", "100")
    trimfile = get(p, "trimfile", "0")
    trimmin = get(p, "trimmin", "0")
    trimmax = get(p, "trimmax", "0")
    shiftons = get(p, "shiftons", "1")
    CompMethod = get(p, "CompMethod", None)
    if CompMethod=="0": fdmode_lc = "1"
    elif CompMethod=="1": fdmode_sf = "1"
    elif CompMethod=="2": fdmode_en = "1"
    methStumble = get(p, "methStumble", None)
    if methStumble=="0": methStumbleNorm = "1"
    elif methStumble=="1": methStumbleForw = "1"
    elif methStumble=="2": methStumbleBack = "1"
    if version=="2.1.0":
        if doublesize=="1":
            doublesize = "100"
        version = "2.1.1"
    if version=="2.1.1":
        if conspause=="1":  conspause = "100"
        if consrep=="1":    consrep = "100"
        if methDur=="2":    methDur="3"
        if methPause=="2":  methPause="3"
        if methFdIn=="2":   methFdIn="3"
        if methFdOut=="2":  methFdOut="3"
        if methCrsfd=="2":  methCrsfd="3"
        if methrep=="2":    methrep="3"
        if methDur=="1":    methDur="2"
        if methPause=="1":  methPause="2"
        if methFdIn=="1":   methFdIn="2"
        if methFdOut=="1":  methFdOut="2"
        if methCrsfd=="1":  methCrsfd="2"
        if methrep=="1":    methrep="2"
        if methrepmsk=="1": methrepmsk="2"
        if TimeMeasure!="1":
            strtdev = uiConvTime(strtdev, "sec2ms")
            _avgstrt = avgstrt
            avgstrt = ""
            for t in _avgstrt.split():
                avgstrt += uiConvTime(t, "sec2ms") + " "
    tmp_stumbmode = w2p(methStumbleNorm, [methStumbleNorm, methStumbleForw, methStumbleBack])
    ab2to3 = f"""[AudioButcher3]
version = 3.0.0

convert2sec = {TimeMeasure}
fromseed = {fromseed}
seed = {seed}

seg = {minSize} {maxSize} {m2d(methDur)}
segReverseChance1 = {mulsp(reverseChance, fdprior, True)}
segReverseChance2 = {mulsp(reverseChance, fdprior, False)}
pause = {minPL} {maxPL} {m2d(methPause)}
pauseChance = {stopChance}
consPauseChance = {conspause}
crossFd = {mincrossfade} {maxcrossfade} {m2d(methCrsfd)}
crossFdChance = {crossfadechance}
fadeInPerc = {propfadein}
fadeIn = {minFadeIn} {maxFadeIn} {m2d(methFdIn)}
fadeInChance = {fadeInChance}
fadeOnlyIntoPauses = {faderestrict}
fadeOutPerc = {propfadeout}
fadeOut = {minFadeOut} {maxFadeOut} {m2d(methFdOut)}
fadeOutChance = {fadeOutChance}
fadeOutPercNote = {notepropfd}
repeat = {repeatMin} {repeatMax} {m2d(methrep)}
repeatChance = {repeatchance}
repeatInMss = {repmode}
rememb = {minsegs} {maxsegs} {m2d(remembertype)}
remembChance = {rememberchance}
avgstrtTimes = {avgstrt}
avgstrtDev = {strtdev}
avgstrtWeights = {strtweights}
avgstrtChance = {normStrtChance}
speeds = {speeds}
speedm = {speedmeasure}
speedw = {speedweights}

backmaskCrossfd = {BackmaskCrossfade}
backmaskChance = {BackmaskChance}
backmaskRevChance = {reverseMaskChance}
backmaskFullChance = {doublesize}
backmaskAsymChance = {asymmetricalBackmaskChance}
backmaskAsymPortion = 0 100 0
bmaskRepeatChance = {maskRepeatChance}
bmaskRepeatNum = {minMaskRepeat} {maxMaskRepeat} {m2d(methrepmsk)}
bmaskRepeatInMss = {maskmode}

extnoteChance = {w2p(fdmode_en, [fdmode_lc, fdmode_sf, fdmode_en])}
extnoteUseAltPortion = 0
extnoteAltPortion = 0 100 0
extnoteAltFadeOut = 0
extnoteMinNoteLen = {minfdmsk}
extnoteCrossfd = {backmaskFadeCrossfade}

quanMode = {quantizeMode}
quanBPM = {bpm}
quanAvgStart = {quanavgstrt}
quanAvgStartDir = 3
quanStumbBegin = 0
quanStumbBeginDir = 0
quanStumbleSkip = 100
quanStumbleSkipDir = 3
quanBegin = {quanstrt}
quanBeginDir = 0
quanDuration = {quanseglgth}
quanDurationDir = 2
quanUseStOnsets = {usestartonsets}
quanUseStOnsetsDir = 0

stumbleChance = {stumblechance}
stumbleLockedMode = {1 if tmp_stumbmode > 50 else 0}
stumbleOnlyStumbled = {tmp_stumbmode}
stumbleIgnoreAvgSt = {stumavgstrt}
stumbleCountPauses = {countstumblepauses}
skipChance = 100

skipRandWeight = {methStumbleNorm}
skipRandMin = 0
skipRandMinChance = 100
skipRandAddDev = {stumbledeviation}
skipRandAddDevChance = {stumbdeviate}

skipForwWeight = {methStumbleForw}
skipForwMin = 0
skipForwMinChance = 100
skipForwAddDev = {stumbledeviation}
skipForwAddDevChance = {stumbdeviate}

skipBackWeight = {methStumbleBack}
skipBackMin = 0
skipBackMinChance = 100
skipBackAddDev = {stumbledeviation}
skipBackAddDevChance = {stumbdeviate}

fadeInCut = {minCutFdIn} {maxCutFdIn} {m2d(methCutFdIn)}
fadeInCutChance = {cutFdInChance}
fadeOutCut = {minCutFdOut} {maxCutFdOut} {m2d(methCutFdOut)}
fadeOutCutChance = {cutFdOutChance}

consecPauseFirst = 0
consecRepeatFirst = 0
consecRepeatChance = {consrep}
consecBmaskFirst = 0
consecBmaskChance = {consecbackmask}

trim = {trimfile}
trimVal1 = {trimmin}
trimVal2 = {trimmax}
trimShiftOns = {shiftons}
"""
    cfgImport(None, ab2to3, rempath)

def cfgExport(path=""):
    global presetPath
    if not isfile(path):
        if presetPath == "":
            defname = getNoExt(audioPath)
            if defname!="": defname+=" preset"
        else:
            defname = getNoExt(presetPath)
        path = fd.asksaveasfilename(filetypes=types_preset, defaultextension=types_preset, initialfile=defname, initialdir=abSavCfg.get("dir_presets"))
    if not validPath(path): return
    presetPath = path
    abSavCfg.set("dir_presets", path=path)
    try:
        summary = f"""[AudioButcher3]
version = {abVersionShort}

convert2sec = {b_convert2sec.save()}
fromseed = {b_fromseed.save()}
seed = {i_seed.get()}

seg = {ir_seg.save()}
segReverseChance1 = {ic_segReverseChance1.save()}
segReverseChance2 = {ic_segReverseChance2.save()}
pause = {ir_pause.save()}
pauseChance = {ic_pause.save()}
consPauseChance = {ic_consPause.save()}
crossFd = {ir_crossFd.save()}
crossFdChance = {ic_crossFd.save()}
fadeInPerc = {ib_fadeInPerc.save()}
fadeIn = {ir_fadeIn.save()}
fadeInChance = {ic_fadeIn.save()}
fadeOnlyIntoPauses = {ic_fadeOnlyIntoPauses.save()}
fadeOutPerc = {ib_fadeOutPerc.save()}
fadeOut = {ir_fadeOut.save()}
fadeOutChance = {ic_fadeOut.save()}
fadeOutPercNote = {ib_fadeOutPercNote.save()}
repeat = {ir_repeat.save()}
repeatChance = {ic_repeat.save()}
repeatInMss = {ib_repeatInMss.save()}
rememb = {ir_rememb.save()}
remembChance = {ic_rememb.save()}
avgstrtTimes = {i_avgstrtTimes.get()}
avgstrtDev = {i_avgstrtDev.get()}
avgstrtWeights = {i_avgstrtWeights.get()}
avgstrtChance = {i_avgstrtChance.save()}
speeds = {i_speeds.get()}
speedm = {x_speedm.current()}
speedw = {i_speedw.get()}

backmaskCrossfd = {i_backmaskCrossfd.get()}
backmaskChance = {i_backmaskChance.save()}
backmaskRevChance = {i_backmaskRevChance.save()}
backmaskFullChance = {i_backmaskFullChance.save()}
backmaskAsymChance = {i_backmaskAsymChance.save()}
backmaskAsymPortion = {i_backmaskAsymPortion.save()}
bmaskRepeatChance = {i_bmaskRepeatChance.save()}
bmaskRepeatNum = {i_bmaskRepeatNum.save()}
bmaskRepeatInMss = {b_bmaskRepeatInMss.save()}

extnoteChance = {i_extnoteChance.save()}
extnotePriority = {b_extnotePriority.save()}
extnoteUseAltPortion = {i_extnoteUseAltPortion.save()}
extnoteAltPortion = {i_extnoteAltPortion.save()}
extnoteAltFadeOut = {b_extnoteAltFadeOut.save()}
extnoteMinNoteLen = {i_extnoteMinNoteLen.get()}
extnoteCrossfd = {i_extnoteCrossfd.get()}

quanMode = {x_quanMode.current()}
quanBPM = {i_quanBPM.get()}
quanAvgStart = {i_quanAvgStart.save()}
quanAvgStartDir = {x_quanAvgStartDir.current()}
quanStumbBegin = {i_quanStumbBegin.save()}
quanStumbBeginDir = {x_quanStumbBeginDir.current()}
quanStumbleSkip = {i_quanStumbleSkip.save()}
quanStumbleSkipDir = {x_quanStumbleSkipDir.current()}
quanBegin = {i_quanBegin.save()}
quanBeginDir = {x_quanBeginDir.current()}
quanDuration = {i_quanDuration.save()}
quanDurationDir = {x_quanDurationDir.current()}
quanUseStOnsets = {i_quanUseStOnsets.save()}
quanUseStOnsetsDir = {x_quanUseStOnsetsDir.current()}

stumbleChance = {i_stumbleChance.save()}
stumbleLockedMode = {b_stumbleLockedMode.save()}
stumbleOnlyStumbled = {i_stumbleOnlyStumbled.save()}
stumbleIgnoreAvgSt = {i_stumbleIgnoreAvgSt.save()}
stumbleCountPauses = {i_stumbleCountPauses.save()}
stumbleCountMuted = {i_stumbleCountMuted.save()}
skipChance = {i_skipChance.save()}

skipForwWeight = {i_skipForwWeight.get()}
skipForwMin = {i_skipForwMin.get()}
skipForwMinChance = {i_skipForwMinChance.save()}
skipForwAddDev = {i_skipForwAddDev.get()}
skipForwAddDevChance = {i_skipForwAddDevChance.save()}

skipBackWeight = {i_skipBackWeight.get()}
skipBackMin = {i_skipBackMin.get()}
skipBackMinChance = {i_skipBackMinChance.save()}
skipBackAddDev = {i_skipBackAddDev.get()}
skipBackAddDevChance = {i_skipBackAddDevChance.save()}

skipRandWeight = {i_skipRandWeight.get()}
skipRandMin = {i_skipRandMin.get()}
skipRandMinChance = {i_skipRandMinChance.save()}
skipRandAddDev = {i_skipRandAddDev.get()}
skipRandAddDevChance = {i_skipRandAddDevChance.save()}

looping = {b_looping.save()}
loopDuration = {i_loopDuration.get()}
loopStrictly = {b_loopStrictly.save()}
loopVarNumber = {i_loopVarNumber.get()}
loopKeepSize = {b_loopKeepSize.save()}
loopFillWithSilence = {i_loopFillWithSilence.save()}
loopAltSpeed = {i_loopAltSpeed.save()}
loopAltSource = {i_loopAltSource.save()}
loopAltBegin = {i_loopAltBegin.save()}
loopAltRandBegin = {i_loopAltRandBegin.save()}
loopAltAvgBegin = {i_loopAltAvgBegin.save()}
loopAltStumBegin = {i_loopAltStumBegin.save()}
loopAltDuration = {i_loopAltDuration.save()}
loopAltReQnDur = {i_loopAltReQnDur.save()}
loopAltRev1 = {i_loopAltRev1.save()}
loopAltRev2 = {i_loopAltRev2.save()}
loopAltRepeats = {i_loopAltRepeats.save()}
loopAltBmask = {i_loopAltBmask.save()}
loopAltBmRep = {i_loopAltBmRep.save()}
loopAltFadeIn = {i_loopAltFadeIn.save()}
loopAltFadeOut = {i_loopAltFadeOut.save()}
loopAltNoteExt = {i_loopAltNoteExt.save()}

fadeInCut = {ir_fadeInCut.save()}
fadeInCutChance = {ic_fadeInCut.save()}
fadeOutCut = {ir_fadeOutCut.save()}
fadeOutCutChance = {ic_fadeOutCut.save()}

consecPauseFirst = {b_consecPauseFirst.save()}
consecRepeatFirst = {b_consecRepeatFirst.save()}
consecRepeatChance = {i_consecRepeatChance.save()}
consecBmaskFirst = {b_consecBmaskFirst.save()}
consecBmaskChance = {i_consecBmaskChance.save()}
consecMutedFirst = {b_consecMutedFirst.save()}
consecMutedChance = {i_consecMutedChance.save()}

trim = {b_trim.save()}
trimVal1 = {i_trimVal1.get()}
trimVal2 = {i_trimVal2.get()}
trimShiftOns = {b_trimShiftOns.save()}

stumbPrior = {i_stumbPrior.save()}
muteChance = {i_muteChance.save()}
muteToPauseChance = {i_muteToPauseChance.save()}
muteCountPauses = {b_muteCountPauses.save()}
"""
        p = open(path, "w", encoding="utf-8")
        p.write(summary)
        p.close()
    except Exception as e:
        abError("Preset", e)

def cfgConvTime():
    if abCurrCfg.convsec2ms.get()==0: return
    if b_convert2sec.get(): mode = "ms2sec"
    else: mode="sec2ms"
    cfgUnlockAll()
    ir_seg.convtime(mode)
    ir_pause.convtime(mode)
    ir_crossFd.convtime(mode)
    if not ib_fadeInPerc.get(): ir_fadeIn.convtime(mode)
    if not ib_fadeOutPerc.get(): ir_fadeOut.convtime(mode)
    if ib_repeatInMss.get(): ir_repeat.convtime(mode)
    avgsttimes = i_avgstrtTimes.get().split()
    uiSetText(i_avgstrtTimes, "")
    for j in [uiConvTime(i, mode) for i in avgsttimes]:
        i_avgstrtTimes.insert(END, j)
        i_avgstrtTimes.insert(END, " ")
    uiEntryConvert(i_avgstrtDev, mode)
    uiEntryConvert(i_backmaskCrossfd, mode, True)
    if b_bmaskRepeatInMss.get(): i_bmaskRepeatNum.convtime(mode)
    uiEntryConvert(i_extnoteMinNoteLen, mode)
    uiEntryConvert(i_extnoteCrossfd, mode, True)
    uiEntryConvert(i_skipForwMin, mode)
    uiEntryConvert(i_skipForwAddDev, mode)
    uiEntryConvert(i_skipBackMin, mode)
    uiEntryConvert(i_skipBackAddDev, mode)
    uiEntryConvert(i_skipRandMin, mode)
    uiEntryConvert(i_skipRandAddDev, mode)
    uiEntryConvert(i_loopDuration, mode)
    uiEntryConvert(i_trimVal1, mode)
    uiEntryConvert(i_trimVal2, mode)
    cfgUpdate()

def cfgUnlockAll():
    i_seed.configure(state="normal")
    i_quanBPM.configure(state="normal")
    i_quanAvgStart.val.configure(state="normal")
    i_quanStumbBegin.val.configure(state="normal")
    i_quanStumbleSkip.val.configure(state="normal")
    i_quanBegin.val.configure(state="normal")
    i_quanDuration.val.configure(state="normal")
    i_quanUseStOnsets.val.configure(state="normal")
    i_loopDuration.configure(state="normal")
    i_loopVarNumber.configure(state="normal")
    i_loopFillWithSilence.val.configure(state="normal")
    i_loopAltSpeed.val.configure(state="normal")
    i_loopAltSource.val.configure(state="normal")
    i_loopAltBegin.val.configure(state="normal")
    i_loopAltRandBegin.val.configure(state="normal")
    i_loopAltAvgBegin.val.configure(state="normal")
    i_loopAltStumBegin.val.configure(state="normal")
    i_loopAltDuration.val.configure(state="normal")
    i_loopAltReQnDur.val.configure(state="normal")
    i_loopAltRev1.val.configure(state="normal")
    i_loopAltRev2.val.configure(state="normal")
    i_loopAltRepeats.val.configure(state="normal")
    i_loopAltBmask.val.configure(state="normal")
    i_loopAltBmRep.val.configure(state="normal")
    i_loopAltFadeIn.val.configure(state="normal")
    i_loopAltFadeOut.val.configure(state="normal")
    i_loopAltNoteExt.val.configure(state="normal")
    i_trimVal1.configure(state="normal")
    i_trimVal2.configure(state="normal")

def cfgUpdate():
    if not ib_fadeOutPerc.get():
        ib_fadeOutPercNote.set(0)
        ib_fadeOutPercNote.main.configure(state="disabled")
    else:
        ib_fadeOutPercNote.main.configure(state="normal")

    if ib_repeatInMss.get():
        tr_repeat.configure(text="Repeat segment for: ")
    else:
        tr_repeat.configure(text="Repeat segment ... times: ")

    if b_fromseed.get():
        i_seed.configure(state="normal")
    else:
        i_seed.configure(state="disabled")

    if x_quanMode.current() == 0:
        i_quanBPM.configure(state="disabled")
        i_quanAvgStart.val.configure(state="disabled")
        x_quanAvgStartDir.configure(state="disabled")
        i_quanStumbBegin.val.configure(state="disabled")
        x_quanStumbBeginDir.configure(state="disabled")
        i_quanStumbleSkip.val.configure(state="disabled")
        x_quanStumbleSkipDir.configure(state="disabled")
        i_quanBegin.val.configure(state="disabled")
        x_quanBeginDir.configure(state="disabled")
        i_quanDuration.val.configure(state="disabled")
        x_quanDurationDir.configure(state="disabled")
        i_quanUseStOnsets.val.configure(state="disabled")
        x_quanUseStOnsetsDir.configure(state="disabled")
    else:
        if x_quanMode.current() == 2:
            i_quanBPM.configure(state="normal")
        else:
            i_quanBPM.configure(state="disabled")
        i_quanAvgStart.val.configure(state="normal")
        x_quanAvgStartDir.configure(state="readonly")
        i_quanStumbBegin.val.configure(state="normal")
        x_quanStumbBeginDir.configure(state="readonly")
        i_quanStumbleSkip.val.configure(state="normal")
        x_quanStumbleSkipDir.configure(state="readonly")
        i_quanBegin.val.configure(state="normal")
        x_quanBeginDir.configure(state="readonly")
        i_quanDuration.val.configure(state="normal")
        x_quanDurationDir.configure(state="readonly")
        i_quanUseStOnsets.val.configure(state="normal")
        x_quanUseStOnsetsDir.configure(state="readonly")

    if b_looping.get():
        i_loopDuration.configure(state="normal")
        i_loopVarNumber.configure(state="normal")
        b_loopKeepSize.main.configure(state="normal")
        if b_loopKeepSize.get():
            b_loopStrictly.main.configure(state="normal")
            i_loopFillWithSilence.val.configure(state="normal")
        else:
            b_loopStrictly.main.configure(state="disabled")
            i_loopFillWithSilence.val.configure(state="disabled")
        i_loopAltSpeed.val.configure(state="normal")
        i_loopAltSource.val.configure(state="normal")
        i_loopAltBegin.val.configure(state="normal")
        i_loopAltRandBegin.val.configure(state="normal")
        i_loopAltAvgBegin.val.configure(state="normal")
        i_loopAltStumBegin.val.configure(state="normal")
        i_loopAltDuration.val.configure(state="normal")
        i_loopAltReQnDur.val.configure(state="normal")
        i_loopAltRev1.val.configure(state="normal")
        i_loopAltRev2.val.configure(state="normal")
        i_loopAltRepeats.val.configure(state="normal")
        i_loopAltBmask.val.configure(state="normal")
        i_loopAltBmRep.val.configure(state="normal")
        i_loopAltFadeIn.val.configure(state="normal")
        i_loopAltFadeOut.val.configure(state="normal")
        i_loopAltNoteExt.val.configure(state="normal")
    else:
        i_loopDuration.configure(state="disabled")
        b_loopStrictly.main.configure(state="disabled")
        i_loopVarNumber.configure(state="disabled")
        b_loopKeepSize.main.configure(state="disabled")
        i_loopFillWithSilence.val.configure(state="disabled")
        i_loopAltSpeed.val.configure(state="disabled")
        i_loopAltSource.val.configure(state="disabled")
        i_loopAltBegin.val.configure(state="disabled")
        i_loopAltRandBegin.val.configure(state="disabled")
        i_loopAltAvgBegin.val.configure(state="disabled")
        i_loopAltStumBegin.val.configure(state="disabled")
        i_loopAltDuration.val.configure(state="disabled")
        i_loopAltReQnDur.val.configure(state="disabled")
        i_loopAltRev1.val.configure(state="disabled")
        i_loopAltRev2.val.configure(state="disabled")
        i_loopAltRepeats.val.configure(state="disabled")
        i_loopAltBmask.val.configure(state="disabled")
        i_loopAltBmRep.val.configure(state="disabled")
        i_loopAltFadeIn.val.configure(state="disabled")
        i_loopAltFadeOut.val.configure(state="disabled")
        i_loopAltNoteExt.val.configure(state="disabled")

    if not b_loopKeepSize.get():
        b_loopStrictly.set(0)

    if b_trim.get():
        i_trimVal1.configure(state="normal")
        i_trimVal2.configure(state="normal")
        b_trimShiftOns.main.configure(state="normal")
    else:
        i_trimVal1.configure(state="disabled")
        i_trimVal2.configure(state="disabled")
        b_trimShiftOns.main.configure(state="disabled")

def cfgLastSeed():
    if lastSeed != None:
        b_fromseed.set(1)
        cfgUpdate()
        uiSetText(i_seed, lastSeed)


class abSavedConfigHandler:
    def __init__(self, file, section):
        self.config = RawConfigParser()
        self.file = file
        self.section = section
        try: self.config.read(self.file, encoding="utf-8")
        except Exception as e: pass
        if not self.config.has_section(self.section): self.config[self.section] = {}
    def get(self, what):
        fallbacks = {
            "dir_audio": homepath,
            "dir_scramble": homepath,
            "dir_presets": homepath,
            "dir_onsets": homepath,
            "dir_onsets2": homepath,
            "len_export": 120,
            "len_preview": 10,
            "livepr_buff": 15,
            "onsetsdropdown": 2,
            "aubiomethod": "energy",
            "uniqfilename": 1,
            "shadderrinf": 0,
            "convsec2ms": 1,
            "secimpaudlen": 0,
            "moreformats": 0,
            "remdndpath": 1,
            "openscrfolder": 1,
            "autoonsdet": 0,
            "resetonsets": 1,
            "closeonsets": 0,
        }
        return self.config.get(self.section, what, fallback=fallbacks[what])
    def set(self, what, value=0, path=""):
        values = {
            "dir_audio": dirname(path),
            "dir_scramble": dirname(path),
            "dir_presets": dirname(path),
            "dir_onsets": dirname(path),
            "dir_onsets2": dirname(path),
            "len_export": value,
            "len_preview": abCurrCfg.len_preview.get(),
            "livepr_buff": value,
            "onsetsdropdown": value,
            "aubiomethod": value,
            "uniqfilename": abCurrCfg.uniqfilename.get(),
            "shadderrinf": abCurrCfg.shadderrinf.get(),
            "convsec2ms": abCurrCfg.convsec2ms.get(),
            "secimpaudlen": abCurrCfg.secimpaudlen.get(),
            "moreformats": abCurrCfg.moreformats.get(),
            "remdndpath": abCurrCfg.remdndpath.get(),
            "openscrfolder": abCurrCfg.openscrfolder.get(),
            "autoonsdet": abCurrCfg.autoonsdet.get(),
            "resetonsets": abCurrCfg.resetonsets.get(),
            "closeonsets": abCurrCfg.closeonsets.get(),
        }
        self.config[self.section][what] = str(values[what])
        cfgfile = open(self.file, "w", encoding="utf-8")
        self.config.write(cfgfile)
        cfgfile.close()

class abLivePreview:
    def __init__(self):
        self.playing = False
    def play(self, audio):
        self.playing = True
        try:
            play(audio)
        except Exception as e:
            abError("Live preview", e)
        self.playing = False
    def wait(self):
        while self.playing: pass

def abOnsetsWindow():
    modes_andthen = ["Save to file and apply", "Save to file only", "Apply only"]
    modes_aubio = ["energy", "hfc", "complex", "phase", "specdiff", "kl", "mkl", "specflux"]

    def updateButtons(b_geno_curr, b_geno_othr):
        if AB_ALT_USE_AUBIO or not AB_DISABLE_LIBROSA:
            if detecting:
                b_geno_curr.configure(state="disabled")
                b_geno_othr.configure(state="disabled")
            else:
                b_geno_curr.configure(state="normal")
                b_geno_othr.configure(state="normal")

        if audio == None:
            b_geno_curr.configure(state="disabled")

        if AB_DISABLE_LIBROSA and not AB_ALT_USE_AUBIO:
            b_geno_curr.configure(state="disabled")
            b_geno_othr.configure(state="disabled")

    onswin = Toplevel(root)
    onswin.title("Manage onsets")
    face = Frame(onswin, padding=3); face.pack(fill="both", expand=True)
    group = Frame(face); group.grid(row=0, column=0, columnspan=3, sticky="w")
    lower = Frame(face)

    if AB_ALT_USE_AUBIO: lower.grid(row=3, column=0, columnspan=3, sticky="w")
    Separator(group, orient=VERTICAL).grid(row=0, column=1, rowspan=3, padx=3, ipady=30)

    b_ons1_file = Button(group, text="Apply onset list from file", command=lambda: onsOpen(onswin))
    b_ons1_edit = Button(group, text="Manually edit onsets", command=lambda: abEditOnsets(onswin))
    b_ons1_eras = Button(group, text="Erase onsets", command=lambda: onsProcess(2, []))
    b_ons2_file = Button(group, text="Apply start onset list from file", command=lambda: onsOpen(onswin, ons2=True))
    b_ons2_edit = Button(group, text="Manually edit start onsets", command=lambda: abEditOnsets(onswin, ons2=True))
    b_ons2_eras = Button(group, text="Erase start onsets", command=lambda: onsProcess(2, [], True))
    b_geno_curr = Button(face,  text="Generate onset list from current audio", command=lambda: run(onsGet, onswin, x_andthen.current(), False, True))
    b_geno_othr = Button(face,  text="Generate onset list from other file", command=lambda: run(onsGet, onswin, x_andthen.current()))
    t_andthen = Label(face, text="And then,")
    x_andthen = Combobox(face, values=modes_andthen, width=20, state="readonly")
    t_method = Label(lower, text="Method: ")
    x_method = Combobox(lower, values=modes_aubio, width=18)

    b_ons1_file.grid(column=0, row=0, sticky="w")
    b_ons1_edit.grid(column=0, row=1, sticky="w")
    b_ons1_eras.grid(column=0, row=2, sticky="w")
    b_ons2_file.grid(column=2, row=0, sticky="w")
    b_ons2_edit.grid(column=2, row=1, sticky="w")
    b_ons2_eras.grid(column=2, row=2, sticky="w")
    b_geno_curr.grid(column=0, row=1, sticky="w")
    b_geno_othr.grid(column=0, row=2, sticky="w")
    t_andthen.grid(column=1, row=1, rowspan=2, padx=2)
    x_andthen.grid(column=2, row=1, rowspan=2)
    t_method.grid(row=0, column=0)
    x_method.grid(row=0, column=1)

    uiSelCbox(x_andthen, abSavCfg.get("onsetsdropdown"))
    uiSetText(x_method,  abSavCfg.get("aubiomethod"))

    onswin.bind("<<UpdadeButtons>>", lambda event: updateButtons(b_geno_curr, b_geno_othr))
    x_andthen.bind("<<ComboboxSelected>>", lambda event: abSavCfg.set("onsetsdropdown", value=x_andthen.current()))
    x_method.bind("<<ComboboxSelected>>",  lambda event: abSavCfg.set("aubiomethod",    value=x_method.get()))

    applyWindowStyle(onswin)
    updateButtons(b_geno_curr, b_geno_othr)
    onswin.grab_set()

def abEditOnsets(parent, ons2=False):
    parent.destroy()
    edonsw = Toplevel(root)
    if not ons2: edonsw.title("Edit onsets")
    else: edonsw.title("Edit start onsets")

    menu_upper = Menu(edonsw, tearoff=False)
    menu_import = Menu(menu_upper, tearoff=False)
    menu_upper.add_cascade(label="Import", menu=menu_import)
    menu_import.add_command(label="Open onset list", command=lambda: eoImportOnsets(edonsw, t_onsets, ons2))
    menu_import.add_command(label="Import current onsets", command=lambda: eoCurrentOnsets(t_onsets, ons2))
    if ons2: menu_import.add_command(label="Import current usual onsets", command=lambda: eoCurrentOnsets(t_onsets, False))

    menu_lower = Frame(edonsw, padding=1)
    b_apply = Button(menu_lower, text="Apply", command=lambda: onsProcess(2, convOns(t_onsets.get("1.0", END).split()), ons2))
    b_export = Button(menu_lower, text="Export", command=lambda: onsProcess(1, convOns(t_onsets.get("1.0", END).split()), ons2, "Custom", edonsw))
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

    edonsw.wait_window()
    if abCurrCfg.closeonsets.get()==0: abOnsetsWindow()

def abError(title, exception, parent=None, form=mb.showerror):
    if abCurrCfg.shadderrinf.get() == 1: text = format_exc()
    else: text = exception
    return form(title, text, parent=parent)


def defOnsPath(ons2):
    if ons2: return "dir_onsets2"
    else: return "dir_onsets"

def onsGenerate_librosa(source, sr = 22050):
    y = array(source.set_frame_rate(sr).set_channels(1).get_array_of_samples()).astype(float32)
    onset_function = onset_strength(y=y, sr=sr, aggregate=median, n_fft=1024, fmax=1500)
    backtrack_function = onset_strength(y=y, sr=sr)
    onset_times = onset_detect(y=y, sr=sr, onset_envelope = onset_function, backtrack=1, energy=backtrack_function, units="time")
    return [round(element * 1000) for element in onset_times]

def onsGenerate_aubio(source):
    wavpath = tempWavPath()
    window_size = 1024
    hop_size = window_size // 4

    try:
        source.set_frame_rate(44100).set_sample_width(2).set_channels(1).export(wavpath, format="wav")
        src_func = aubio.source(wavpath, 0, hop_size)
        delFile(wavpath)
    except Exception:
        delFile(wavpath)
        raise

    onset_func = aubio.onset(abSavCfg.get("aubiomethod"), window_size, hop_size)
    duration = float(src_func.duration) / src_func.samplerate

    onset_times = []
    while True:
        samples, num_frames_read = src_func()
        if onset_func(samples):
            onset_time = onset_func.get_last_s()
            if onset_time < duration: onset_times.append(round(onset_time*1000))
            else: break
        if num_frames_read < hop_size:
            break

    return onset_times

def onsGenerate(source):
    if AB_ALT_USE_AUBIO: return onsGenerate_aubio(source)
    else: return onsGenerate_librosa(source)

def onsNormalize(onsets):
    return sorted(list(set(onsets)))

def onsProcess(mode, _onsets, ons2=False, source=None, parent=None):
    global onsets, stOnsets
    if _onsets == None: return
    _onsets = onsNormalize(_onsets)
    if mode in [0, 1]:
        try:
            if ons2:
                types = types_onset2
                fname = ""
            else:
                types = types_onset
                fname = getNoExt(source)+" [onsets]"
            dist = fd.asksaveasfilename(filetypes=types, defaultextension=types, initialdir=abSavCfg.get(defOnsPath(ons2)), initialfile=fname, parent=parent)
            if not validPath(dist): return
            abSavCfg.set(defOnsPath(ons2), path=dist)
            abofile = open(dist, "w")
            for onset in _onsets: abofile.write("%s " % onset)
            abofile.close()
        except Exception as e:
            abError("Onsets", e, parent)
    if mode in [0, 2]:
        if ons2: stOnsets = _onsets
        else: onsets = _onsets
    usrUpdWindowTitle()

def onsOpen(parent, ons2=False, path=None, rempath=True, window=True):
    if path == None:
        if ons2: types = types_onset2
        else: types = types_onset
        path = fd.askopenfilename(filetypes=types, initialdir=abSavCfg.get(defOnsPath(ons2)), parent=parent)
    if not validPath(path): return
    try:
        if rempath: abSavCfg.set(defOnsPath(ons2), path=path)
        abofile = open(path, "r")
        onsProcess(2, [int(o) for o in abofile.read().split()], ons2)
        abofile.close()
    except Exception as e:
        abError("Onsets", e, parent)
    else:
        mb.showinfo("Onsets", "Applied successfully.", parent=parent)
        if abCurrCfg.closeonsets.get() == 1 and window: parent.destroy()

def onsGet(parent, mode, ons2=False, fromCurrent=False, path=None, window=True):
    global audio, detecting
    if fromCurrent: path=audioPath
    elif path==None: path = fd.askopenfilename(filetypes=types_import, initialdir=abSavCfg.get("dir_audio"), parent=parent)
    if not validPath(path): return
    try:
        detecting = True
        if window: parent.event_generate("<<UpdadeButtons>>")
        if fromCurrent: _onsets = onsGenerate(audio)
        else: _onsets = onsGenerate(loadAudio(path))
        detecting = False
        if window: parent.event_generate("<<UpdadeButtons>>")
        mb.showinfo("Onsets", "All onsets detected.", parent=parent)
        onsProcess(mode, _onsets, ons2, path, parent)
    except Exception as e:
        detecting = False
        if window: parent.event_generate("<<UpdadeButtons>>")
        abError("Onsets", e, parent)
    else:
        if abCurrCfg.closeonsets.get()==1 and window: parent.destroy()

def eoImportOnsets(parent, entry, ons2):
    if ons2: types = types_onset2
    else: types = types_onset
    selfile = fd.askopenfilename(filetypes=types, initialdir=abSavCfg.get(defOnsPath(ons2)), parent=parent)
    if not validPath(selfile): return
    try:
        abSavCfg.set(defOnsPath(ons2), path=selfile)
        abofile = open(selfile, "r")
        entry.delete("1.0", END)
        entry.insert(END, abofile.read())
        abofile.close()
    except Exception as e:
        abError("Onsets", e, parent)

def eoCurrentOnsets(entry, ons2):
    global onsets, stOnsets
    if not ons2: _onsets = onsets
    else: _onsets = stOnsets
    entry.delete("1.0", END)
    for o in _onsets: entry.insert(END, "%s " % o)


def findNearestIdx(value, arr):
    diff = [abs(i - value) for i in arr]
    return diff.index(min(diff))

def quantize(mode, value, arr, bpm, direction = 0, getIdx = False):
    if mode == 0:
        return value
    elif mode == 1:
        idx = findNearestIdx(value, arr)
        if direction == 1 and arr[idx] > value and idx > 0: idx -= 1
        if direction == 2 and arr[idx] < value and idx < len(arr) - 1: idx += 1
        if getIdx: return idx
        else: return arr[idx]
    elif mode == 2:
        beat_dur = 60000 / bpm
        if direction   == 0: r = round(value / beat_dur) * beat_dur
        elif direction == 1: r = int(value / beat_dur) * beat_dur
        elif direction == 2: r = ceil(value / beat_dur) * beat_dur
        else: r = 0
        return round(r)

def findNoteLen(start, end, arr, minNoteLen, reverse):
    if reverse:
        value = start
        direction = 1
    else:
        value = end
        direction = 2
    idx = quantize(1, value, arr, 0, direction, True)
    while True:
        notelen = abs(value - arr[idx])
        if notelen <= 0 or notelen < minNoteLen:
            if direction == 1:
                if idx + 1 >= len(arr): break
                else: idx += 1
            else:
                if idx <= 0: break
                else: idx -= 1
        else:
            break
    return notelen


def randSeed(length):
    random.seed()
    symbols = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789-_=+"
    proposed = ""
    for i in range(0, length):
        proposed += random.choice(symbols)
    return proposed

def randTF(chance=50):
    return random.uniform(0, 100) <= chance

def randNum(val1, val2, mode):
    if mode == 0:
        return random.uniform(val1, val2)
    elif mode == 1:
        _return = -1
        while _return < 0:
            _return = random.gauss(val1, val2)
        return _return
    elif mode == 2:
        return random.lognormvariate(val1, val2)

def randWeight(values, weights):
    return random.choices(values, weights=weights)[0]


def audSelect(audio, begin, end):
    audlen = audio.duration_seconds * 1000
    if end <= audlen:
        return audio[begin:end]
    else:
        loops = ceil(end / audlen)
        if loops > 50: raise Exception(f"Too many loops ({loops})")
        print(f"Audio looped {loops} times")
        return (audio*loops)[begin:end]

def audCropMs(audio):
    return audio[0:int(audio.duration_seconds*1000 + 0.1)]

def audReverse(audio):
    if audio.channels == 1:
        return audio.reverse()
    else:
        return AudioSegment.from_mono_audiosegments(*(channel.reverse() for channel in audio.split_to_mono()))

def audSpeed(audio, speed):
    if speed == 1:
        return audio
    else:
        ogfr = audio.frame_rate
        audio = audio._spawn(audio.raw_data, overrides={"frame_rate": round(ogfr * speed)})
        return audio.set_frame_rate(ogfr)

def audMaxCross(duration, audios):
    cross = int(duration)
    for audio in audios:
        dur = int(audio.duration_seconds * 1000)
        if cross >= dur: cross = dur // 2
    return cross

def audFadeIn(audio, fadein, cutoff):
    from_gain = cut2gain(cutoff)
    return audio.fade(from_gain=from_gain, duration=fadein, start=0)

def audFadeOut(audio, fadeout, cutoff):
    to_gain = cut2gain(cutoff)
    return audio.fade(to_gain=to_gain, duration=fadeout, end=float("inf"))


class abStats:
    def __init__(self):
        self.slicecr = AudioSegment.empty()
        self.audio = copy(audio)
        self.audioLength = None
        self.onsets = onsets.copy()
        self.stOnsets = stOnsets.copy()
        self.stumblePos = 0
        self.pause_prev = None
        self.pause_curr = None
        self.pause_next = None
        self.lastRepeat = None
        self.lastBackmask = None
        self.lastMute = None
        self.muteCount = None
        self.fromScratch = True

class abOptions:
    def __init__(self):
        if b_fromseed.get():
            self.seed = i_seed.get()
        else:
            self.seed = None

        self.trim = b_trim.get()
        self.trimVal1 = float(i_trimVal1.get())
        self.trimVal2 = float(i_trimVal2.get())
        self.trimShiftOns = b_trimShiftOns.get()

        self.pauseVal1, self.pauseVal2, self.pauseDist = ir_pause.get()
        self.pauseChance = ic_pause.get()
        self.consecPauseFirst = b_consecPauseFirst.get()
        self.consPauseChance = ic_consPause.get()

        self.avgstrtTimes = [float(i) for i in i_avgstrtTimes.get().split()]
        self.avgstrtDev = float(i_avgstrtDev.get())
        self.avgstrtWeights = [int(i) for i in i_avgstrtWeights.get().split()]
        if self.avgstrtWeights == []:
            self.avgstrtWeights = [1]*len(self.avgstrtTimes)
        self.avgstrtChance = i_avgstrtChance.get()

        self.segVal1, self.segVal2, self.segDist = ir_seg.get()
        self.segReverseChance1 = ic_segReverseChance1.get()
        self.segReverseChance2 = ic_segReverseChance2.get()

        self.speeds = [float(i) for i in i_speeds.get().split()]
        if x_speedm.current() == 0:
            self.speeds = [2**(i/12) for i in self.speeds]
        elif x_speedm.current() == 1:
            self.speeds = [1+i/100 for i in self.speeds]
        self.speedw = [int(i) for i in i_speedw.get().split()]
        if self.speedw == []:
            self.speedw = [1]*len(self.speeds)

        self.crossFdVal1, self.crossFdVal2, self.crossFdDist = ir_crossFd.get()
        self.crossFdChance = ic_crossFd.get()

        self.consecRepeatFirst = b_consecRepeatFirst.get()
        self.consecRepeatChance = i_consecRepeatChance.get()
        self.repeatVal1, self.repeatVal2, self.repeatDist = ir_repeat.get()
        self.repeatInMss = ib_repeatInMss.get()
        self.repeatChance = ic_repeat.get()

        self.consecBmaskFirst = b_consecBmaskFirst.get()
        self.consecBmaskChance = i_consecBmaskChance.get()
        self.backmaskCrossfd = float(i_backmaskCrossfd.get())
        self.backmaskChance = i_backmaskChance.get()
        self.backmaskRevChance = i_backmaskRevChance.get()
        self.backmaskFullChance = i_backmaskFullChance.get()
        self.backmaskAsymChance = i_backmaskAsymChance.get()
        self.backmaskAsymPortionVal1, self.backmaskAsymPortionVal2, self.backmaskAsymPortionDist = i_backmaskAsymPortion.get()

        self.bmaskRepeatChance = i_bmaskRepeatChance.get()
        self.extnotePriority = b_extnotePriority.get()
        self.bmaskRepeatVal1, self.bmaskRepeatVal2, self.bmaskRepeatDist = i_bmaskRepeatNum.get()
        self.bmaskRepeatInMss = b_bmaskRepeatInMss.get()

        self.fadeInVal1, self.fadeInVal2, self.fadeInDist = ir_fadeIn.get()
        self.fadeInPerc = ib_fadeInPerc.get()
        self.fadeInChance = ic_fadeIn.get()
        self.fadeOnlyIntoPauses = ic_fadeOnlyIntoPauses.get()

        self.fadeInCutVal1, self.fadeInCutVal2, self.fadeInCutDist = ir_fadeInCut.get()
        self.fadeInCutChance = ic_fadeInCut.get()

        self.fadeOutVal1, self.fadeOutVal2, self.fadeOutDist = ir_fadeOut.get()
        self.fadeOutPerc = ib_fadeOutPerc.get()
        self.fadeOutPercNote = ib_fadeOutPercNote.get()
        self.fadeOutChance = ic_fadeOut.get()

        self.fadeOutCutVal1, self.fadeOutCutVal2, self.fadeOutCutDist = ir_fadeOutCut.get()
        self.fadeOutCutChance = ic_fadeOutCut.get()

        self.extnoteChance = i_extnoteChance.get()
        self.extnoteMinNoteLen = float(i_extnoteMinNoteLen.get())
        self.extnoteCrossfd = float(i_extnoteCrossfd.get())
        self.extnoteUseAltPortion = i_extnoteUseAltPortion.get()
        self.extnoteAltPortionVal1, self.extnoteAltPortionVal2, self.extnoteAltPortionDist = i_extnoteAltPortion.get()
        self.extnoteAltFadeOut = b_extnoteAltFadeOut.get()

        self.looping = b_looping.get()
        self.loopDuration = float(i_loopDuration.get())
        self.loopStrictly = b_loopStrictly.get()
        self.loopVarNumber = int(i_loopVarNumber.get())
        self.loopKeepSize = b_loopKeepSize.get()
        self.loopFillWithSilence = i_loopFillWithSilence.get()
        self.loopAltSpeed = i_loopAltSpeed.get()
        self.loopAltSource = i_loopAltSource.get()
        self.loopAltBegin = i_loopAltBegin.get()
        self.loopAltRandBegin = i_loopAltRandBegin.get()
        self.loopAltAvgBegin = i_loopAltAvgBegin.get()
        self.loopAltStumBegin = i_loopAltStumBegin.get()
        self.loopAltDuration = i_loopAltDuration.get()
        self.loopAltReQnDur = i_loopAltReQnDur.get()
        self.loopAltRev1 = i_loopAltRev1.get()
        self.loopAltRev2 = i_loopAltRev2.get()
        self.loopAltRepeats = i_loopAltRepeats.get()
        self.loopAltBmask = i_loopAltBmask.get()
        self.loopAltBmRep = i_loopAltBmRep.get()
        self.loopAltFadeIn = i_loopAltFadeIn.get()
        self.loopAltFadeOut = i_loopAltFadeOut.get()
        self.loopAltNoteExt = i_loopAltNoteExt.get()

        self.stumbleChance = i_stumbleChance.get()
        self.stumbPrior = i_stumbPrior.get()
        self.stumbleLockedMode = b_stumbleLockedMode.get()
        self.stumbleOnlyStumbled = i_stumbleOnlyStumbled.get()
        self.stumbleIgnoreAvgSt = i_stumbleIgnoreAvgSt.get()
        self.stumbleCountPauses = i_stumbleCountPauses.get()
        self.stumbleCountMuted = i_stumbleCountMuted.get()
        self.skipChance = i_skipChance.get()

        self.skipForwWeight = int(i_skipForwWeight.get())
        self.skipForwMin = float(i_skipForwMin.get())
        self.skipForwMinChance = i_skipForwMinChance.get()
        self.skipForwAddDev = float(i_skipForwAddDev.get())
        self.skipForwAddDevChance = i_skipForwAddDevChance.get()

        self.skipBackWeight = int(i_skipBackWeight.get())
        self.skipBackMin = float(i_skipBackMin.get())
        self.skipBackMinChance = i_skipBackMinChance.get()
        self.skipBackAddDev = float(i_skipBackAddDev.get())
        self.skipBackAddDevChance = i_skipBackAddDevChance.get()

        self.skipRandWeight = int(i_skipRandWeight.get())
        self.skipRandMin = float(i_skipRandMin.get())
        self.skipRandMinChance = i_skipRandMinChance.get()
        self.skipRandAddDev = float(i_skipRandAddDev.get())
        self.skipRandAddDevChance = i_skipRandAddDevChance.get()

        self.quanMode = x_quanMode.current()
        self.quanBPM = float(i_quanBPM.get())
        self.quanAvgStart = i_quanAvgStart.get()
        self.quanAvgStartDir = x_quanAvgStartDir.current()
        self.quanStumbBegin = i_quanStumbBegin.get()
        self.quanStumbBeginDir = x_quanStumbBeginDir.current()
        self.quanStumbleSkip = i_quanStumbleSkip.get()
        self.quanStumbleSkipDir = x_quanStumbleSkipDir.current()
        self.quanBegin = i_quanBegin.get()
        self.quanBeginDir = x_quanBeginDir.current()
        self.quanDuration = i_quanDuration.get()
        self.quanDurationDir = x_quanDurationDir.current()
        self.quanUseStOnsets = i_quanUseStOnsets.get()
        self.quanUseStOnsetsDir = x_quanUseStOnsetsDir.current()

        self.muteChance = i_muteChance.get()
        self.muteToPauseChance = i_muteToPauseChance.get()
        self.muteCountPauses = b_muteCountPauses.get()
        self.consecMutedFirst = b_consecMutedFirst.get()
        self.consecMutedChance = i_consecMutedChance.get()

        self.remembChance = ic_rememb.get()
        self.remembAfterVal1, self.remembAfterVal2, self.remembAfterDist = ir_rememb.get()

        if b_convert2sec.get(): self.sec2ms()
    def sec2ms(self):
        self.trimVal1 *= 1000
        self.trimVal2 *= 1000
        if self.pauseDist != 2:
            self.pauseVal1 *= 1000
            self.pauseVal2 *= 1000
        self.avgstrtTimes = [i*1000 for i in self.avgstrtTimes]
        self.avgstrtDev *= 1000
        if self.segDist != 2:
            self.segVal1 *= 1000
            self.segVal2 *= 1000
        if self.crossFdDist != 2:
            self.crossFdVal1 *= 1000
            self.crossFdVal2 *= 1000
        if self.repeatInMss and self.repeatDist != 2:
            self.repeatVal1 *= 1000
            self.repeatVal2 *= 1000
        if self.backmaskCrossfd != -1:
            self.backmaskCrossfd *= 1000
        if self.bmaskRepeatInMss and self.bmaskRepeatDist != 2:
            self.bmaskRepeatVal1 *= 1000
            self.bmaskRepeatVal2 *= 1000
        if self.fadeInDist != 2 and not self.fadeInPerc:
            self.fadeInVal1 *= 1000
            self.fadeInVal2 *= 1000
        if self.fadeOutDist != 2 and not self.fadeOutPerc:
            self.fadeOutVal1 *= 1000
            self.fadeOutVal2 *= 1000
        self.extnoteMinNoteLen *= 1000
        if self.extnoteCrossfd != -1:
            self.extnoteCrossfd *= 1000
        self.loopDuration *= 1000
        self.skipForwMin *= 1000
        self.skipForwAddDev *= 1000
        self.skipBackMin *= 1000
        self.skipBackAddDev *= 1000
        self.skipRandMin *= 1000
        self.skipRandAddDev *= 1000

class abAlterInfo:
    def __init__(self, cfg, alltrue):
        self.Crossfade = alltrue
        self.Speed     = alltrue or randTF(cfg.loopAltSpeed)
        self.Source    = alltrue or randTF(cfg.loopAltSource)
        self.Begin     = alltrue or randTF(cfg.loopAltBegin)
        self.RandBegin = alltrue or randTF(cfg.loopAltRandBegin)
        self.AvgBegin  = alltrue or randTF(cfg.loopAltAvgBegin)
        self.StumBegin = alltrue or randTF(cfg.loopAltStumBegin)
        self.Duration  = alltrue or randTF(cfg.loopAltDuration)
        self.ReQnDur   = alltrue or randTF(cfg.loopAltReQnDur)
        self.Rev1      = alltrue or randTF(cfg.loopAltRev1)
        self.Rev2      = alltrue or randTF(cfg.loopAltRev2)
        self.Repeats   = alltrue or randTF(cfg.loopAltRepeats)
        self.Bmask     = alltrue or randTF(cfg.loopAltBmask)
        self.BmRep     = alltrue or randTF(cfg.loopAltBmRep)
        self.FadeIn    = alltrue or randTF(cfg.loopAltFadeIn)
        self.FadeOut   = alltrue or randTF(cfg.loopAltFadeOut)
        self.NoteExt   = alltrue or randTF(cfg.loopAltNoteExt)

class abSegmentInfo:
    pause, pause_dur = False, 0
    speed, crossfade = [None] * 2
    source, begin, duration, duration_og, rev1, rev2 = [None] * 6
    repeat, rep_len, rep_inmss = [None] * 3
    backmask, bmask_cross, bmask_rev, bmask_full, bmask_portion = [None] * 5
    bmask_repeat, bmask_rep_len, bmask_rep_inmss = [None] * 3
    extnote, extnote_len, extnote_len_fadeout, extnote_prior, notecross, minnote = [None] * 6
    fadein, fadein_p, fadeincut, fadeout, fadeout_p, fadeout_n, fadeout_nl, fadeoutcut = [None] * 8

def genPauseInfo(cfg):
    segment = abSegmentInfo()
    segment.pause = True
    segment.pause_dur = round(randNum(cfg.pauseVal1, cfg.pauseVal2, cfg.pauseDist))
    segment.speed = randWeight(cfg.speeds, cfg.speedw)
    if randTF(cfg.crossFdChance):
        segment.crossfade = round(randNum(cfg.crossFdVal1, cfg.crossFdVal2, cfg.crossFdDist))
    else: segment.crossfade = 0
    segment.pause_dur += segment.crossfade
    return [segment]

def genSegmentInfo(seg, cfg, stats, alt, crossfade):
    # Analyze if we need to re-quantize
    requan = False

    # Segment speed
    if alt.Speed:
        old_speed = seg.speed
        seg.speed = randWeight(cfg.speeds, cfg.speedw)
        if old_speed != seg.speed: requan = True
        del old_speed

    # Stop changing any parametes if the segment is pause
    if seg.pause: return

    # Crossfade
    if alt.Crossfade: seg.crossfade = crossfade
    spedcross = round(seg.crossfade * seg.speed)
    if genReady == 0: spedcross = 0

    # Segment duration
    if alt.Duration:
        old_duration = seg.duration_og
        seg.duration_og = randNum(cfg.segVal1, cfg.segVal2, cfg.segDist)
        if seg.duration_og < 1: seg.duration_og = 1
        seg.duration_og += seg.crossfade
        while seg.duration_og <= seg.crossfade * 2:
            seg.duration_og += seg.crossfade
        seg.duration_og = round(seg.duration_og)
        if old_duration != seg.duration_og: requan = True
        del old_duration

    # Start time (find source)
    source_old = seg.source
    if alt.Source or alt.Begin:
        fromavgs = randTF(cfg.avgstrtChance)
        fromstum = randTF(cfg.stumbleChance)
        if fromavgs and fromstum:
            if randTF(cfg.stumbPrior):
                fromavgs = False
            else:
                fromstum = False
        if fromavgs: seg.source = "avgstart"
        elif fromstum: seg.source = "stumble"
        else: seg.source = "none"
    altBegin = alt.Begin or (source_old != seg.source)
    old_begin = seg.begin

    # Start time (no source)
    if seg.source == "none" and (altBegin or alt.RandBegin):
        qOns1 = randTF(cfg.quanBegin)
        qOns2 = randTF(cfg.quanUseStOnsets) and stats.stOnsets!=[]
        if cfg.quanMode==1 and qOns2 and cfg.quanUseStOnsetsDir==0:
            seg.begin = random.choice(stats.stOnsets) - spedcross
        elif cfg.quanMode==1 and qOns1 and cfg.quanBeginDir==0:
            seg.begin = random.choice(stats.onsets) - spedcross
        else:
            seg.begin = round(random.uniform(0, stats.audioLength - seg.duration_og * seg.speed))
            if cfg.quanMode != 0:
                if qOns2 and (cfg.quanUseStOnsetsDir!=0 or cfg.quanMode==2):
                    seg.begin = quantize(cfg.quanMode, seg.begin, stats.stOnsets, cfg.quanBPM, cfg.quanUseStOnsetsDir-1)
                    seg.begin -= spedcross
                elif qOns1 and (cfg.quanBeginDir!=0 or cfg.quanMode==2):
                    seg.begin = quantize(cfg.quanMode, seg.begin, stats.onsets, cfg.quanBPM, cfg.quanBeginDir-1)
                    seg.begin -= spedcross
        del qOns1, qOns2

    # Start time (average start times)
    if seg.source == "avgstart" and (altBegin or alt.AvgBegin):
        avgdev = random.gauss(0, cfg.avgstrtDev)
        seg.begin = randWeight(cfg.avgstrtTimes, cfg.avgstrtWeights) + avgdev
        seg.begin = round(seg.begin)
        if randTF(cfg.quanAvgStart):
            direction = cfg.quanAvgStartDir
            if direction == 3:
                if avgdev < 0: direction = 1
                elif avgdev > 0: direction = 2
                else: direction = 0
            seg.begin = quantize(cfg.quanMode, seg.begin, stats.onsets, cfg.quanBPM, direction)
            seg.begin -= spedcross
            del direction

    # Start time (stumbling)
    if seg.source == "stumble" and (altBegin or alt.StumBegin):
        stumbSkip = 0
        if randTF(cfg.skipChance):
            randback = randTF()
            devdir = randWeight([0, 1, 2], [cfg.skipForwWeight, cfg.skipBackWeight, cfg.skipRandWeight])
            if devdir == 0:
                if randTF(cfg.skipForwMinChance):    stumbSkip += cfg.skipForwMin
                if randTF(cfg.skipForwAddDevChance): stumbSkip += randNum(0, cfg.skipForwAddDev, 1)
            elif devdir == 1:
                if randTF(cfg.skipBackMinChance):    stumbSkip -= cfg.skipBackMin
                if randTF(cfg.skipBackAddDevChance): stumbSkip -= randNum(0, cfg.skipBackAddDev, 1)
            elif devdir == 2:
                if randTF(cfg.skipRandMinChance):    stumbSkip += cfg.skipRandMin
                if randTF(cfg.skipRandAddDevChance): stumbSkip += randNum(0, cfg.skipRandAddDev, 1)
                if randback: stumbSkip *= -1
            del randback, devdir
        pos = stats.stumblePos
        if randTF(cfg.quanStumbBegin):
            pos = quantize(cfg.quanMode, pos, stats.onsets, cfg.quanBPM, cfg.quanStumbBeginDir)
        seg.begin = pos + stumbSkip
        del pos
        if stumbSkip != 0 and randTF(cfg.quanStumbleSkip):
            direction = cfg.quanStumbleSkipDir
            if direction == 3:
                if stumbSkip < 0: direction = 1
                else: direction = 2
            seg.begin = quantize(cfg.quanMode, seg.begin, stats.onsets, cfg.quanBPM, direction)
            del direction
        seg.begin -= spedcross

    # Start time (normalize)
    seg.begin = round(seg.begin % stats.audioLength)
    if old_begin != seg.begin: requan = True
    del source_old, altBegin, old_begin

    # Quantize segment duration
    if alt.Duration or (alt.ReQnDur and requan):
        if cfg.quanMode!=0 and randTF(cfg.quanDuration):
            if cfg.quanMode == 1:
                quanEnd = seg.begin + seg.duration_og * seg.speed
                quanEndLoops = stats.audioLength * int(quanEnd / stats.audioLength)
                quanEnd = quanEnd % stats.audioLength
                idx = quantize(1, quanEnd, stats.onsets, cfg.quanBPM, cfg.quanDurationDir, True)
                quanEnd = stats.onsets[idx]
                while stats.onsets[idx] + quanEndLoops <= seg.begin + spedcross + (seg.duration_og*seg.speed if cfg.quanDurationDir==2 else 0):
                    idx += 1
                    if idx + 1 > len(stats.onsets):
                        quanEnd = stats.audioLength + 1
                        break
                    quanEnd = stats.onsets[idx]
                seg.duration = (quanEndLoops + quanEnd - seg.begin) / seg.speed
                del quanEnd, quanEndLoops, idx
            elif cfg.quanMode == 2:
                quanEnd = quantize(2, seg.begin + seg.duration_og * seg.speed, stats.onsets, cfg.quanBPM, cfg.quanDurationDir, True)
                seg.duration = (quanEnd - seg.begin) / seg.speed
                del quanEnd
        else:
            seg.duration = seg.duration_og
        seg.duration = round(seg.duration)

    # Reverses
    if alt.Rev1: seg.rev1 = randTF(cfg.segReverseChance1)
    if alt.Rev2: seg.rev2 = randTF(cfg.segReverseChance2)

    # Repeats
    if alt.Repeats:
        seg.repeat = randTF(cfg.repeatChance) and (randTF(cfg.consecRepeatChance) or not stats.lastRepeat)
        seg.rep_len = round(randNum(cfg.repeatVal1, cfg.repeatVal2, cfg.repeatDist))
        seg.rep_inmss = cfg.repeatInMss

    # Backmask
    if alt.Bmask:
        seg.backmask = randTF(cfg.backmaskChance) and (randTF(cfg.consecBmaskChance) or not stats.lastBackmask)
        seg.bmask_cross = cfg.backmaskCrossfd
        seg.bmask_rev = randTF(cfg.backmaskRevChance)
        seg.bmask_full = randTF(cfg.backmaskFullChance)
        if randTF(cfg.backmaskAsymChance):
            seg.bmask_portion = randNum(cfg.backmaskAsymPortionVal1, cfg.backmaskAsymPortionVal2, cfg.backmaskAsymPortionDist)
            if seg.bmask_portion > 100: seg.bmask_portion = 100
        else: seg.bmask_portion = 100
        if not seg.bmask_full: seg.bmask_portion /= 2

    # Backmask repeats
    if alt.BmRep:
        seg.bmask_repeat = randTF(cfg.bmaskRepeatChance)
        seg.bmask_rep_len = round(randNum(cfg.bmaskRepeatVal1, cfg.bmaskRepeatVal2, cfg.bmaskRepeatDist))
        seg.bmask_rep_inmss = cfg.bmaskRepeatInMss

    # Fades
    if alt.FadeIn or alt.FadeOut:
        onlypauses = randTF(cfg.fadeOnlyIntoPauses)

    # Fade-in
    if alt.FadeIn:
        seg.fadein_p = cfg.fadeInPerc
        if (stats.pause_prev or not onlypauses) and randTF(cfg.fadeInChance):
            seg.fadein = randNum(cfg.fadeInVal1, cfg.fadeInVal2, cfg.fadeInDist)
        else: seg.fadein = 0
        if randTF(cfg.fadeInCutChance):
            seg.fadeincut = randNum(cfg.fadeInCutVal1, cfg.fadeInCutVal2, cfg.fadeInCutDist)
        else: seg.fadeincut = 0

    # Fade-out
    if cfg.fadeOutPercNote:
        if stats.onsets == []: seg.fadeout_nl = max(100, cfg.extnoteMinNoteLen)
        else: seg.fadeout_nl = findNoteLen(seg.begin, seg.begin + seg.duration * seg.speed, stats.onsets, 0, seg.rev1 != seg.bmask_rev)
    if alt.FadeOut:
        seg.fadeout_p = cfg.fadeOutPerc
        seg.fadeout_n = cfg.fadeOutPercNote
        if (stats.pause_next or not onlypauses) and randTF(cfg.fadeOutChance):
            seg.fadeout = randNum(cfg.fadeOutVal1, cfg.fadeOutVal2, cfg.fadeOutDist)
        else: seg.fadeout = 0
        if randTF(cfg.fadeOutCutChance):
            seg.fadeoutcut = randNum(cfg.fadeOutCutVal1, cfg.fadeOutCutVal2, cfg.fadeOutCutDist)
        else: seg.fadeoutcut = 0

    # Note extension
    if alt.NoteExt:
        seg.extnote = randTF(cfg.extnoteChance)
        seg.notecross = cfg.extnoteCrossfd
        seg.minnote = cfg.extnoteMinNoteLen
        if randTF(cfg.extnoteUseAltPortion):
            seg.extnote_len = randNum(cfg.extnoteAltPortionVal1, cfg.extnoteAltPortionVal2, cfg.extnoteAltPortionDist)
        else:
            seg.extnote_len = 100
        seg.extnote_len_fadeout = cfg.extnoteAltFadeOut
        seg.extnote_prior = cfg.extnotePriority

def genSegmentAudio(seg, stats):
    # Base segment
    revAudio = seg.rev1 != (seg.backmask and seg.bmask_rev)
    endPosition = int(seg.begin + seg.duration * seg.speed)
    if endPosition <= seg.begin: endPosition = seg.begin + 1
    appender = audSelect(stats.audio, seg.begin, endPosition)
    appender = audSpeed(appender, seg.speed)
    appender = audCropMs(appender)
    if revAudio: appender = audReverse(appender)

    # Resolve backmasks conflict
    seg_backmask = seg.backmask
    seg_extnote  = seg.extnote
    if seg_backmask and seg_extnote:
        if seg.extnote_prior:
            seg_backmask = False
        else:
            seg_extnote = False

    # Backamsk (Prepare)
    if seg_backmask:
        length = int(appender.duration_seconds * seg.bmask_portion * 10) # * 1000 / 10
        if seg.bmask_full:
            bmaskaud = appender[-length:]
        else:
            bmaskaud = appender[-2 * length : -length]
        bmaskaud_length = bmaskaud.duration_seconds * 1000
        del length

    # Repeat segment
    if seg.repeat:
        ogappend = appender
        oglength = appender.duration_seconds * 1000
        done = 0
        while segTime != -1 and done < seg.rep_len:
            crossfade = audMaxCross(seg.crossfade, [appender, ogappend])
            appender = appender.append(ogappend, crossfade=crossfade)
            if seg.rep_inmss: done += oglength - crossfade
            else: done += 1
            del crossfade
        del ogappend, oglength, done

    # Backmask
    if seg_backmask:
        if not seg.bmask_full: appender = appender[: -bmaskaud.duration_seconds * 1000]
        first, done = True, 0
        while segTime != -1 and (first or (seg.bmask_repeat and done < seg.bmask_rep_len)):
            bmaskaud = audReverse(bmaskaud)
            if seg.bmask_cross == -1: crossfade = seg.crossfade
            else: crossfade = seg.bmask_cross
            crossfade = audMaxCross(crossfade, [appender, bmaskaud])
            appender = appender.append(bmaskaud, crossfade=crossfade)
            if first: first = False
            else:
                if seg.bmask_rep_inmss: done += bmaskaud_length - crossfade
                else: done += 1
            del crossfade
        del bmaskaud, bmaskaud_length, first, done

    # Prepare fades
    fadein, fadeout = seg.fadein, seg.fadeout
    if seg.fadein_p:
        fadein *= seg.duration / 100
    if seg.fadeout_p:
        if seg.fadeout_n:
            fadeout *= seg.fadeout_nl / 100
        else:
            fadeout *= seg.duration / 100

    # Prepare note extension
    extnote_len = seg.extnote_len
    if seg_extnote and seg.extnote_len_fadeout:
        fadeout *= extnote_len / 100
        extnote_len = 100 / extnote_len * 100
    extnote_len = round(fadeout * extnote_len / 100)

    # Compensate fades
    segdur = appender.duration_seconds * 1000 + (extnote_len if seg_extnote else 0)
    fadesum = fadein + fadeout
    if fadesum > segdur:
        fadein  = segdur * fadein  / fadesum
        fadeout = segdur * fadeout / fadesum

    # Get note audio
    if seg_extnote:
        if stats.onsets == []:
            notelen = max(100, seg.minnote * seg.speed)
        else:
            notelen = findNoteLen(seg.begin, endPosition, stats.onsets, seg.minnote * seg.speed, seg.rev1)
        notelen = int(notelen)
        if not revAudio:
            if endPosition <= 0:
                noteaudio = []
            elif endPosition < notelen:
                noteaudio = stats.audio[:endPosition]
            else:
                noteaudio = stats.audio[endPosition - notelen : endPosition]
        else:
            if seg.begin >= stats.audioLength:
                noteaudio = []
            elif seg.begin + notelen > stats.audioLength:
                noteaudio = stats.audio[seg.begin:]
            else:
                noteaudio = stats.audio[seg.begin : seg.begin + notelen]

    # Extend note
    if seg_extnote and len(noteaudio) > 0:
        if seg.speed != 1: noteaudio = audSpeed(noteaudio, seg.speed)
        if revAudio: noteaudio = audReverse(noteaudio)
        noteaudio = audCropMs(noteaudio)
    if seg_extnote and len(noteaudio) > 0: # Check again
        notes = AudioSegment.empty()
        if seg.notecross == -1: crossfade = seg.crossfade
        else: crossfade = seg.notecross
        while segTime != -1 and notes.duration_seconds * 1000 < extnote_len:
            noteaudio = audReverse(noteaudio)
            _crfd = audMaxCross(crossfade, [notes, noteaudio])
            notes = notes.append(noteaudio, crossfade=_crfd)
        notes = audCropMs(notes[:extnote_len])
        _crfd = audMaxCross(crossfade, [appender, notes])
        appender = appender.append(notes, crossfade=_crfd)
        del noteaudio, notes, crossfade

    # Basic segment options (Again)
    fadein  = int(fadein)
    fadeout = int(fadeout)
    if fadein  > 0: appender = audFadeIn (appender, fadein,  seg.fadeincut)
    if fadeout > 0: appender = audFadeOut(appender, fadeout, seg.fadeoutcut)
    if seg.rev2: appender = audReverse(appender)

    return audCropMs(appender)

def genChunkAudio(seg, cfg, stats):
    if seg.pause: return AudioSegment.silent(duration = seg.pause_dur)

    mute = randTF(cfg.muteChance) and (randTF(cfg.consecMutedChance) or not (stats.lastMute or (stats.pause_prev and cfg.muteCountPauses)))

    if mute and randTF(cfg.muteToPauseChance):
        pause_cfg = genPauseInfo(cfg)[0]
        appender = genChunkAudio(pause_cfg, None, None)
    else:
        appender = genSegmentAudio(seg, stats)

    if mute:
        stats.muteCount[1] += 1
        stats.lastMute = True
        applen = len(appender)
        appender = AudioSegment.silent(duration=applen)
    else:
        stats.muteCount[0] += 1
        stats.lastMute = False

    return appender

def genCutSegment(audio, duration):
    auddur = audio.duration_seconds * 1000
    if auddur >= duration:
        return audio[0:duration]
    else:
        return audio.append(AudioSegment.silent(duration = duration - auddur + 1), crossfade=1)

def genAnalyzeMem(arr, pause):
    if pause:
        return None, arr
    else:
        arr1 = []
        arr2 = []
        for i in arr:
            if i[0] == 0: arr1.append(i[1])
            else: arr2.append([i[0]-1, i[1]])
        arr1r = None if arr1==[] else random.choice(arr1)
        return arr1r, arr2

def genMain(stats, cfg):
    global genReady, lastSeed, liveUpdate, scrstats
    scrstats = stats
    if cfg.seed == None: cfg.seed = randSeed(10)
    liveUpdate = None
    lastSeed = cfg.seed
    random.seed(cfg.seed)
    print(f"\n=== Scrambling at {strftime('%Y-%m-%d %H:%M:%S', localtime())}. Seed: {cfg.seed} ===")

    # Live preview analysis
    live = segTime == float("inf")
    if live:
        livepr = abLivePreview()
        stats.audio = makePlayable(stats.audio)

    # Trim audio
    stats.audioLength = int(stats.audio.duration_seconds * 1000)
    if cfg.trim:
        if cfg.trimVal2 > stats.audioLength or cfg.trimVal2 <= cfg.trimVal1:
            cfg.trimVal2 = stats.audioLength
        stats.audio = stats.audio[cfg.trimVal1 : cfg.trimVal2]
        stats.audioLength = int(stats.audio.duration_seconds * 1000)
        if cfg.trimShiftOns:
            stats.onsets   = [o - cfg.trimVal1 for o in stats.onsets]
            stats.stOnsets = [o - cfg.trimVal1 for o in stats.stOnsets]

    # Onsets
    stats.onsets   = [o for o in stats.onsets   if 0 <= o <= stats.audioLength]
    stats.stOnsets = [o for o in stats.stOnsets if 0 <= o <= stats.audioLength]
    if cfg.quanMode == 0: stats.stOnsets = []
    if cfg.quanMode == 1:
        stats.audio = stats.audio[0:stats.onsets[-1]]
        stats.audioLength = stats.audio.duration_seconds * 1000

    # Misc preparations
    genReady = 0
    memory      = []
    segmentList = []
    lengthList  = []

    stats.pause_curr   = cfg.consecPauseFirst
    stats.lastRepeat   = cfg.consecRepeatFirst
    stats.lastBackmask = cfg.consecBmaskFirst
    stats.lastMute     = cfg.consecMutedFirst

    segID = 0
    stats.pause_next = randTF(cfg.pauseChance)and (randTF(cfg.consPauseChance) or not stats.pause_curr)
    while genReady < segTime:
        # Live preview update
        if liveUpdate != None:
            cfg = liveUpdate
            liveUpdate = None

        # Generate segment info
        alter = abAlterInfo(cfg, stats.fromScratch)
        if stats.fromScratch:
            stats.pause_prev = stats.pause_curr
            stats.pause_curr = stats.pause_next
            stats.pause_next = randTF(cfg.pauseChance) and (randTF(cfg.consPauseChance) or not stats.pause_curr)
            torem, memory = genAnalyzeMem(memory, stats.pause_curr)
            if stats.pause_curr:
                variations = genPauseInfo(cfg)
            else:
                if cfg.looping or torem==None:
                    if randTF(cfg.crossFdChance):
                        crossfade = round(randNum(cfg.crossFdVal1, cfg.crossFdVal2, cfg.crossFdDist))
                    else: crossfade = 0
                    variations = []
                    for i in range(cfg.loopVarNumber if cfg.looping else 1):
                        segment = abSegmentInfo()
                        genSegmentInfo(segment, cfg, stats, alter, crossfade)
                        variations.append(segment)
                else:
                    variations = None
            segmentList.append(variations)
        else:
            stats.pause_prev = segmentList[(segID - 1) % len(segmentList)][0].pause
            stats.pause_curr = segmentList[ segID      % len(segmentList)][0].pause
            stats.pause_next = segmentList[(segID + 1) % len(segmentList)][0].pause
            torem, memory = genAnalyzeMem(memory, stats.pause_curr)
            for segment in segmentList[segID]:
                genSegmentInfo(segment, cfg, stats, alter, None)
        del alter

        # Generate timeframe
        timeframe = AudioSegment.empty()
        stats.muteCount = [0, 0] # [normal_count, mute_count]
        idx = 0
        while True:
            if torem != None:
                segment = torem
                torem = None
            else:
                if idx == 0: random.shuffle(segmentList[segID])
                segment = segmentList[segID][idx]
                if randTF(cfg.remembChance) and not segment.pause:
                    remseg = copy(segment)
                    remseg.source = None
                    after = randNum(cfg.remembAfterVal1, cfg.remembAfterVal2, cfg.remembAfterDist)
                    memory.append([round(after), remseg])
                idx += 1; idx %= len(segmentList[segID])
            appender = genChunkAudio(segment, cfg, stats)
            _crfd = audMaxCross(segment.crossfade, [appender, timeframe])
            timeframe = timeframe.append(appender, crossfade=_crfd)
            if (stats.fromScratch or not cfg.loopKeepSize) or timeframe.duration_seconds * 1000 > lengthList[segID] or randTF(cfg.loopFillWithSilence):
                break
        del idx

        # Misc
        if not segment.pause:
            stats.lastRepeat = segment.repeat
            stats.lastBackmask = segment.backmask
        if cfg.looping:
            if stats.fromScratch:
                lengthList.append(timeframe.duration_seconds * 1000)
                if genReady*1000 + lengthList[-1] - segment.crossfade > cfg.loopDuration:
                    if cfg.loopStrictly: lengthList[-1] = cfg.loopDuration - genReady*1000 + segment.crossfade
                    stats.fromScratch = False
            if cfg.loopKeepSize: timeframe = genCutSegment(timeframe, lengthList[segID])
        else:
            segmentList[segID] = None

        # Append
        _crfd = audMaxCross(segment.crossfade, [timeframe, stats.slicecr])
        stats.slicecr = stats.slicecr.append(timeframe, crossfade=_crfd)

        # Live preview
        if live and stats.slicecr.duration_seconds >= float(abSavCfg.get("livepr_buff")):
            livepr.wait()
            if segTime > 0: run(livepr.play, stats.slicecr)
            stats.slicecr = AudioSegment.empty()

        # Stumbling
        if segment.pause:
            if randTF(cfg.stumbleCountPauses):
                stats.stumblePos += (len(timeframe) - _crfd) * segment.speed
        elif segment.source=="stumble" or not(randTF(cfg.stumbleOnlyStumbled)):
            if segment.source!="avgstart" or not randTF(cfg.stumbleIgnoreAvgSt):
                if stats.muteCount[0] > stats.muteCount[1] or randTF(cfg.stumbleCountMuted):
                    if cfg.stumbleLockedMode:
                        stats.stumblePos += (len(timeframe) - _crfd) * segment.speed
                    else:
                        stats.stumblePos = segment.begin + len(timeframe) * segment.speed
        stats.stumblePos %= stats.audioLength
        stats.stumblePos = round(stats.stumblePos)

        # Check segment length
        if live:
            genReady += (len(timeframe) - _crfd) / 1000
        else:
            genReady = len(stats.slicecr) / 1000
        progressbar["value"] = genReady / segTime * 100
        del _crfd

        # Check looping
        segID += 1
        if segID == len(segmentList) and not stats.fromScratch: segID = 0


def wrongAudio(stats):
    if stats.audio==None:
        mb.showerror("Error", "You have to first import an audio file!")
        return True
    else:
        return False

def wrongComboboxes(cfg):
    wrong = (cfg.segDist == -1 or
        cfg.pauseDist == -1 or
        cfg.crossFdDist == -1 or
        cfg.fadeInDist == -1 or
        cfg.fadeOutDist == -1 or
        cfg.repeatDist == -1 or
        cfg.remembAfterDist == -1 or
        x_speedm.current() == -1 or
        cfg.backmaskAsymPortionDist == -1 or
        cfg.bmaskRepeatDist == -1 or
        cfg.extnoteAltPortionDist == -1 or
        cfg.quanMode == -1 or
        cfg.quanAvgStartDir == -1 or
        cfg.quanStumbBeginDir == -1 or
        cfg.quanStumbleSkipDir == -1 or
        cfg.quanBeginDir == -1 or
        cfg.quanDurationDir == -1 or
        cfg.quanUseStOnsetsDir == -1 or
        cfg.fadeInCutDist == -1 or
        cfg.fadeOutCutDist == -1)
    if wrong: mb.showerror("Error", "Please check all checkboxes!")
    return wrong

def wrongZeroSegment(cfg):
    wrong = cfg.segVal1 == cfg.segVal2 == 0
    if wrong: mb.showerror("Error", "Segment length can't be zero!")
    return wrong

def wrongLognorm(cfg):
    wrong = ((cfg.segDist == 2 and (cfg.segVal1 > 10 or cfg.segVal2 > 10)) or
        (cfg.pauseDist == 2 and (cfg.pauseVal1 > 10 or cfg.pauseVal2 > 10)) or
        (cfg.crossFdDist == 2 and (cfg.crossFdVal1 > 10 or cfg.crossFdVal2 > 10)) or
        (cfg.fadeInDist == 2 and (cfg.fadeInVal1 > 10 or cfg.fadeInVal2 > 10)) or
        (cfg.fadeOutDist == 2 and (cfg.fadeOutVal1 > 10 or cfg.fadeOutVal2 > 10)) or
        (cfg.repeatDist == 2 and (cfg.repeatVal1 > 10 or cfg.repeatVal2 > 10)) or
        (cfg.remembAfterDist == 2 and (cfg.remembAfterVal1 > 10 or cfg.remembAfterVal2 > 10)) or
        (cfg.bmaskRepeatDist == 2 and (cfg.bmaskRepeatVal1 > 10 or cfg.bmaskRepeatVal2 > 10)) or
        (cfg.fadeInCutDist == 2 and (cfg.fadeInCutVal1 > 10 or cfg.fadeInCutVal2 > 10)) or
        (cfg.fadeOutCutDist == 2 and (cfg.fadeOutCutVal1 > 10 or cfg.fadeOutCutVal2 > 10)))
    if wrong: return not mb.askyesno("Warning", "In LOGNORMAL random mode, parameters greater than 10 are not recommended! Continue anyway?", default=mb.NO, icon="warning")
    else: return False

def wrongSegmentLength(cfg, min_sdur = 100, min_ratio = 1/6, pop_size = 500):
    if cfg.quanMode == 1 or generating:
        return False
    opts = (cfg.segVal1, cfg.segVal2, cfg.segDist)
    counter = 0
    for _ in range(pop_size):
        if randNum(*opts) > min_sdur:
            counter += 1
    if counter/pop_size > min_ratio:
        return False
    else:
        return not mb.askyesno("Warning", f"Only {round(counter/pop_size*100, 1)}% of the pre-calculated segment lengths are greater than {min_sdur} ms. The scrambling may be very slow. Continue anyway?", default=mb.NO, icon="warning")

def wrongNumAvgSt(cfg):
    a = len(cfg.avgstrtTimes)
    b = len(cfg.avgstrtWeights)
    if a!=b: mb.showerror("Error", f"The number of average start times and their weights must match! ({a} vs {b})\nYou can leave weights field blank for equal weighting.")
    return a!=b

def wrongNumSpeeds(cfg):
    a = len(cfg.speeds)
    b = len(cfg.speedw)
    if a!=b: mb.showerror("Error", f"The number of speeds and their weights must match! ({a} vs {b})\nYou can leave weights field blank for equal weighting.")
    return a!=b

def wrongSpeeds(cfg):
    wrong = False in [0 < speed for speed in cfg.speeds]
    if wrong: mb.showerror("Error", "Speed ​​cannot be zero or negative!")
    return wrong

def wrongZeroWeights(cfg):
    if sum(cfg.speedw) <= 0:
        mb.showerror("Error", "Total of speed variation weights must be greater that zero!")
        return True
    elif cfg.avgstrtChance > 0 and sum(cfg.avgstrtWeights) <= 0:
        mb.showerror("Error", "Total of average start time weights must be greater that zero!")
        return True
    elif cfg.stumbleChance > 0 and cfg.skipChance > 0 and (cfg.skipRandWeight + cfg.skipForwWeight + cfg.skipBackWeight <= 0):
        mb.showerror("Error", "Total of skip direction weights must be greater that zero!")
        return True
    else:
        return False

def wrongOnsets(stats, cfg):
    if cfg.quanMode==1:
        if stats.onsets==[]:
            if mb.askyesno("Error", "You can't use ONSET quantize mode without onsets detected.\nDo you want to detect onsets?", icon="error"): abOnsetsWindow()
            return True
        else:
            return False
    else:
        return False

def wrongQuanDirMode(cfg):
    if cfg.quanMode == 2 and cfg.quanBeginDir == 0:
        mb.showerror("Error", "Can't use EQUAL direction mode for segment begin in BPM mode")
        return True
    else:
        return False

def wrongConfig(stats, cfg):
    return (wrongAudio(stats)
        or wrongComboboxes(cfg)
        or wrongZeroSegment(cfg)
        or wrongLognorm(cfg)
        or wrongSegmentLength(cfg)
        or wrongNumAvgSt(cfg)
        or wrongNumSpeeds(cfg)
        or wrongSpeeds(cfg)
        or wrongZeroWeights(cfg)
        or wrongOnsets(stats, cfg)
        or wrongQuanDirMode(cfg))


def usrUpdWindowTitle():
    title = abVersion
    if audio != None:
        audlen = round(audio.duration_seconds)
        if abCurrCfg.secimpaudlen.get() == 0:
            audlen = f"{audlen//60}:{str(audlen%60).zfill(2)}"
        else: audlen = f"{audlen} sec"
        title += f" - {basename(audioPath)} ({audlen})"
    if onsets != []:
        title += " - Onsets loaded"
        if stOnsets != []:
            title += " - Start onsets loaded"
    if previewing: title += " - Previewing"
    if segTime == float("inf"): title += " - Live preview"
    root.title(title)

    if segTime == float("inf"):
        abort.configure(text="Update")
    else:
        abort.configure(text="Abort")

def usrUpdSecImpAudLen():
    abSavCfg.set("secimpaudlen")
    usrUpdWindowTitle()

def usrUpdFormats(init=False):
    global types_import
    if not init: abSavCfg.set("moreformats")
    if abCurrCfg.moreformats.get() == 1: types_import = types_import_2
    else: types_import = types_import_1

def usrAbortUpdate():
    global segTime, liveUpdate
    if segTime != float("inf"): # Abort button
        if mb.askyesno("Abort", f"Are you sure you want to abort scrambling?\nThe current rendered length is {round(genReady, 3)} seconds out of {segTime} ({round(genReady/segTime*100, 2)}%).\nAudio will be exported/previewed anyway.", icon="warning"):
            segTime = -1
    else: # Update button (Live preview)
        try:
            newcfg = abOptions()
        except Exception as e:
            abError("Error", e)
            newcfg = None
        else:
            if wrongConfig(scrstats, newcfg):
                newcfg = None
        liveUpdate = newcfg

def usrStopPreview():
    global segTime
    if segTime == float("inf"): segTime = -1
    if not AB_DISABLE_SIMPLEAUDIO:
        simpleaudio.stop_all()


def usrLoadAudio(path=None, rempath=True):
    global audio, audioPath, onsets
    def stopPB():
        progressbar.configure(mode="determinate")
        progressbar.stop()
    if path==None: path = fd.askopenfilename(filetypes=types_import, initialdir=abSavCfg.get("dir_audio"))
    if not validPath(path): return
    if rempath: abSavCfg.set("dir_audio", path=path)
    progressbar.configure(mode="indeterminate")
    progressbar.start()
    audioPath = path
    try:
        audio = None
        audio = loadAudio(path)
    except Exception as e:
        abError("Import", e)
        if abCurrCfg.resetonsets.get() == 1:
            onsProcess(2, [])
            onsProcess(2, [], True)
    else:
        if abCurrCfg.resetonsets.get() == 1:
            onsProcess(2, [])
            onsProcess(2, [], True)
        usrUpdWindowTitle()
        mb.showinfo("Import", "Audio imported successfully.")
        if abCurrCfg.autoonsdet.get() == 1:
            onsGet(None, 2, fromCurrent=True, window=False)
    usrUpdWindowTitle(); stopPB()

def usrScrambleA(mode):
    # Modes: 0 - Export, 1 - Preview, 2 - Live preview
    if generating or (previewing and mode != 0): return
    try:
        stats = abStats()
        cfg = abOptions()
        if wrongConfig(stats, cfg): return
        if mode == 0:
            duration = sd.askfloat("Export", "Exported audio length (in seconds):", initialvalue=abSavCfg.get("len_export"), parent=root)
            if duration == None: return
            else: abSavCfg.set("len_export",   value=uiF2N(duration))
            fname = "untitled_"+str(int(time())) if abCurrCfg.uniqfilename.get()==1 else "untitled"
            dest = fd.asksaveasfilename(filetypes=types_export, defaultextension=types_export, typevariable=abCurrCfg.exportf, initialfile=fname, initialdir=abSavCfg.get("dir_scramble"))
            if not validPath(dest): return
            else: abSavCfg.set("dir_scramble", path=dest)
        elif mode == 1:
            duration = abCurrCfg.len_preview.get()
            dest = None
        elif mode == 2:
            duration = float("inf")
            dest = None
    except Exception as e:
        abError("Error", e)
        return
    else:
        run(usrScrambleB, duration, dest, stats, cfg)

def usrScrambleB(duration, dest, stats, cfg):
    global segTime, generating
    try:
        segTime = duration
        generating = True
        usrUpdWindowTitle()
        abort.configure(state="normal")
        genMain(stats, cfg)
    except Exception as e:
        abError("Scrambling", e)
    if stats.slicecr.duration_seconds > 0:
        if dest != None:
            save = True
            while save:
                try:
                    exportAudio(stats.slicecr, dest)
                except Exception as e:
                    save = abError("Export", e, form=mb.askretrycancel)
                else:
                    break
            if save:
                if mb.askyesno("Complete!", "Scrambling complete.\nDo you want to open your file now?", icon="info"): openFile(dest)
        elif duration != float("inf"):
            run(usrPreview, stats.slicecr, duration)
    generating = False
    usrUpdWindowTitle()
    abort.configure(state="disabled")
    progressbar["value"] = 0

def usrPreview(audio, duration):
    global previewing
    try:
        previewing = True; usrUpdWindowTitle()
        audio = makePlayable(audio)
        duration = min(duration, audio.duration_seconds)
        play(audio[:duration*1000])
    except Exception as e:
        abError("Preview", e)
    previewing = False; usrUpdWindowTitle()

def usrQuit():
    usrStopPreview()
    sys.exit()


def uiF2N(value):
    value = str(value)
    if value[-2:] == ".0":
        value = value[:-2]
    return value

def uiConvTime(value, mode):
    try:
        value = float(value)
        if mode == "ms2sec":
            return uiF2N(value / 1000)
        if mode == "sec2ms":
            return uiF2N(value * 1000)
    except:
        return value

def uiEntryConvert(entry, mode, ignoreMinusOne = False):
    try:
        value = float(entry.get())
        if not (ignoreMinusOne and value == -1):
            uiSetText(entry, uiConvTime(value, mode))
    except Exception:
        pass

def uiSetText(entry, text):
    entry.delete(0, END)
    entry.insert(0, str(text))

def uiSelCbox(cbox, value):
    try:
        cbox.current(int(float(value)))
    except Exception:
        cbox.configure(state="normal")
        cbox.delete(0, END)
        cbox.insert(0, "<Error>")
        cbox.configure(state="readonly")

class uiRandom:
    def __init__(self, parent, ent_w=6, cbx_w=10, padding=1, noLognorm=False):
        randdists = ["Uniform", "Normal", "Lognormal"]
        if noLognorm: randdists = randdists[:-1]
        self.main = Frame(parent, padding=padding)
        self.val1 = Entry(self.main, width=ent_w)
        self.val1.grid(row=0, column=0)
        self.sep1 = Label(self.main, text="-", width=1)
        self.sep1.grid(row=0, column=1)
        self.val2 = Entry(self.main, width=ent_w)
        self.val2.grid(row=0, column=2)
        self.sep2 = Label(self.main, text="/", width=1)
        self.sep2.grid(row=0, column=3)
        self.dist = Combobox(self.main, values=randdists, width=cbx_w, state="readonly")
        self.dist.grid(row=0, column=4)
        self.dist.bind("<<ComboboxSelected>>", self.update)
    def update(self, dummy=None):
        self.sep1.configure(text=["-", "±", ",", "?"][self.dist.current()])
    def get(self):
        return float(self.val1.get()), float(self.val2.get()), self.dist.current()
    def set(self, val1="", val2="", dist="", *dummy):
        uiSetText(self.val1, val1)
        uiSetText(self.val2, val2)
        uiSelCbox(self.dist, dist)
        self.update()
    def save(self):
        return f"{self.val1.get() or '?'} {self.val2.get() or '?'} {self.dist.current()}"
    def convtime(self, mode):
        if self.dist.current() != 2:
            uiSetText(self.val1, uiConvTime(self.val1.get(), mode))
            uiSetText(self.val2, uiConvTime(self.val2.get(), mode))

class uiChance:
    def __init__(self, parent, width=4, padding=1):
        self.main = Frame(parent, padding=padding)
        self.val = Entry(self.main, width=width)
        self.val.grid(row=0, column=0)
        self.prc = Label(self.main, text="%")
        self.prc.grid(row=0, column=1)
    def get(self):
        return float(self.val.get())
    def set(self, value=""):
        uiSetText(self.val, value)
    def save(self):
        return self.val.get()

class uiCheckbox:
    def __init__(self, parent, text):
        self.var = IntVar()
        self.main = Checkbutton(parent, text=text, variable=self.var)
    def get(self):
        return bool(self.var.get())
    def set(self, value):
        self.var.set(binBool(value))
    def save(self):
        return self.var.get()


if True:
    # Some global variables
    audio = None
    audioPath = ""
    presetPath = ""
    onsets = []
    stOnsets = []
    lastSeed = None
    segTime = -1
    genReady = 0
    generating = False
    previewing = False
    detecting  = False
    liveUpdate = None

    # Combobox modes
    modes_speed = ["Semitones", "Percent change", "Speed multiplier"]
    modes_quan = ["None", "Onsets", "BPM"]
    modes_quan_dir = ["Equal", "Closer", "Backw.", "Forw.", "Auto"]

    # File extensions
    allfiles = ["All files", "*.*"]

    types_preset     = [["AudioButcher 3.0 Preset", "*.ab3"], allfiles]
    types_preset_ab2 = [["AudioButcher 2.0 Preset", "*.abp"], allfiles]

    types_export = [["Wave", "*.wav"],
                    ["MPEG Layer-3", "*.mp3"],
                    ["FLAC", "*.flac"],
                     allfiles]

    types_import_1 = [["Popular formats", "*.wav *.mp3 *.ogg *.flac"],
                      ["Wave", "*.wav"],
                      ["MPEG Layer-3", "*.mp3"],
                      ["Ogg Vorbis", "*.ogg"],
                      ["FLAC", "*.flac"],
                       allfiles]

    types_import_2 = [["Popular formats", "*.wav *.mp3 *.wma *.ogg *.opus *.flac *.aac *.m4a"],
                      ["Wave", "*.wav"],
                      ["MPEG Layer-3", "*.mp3"],
                      ["Windows Media Audio", "*.wma"],
                      ["Ogg Vorbis", "*.ogg"],
                      ["Opus", "*.opus"],
                      ["FLAC", "*.flac"],
                      ["AAC", "*.aac"],
                      ["MPEG-4 Audio", "*.m4a"],
                       allfiles]

    types_onset = [["AudioButcher Onset List", "*.abo"],
                   ["Text files", "*.txt"],
                    allfiles]

    types_onset2 = [["AudioButcher Start Onset List", "*.sto"],
                    ["AudioButcher Onset List", "*.abo"],
                    ["Text files", "*.txt"],
                     allfiles]

    # Commands
    doImport   = lambda event=None: run(usrLoadAudio)
    doRefresh  = lambda event=None: run(usrLoadAudio, audioPath)
    doExport   = lambda event=None: usrScrambleA(0)
    doCfgOpen  = lambda event=None: cfgImport()
    doCfgSave  = lambda event=None: cfgExport(path=presetPath)
    doCfgSavAs = lambda event=None: cfgExport()
    doPreview  = lambda event=None: usrScrambleA(1)
    doLivePrev = lambda event=None: usrScrambleA(2)
    doStopPrev = lambda event=None: usrStopPreview()

    # Window
    if AB_DISABLE_TKDND2: root = Tk()
    else:
        root = TkinterDnD.Tk()
        root.drop_target_register("DND_Files")
        root.dnd_bind("<<Drop>>", dndGotFile)
    root.bind("<Button-3>", popup)
    menu = Menu(root, tearoff=False)
    menu_file = Menu(menu, tearoff=False)
    smen_pres = Menu(menu_file, tearoff=False)
    menu_prev = Menu(menu, tearoff=False)
    smen_plen = Menu(menu_prev, tearoff=False)
    smen_live = Menu(menu_prev, tearoff=False)
    menu_pref = Menu(menu, tearoff=False)
    menu_help = Menu(menu, tearoff=False)
    root.config(menu=menu)

    # Config
    abSavCfg = abSavedConfigHandler(join(homepath, ".audiobutcher"), "AudioButcher_Config")
    class abCurrCfg:
        len_preview = IntVar()
        len_preview.set(abSavCfg.get("len_preview"))
        uniqfilename = IntVar()
        uniqfilename.set(binBool(abSavCfg.get("uniqfilename")))
        shadderrinf = IntVar()
        shadderrinf.set(binBool(abSavCfg.get("shadderrinf")))
        convsec2ms = IntVar()
        convsec2ms.set(binBool(abSavCfg.get("convsec2ms")))
        secimpaudlen = IntVar()
        secimpaudlen.set(binBool(abSavCfg.get("secimpaudlen")))
        moreformats = IntVar()
        moreformats.set(binBool(abSavCfg.get("moreformats")))
        remdndpath = IntVar()
        remdndpath.set(binBool(abSavCfg.get("remdndpath")))
        openscrfolder = IntVar()
        openscrfolder.set(binBool(abSavCfg.get("openscrfolder")))
        if osname != "Windows": openscrfolder.set(0)
        autoonsdet = IntVar()
        autoonsdet.set(binBool(abSavCfg.get("autoonsdet")))
        if AB_DISABLE_LIBROSA and not AB_ALT_USE_AUBIO: autoonsdet.set(0)
        resetonsets = IntVar()
        resetonsets.set(binBool(abSavCfg.get("resetonsets")))
        closeonsets = IntVar()
        closeonsets.set(binBool(abSavCfg.get("closeonsets")))
        exportf = StringVar()

    # Hotkeys
    root.bind("<Control-i>", doImport)
    root.bind("<Control-e>", doExport)
    root.bind("<Control-r>", doRefresh)
    root.bind("<Control-o>", doCfgOpen)
    root.bind("<Control-n>", lambda event: cfgImport(data=abPresets["Default"]))
    root.bind("<Control-s>", doCfgSave)
    root.bind("<Control-Shift-S>", doCfgSavAs)
    if not AB_DISABLE_SIMPLEAUDIO:
        root.bind("<Control-p>", doPreview)
        root.bind("<Control-Alt-p>", doStopPrev)
        root.bind("<Control-l>", doLivePrev) if AB_SHOW_LIVE_PREVIEW else None

    # File menu
    menu.add_cascade(label="File", menu=menu_file)
    menu_file.add_command(label="Import audio file...", accelerator="Ctrl+I", command=doImport)
    menu_file.add_command(label="Export audio...", accelerator="Ctrl+E", command=doExport)
    menu_file.add_command(label="Refresh file", accelerator="Ctrl+R", command=doRefresh)
    menu_file.add_separator()
    menu_file.add_command(label="Open preset...", accelerator="Ctrl+O", command=doCfgOpen)
    menu_file.add_command(label="Save preset", accelerator="Ctrl+S", command=doCfgSave)
    menu_file.add_command(label="Save preset as...", accelerator="Ctrl+Shift+S", command=doCfgSavAs)
    menu_file.add_cascade(label="Factory presets", menu=smen_pres)
    menu_file.add_separator()
    menu_file.add_command(label="Open AB2 preset", command=cfgImportAB2)
    menu_file.add_command(label="Restore the last seed", command=lambda: cfgLastSeed())
    menu_file.add_separator()
    menu_file.add_command(label="Quit", command=lambda: usrQuit())

    # File menu / Factory presets
    for name in abPresets:
        if name[0] == "_":
            smen_pres.add_separator()
        else:
            accel = "Ctrl+N" if name=="Default" else ""
            smen_pres.add_command(label=name, accelerator=accel, command=lambda name=name: cfgImport(data=abPresets[name]))

    # Preview menu
    if not AB_DISABLE_SIMPLEAUDIO:
        menu.add_cascade(label="Preview", menu=menu_prev)
        menu_prev.add_command(label="Preview", accelerator="Ctrl+P", command=doPreview)
        menu_prev.add_command(label="Stop preview", accelerator="Ctrl+Alt+P", command=doStopPrev)
        menu_prev.add_cascade(label="Preview length", menu=smen_plen)
        if AB_SHOW_LIVE_PREVIEW:
            menu_prev.add_separator()
            menu_prev.add_cascade(label="Live preview", menu=smen_live)

    # Preview length
    smen_plen.add_radiobutton(label="5 seconds",  var=abCurrCfg.len_preview, value=5,  command=lambda: abSavCfg.set("len_preview"))
    smen_plen.add_radiobutton(label="10 seconds", var=abCurrCfg.len_preview, value=10, command=lambda: abSavCfg.set("len_preview"))
    smen_plen.add_radiobutton(label="20 seconds", var=abCurrCfg.len_preview, value=20, command=lambda: abSavCfg.set("len_preview"))
    smen_plen.add_radiobutton(label="30 seconds", var=abCurrCfg.len_preview, value=30, command=lambda: abSavCfg.set("len_preview"))
    smen_plen.add_radiobutton(label="40 seconds", var=abCurrCfg.len_preview, value=40, command=lambda: abSavCfg.set("len_preview"))
    smen_plen.add_radiobutton(label="50 seconds", var=abCurrCfg.len_preview, value=50, command=lambda: abSavCfg.set("len_preview"))
    smen_plen.add_radiobutton(label="60 seconds", var=abCurrCfg.len_preview, value=60, command=lambda: abSavCfg.set("len_preview"))

    # Live preview
    smen_live.add_command(label="Start live preview", accelerator="Ctrl+L", command=doLivePrev)
    smen_live.add_command(label="Change buffer size", command=lambda: getBufferSize())

    # Preferencses menu
    menu.add_cascade(label="Preferences", menu=menu_pref)
    menu_pref.add_checkbutton(label="Generate unique filenames", var=abCurrCfg.uniqfilename, command=lambda: abSavCfg.set("uniqfilename"))
    menu_pref.add_checkbutton(label="Show additional error information", var=abCurrCfg.shadderrinf, command=lambda: abSavCfg.set("shadderrinf"))
    menu_pref.add_checkbutton(label="Automatic ms-sec conversion", var=abCurrCfg.convsec2ms, command=lambda: abSavCfg.set("convsec2ms"))
    menu_pref.add_separator()
    menu_pref.add_checkbutton(label="Imported audio length in seconds", var=abCurrCfg.secimpaudlen, command=lambda: usrUpdSecImpAudLen())
    menu_pref.add_checkbutton(label="Show more import formats (ffmpeg)", var=abCurrCfg.moreformats, command=lambda: usrUpdFormats())
    menu_pref.add_checkbutton(label="Remember dropped file path", var=abCurrCfg.remdndpath, command=lambda: abSavCfg.set("remdndpath"))
    menu_pref.add_checkbutton(label="Open scrambled file in folder", var=abCurrCfg.openscrfolder, command=lambda: abSavCfg.set("openscrfolder"))
    menu_pref.add_separator()
    menu_pref.add_checkbutton(label="Automatically detect onsets", var=abCurrCfg.autoonsdet, command=lambda: abSavCfg.set("autoonsdet"))
    menu_pref.add_checkbutton(label="Reset onsets after new file imported", var=abCurrCfg.resetonsets, command=lambda: abSavCfg.set("resetonsets"))
    menu_pref.add_checkbutton(label="Automatically close onsets window", var=abCurrCfg.closeonsets, command=lambda: abSavCfg.set("closeonsets"))
    if osname != "Windows": menu_pref.entryconfig(7, state="disabled")
    if AB_DISABLE_LIBROSA and not AB_ALT_USE_AUBIO: menu_pref.entryconfig(9, state="disabled")

    # Help menu
    menu.add_cascade(label="Help", menu=menu_help)
    menu_help.add_command(label="Join our Discord server", command=lambda: webbrowser.open(abDiscordLink))
    menu_help.add_separator()
    menu_help.add_command(label="License...", command=lambda: webbrowser.open(abLicenceLink))
    menu_help.add_command(label="About...", command=lambda: mb.showinfo(abVersion, abDescription.format(sys.version)))

    # Tabs
    tabs = Notebook(root)
    tab1 = Frame(tabs, padding=10)
    tab2 = Frame(tabs, padding=10)
    tab3 = Frame(tabs, padding=10)
    tab4 = Frame(tabs, padding=10)
    tabs.pack(side="top", fill="both", expand=True)
    tabs.add(tab1, text="Basic")
    tabs.add(tab2, text="Backmasking + Quantization")
    tabs.add(tab3, text="Stumbling + Looping")
    tabs.add(tab4, text="Miscellaneous")

    # Main tab
    Label(tab1).grid(row=0, column=3)
    Label(tab1).grid(row=0, column=6)

    tr_seg = Label(tab1, text="Segment length: ")
    tr_seg.grid(row=0, column=0, columnspan=2, sticky="w")
    ir_seg = uiRandom(tab1)
    ir_seg.main.grid(row=0, column=2)
    tc_segReverseChance1 = Label(tab1, text="First reverse chance: ")
    tc_segReverseChance1.grid(row=0, column=4, sticky="w")
    ic_segReverseChance1 = uiChance(tab1)
    ic_segReverseChance1.main.grid(row=0, column=5)
    tc_segReverseChance2 = Label(tab1, text="Second reverse chance: ")
    tc_segReverseChance2.grid(row=0, column=7, sticky="w")
    ic_segReverseChance2 = uiChance(tab1)
    ic_segReverseChance2.main.grid(row=0, column=8)

    tr_pause = Label(tab1, text="Pause length: ")
    tr_pause.grid(row=1, column=0, columnspan=2, sticky="w")
    ir_pause = uiRandom(tab1)
    ir_pause.main.grid(row=1, column=2)
    tc_pause = Label(tab1, text="Pause chance: ")
    tc_pause.grid(row=1, column=4, sticky="w")
    ic_pause = uiChance(tab1)
    ic_pause.main.grid(row=1, column=5)
    tc_consPause = Label(tab1, text="Consecutive pause chance: ")
    tc_consPause.grid(row=1, column=7, sticky="w")
    ic_consPause = uiChance(tab1)
    ic_consPause.main.grid(row=1, column=8)

    tr_crossFd = Label(tab1, text="Crossfade length: ")
    tr_crossFd.grid(row=2, column=0, columnspan=2, sticky="w")
    ir_crossFd = uiRandom(tab1)
    ir_crossFd.main.grid(row=2, column=2)
    tc_crossFd = Label(tab1, text="Crossfade chance: ")
    tc_crossFd.grid(row=2, column=4, sticky="w")
    ic_crossFd = uiChance(tab1)
    ic_crossFd.main.grid(row=2, column=5)

    tr_fadeIn = Label(tab1, text="Fade-in length: ")
    tr_fadeIn.grid(row=3, column=0, sticky="w")
    ib_fadeInPerc = uiCheckbox(tab1, "%")
    ib_fadeInPerc.main.grid(row=3, column=1)
    ir_fadeIn = uiRandom(tab1)
    ir_fadeIn.main.grid(row=3, column=2)
    tc_fadeIn = Label(tab1, text="Fade-in chance: ")
    tc_fadeIn.grid(row=3, column=4, sticky="w")
    ic_fadeIn = uiChance(tab1)
    ic_fadeIn.main.grid(row=3, column=5)
    tc_fadeOnlyIntoPauses = Label(tab1, text="Fade only into pauses (chance): ")
    tc_fadeOnlyIntoPauses.grid(row=3, column=7, sticky="w")
    ic_fadeOnlyIntoPauses = uiChance(tab1)
    ic_fadeOnlyIntoPauses.main.grid(row=3, column=8)

    tr_fadeOut = Label(tab1, text="Fade-out length: ")
    tr_fadeOut.grid(row=4, column=0, sticky="w")
    ib_fadeOutPerc = uiCheckbox(tab1, "%")
    ib_fadeOutPerc.main.configure(command=lambda: cfgUpdate())
    ib_fadeOutPerc.main.grid(row=4, column=1)
    ir_fadeOut = uiRandom(tab1)
    ir_fadeOut.main.grid(row=4, column=2)
    tc_fadeOut = Label(tab1, text="Fade-out chance: ")
    tc_fadeOut.grid(row=4, column=4, sticky="w")
    ic_fadeOut = uiChance(tab1)
    ic_fadeOut.main.grid(row=4, column=5)
    ib_fadeOutPercNote = uiCheckbox(tab1, "Measure fade-out from last note")
    ib_fadeOutPercNote.main.grid(row=4, column=7, columnspan=2, sticky="w")

    tr_repeat = Label(tab1, text="Repeat segment ... times: ")
    tr_repeat.grid(row=5, column=0, columnspan=2, sticky="w")
    ir_repeat = uiRandom(tab1)
    ir_repeat.main.grid(row=5, column=2)
    tc_repeat = Label(tab1, text="Repeat chance: ")
    tc_repeat.grid(row=5, column=4, sticky="w")
    ic_repeat = uiChance(tab1)
    ic_repeat.main.grid(row=5, column=5)
    ib_repeatInMss = uiCheckbox(tab1, "Measure repeats in ms/sec")
    ib_repeatInMss.main.configure(command=lambda: cfgUpdate())
    ib_repeatInMss.main.grid(row=5, column=7, columnspan=2, sticky="w")

    tr_rememb = Label(tab1, text="Reappear after ... segments: ")
    tr_rememb.grid(row=6, column=0, columnspan=2, sticky="w")
    ir_rememb = uiRandom(tab1)
    ir_rememb.main.grid(row=6, column=2)
    tc_rememb = Label(tab1, text="Reappearance chance: ")
    tc_rememb.grid(row=6, column=4, sticky="w")
    ic_rememb = uiChance(tab1)
    ic_rememb.main.grid(row=6, column=5)

    lf_avgstrt = LabelFrame(tab1, text="Average start times", padding=2)
    lf_avgstrt.grid(row=7, column=0, columnspan=9)
    Label(lf_avgstrt).grid(row=0, column=2)
    t_avgstrtTimes = Label(lf_avgstrt, text="Start times: ")
    t_avgstrtTimes.grid(row=0, column=0, sticky="w")
    i_avgstrtTimes = Entry(lf_avgstrt, width=82)
    i_avgstrtTimes.grid(row=0, column=1)
    t_avgstrtDev = Label(lf_avgstrt, text="Deviation: ")
    t_avgstrtDev.grid(row=0, column=3, sticky="w")
    i_avgstrtDev = Entry(lf_avgstrt, width=6)
    i_avgstrtDev.grid(row=0, column=4, sticky="w", padx=1)
    t_avgstrtWeights = Label(lf_avgstrt, text="Start time weights: ")
    t_avgstrtWeights.grid(row=1, column=0, sticky="w")
    i_avgstrtWeights = Entry(lf_avgstrt, width=82)
    i_avgstrtWeights.grid(row=1, column=1)
    t_avgstrtChance = Label(lf_avgstrt, text="Chance: ")
    t_avgstrtChance.grid(row=1, column=3, sticky="w")
    i_avgstrtChance = uiChance(lf_avgstrt, width=6)
    i_avgstrtChance.main.grid(row=1, column=4)

    lf_speed = LabelFrame(tab1, text="Speed change", padding=2)
    lf_speed.grid(row=8, column=0, columnspan=9)
    t_speeds = Label(lf_speed, text="Speed variations: ")
    t_speeds.grid(row=0, column=0, sticky="w")
    i_speeds = Entry(lf_speed, width=83)
    i_speeds.grid(row=0, column=1, pady=1)
    x_speedm = Combobox(lf_speed, width=16, values=modes_speed, state="readonly")
    x_speedm.grid(row=0, column=2, sticky="e")
    t_speedw = Label(lf_speed, text="Variation weights: ")
    t_speedw.grid(row=1, column=0, sticky="w")
    i_speedw = Entry(lf_speed, width=103)
    i_speedw.grid(row=1, column=1, columnspan=2)

    # Advanced tab 1
    lf_backmask = LabelFrame(tab2, text="Backmasking", padding=2)
    lf_backmask.grid(row=0, column=0)
    Label(lf_backmask).grid(row=0, column=2)
    t_backmaskCrossfd = Label(lf_backmask, text="Crossfade: ")
    t_backmaskCrossfd.grid(row=0, column=0, sticky="w")
    i_backmaskCrossfd = Entry(lf_backmask, width=4)
    i_backmaskCrossfd.grid(row=0, column=1, sticky="w", pady=1, padx=1)
    t_backmaskChance = Label(lf_backmask, text="Backmask chance (general): ")
    t_backmaskChance.grid(row=1, column=0, sticky="w")
    i_backmaskChance = uiChance(lf_backmask)
    i_backmaskChance.main.grid(row=1, column=1)
    t_backmaskRevChance = Label(lf_backmask, text="Reverse backmask chance: ")
    t_backmaskRevChance.grid(row=2, column=0, sticky="w")
    i_backmaskRevChance = uiChance(lf_backmask)
    i_backmaskRevChance.main.grid(row=2, column=1)
    t_backmaskFullChance = Label(lf_backmask, text="Full backmask chance: ")
    t_backmaskFullChance.grid(row=3, column=0, sticky="w")
    i_backmaskFullChance = uiChance(lf_backmask)
    i_backmaskFullChance.main.grid(row=3, column=1)
    t_backmaskAsymChance = Label(lf_backmask, text="Asymmetrical backmask chance: ")
    t_backmaskAsymChance.grid(row=4, column=0, sticky="w")
    i_backmaskAsymChance = uiChance(lf_backmask)
    i_backmaskAsymChance.main.grid(row=4, column=1)
    t_backmaskAsymPortion = Label(lf_backmask, text="Portion: ")
    t_backmaskAsymPortion.grid(row=4, column=3, sticky="w")
    i_backmaskAsymPortion = uiRandom(lf_backmask, noLognorm=True)
    i_backmaskAsymPortion.main.grid(row=4, column=4)
    t_bmaskRepeatChance = Label(lf_backmask, text="Backmask repeat chance: ")
    t_bmaskRepeatChance.grid(row=5, column=0, sticky="w")
    i_bmaskRepeatChance = uiChance(lf_backmask)
    i_bmaskRepeatChance.main.grid(row=5, column=1)
    t_bmaskRepeatNum = Label(lf_backmask, text="Repeats: ")
    t_bmaskRepeatNum.grid(row=5, column=3, sticky="w")
    i_bmaskRepeatNum = uiRandom(lf_backmask)
    i_bmaskRepeatNum.main.grid(row=5, column=4)
    b_bmaskRepeatInMss = uiCheckbox(lf_backmask, "Measure repeats in ms/sec")
    b_bmaskRepeatInMss.main.grid(row=7, column=3, columnspan=2, sticky="w")

    lf_extnote = LabelFrame(tab2, text="Note extension", padding=2)
    lf_extnote.grid(row=1, column=0, sticky="w")
    Label(lf_extnote).grid(row=0, column=2)
    t_extnoteChance = Label(lf_extnote, text="Note extension chance: ")
    t_extnoteChance.grid(row=0, column=0, sticky="w")
    i_extnoteChance = uiChance(lf_extnote)
    i_extnoteChance.main.grid(row=0, column=1)
    b_extnotePriority = uiCheckbox(lf_extnote, "Priority over usual backmask")
    b_extnotePriority.main.grid(row=0, column=3, columnspan=2, sticky="w")
    t_extnoteUseAltPortion = Label(lf_extnote, text="Unequal portion chance: ")
    t_extnoteUseAltPortion.grid(row=1, column=0, sticky="w")
    i_extnoteUseAltPortion = uiChance(lf_extnote)
    i_extnoteUseAltPortion.main.grid(row=1, column=1)
    t_extnoteAltPortion = Label(lf_extnote, text="Fade-out portion: ")
    t_extnoteAltPortion.grid(row=1, column=3, sticky="w")
    i_extnoteAltPortion = uiRandom(lf_extnote, ent_w=5, noLognorm=True)
    i_extnoteAltPortion.main.grid(row=1, column=4)
    b_extnoteAltFadeOut = uiCheckbox(lf_extnote, "Alternate fade-out instead")
    b_extnoteAltFadeOut.main.grid(row=2, column=4)
    t_extnoteMinNoteLen = Label(lf_extnote, text="Minimum note length: ")
    t_extnoteMinNoteLen.grid(row=2, column=0, sticky="w")
    i_extnoteMinNoteLen = Entry(lf_extnote, width=4)
    i_extnoteMinNoteLen.grid(row=2, column=1, sticky="w", padx=1)
    t_extnoteCrossfd = Label(lf_extnote, text="Crossfade: ")
    t_extnoteCrossfd.grid(row=3, column=0, sticky="w")
    i_extnoteCrossfd = Entry(lf_extnote, width=4)
    i_extnoteCrossfd.grid(row=3, column=1, sticky="w", padx=1, pady=1)

    lf_quantize = LabelFrame(tab2, text="Quantization", padding=2)
    lf_quantize.grid(row=0, column=1, rowspan=2, padx=10, sticky="n")
    t_quanMode = Label(lf_quantize, text="Mode: ")
    t_quanMode.grid(row=0, column=0, sticky="w")
    x_quanMode = Combobox(lf_quantize, width=7, values=modes_quan, state="readonly")
    x_quanMode.bind("<<ComboboxSelected>>", lambda event: cfgUpdate())
    x_quanMode.grid(row=0, column=1, sticky="e")
    t_quanBPM = Label(lf_quantize, text="BPM: ")
    t_quanBPM.grid(row=1, column=0, sticky="w")
    i_quanBPM = Entry(lf_quantize, width=7)
    i_quanBPM.grid(row=1, column=1, sticky="e", pady=1)
    lf_quanChances = LabelFrame(lf_quantize, text="Chances", padding=2)
    lf_quanChances.grid(row=2, column=0, columnspan=2)
    Label(lf_quanChances).grid(row=0, column=2)
    t_quanAvgStart = Label(lf_quanChances, text="Average start times: ")
    t_quanAvgStart.grid(row=0, column=0, sticky="w")
    i_quanAvgStart = uiChance(lf_quanChances)
    i_quanAvgStart.main.grid(row=0, column=1)
    x_quanAvgStartDir = Combobox(lf_quanChances, width=7, values=modes_quan_dir[1:], state="readonly")
    x_quanAvgStartDir.grid(row=0, column=3)
    t_quanStumbBegin = Label(lf_quanChances, text="Stumbling start: ")
    t_quanStumbBegin.grid(row=1, column=0, sticky="w")
    i_quanStumbBegin = uiChance(lf_quanChances)
    i_quanStumbBegin.main.grid(row=1, column=1)
    x_quanStumbBeginDir = Combobox(lf_quanChances, width=7, values=modes_quan_dir[1:-1], state="readonly")
    x_quanStumbBeginDir.grid(row=1, column=3)
    t_quanStumbleSkip = Label(lf_quanChances, text="Stumbling skip: ")
    t_quanStumbleSkip.grid(row=2, column=0, sticky="w")
    i_quanStumbleSkip = uiChance(lf_quanChances)
    i_quanStumbleSkip.main.grid(row=2, column=1)
    x_quanStumbleSkipDir = Combobox(lf_quanChances, width=7, values=modes_quan_dir[1:], state="readonly")
    x_quanStumbleSkipDir.grid(row=2, column=3)
    t_quanBegin = Label(lf_quanChances, text="Segment begin: ")
    t_quanBegin.grid(row=3, column=0, sticky="w")
    i_quanBegin = uiChance(lf_quanChances)
    i_quanBegin.main.grid(row=3, column=1)
    x_quanBeginDir = Combobox(lf_quanChances, width=7, values=modes_quan_dir[:-1], state="readonly")
    x_quanBeginDir.grid(row=3, column=3)
    t_quanDuration = Label(lf_quanChances, text="Segment duration: ")
    t_quanDuration.grid(row=4, column=0, sticky="w")
    i_quanDuration = uiChance(lf_quanChances)
    i_quanDuration.main.grid(row=4, column=1)
    x_quanDurationDir = Combobox(lf_quanChances, width=7, values=modes_quan_dir[1:-1], state="readonly")
    x_quanDurationDir.grid(row=4, column=3)
    t_quanUseStOnsets = Label(lf_quanChances, text="Use start onsets: ")
    t_quanUseStOnsets.grid(row=5, column=0, sticky="w")
    i_quanUseStOnsets = uiChance(lf_quanChances)
    i_quanUseStOnsets.main.grid(row=5, column=1)
    x_quanUseStOnsetsDir = Combobox(lf_quanChances, width=7, values=modes_quan_dir[:-1], state="readonly")
    x_quanUseStOnsetsDir.grid(row=5, column=3)
    t_onsman = Button(lf_quantize, text="Manage onsets", command=lambda: abOnsetsWindow())
    t_onsman.grid(row=3, column=0, columnspan=2)

    # Advanced tab 2
    lf_stumbling = LabelFrame(tab3, text="Stumbling", padding=2)
    lf_stumbling.grid(row=0, column=0, sticky="n")
    lf_stumbChances = LabelFrame(lf_stumbling, text="Chances", padding=2)
    lf_stumbChances.pack(side="top", fill="x")
    t_stumbleChance = Label(lf_stumbChances, text="Stumble chance: ")
    t_stumbleChance.grid(row=0, column=0, sticky="w")
    i_stumbleChance = uiChance(lf_stumbChances)
    i_stumbleChance.main.grid(row=0, column=1)
    b_stumbleLockedMode = uiCheckbox(lf_stumbChances, text="Locked")
    b_stumbleLockedMode.main.grid(row=0, column=2, padx=3)
    t_stumbleOnlyStumbled = Label(lf_stumbChances, text="Count only stumbled: ")
    t_stumbleOnlyStumbled.grid(row=1, column=0, sticky="w")
    i_stumbleOnlyStumbled = uiChance(lf_stumbChances)
    i_stumbleOnlyStumbled.main.grid(row=1, column=1)
    t_stumbleIgnoreAvgSt = Label(lf_stumbChances, text="Ignore average start times: ")
    t_stumbleIgnoreAvgSt.grid(row=2, column=0, sticky="w")
    i_stumbleIgnoreAvgSt = uiChance(lf_stumbChances)
    i_stumbleIgnoreAvgSt.main.grid(row=2, column=1)
    t_stumbleCountPauses = Label(lf_stumbChances, text="Count pauses: ")
    t_stumbleCountPauses.grid(row=3, column=0, sticky="w")
    i_stumbleCountPauses = uiChance(lf_stumbChances)
    i_stumbleCountPauses.main.grid(row=3, column=1)
    t_stumbleCountMuted = Label(lf_stumbChances, text="Count muted segments*: ")
    t_stumbleCountMuted.grid(row=4, column=0, sticky="w")
    i_stumbleCountMuted = uiChance(lf_stumbChances)
    i_stumbleCountMuted.main.grid(row=4, column=1)

    lf_stumbSkip = LabelFrame(lf_stumbling, text="Skipping", padding=2)
    lf_stumbSkip.pack(side="bottom")
    t_skipChance = Label(lf_stumbSkip, text="Skip chance: ")
    t_skipChance.grid(row=0, column=0, sticky="w")
    i_skipChance = uiChance(lf_stumbSkip)
    i_skipChance.main.grid(row=0, column=1, sticky="e")
    x_skipDirections = Notebook(lf_stumbSkip)
    x_skipDirections.grid(row=1, column=0, columnspan=2)

    f_stumbSkipForw = Frame(lf_stumbSkip, padding=1)
    x_skipDirections.add(f_stumbSkipForw, text="Forwards")
    Label(f_stumbSkipForw).grid(row=0, column=2)
    t_skipForwWeight = Label(f_stumbSkipForw, text="Direction weight: ")
    t_skipForwWeight.grid(row=0, column=0, sticky="w", pady=2)
    i_skipForwWeight = Entry(f_stumbSkipForw, width=6)
    i_skipForwWeight.grid(row=0, column=1, sticky="w")
    t_skipForwMin = Label(f_stumbSkipForw, text="Minimum skip: ")
    t_skipForwMin.grid(row=1, column=0, sticky="w")
    i_skipForwMin = Entry(f_stumbSkipForw, width=6)
    i_skipForwMin.grid(row=1, column=1, sticky="w")
    t_skipForwMinChance = Label(f_stumbSkipForw, text="Chance: ")
    t_skipForwMinChance.grid(row=1, column=3, sticky="w")
    i_skipForwMinChance = uiChance(f_stumbSkipForw)
    i_skipForwMinChance.main.grid(row=1, column=4)
    t_skipForwAddDev = Label(f_stumbSkipForw, text="Additional deviation: ")
    t_skipForwAddDev.grid(row=2, column=0, sticky="w")
    i_skipForwAddDev = Entry(f_stumbSkipForw, width=6)
    i_skipForwAddDev.grid(row=2, column=1, sticky="w")
    t_skipForwAddDevChance = Label(f_stumbSkipForw, text="Chance: ")
    t_skipForwAddDevChance.grid(row=2, column=3, sticky="w")
    i_skipForwAddDevChance = uiChance(f_stumbSkipForw)
    i_skipForwAddDevChance.main.grid(row=2, column=4)

    f_stumbSkipBack = Frame(lf_stumbSkip, padding=1)
    x_skipDirections.add(f_stumbSkipBack, text="Backwards")
    Label(f_stumbSkipBack).grid(row=0, column=2)
    t_skipBackWeight = Label(f_stumbSkipBack, text="Direction weight: ")
    t_skipBackWeight.grid(row=0, column=0, sticky="w", pady=2)
    i_skipBackWeight = Entry(f_stumbSkipBack, width=6)
    i_skipBackWeight.grid(row=0, column=1, sticky="w")
    t_skipBackMin = Label(f_stumbSkipBack, text="Minimum skip: ")
    t_skipBackMin.grid(row=1, column=0, sticky="w")
    i_skipBackMin = Entry(f_stumbSkipBack, width=6)
    i_skipBackMin.grid(row=1, column=1, sticky="w")
    t_skipBackMinChance = Label(f_stumbSkipBack, text="Chance: ")
    t_skipBackMinChance.grid(row=1, column=3, sticky="w")
    i_skipBackMinChance = uiChance(f_stumbSkipBack)
    i_skipBackMinChance.main.grid(row=1, column=4)
    t_skipBackAddDev = Label(f_stumbSkipBack, text="Additional deviation: ")
    t_skipBackAddDev.grid(row=2, column=0, sticky="w")
    i_skipBackAddDev = Entry(f_stumbSkipBack, width=6)
    i_skipBackAddDev.grid(row=2, column=1, sticky="w")
    t_skipBackAddDevChance = Label(f_stumbSkipBack, text="Chance: ")
    t_skipBackAddDevChance.grid(row=2, column=3, sticky="w")
    i_skipBackAddDevChance = uiChance(f_stumbSkipBack)
    i_skipBackAddDevChance.main.grid(row=2, column=4)

    f_stumbskipRand = Frame(lf_stumbSkip, padding=1)
    x_skipDirections.add(f_stumbskipRand, text="Random")
    Label(f_stumbskipRand).grid(row=0, column=2)
    t_skipRandWeight = Label(f_stumbskipRand, text="Direction weight: ")
    t_skipRandWeight.grid(row=0, column=0, sticky="w", pady=2)
    i_skipRandWeight = Entry(f_stumbskipRand, width=6)
    i_skipRandWeight.grid(row=0, column=1, sticky="w")
    t_skipRandMin = Label(f_stumbskipRand, text="Minimum skip: ")
    t_skipRandMin.grid(row=1, column=0, sticky="w")
    i_skipRandMin = Entry(f_stumbskipRand, width=6)
    i_skipRandMin.grid(row=1, column=1, sticky="w")
    t_skipRandMinChance = Label(f_stumbskipRand, text="Chance: ")
    t_skipRandMinChance.grid(row=1, column=3, sticky="w")
    i_skipRandMinChance = uiChance(f_stumbskipRand)
    i_skipRandMinChance.main.grid(row=1, column=4)
    t_skipRandAddDev = Label(f_stumbskipRand, text="Additional deviation: ")
    t_skipRandAddDev.grid(row=2, column=0, sticky="w")
    i_skipRandAddDev = Entry(f_stumbskipRand, width=6)
    i_skipRandAddDev.grid(row=2, column=1, sticky="w")
    t_skipRandAddDevChance = Label(f_stumbskipRand, text="Chance: ")
    t_skipRandAddDevChance.grid(row=2, column=3, sticky="w")
    i_skipRandAddDevChance = uiChance(f_stumbskipRand)
    i_skipRandAddDevChance.main.grid(row=2, column=4)

    lf_looping = LabelFrame(tab3, text="Looping", padding=2)
    lf_looping.grid(row=0, column=1, padx=10, sticky="nw")
    f_loopingMain = Frame(lf_looping)
    f_loopingMain.pack(side="top", fill="x")
    b_looping = uiCheckbox(f_loopingMain, "Loop length: ")
    b_looping.main.configure(command=lambda: cfgUpdate())
    b_looping.main.grid(row=0, column=0, sticky="w")
    i_loopDuration = Entry(f_loopingMain, width=7)
    i_loopDuration.grid(row=0, column=1, sticky="e", padx=1, pady=1)
    b_loopStrictly = uiCheckbox(f_loopingMain, "Strictly")
    b_loopStrictly.main.grid(row=0, column=3, sticky="w", padx=5)
    t_loopVarNumber = Label(f_loopingMain, text="Variations number: ")
    t_loopVarNumber.grid(row=1, column=0, sticky="w")
    i_loopVarNumber = Entry(f_loopingMain, width=7)
    i_loopVarNumber.grid(row=1, column=1, sticky="e", padx=1)
    b_loopKeepSize = uiCheckbox(f_loopingMain, "Keep segment size")
    b_loopKeepSize.main.configure(command=lambda: cfgUpdate())
    b_loopKeepSize.main.grid(row=1, column=3, sticky="w", padx=5)
    t_loopFillWithSilence = Label(f_loopingMain, text="Complete with silence: ")
    t_loopFillWithSilence.grid(row=2, column=0, sticky="w")
    i_loopFillWithSilence = uiChance(f_loopingMain)
    i_loopFillWithSilence.main.grid(row=2, column=1, sticky="w")
    
    lf_loopAlt = LabelFrame(lf_looping, text="Alternation chances", padding=2)
    lf_loopAlt.pack(side="bottom")
    Label(lf_loopAlt).grid(row=0, column=2)
    t_loopAltSpeed = Label(lf_loopAlt, text="Speed: ")
    t_loopAltSpeed.grid(row=0, column=0, sticky="w")
    i_loopAltSpeed = uiChance(lf_loopAlt)
    i_loopAltSpeed.main.grid(row=0, column=1)
    t_loopAltSource = Label(lf_loopAlt, text="Begin source: ")
    t_loopAltSource.grid(row=1, column=0, sticky="w")
    i_loopAltSource = uiChance(lf_loopAlt)
    i_loopAltSource.main.grid(row=1, column=1)
    t_loopAltBegin = Label(lf_loopAlt, text="Segment begin: ")
    t_loopAltBegin.grid(row=2, column=0, sticky="w")
    i_loopAltBegin = uiChance(lf_loopAlt)
    i_loopAltBegin.main.grid(row=2, column=1)
    t_loopAltRandBegin = Label(lf_loopAlt, text="Random start time: ")
    t_loopAltRandBegin.grid(row=3, column=0, sticky="w")
    i_loopAltRandBegin = uiChance(lf_loopAlt)
    i_loopAltRandBegin.main.grid(row=3, column=1)
    t_loopAltAvgBegin = Label(lf_loopAlt, text="Average start time: ")
    t_loopAltAvgBegin.grid(row=4, column=0, sticky="w")
    i_loopAltAvgBegin = uiChance(lf_loopAlt)
    i_loopAltAvgBegin.main.grid(row=4, column=1)
    t_loopAltStumBegin = Label(lf_loopAlt, text="Stumbling: ")
    t_loopAltStumBegin.grid(row=5, column=0, sticky="w")
    i_loopAltStumBegin = uiChance(lf_loopAlt)
    i_loopAltStumBegin.main.grid(row=5, column=1)
    t_loopAltDuration = Label(lf_loopAlt, text="Segment duration: ")
    t_loopAltDuration.grid(row=6, column=0, sticky="w")
    i_loopAltDuration = uiChance(lf_loopAlt)
    i_loopAltDuration.main.grid(row=6, column=1)
    t_loopAltReQnDur = Label(lf_loopAlt, text="Re-quantize duration: ")
    t_loopAltReQnDur.grid(row=7, column=0, sticky="w")
    i_loopAltReQnDur = uiChance(lf_loopAlt)
    i_loopAltReQnDur.main.grid(row=7, column=1)
    t_loopAltRev1 = Label(lf_loopAlt, text="First reverse: ")
    t_loopAltRev1.grid(row=0, column=3, sticky="w")
    i_loopAltRev1 = uiChance(lf_loopAlt)
    i_loopAltRev1.main.grid(row=0, column=4)
    t_loopAltRev2 = Label(lf_loopAlt, text="Second reverse: ")
    t_loopAltRev2.grid(row=1, column=3, sticky="w")
    i_loopAltRev2 = uiChance(lf_loopAlt)
    i_loopAltRev2.main.grid(row=1, column=4)
    t_loopAltRepeats = Label(lf_loopAlt, text="Repeats: ")
    t_loopAltRepeats.grid(row=2, column=3, sticky="w")
    i_loopAltRepeats = uiChance(lf_loopAlt)
    i_loopAltRepeats.main.grid(row=2, column=4)
    t_loopAltBmask = Label(lf_loopAlt, text="Backmask: ")
    t_loopAltBmask.grid(row=3, column=3, sticky="w")
    i_loopAltBmask = uiChance(lf_loopAlt)
    i_loopAltBmask.main.grid(row=3, column=4)
    t_loopAltBmRep = Label(lf_loopAlt, text="Backmask repeats: ")
    t_loopAltBmRep.grid(row=4, column=3, sticky="w")
    i_loopAltBmRep = uiChance(lf_loopAlt)
    i_loopAltBmRep.main.grid(row=4, column=4)
    t_loopAltFadeIn = Label(lf_loopAlt, text="Fade-in: ")
    t_loopAltFadeIn.grid(row=5, column=3, sticky="w")
    i_loopAltFadeIn = uiChance(lf_loopAlt)
    i_loopAltFadeIn.main.grid(row=5, column=4)
    t_loopAltFadeOut = Label(lf_loopAlt, text="Fade-out: ")
    t_loopAltFadeOut.grid(row=6, column=3, sticky="w")
    i_loopAltFadeOut = uiChance(lf_loopAlt)
    i_loopAltFadeOut.main.grid(row=6, column=4)
    t_loopAltNoteExt = Label(lf_loopAlt, text="Note extension: ")
    t_loopAltNoteExt.grid(row=7, column=3, sticky="w")
    i_loopAltNoteExt = uiChance(lf_loopAlt)
    i_loopAltNoteExt.main.grid(row=7, column=4)

    # Advanced tab 3
    lf_fadeCutoff = LabelFrame(tab4, text="Fade cutoff (%)", padding=2)
    lf_fadeCutoff.grid(row=0, column=0, sticky="w")
    Label(lf_fadeCutoff).grid(row=0, column=2)
    tr_fadeInCut = Label(lf_fadeCutoff, text="Fade-in: ")
    tr_fadeInCut.grid(row=0, column=0, sticky="w")
    ir_fadeInCut = uiRandom(lf_fadeCutoff, noLognorm=True)
    ir_fadeInCut.main.grid(row=0, column=1)
    tc_fadeInCut = Label(lf_fadeCutoff, text="Chance: ")
    tc_fadeInCut.grid(row=0, column=3)
    ic_fadeInCut = uiChance(lf_fadeCutoff)
    ic_fadeInCut.main.grid(row=0, column=4)
    tr_fadeOutCut = Label(lf_fadeCutoff, text="Fade-out: ")
    tr_fadeOutCut.grid(row=1, column=0, sticky="w")
    ir_fadeOutCut = uiRandom(lf_fadeCutoff, noLognorm=True)
    ir_fadeOutCut.main.grid(row=1, column=1)
    tc_fadeOutCut = Label(lf_fadeCutoff, text="Chance: ")
    tc_fadeOutCut.grid(row=1, column=3)
    ic_fadeOutCut = uiChance(lf_fadeCutoff)
    ic_fadeOutCut.main.grid(row=1, column=4)

    lf_consec = LabelFrame(tab4, text="Consecutives", padding=2)
    lf_consec.grid(row=1, column=0, sticky="w")
    Label(lf_consec).grid(row=0, column=1)
    b_consecPauseFirst = uiCheckbox(lf_consec, "Pre-paused")
    b_consecPauseFirst.main.grid(row=0, column=0, sticky="w")
    b_consecRepeatFirst = uiCheckbox(lf_consec, "Pre-repeated")
    b_consecRepeatFirst.main.grid(row=1, column=0, sticky="w")
    t_consecRepeatChance = Label(lf_consec, text="Consecutive repeat chance: ")
    t_consecRepeatChance.grid(row=1, column=2, sticky="w")
    i_consecRepeatChance = uiChance(lf_consec)
    i_consecRepeatChance.main.grid(row=1, column=3)
    b_consecBmaskFirst = uiCheckbox(lf_consec, "Pre-backmasked")
    b_consecBmaskFirst.main.grid(row=2, column=0, sticky="w")
    t_consecBmaskChance = Label(lf_consec, text="Consecutive backmask chance: ")
    t_consecBmaskChance.grid(row=2, column=2, sticky="w")
    i_consecBmaskChance = uiChance(lf_consec)
    i_consecBmaskChance.main.grid(row=2, column=3)
    b_consecMutedFirst = uiCheckbox(lf_consec, "Pre-muted")
    b_consecMutedFirst.main.grid(row=3, column=0, sticky="w")
    t_consecMutedChance = Label(lf_consec, text="Consecutive mute chance: ")
    t_consecMutedChance.grid(row=3, column=2, sticky="w")
    i_consecMutedChance = uiChance(lf_consec)
    i_consecMutedChance.main.grid(row=3, column=3)

    lf_trim = LabelFrame(tab4, text="Trim", padding=2)
    lf_trim.grid(row=2, column=0, sticky="w")
    b_trim = uiCheckbox(lf_trim, "Trim audio file")
    b_trim.main.configure(command=lambda: cfgUpdate())
    b_trim.main.grid(row=0, column=0, columnspan=2, sticky="w")
    t_trimVal1 = Label(lf_trim, text="From: ")
    t_trimVal1.grid(row=1, column=0, sticky="w")
    i_trimVal1 = Entry(lf_trim, width=7)
    i_trimVal1.grid(row=1, column=1, sticky="e", pady=1)
    t_trimVal2 = Label(lf_trim, text="To: ")
    t_trimVal2.grid(row=2, column=0, sticky="w")
    i_trimVal2 = Entry(lf_trim, width=7)
    i_trimVal2.grid(row=2, column=1, sticky="e", pady=1)
    b_trimShiftOns = uiCheckbox(lf_trim, "Shift onset times")
    b_trimShiftOns.main.grid(row=3, column=0, columnspan=2, sticky="w")

    lf_misc = LabelFrame(tab4, text="Miscellaneous", padding=2)
    lf_misc.grid(row=0, column=1, rowspan=3, padx=10, sticky="wn")
    t_stumbPrior = Label(lf_misc, text="Stumbling priority over\naverage start times (chance): ")
    t_stumbPrior.grid(row=0, column=0, sticky="w")
    i_stumbPrior = uiChance(lf_misc)
    i_stumbPrior.main.grid(row=0, column=1, sticky="e")
    t_muteChance = Label(lf_misc, text="Mute segment (chance): ")
    t_muteChance.grid(row=1, column=0, sticky="w")
    i_muteChance = uiChance(lf_misc)
    i_muteChance.main.grid(row=1, column=1, sticky="e")
    t_muteToPauseChance = Label(lf_misc, text="Resize muted segment\nto pause length (chance): ")
    t_muteToPauseChance.grid(row=2, column=0, sticky="w")
    i_muteToPauseChance = uiChance(lf_misc)
    i_muteToPauseChance.main.grid(row=2, column=1, sticky="e")
    b_muteCountPauses = uiCheckbox(lf_misc, "Count pauses as muted segments")
    b_muteCountPauses.main.grid(row=3, column=0, columnspan=2, sticky="w")

    # Bottom
    bottom = Frame(root); bottom.pack(side="top", fill="x", expand=False)
    bottom_l1 = Frame(bottom, padding=2); bottom_l1.pack(side="top", fill="x", expand=True)
    bottom_l2 = Frame(bottom); bottom_l2.pack(side="bottom", fill="x", expand=True)

    b_convert2sec = uiCheckbox(bottom_l1, text="Use seconds")
    b_convert2sec.main.configure(command=lambda: cfgConvTime())
    b_convert2sec.main.pack(side="left")
    b_fromseed = uiCheckbox(bottom_l1, text="Generate from seed: ")
    b_fromseed.main.configure(command=lambda: cfgUpdate())
    i_seed = Entry(bottom_l1, width=16)
    i_seed.pack(side="right")
    b_fromseed.main.pack(side="right")

    progressbar = Progressbar(bottom_l2, orient="horizontal")
    progressbar.pack(side="left", fill="x", padx=1, expand=True)
    abort = Button(bottom_l2, text="Abort", state="disabled", command=lambda: usrAbortUpdate())
    abort.pack(side="right", fill="x")

    # Misc
    usrUpdWindowTitle()
    usrUpdFormats(True)
    applyWindowStyle(root)
    cfgImport(data=abPresets["Default"])

    if len(sys.argv)>=2: dndAnalyzeFile(sys.argv[1])
    root.protocol('WM_DELETE_WINDOW', usrQuit)
    root.mainloop()
