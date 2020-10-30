from typing import Type, List
from abc import ABC
from math import cos, exp, sqrt, e

from genetic_framework.fitness import FitnessComputer
from ackley.chromosomes import FloatChromosome, AdaptiveStepFloatChromosome, CovarianceFloatChromosome
from ackley.util import ackley_function


class AckleyFitnessComputer(FitnessComputer[FloatChromosome], ABC):
    @classmethod
    def fitness(cls: Type, chromosome: FloatChromosome) -> float:
        c1: float = cls.custom_data['c1']
        c2: float = cls.custom_data['c2']
        c3: float = cls.custom_data['c3']
        data = list(map(lambda gene: gene.data, chromosome.genotypes))

        return ackley_function(c1, c2, c3, data)


class AdaptiveStepAckleyFitnessComputer(
        FitnessComputer[AdaptiveStepFloatChromosome], ABC):
    @classmethod
    def fitness(cls: Type, chromosome: AdaptiveStepFloatChromosome) -> float:
        c1: float = cls.custom_data['c1']
        c2: float = cls.custom_data['c2']
        c3: float = cls.custom_data['c3']
        data = list(map(lambda gene: gene.data[0], chromosome.genotypes))

        return ackley_function(c1, c2, c3, data)


class CovarianceAckleyFitnessComputer(
        FitnessComputer[CovarianceFloatChromosome], ABC):
    @classmethod
    def fitness(cls: Type, chromosome: CovarianceFloatChromosome) -> float:
        n: int = cls.custom_data['n']
        c1: float = cls.custom_data['c1']
        c2: float = cls.custom_data['c2']
        c3: float = cls.custom_data['c3']
        data = list(map(lambda gene: gene.data, chromosome.genotypes[:n]))

        return ackley_function(c1, c2, c3, data)
