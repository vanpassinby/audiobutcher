def build_token_index(tokens_by_line: list[int]):
    result: list = [None] * sum(tokens_by_line)

    pos = 0
    for line_num, token_count in enumerate(tokens_by_line):
        for token_num in range(token_count):
            result[pos] = (line_num, token_num)
            pos += 1

    return result


def build_jump_index(script: list[str]):
    indexing: dict[str, int] = {}

    abstr_level = 0
    for i in range(len(script) - 1):
        if script[i] == "define":
            abstr_level += 1

        elif script[i] == "end_def":
            abstr_level -= 1

        elif script[i] == "label":
            label_name = script[i+1]
            if label_name not in indexing:
                indexing[label_name] = i+1

    return indexing


def format_script(script: str):
    def filtered(char):
        if char in "() [] {} ,;:":
            return " "
        else:
            return char

    result = []
    tokens_by_line = []
    text = "".join(filtered(char) for char in script)

    for line in text.split("\n"):
        line = line.split("#")[0].split()

        result.extend(line)
        tokens_by_line.append(len(line))

    return result, build_token_index(tokens_by_line), build_jump_index(result)
