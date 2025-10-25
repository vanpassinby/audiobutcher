import abpl.lib_vars as variables
import abpl.lib_math as math
import abpl.lib_random as random
import abpl.lib_props as props
import abpl.lib_preset as preset
import abpl.lib_switch as switching
import abpl.lib_const as constants
import abpl.lib_quan as quantization


library = {}
for module in (variables, math, random, props, preset, switching, constants, quantization):
    library |= module.library
