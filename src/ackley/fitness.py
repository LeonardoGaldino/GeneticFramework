from typing import Type
from abc import ABC
from functools import reduce
from math import cos, exp, sqrt

from genetic_framework.fitness import FitnessComputer
from ackley.chromosomes import FloatChromosome


class AckleyFitnessComputer(FitnessComputer[FloatChromosome], ABC):
    @classmethod
    def fitness(cls: Type, chromosome: FloatChromosome) -> float:
        n: int = cls.custom_data['n']
        c1: float = cls.custom_data['c1']
        c2: float = cls.custom_data['c2']
        c3: float = cls.custom_data['c3']
        genes = chromosome.genotypes

        result: float = 1.0 + c1
        squares = reduce(lambda acc, gene: acc + gene.data * gene.data, genes,
                         0.0)
        second_sum = reduce(lambda acc, gene: acc + cos(c3 * gene.data), genes,
                            0.0)

        result -= c1 * exp(-c2 * sqrt(squares / n))
        result -= exp(second_sum / n)

        return -result
