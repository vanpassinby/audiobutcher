def int1(string, fallback=0):
    try:
        return int(float(string))
    except:
        return fallback


def float1(string, fallback=0.0):
    try:
        return float(string)
    except:
        return fallback


def x_bool(string: str):
    return string.strip().lower() in ("1", "y", "yes", "true")


def round1(number):
    rounded = round(number)
    if rounded < 1:
        return 1
    return rounded


def clip_number(number, min_val, max_val):
    if number <= min_val:
        return min_val
    if number >= max_val:
        return max_val
    return number


def range1(a, b, step=1):
    if step == 0:
        exc = ValueError("Step cannot be zero.")
        raise exc

    step = abs(step)
    if a > b:
        step = -step

    result = []
    i = 0
    while True:
        val = a + i * step
        if (step > 0 and val > b) or (step < 0 and val < b):
            break
        result.append(val)
        i += 1

    if result[-1] != b:
        result.append(b)

    return result


def str_list_with_range(string: str):
    result = []
    buffer = []
    expect = "any"  # any, open, range

    for sub in string.replace("[", " [ ").replace("]", " ] ").split():
        if expect == "any":
            if sub.lower() == "range":
                expect = "open"
            else:
                result.append(float(sub))

        elif expect == "open":
            if sub == "[":
                expect = "range"
            else:
                exc = ValueError(f"Expected '[' after 'RANGE', but got '{sub}'.")
                raise exc

        elif expect == "range":
            if sub == "]":
                if len(buffer) == 1:
                    result += buffer
                else:
                    result += range1(*buffer)

                buffer.clear()
                expect = "any"

            else:
                buffer.append(float(sub))

    if len(buffer) > 0:
        exc = ValueError("Missing ']' to close RANGE.")
        raise exc

    return result
