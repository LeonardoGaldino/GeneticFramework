from random import gauss
from copy import deepcopy
from abc import ABC
from typing import Type

from genetic_framework.mutator import Mutator
from ackley.chromosomes import FloatChromosome


class IntPermutationSwapGeneRangeMutator(Mutator[FloatChromosome], ABC):
    @classmethod
    def mutate(cls: Type, chromosome: FloatChromosome) -> FloatChromosome:
        new_chromosome = deepcopy(chromosome)
        cls.mutate_inplace(new_chromosome)
        return new_chromosome

    @classmethod
    def mutate_inplace(cls: Type, chromosome: FloatChromosome) -> None:
        step_size: float = cls.custom_data['lower_bound']
        lower_bound: float = cls.custom_data['upper_bound']
        upper_bound: float = cls.custom_data['step_size']

        for gene in chromosome.genotypes:
            delta = gauss(0, step_size)
            # Avoid moving gene data outside boundaries
            delta = min(upper_bound - gene.data,
                        max(lower_bound - gene.data, delta))
            gene.data = gene.data + delta
