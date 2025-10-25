import math
import random


class RD:
    uniform = 0
    gauss = 1
    gauss_c = 2  # Gauss Clipped
    lognorm = 3
    exp = 4


class RandNumber:
    def __init__(self, mode, value1, value2):
        self.mode = mode
        self.value1 = value1
        self.value2 = value2

    def get(self):
        if self.mode == RD.uniform:
            return abs(random.uniform(self.value1, self.value2))

        elif self.mode == RD.gauss:
            number = -1
            while number < 0:
                number = random.gauss(self.value1, self.value2)
            return number

        elif self.mode == RD.gauss_c:
            min_val = max(0, self.value1 - abs(self.value2))
            max_val = self.value1 + abs(self.value2)

            if max_val < 0:
                exc = ValueError("Clipped Gauss: wrong parameters.")
                raise exc

            number = -1
            while not (min_val <= number <= max_val):
                number = random.gauss(self.value1, self.value2)
            return number

        elif self.mode == RD.lognorm:
            return random.lognormvariate(self.value1, self.value2)

        elif self.mode == RD.exp:
            return -math.log(1 - random.random()) * abs(self.value1)

        else:
            return 0

    def convert_seconds(self):
        if self.mode != RD.lognorm:
            self.value1 *= 1000
            self.value2 *= 1000

    def is_zero(self):
        if self.mode == RD.gauss_c:
            return self.value1 + abs(self.value2) <= 0
        elif self.mode != RD.lognorm:
            return self.value1 == self.value2 == 0
        else:
            return False

    def check_wrong_mode(self):
        return self.mode == -1

    def check_wrong_gauss(self):
        return self.mode == RD.gauss_c and (self.value1 + abs(self.value2) < 0)

    def check_wrong_lognorm(self):
        return self.mode == RD.lognorm and (self.value1 + abs(self.value2) > 10)


class RandChance:
    def __init__(self, chance=50.0):
        self.chance = chance

    def get(self):
        return random.random() < self.chance / 100


class RandChoice:
    def __init__(self, elements: list, weights: list[int]):
        self.elements = elements
        self.weights = weights

    def get(self):
        return random.choices(self.elements, self.weights)[0]

    def check_wrong_zero_sum(self):
        return sum(self.weights) <= 0


def rand_gauss_deviation(deviation: float):
    number = -1
    while not (0 <= number <= abs(deviation)):
        number = random.gauss(0, deviation)
    return number


def rand_by_chance(chance: RandChance, generator: RandNumber | RandChoice, fallback=0.0):
    return generator.get() if chance.get() else fallback
