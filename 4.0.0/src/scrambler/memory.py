import random


class ScrambleMemory:
    def __init__(self):
        self.memory = {}

    def remember(self, segment, position):
        if position in self.memory:
            self.memory[position].append(segment)
        else:
            self.memory[position] = [segment]

    def get_segment(self):
        if -1 in self.memory and len(self.memory[-1]) > 0:
            return random.choice(self.memory[-1])
        else:
            return None

    def move_on(self):
        new_mem = {}
        for element in self.memory:
            if element >= 0:
                new_mem[element-1] = self.memory[element]
        self.memory = new_mem
