from random import random
from enum import Enum


class DataType(Enum):
    VARIABLE = 0
    STEP_SIZE = 1
    ROTATION_ANGLE = 2


def random_lerp(v1: float, v2: float) -> float:
    return lerp(random(), v1, v2)


def lerp(t: float, v1: float, v2: float) -> float:
    return t * v1 + (1 - t) * v2


def clamp(x: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(x, maximum))


def sign(x: float):
    return 1 if x >= 0 else -1
