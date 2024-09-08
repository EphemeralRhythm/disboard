from enum import Enum
import random


def distance(entity1, entity2):
    return abs(entity1.x - entity2.x) + abs(entity1.y - entity2.y)


def normalize(a: float):
    if abs(a) < 8:
        return 0

    return 1 if a > 0 else (-1 if a < 0 else 0)


def randomize(number: int, percentage: int):
    assert 0 <= percentage <= 100, "The number provided to random function is invalid"

    return int(random.randint(100 - percentage, 100 + percentage) * number / 100)


def random_roll(chance: int):
    return random.randint(1, 100) <= chance


ATTAK_TYPES = Enum("type", ["PHYSICAL", "MAGICAL"])
