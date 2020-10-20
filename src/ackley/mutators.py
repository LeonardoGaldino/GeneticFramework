from random import gauss
from abc import ABC
from typing import Type

from genetic_framework.mutator import Mutator
from ackley.chromosomes import FloatChromosome


class DeltaMutator(Mutator[FloatChromosome], ABC):
    @classmethod
    def mutate_inplace(cls: Type, chromosome: FloatChromosome) -> None:
        step_size: float = cls.custom_data['step_size']
        lower_bound: float = cls.custom_data['lower_bound']
        upper_bound: float = cls.custom_data['upper_bound']

        for gene in chromosome.genotypes:
            delta = gauss(0, step_size)
            new_val = gene.data + delta
            
            # Avoid moving gene data outside boundaries
            new_val = min(upper_bound, max(lower_bound, new_val))
            gene.data = new_val
