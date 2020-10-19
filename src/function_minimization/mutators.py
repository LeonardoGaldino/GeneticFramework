from math import sqrt
from random import randint, uniform
from abc import ABC
from typing import Type

from genetic_framework.mutator import Mutator
from function_minimization.chromosomes import FloatVectorChromosome
from function_minimization.util import clamp


class RandomizeGeneMutator(Mutator[FloatVectorChromosome], ABC):
    @classmethod
    def mutate_inplace(cls: Type, chromosome: FloatVectorChromosome) -> None:
        vector_size: int = cls.custom_data['vector_size']
        lower_bound: float = cls.custom_data['parameter_lower_bound']
        upper_bound: float = cls.custom_data['parameter_upper_bound']
        genes = chromosome.genotypes

        gene_index = randint(0, vector_size - 1)
        current_gene_value = genes[gene_index].data
        max_addition = min(current_gene_value - lower_bound,
                           upper_bound - current_gene_value)
        new_gene_value = current_gene_value + uniform(-max_addition,
                                                      max_addition)
        new_gene_value = clamp(new_gene_value, lower_bound, upper_bound)

        genes[gene_index].data = new_gene_value
        chromosome.genotypes = genes
