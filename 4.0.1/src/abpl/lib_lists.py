from abpl.abpl_main import *


def new_list(state: ScriptState):
    list_size = read_command(state)
    list_contents = read_multi(state, list_size)

    return ABPLObject(ABPLList(list_contents))


class ABPLList:
    def __init__(self, contents: list):
        self.contents = contents

    def __str__(self):
        return "[" + ", ".join(map(str, self.contents)) + "]"

    def __eq__(self, other):
        return isinstance(other, ABPLList) and self.contents == other.contents

    def __call__(self, state: ScriptState):
        command = state.read()
        state.debug("list:", command)
        state.call_stack_add(command)

        result = None

        if command == "as_obj":
            result = ABPLObject(self)

        elif command == "get":
            idx = read_command(state)
            result = self.contents[idx]

        elif command == "assign":
            idx, value = read_multi(state, 2)
            self.contents[idx] = value

        elif command == "get_slice":
            idx1, idx2 = read_multi(state, 2)
            new = self.contents[idx1:idx2]
            result = ABPLObject(ABPLList(new))

        elif command == "get_slice_st":
            idx1, idx2, step = read_multi(state, 3)
            new = self.contents[idx1:idx2:step]
            result = ABPLObject(ABPLList(new))

        elif command == "length":
            result = len(self.contents)

        elif command == "append":
            x = read_command(state)
            self.contents.append(x)

        elif command == "extend":
            x = read_command(state)
            self.contents.extend(x)

        elif command == "insert":
            i, x = read_multi(state, 2)
            self.contents.insert(i, x)

        elif command == "remove":
            x = read_command(state)
            self.contents.remove(x)

        elif command == "pop":
            i = read_command(state)
            result = self.contents.pop(i)

        elif command == "contains":
            x = read_command(state)
            result = x in self.contents

        elif command == "index":
            x = read_command(state)
            result = self.contents.index(x)

        elif command == "index_lim":
            x, start, end = read_multi(state, 3)
            result = self.contents.index(x, start, end)

        elif command == "count":
            x = read_command(state)
            result = self.contents.count(x)

        elif command == "sort":
            self.contents.sort()

        elif command == "sort_key":
            from abpl.abpl_function import ABPLFunction

            sort_f = read_command(state)
            if isinstance(sort_f, ABPLFunction):
                if len(sort_f.arg_names) != 1:
                    raise Error("'sort_key' function should take exactly 1 argument")
                self.contents.sort(key=lambda val: sort_f.call_local(state, val))
            else:
                raise Error("'sort_key' only supports user-defined functions")

        elif command == "reverse":
            self.contents.reverse()

        elif command == "get_copy":
            result = ABPLObject(ABPLList(self.contents.copy()))

        elif command == "clear":
            self.contents.clear()

        else:
            raise Error(f"'list' doesn't support '{command}'")

        state.call_stack.pop(-1)
        return result


def is_list(state: ScriptState):
    obj = read_command(state)
    return isinstance(obj, ABPLList)


library = {
    "list": new_list,
    "is_list": is_list
}

misc_kw = {"as_obj", "get", "assign", "get_slice", "get_slice_st", "length",
           "append", "extend", "insert", "remove", "pop",
           "contains", "index", "index_lim", "count",
           "sort", "sort_key", "reverse", "get_copy", "clear"}
