# Most of this code was transferred from AB 3.1
from preset import PresetOpen
from convert_ab3 import convert_ab3


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


class cfgQuickGet:
    def __init__(self, config, ident):
        self.config = config
        self.ident  = ident
    def get(self, variable, fallback):
        return self.config.get(self.ident, variable, fallback=fallback)


class cfgAB2StringWorks:
    @staticmethod
    def m2d(meth): # AB2 random mode -> AB3 random mode
        try:
            return [0, 1, 1, 2][int(meth)]
        except Exception:
            return -1

    @staticmethod
    def try2flt(a): # Try converting string to float
        try: return float(a)
        except Exception: return 0

    @classmethod
    def mulsp(sw, a, b, opposite): # Multiply two strings
        a = sw.try2flt(a)
        b = sw.try2flt(b)
        if opposite: b = 100 - b
        return round(a * b / 100, 1)

    @classmethod
    def w2p(sw, weight, weights): # Weight to percent chance
        try:
            summ = sw.strsum(weights)
            return round(int(weight) / summ * 100, 1)
        except Exception:
            return 0

    @staticmethod
    def strsum(strs): # Summ of integer strings
        summ = 0
        for s in strs:
            try: summ += int(s)
            except Exception: pass
        return summ


def convert_main(preset):
    g = cfgQuickGet(preset, "AudioButcher")
    version = g.get("version", "2.1.0")

    # Get parameters
    minSize = g.get("minSize", "0")
    maxSize = g.get("maxSize", "0")
    methDur = g.get("methDur", "0")
    reverseChance = g.get("reverseChance", "0")
    minPL = g.get("minPL", "0")
    maxPL = g.get("maxPL", "0")
    methPause = g.get("methPause", "0")
    stopChance = g.get("stopChance", "0")
    conspause = g.get("conspause", "0")
    propfadein = g.get("propfadein", "0")
    minFadeIn = g.get("minFadeIn", "0")
    maxFadeIn = g.get("maxFadeIn", "0")
    methFdIn = g.get("methFdIn", "0")
    fadeInChance = g.get("fadeInChance", "100")
    propfadeout = g.get("propfadeout", "0")
    minFadeOut = g.get("minFadeOut", "0")
    maxFadeOut = g.get("maxFadeOut", "0")
    methFdOut = g.get("methFdOut", "0")
    fadeOutChance = g.get("fadeOutChance", "100")
    fdprior = g.get("fdprior", "0")
    faderestrict = g.get("faderestrict", "0")
    mincrossfade = g.get("mincrossfade", "0")
    maxcrossfade = g.get("maxcrossfade", "0")
    methCrsfd = g.get("methCrsfd", "0")
    crossfadechance = g.get("crossfadechance", "100")
    repeatMin = g.get("repeatMin", "0")
    repeatMax = g.get("repeatMax", "0")
    methrep = g.get("methrep", "0")
    repeatchance = g.get("repeatchance", "0")
    consrep = g.get("consrep", "0")
    minsegs = g.get("minsegs", "0")
    maxsegs = g.get("maxsegs", "0")
    remembertype = g.get("remembertype", "0")
    rememberchance = g.get("rememberchance", "0")
    avgstrt = g.get("avgstrt", "0")
    strtdev = g.get("strtdev", "0")
    strtweights = g.get("strtweights", "")
    normStrtChance = g.get("normStrtChance", "0")
    speeds = g.get("speeds", "0")
    speedmeasure = g.get("speedmeasure", "0")
    speedweights = g.get("speedweights", "")
    TimeMeasure = g.get("TimeMeasure", "0")
    fdmode_lc = g.get("fdmode_lc", "0")
    fdmode_sf = g.get("fdmode_sf", "0")
    fdmode_en = g.get("fdmode_en", "0")
    backmaskFadeCrossfade = g.get("backmaskFadeCrossfade", "-1")
    minfdmsk = g.get("minfdmsk", "0")
    BackmaskCrossfade = g.get("BackmaskCrossfade", "0")
    BackmaskChance = g.get("BackmaskChance", "0")
    asymmetricalBackmaskChance = g.get("asymmetricalBackmaskChance", "0")
    reverseMaskChance = g.get("reverseMaskChance", "0")
    doublesize = g.get("doublesize", "0")
    consecbackmask = g.get("consecbackmask", "100")
    minMaskRepeat = g.get("minMaskRepeat", "0")
    maxMaskRepeat = g.get("maxMaskRepeat", "0")
    methrepmsk = g.get("methrepmsk", "0")
    maskmode = g.get("maskmode", "0")
    maskRepeatChance = g.get("maskRepeatChance", "0")
    fromseed = g.get("fromseed", "0")
    seed = g.get("seed", "")
    stumblechance = g.get("stumblechance", "0")
    stumbledeviation = g.get("stumbledeviation", "0")
    stumbdeviate = g.get("stumbdeviate", "100")
    methStumbleNorm = g.get("methStumbleNorm", "0")
    methStumbleForw = g.get("methStumbleForw", "0")
    methStumbleBack = g.get("methStumbleBack", "0")
    stumavgstrt = g.get("stumavgstrt", "0")
    countstumblepauses = g.get("countstumblepauses", "0")
    repmode = g.get("repmode", "0")
    notepropfd = g.get("notepropfd", "0")
    minCutFdIn = g.get("minCutFdIn", "0")
    maxCutFdIn = g.get("maxCutFdIn", "0")
    methCutFdIn = g.get("methCutFdIn", "0")
    cutFdInChance = g.get("cutFdInChance", "100")
    minCutFdOut = g.get("minCutFdOut", "0")
    maxCutFdOut = g.get("maxCutFdOut", "0")
    methCutFdOut = g.get("methCutFdOut", "0")
    cutFdOutChance = g.get("cutFdOutChance", "100")
    quantizeMode = g.get("quantizeMode", "0")
    bpm = g.get("bpm", "120")
    quanavgstrt = g.get("quanavgstrt", "100")
    quanstrt = g.get("quanstrt", "100")
    quanseglgth = g.get("quanseglgth", "100")
    usestartonsets = g.get("usestartonsets", "100")
    trimfile = g.get("trimfile", "0")
    trimmin = g.get("trimmin", "0")
    trimmax = g.get("trimmax", "0")
    shiftons = g.get("shiftons", "1")

    # Compatibility: Comp Method
    CompMethod = g.get("CompMethod", None)
    if CompMethod   == "0": fdmode_lc = "1"
    elif CompMethod == "1": fdmode_sf = "1"
    elif CompMethod == "2": fdmode_en = "1"

    # Compatibility: Stumble direction
    methStumble = g.get("methStumble", None)
    if   methStumble == "0": methStumbleNorm = "1"
    elif methStumble == "1": methStumbleForw = "1"
    elif methStumble == "2": methStumbleBack = "1"

    # Compatibility: AB 2.1
    if version=="2.1.0":
        if doublesize=="1":
            doublesize = "100"
        version = "2.1.1"

    # Compatibility: AB 2.1.1
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

    # Convert
    sw = cfgAB2StringWorks()
    tmp_stumbmode = sw.w2p(methStumbleNorm, [methStumbleNorm, methStumbleForw, methStumbleBack])

    ab2to3 = f"""[AudioButcher3]
version = 3.0.0

convert2sec = {TimeMeasure}
fromseed = {fromseed}
seed = {seed}

seg = {minSize} {maxSize} {sw.m2d(methDur)}
segReverseChance1 = {sw.mulsp(reverseChance, fdprior, True)}
segReverseChance2 = {sw.mulsp(reverseChance, fdprior, False)}
pause = {minPL} {maxPL} {sw.m2d(methPause)}
pauseChance = {stopChance}
consPauseChance = {conspause}
crossFd = {mincrossfade} {maxcrossfade} {sw.m2d(methCrsfd)}
crossFdChance = {crossfadechance}
fadeInPerc = {propfadein}
fadeIn = {minFadeIn} {maxFadeIn} {sw.m2d(methFdIn)}
fadeInChance = {fadeInChance}
fadeOnlyIntoPauses = {faderestrict}
fadeOutPerc = {propfadeout}
fadeOut = {minFadeOut} {maxFadeOut} {sw.m2d(methFdOut)}
fadeOutChance = {fadeOutChance}
fadeOutPercNote = {notepropfd}
repeat = {repeatMin} {repeatMax} {sw.m2d(methrep)}
repeatChance = {repeatchance}
repeatInMss = {repmode}
rememb = {minsegs} {maxsegs} {sw.m2d(remembertype)}
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
bmaskRepeatNum = {minMaskRepeat} {maxMaskRepeat} {sw.m2d(methrepmsk)}
bmaskRepeatInMss = {maskmode}

extnoteChance = {sw.w2p(fdmode_en, [fdmode_lc, fdmode_sf, fdmode_en])}
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

fadeInCut = {minCutFdIn} {maxCutFdIn} {sw.m2d(methCutFdIn)}
fadeInCutChance = {cutFdInChance}
fadeOutCut = {minCutFdOut} {maxCutFdOut} {sw.m2d(methCutFdOut)}
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

    return ab2to3


def convert_ab2(preset: PresetOpen):
    ab3_content = convert_main(preset.rcp)
    ab3_preset = PresetOpen(data=ab3_content)
    ab3_preset.check_ab3()

    ab4_preset = convert_ab3(ab3_preset)
    sec_name = ab4_preset.sec_name
    ab4_preset.rcp[sec_name]["quan_sustain"] = preset.get("quanmask", "100")
    ab4_preset.rcp[sec_name]["reverse_double_mode"] = "2"

    return ab4_preset
