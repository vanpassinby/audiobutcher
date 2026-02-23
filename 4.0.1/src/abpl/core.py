import common
from abpl.abpl_tools import build_jump_index
from scrambler.segment import SegmentInfo
from scrambler.scr_state import ScramblerState


class Error(Exception):
    pass


class Return(Exception):
    pass


class Break(Exception):
    pass


class ABPLObject:
    def __init__(self, obj):
        self.obj = obj


class ScriptState:
    def __init__(self, script: list[str], double_indexing: list[tuple[int, int]],
                 segment: SegmentInfo, scr_state: ScramblerState,
                 exec_shift=0, pre_jump_index=None):

        self._script = script
        self._jump_index = pre_jump_index if pre_jump_index else build_jump_index(script)
        self.double_indexing = double_indexing
        self.exec_shift = exec_shift
        self.abpl400_mode = False

        self.position = -1
        self.jumped = False
        self.loop_breaks = []
        self.loop_skips = []

        self.result = 0
        self.segment = segment
        self.scr_state = scr_state

        # DON'T FORGET TO SYNC THESE FOR FUNCTIONS

        self.round_samples = True
        self.random_positive = True
        self.quan_options = {}
        self.call_stack = []

        self.variables = {}
        self.vars_global = {}
        self.global_var_list = set()

    def debug(self, *args, **kwargs):
        if common.AB_ABPL_DEBUG:
            indent = " ." * len(self.call_stack)
            print(f"ABPL DEBUG:{indent}", *args, **kwargs)

    def error(self, exception: Exception):
        call_stack_text = "\n".join(
            f"[{self._token_pos_str_c(pos)}] {cmd}" for pos, cmd in self.call_stack
        )

        error = Error(f"ABPL call stack:\n"
                      f"{call_stack_text}\n\n"
                      f"{type(exception).__name__}: {exception}")

        raise error from None

    def _token_pos_str_c(self, position):
        if position > len(self.double_indexing):
            return "OUT-RANGE"
        else:
            y, x = self.double_indexing[position]
            return f"{y}:{x}"

    @property
    def token_pos_str(self) -> str:
        return self._token_pos_str_c(self.position + self.exec_shift)

    def call_stack_add(self, command):
        self.call_stack.append((self.position + self.exec_shift, command))

    @property
    def finished(self) -> bool:
        return self.position + 1 >= len(self._script)

    def read(self, move=True):
        if move:
            self.position += 1

        command = self._script[self.position]
        return command

    def set_pos(self, position):
        self.position = position
        self.debug("jump to", self.token_pos_str)

    def seek_label(self, label):
        if label not in self._jump_index:
            raise Error(f"label '{label}' not found")

        self.set_pos(self._jump_index[label])

    def jump(self):
        self.jumped = True
        self.loop_breaks.clear()
        self.loop_skips.clear()
