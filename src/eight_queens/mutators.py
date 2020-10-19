from random import randint
from abc import ABC
from typing import Type

from genetic_framework.mutator import Mutator
from eight_queens.chromosomes import BitStringChromosome


class BitStringRandomizeGeneMutator(Mutator[BitStringChromosome], ABC):
    @classmethod
    def mutate_inplace(cls: Type, chromosome: BitStringChromosome) -> None:
        chess_size: int = cls.custom_data['chess_size']

        gene_index = randint(0, chess_size - 1)
        new_gene_value = randint(0, chess_size - 1)

        genes = chromosome.genotypes
        genes[gene_index].data = "{:032b}".format(new_gene_value)
        chromosome.genotypes = genes
