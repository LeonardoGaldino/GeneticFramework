from typing import Type, List
from abc import ABC
from functools import reduce
from math import cos, exp, sqrt, e

from genetic_framework.fitness import FitnessComputer
from ackley.chromosomes import FloatChromosome, AdaptiveStepFloatChromosome


def ackley_fitness(c1: float, c2: float, c3: float,
                   data: List[float]) -> float:
    n: int = len(data)

    squares = reduce(lambda acc, value: acc + value * value, data, 0.0)
    second_sum = reduce(lambda acc, value: acc + cos(c3 * value), data, 0.0)

    result = c1 + e
    result -= c1 * exp(-c2 * sqrt(1.0 / n) * squares)
    result -= exp(second_sum / n)

    return result


class AckleyFitnessComputer(FitnessComputer[FloatChromosome], ABC):
    @classmethod
    def fitness(cls: Type, chromosome: FloatChromosome) -> float:
        c1: float = cls.custom_data['c1']
        c2: float = cls.custom_data['c2']
        c3: float = cls.custom_data['c3']
        data = list(map(lambda gene: gene.data, chromosome.genotypes))

        return ackley_fitness(c1, c2, c3, data)


class AdaptiveStepAckleyFitnessComputer(
        FitnessComputer[AdaptiveStepFloatChromosome], ABC):
    @classmethod
    def fitness(cls: Type, chromosome: AdaptiveStepFloatChromosome) -> float:
        c1: float = cls.custom_data['c1']
        c2: float = cls.custom_data['c2']
        c3: float = cls.custom_data['c3']
        data = list(map(lambda gene: gene.data[0], chromosome.genotypes))

        return ackley_fitness(c1, c2, c3, data)
