import common
from scrambler.scr_state import ScramblerState
from scrambler.segment import SegmentInfo

DEBUG_CMD_LEVEL = 0  # Be nice and don't use ABPL in multiple places


class Error(Exception):
    pass


class Return(Exception):
    pass


class Break(Exception):
    pass


def f2b(flt):
    return bool(int(round(flt)))


def token_pos_str(position: int, tokens_by_line: list[int]):
    total = 0

    for line_num, token_count in enumerate(tokens_by_line):
        if position < total + token_count:
            token_num = position - total
            return f"{line_num}:{token_num}"
        total += token_count

    return "OUT-RANGE"


def debug(*words):
    if common.AB_ABPL_DEBUG:
        indent =  " ." * DEBUG_CMD_LEVEL
        print(f"ABPL DEBUG:{indent}", *words)


def float_x(value):
    if value is None:
        return 0.0
    return float(value)


class ScriptState:
    def __init__(self, script: list[str], tokens_by_line: list[int],
                 segment: SegmentInfo, scr_state: ScramblerState, exec_shift=0):
        self._script = script
        self._exec_shift = exec_shift
        self._position = -1
        self.tokens_by_line = tokens_by_line

        self.jumped = False
        self.loop_breaks = []
        self.loop_skips = []

        self.return_ = 0
        self.segment = segment
        self.scr_state = scr_state

        # DON'T FORGET TO SYNC THESE FOR FUNCTIONS
        self.round_samples = True
        self.functions = {}
        self.variables = {}
        self.quan_options = {}

    @property
    def position(self) -> int:
        return self._position

    @property
    def token_pos_str(self) -> str:
        return token_pos_str(self._position + self._exec_shift, self.tokens_by_line)

    @property
    def finished(self) -> bool:
        return self._position + 1 >= len(self._script)

    def error(self, text):
        error = Error(f"{self.token_pos_str}: {text}")
        raise error

    def read(self, move=True):
        if move:
            self._position += 1

        command = self._script[self._position]
        # debug("read", self.token_pos_str, command)
        return command

    def set_pos(self, position):
        self._position = position
        debug("jump to", self.token_pos_str)

    def seek_label(self, label):
        abstr_level = 0
        for i in range(len(self._script) - 1):
            if self._script[i] == "define":
                abstr_level += 1

            elif self._script[i] == "end_def":
                abstr_level -= 1

            elif self._script[i] == "label" and abstr_level == 0:
                if self._script[i+1] == label:
                    self.set_pos(i+1)
                    return

        self.error(f"label '{label} not found")

    def jump(self):
        self.jumped = True
        self.loop_breaks.clear()
        self.loop_skips.clear()
