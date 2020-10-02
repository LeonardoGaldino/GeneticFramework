from random import randint
from copy import deepcopy

from genetic_framework.mutator import Mutator
from eight_queens.chromosomes import BitStringChromosome


class RandomizeGeneMutator(Mutator[BitStringChromosome]):

    @staticmethod
    def mutate(chromosome: BitStringChromosome) -> BitStringChromosome:
        new_chromosome = BitStringChromosome(chromosome.custom_data)
        new_chromosome.data = deepcopy(chromosome.data)
        RandomizeGeneMutator.mutate_inplace(new_chromosome)
        return new_chromosome

    @staticmethod
    def mutate_inplace(chromosome: BitStringChromosome) -> None:
        chess_size = RandomizeGeneMutator.custom_data['chess_size']

        gene_index = randint(0, chess_size - 1)
        new_gene_value = randint(0, chess_size - 1)

        genes = chromosome.genotypes
        genes[gene_index].data = "{:032b}".format(new_gene_value)
        chromosome.genotypes = genes
