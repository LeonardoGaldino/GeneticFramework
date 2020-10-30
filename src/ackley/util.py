from random import random
from enum import Enum
from typing import List
from math import sqrt, exp, radians, tan, pi, cos, e
from functools import reduce
import numpy as np  #type: ignore


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

def assembly_covariance_matrix(step_sizes: List[float], rotation_angles: List[float]):
    n: int = len(step_sizes)
    covariance_matrix = np.zeros((n, n))

    k = 0
    for i in range(n):
        for j in range(i, n):
            if i == j:
                covariance_matrix[i][j] = pow(step_sizes[i], 2)
            else:
                value = 0.5 * pow(step_sizes[i] - step_sizes[j], 2) * tan(2 * rotation_angles[k])
                covariance_matrix[i][j] = covariance_matrix[j][i] = value
                k += 1
    
    return covariance_matrix


def ackley_function(c1: float, c2: float, c3: float,
                    data: List[float]) -> float:
    n: int = len(data)

    squares = reduce(lambda acc, value: acc + value * value, data, 0.0)
    second_sum = reduce(lambda acc, value: acc + cos(c3 * value), data, 0.0)

    result = c1 + e
    result -= c1 * exp(-c2 * sqrt(1.0 / n) * squares)
    result -= exp(second_sum / n)

    return result