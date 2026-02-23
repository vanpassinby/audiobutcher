import os
import json
import importlib
import gui.filetypes
from localization import loc


def localize_list(items: list, loc_part: dict):
    result = [""] * len(items)
    for i in range(len(items)):
        result[i] = loc_part.get(items[i], items[i])

    return result


def union(source: dict, dest: dict):
    for key, old_value in dest.items():
        value = source.get(key)

        if (key in source) and type(old_value) == type(value):

            if isinstance(value, dict):
                union(value, dest[key])

            else:
                if isinstance(value, list) and len(value) != len(old_value):
                    continue  # WARNING: The above condition assumes that the list doesn't contain dicts
                dest[key] = value


def override_loc(json_path: str, failsafe=True):
    if not os.path.isfile(json_path):
        return

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            loc_data = json.load(f)
        union(loc_data, loc)

        importlib.reload(gui.filetypes)

    except Exception as e:
        if not failsafe: raise
        print(f"Failed to load localization: {e}")
