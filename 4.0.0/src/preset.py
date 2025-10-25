from configparser import RawConfigParser


class PresetOpen:
    def __init__(self, path=None, data=None):
        self.rcp = RawConfigParser()
        self.sec_name = "AudioButcher"

        if path:
            self.rcp.read(path, encoding="utf-8")
        elif data:
            self.rcp.read_string(data)

    def check_ab3(self):
        ab3_ident = "AudioButcher3"
        if self.rcp.has_section(ab3_ident) and not self.rcp.has_section(self.sec_name):
            self.rcp[self.sec_name] = self.rcp[ab3_ident]

    def get(self, option, fallback):
        return self.rcp.get(self.sec_name, option, fallback=fallback)

    def batch_set(self, batch):
        for parameter in batch:
            parameter[0].set(self.get(parameter[1], parameter[2]))


class PresetSave:
    def __init__(self):
        self.text = "[AudioButcher]\n"

    def write(self, path):
        with open(path, "w", encoding="utf-8") as file:
            file.write(self.text.strip())

    def add(self, parameter, value):
        value_fix = str(value).replace("\n", " ")
        self.text += f"{parameter} = {value_fix}\n"

    def add_separator(self):
        self.text += "\n"
