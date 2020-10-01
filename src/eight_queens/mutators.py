from random import randint
from copy import copy
from functools import reduce

from genetic_framework.core import *
from eight_queens.chromosomes import BitStringChromosome


class BitStringFlipBitMutator(Mutator[BitStringChromosome]):

    @staticmethod
    def mutate(chromosome: BitStringChromosome) -> BitStringChromosome:
        new_chromosome = BitStringChromosome(chromosome.custom_data)
        new_chromosome.data = copy(chromosome.data)
        BitStringFlipBitMutator.mutate_inplace(new_chromosome)
        return new_chromosome

    @staticmethod
    def mutate_inplace(chromosome: BitStringChromosome) -> None:
        chess_size = BitStringFlipBitMutator.custom_data['chess_size']

        gene_index = randint(0, chess_size - 1)
        new_gene_value = randint(0, chess_size - 1)

        genes = chromosome.genotypes()
        genes[gene_index].data = "{:032b}".format(new_gene_value)
        chromosome.data = reduce(lambda acc, gene: acc + gene.data, genes, '')
