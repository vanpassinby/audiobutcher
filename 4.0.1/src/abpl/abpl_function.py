from abpl.abpl_main import *
from abpl.lib_vars import set_variable


class ABPLFunction:
    def __init__(self, name: str, f_start: int, arg_names: list[str], function: list[str]):
        self.name = name
        self.f_start = f_start
        self.arg_names = arg_names
        self.function = function

    def __str__(self):
        return f"Function {self.name}(" + ", ".join(self.arg_names) + ")"

    def get_sub_state(self, state: ScriptState):
        sub_state = ScriptState(self.function, state.double_indexing,
                                state.segment, state.scr_state,
                                exec_shift=self.f_start)

        sub_state.abpl400_mode = state.abpl400_mode
        sub_state.round_samples = state.round_samples
        sub_state.random_positive = state.random_positive
        sub_state.quan_options = state.quan_options
        sub_state.call_stack = state.call_stack
        sub_state.vars_global = state.vars_global | state.variables

        return sub_state

    @staticmethod
    def run(state: ScriptState, parent: ScriptState):
        stack_before = len(parent.call_stack)
        result = execute(state, is_sub=True)

        # Sync variables
        parent.round_samples = state.round_samples
        parent.random_positive = state.random_positive
        parent.call_stack = state.call_stack[:stack_before]

        if parent.abpl400_mode:
            parent.variables |= state.variables
        else:
            for var_name in state.global_var_list:
                if var_name in state.variables:
                    parent.variables[var_name] = state.variables[var_name]

        return ABPLObject(result)

    def __call__(self, state: ScriptState):
        sub_state = self.get_sub_state(state)

        for argument in self.arg_names:
            set_variable(sub_state, argument, read_command(state))

        return self.run(sub_state, state)

    def call_local(self, state: ScriptState, *args):
        state.debug("local call", self.name)
        state.call_stack_add(self.name) # Fake call

        sub_state = self.get_sub_state(state)

        # Execution
        for arg, value in zip(self.arg_names, args):
            set_variable(sub_state, arg, value)
        result = self.run(sub_state, state).obj

        state.call_stack.pop(-1)
        return result


def define_function(state: ScriptState):
    func_name = state.read()
    n_args = int(state.read())
    arg_names = [state.read() for _ in range(n_args)]

    state.debug("defining", func_name, "(", *arg_names, ")")

    f_start = state.position + state.exec_shift + 1
    function = []

    n_nest = 0
    while True:
        sub = state.read()
        if sub == "define":
            n_nest += 1
        elif sub == "end_def":
            if n_nest == 0:
                break
            else:
                n_nest -= 1

        function.append(sub)

    func = ABPLFunction(func_name, f_start, arg_names, function)
    set_variable(state, func_name, func)
