from abpl.core import *
from abpl.abpl_main import read_multi, read_command

import random
from ab_random import RD, RandNumber, RandChance
from scrambler.rand_seg_sp import random_start_pos, random_sp_loop, random_sp_ast, random_sp_pattern


def rand_chance(state: ScriptState):
    chance = read_command(state)
    return RandChance(chance).get()


def rand_int(state: ScriptState):
    val1, val2 = read_multi(state, 2)
    return random.randint(round(val1), round(val2))


def random_number(mode):
    def generate(state: ScriptState):
        val1 = read_command(state)
        val2 = 0 if mode == RD.exp else read_command(state)

        return RandNumber(mode, val1, val2).get()

    return generate


def rand_sp(state: ScriptState):
    mode = state.read()
    st = state.scr_state
    seg = state.segment

    if mode == "auto":
        random_start_pos(st, seg)
    elif mode == "in_loop":
        random_sp_loop(st, seg)
    elif mode == "avgstart":
        random_sp_ast(st, seg)
    elif mode == "pattern":
        random_sp_pattern(st, seg)


library = {
    "rand_chance":  rand_chance,
    "rand_int":     rand_int,

    "rand_uniform": random_number(RD.uniform),
    "rand_gauss":   random_number(RD.gauss),
    "rand_gauss_clip": random_number(RD.gauss_c),
    "rand_lognorm": random_number(RD.lognorm),
    "rand_exp":     random_number(RD.exp),

    "ab_random_sp": rand_sp
}
