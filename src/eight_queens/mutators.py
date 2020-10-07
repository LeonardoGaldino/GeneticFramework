from random import randint
from copy import deepcopy
from abc import ABC

from genetic_framework.mutator import Mutator
from eight_queens.chromosomes import BitStringChromosome, IntPermutationChromosome


class RandomizeGeneMutator(Mutator[BitStringChromosome], ABC):
    @staticmethod
    def mutate(chromosome: BitStringChromosome) -> BitStringChromosome:
        new_chromosome = deepcopy(chromosome)
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


class BitStringSwapGeneMutator(Mutator[BitStringChromosome], ABC):
    @staticmethod
    def mutate(chromosome: BitStringChromosome) -> BitStringChromosome:
        new_chromosome = deepcopy(chromosome)
        BitStringSwapGeneMutator.mutate_inplace(new_chromosome)
        return new_chromosome

    @staticmethod
    def mutate_inplace(chromosome: BitStringChromosome) -> None:
        chess_size = BitStringSwapGeneMutator.custom_data['chess_size']

        r1 = randint(0, chess_size - 1)
        r2 = randint(0, chess_size - 1)
        while r1 == r2:
            r2 = randint(0, chess_size - 1)

        genes = chromosome.genotypes

        # Swap genes
        genes[r1], genes[r2] = genes[r2], genes[r1]
        chromosome.genotypes = genes


class IntPermutationSwapGeneMutator(Mutator[IntPermutationChromosome], ABC):
    @staticmethod
    def mutate(
            chromosome: IntPermutationChromosome) -> IntPermutationChromosome:
        new_chromosome = deepcopy(chromosome)
        IntPermutationSwapGeneMutator.mutate_inplace(new_chromosome)
        return new_chromosome

    @staticmethod
    def mutate_inplace(chromosome: IntPermutationChromosome) -> None:
        chess_size = IntPermutationSwapGeneMutator.custom_data['chess_size']

        r1 = randint(0, chess_size - 1)
        r2 = randint(0, chess_size - 1)
        while r1 == r2:
            r2 = randint(0, chess_size - 1)

        genes = chromosome.genotypes

        # Swap genes
        genes[r1], genes[r2] = genes[r2], genes[r1]
        chromosome.genotypes = genes


class IntPermutationSwapGeneRangeMutator(Mutator[IntPermutationChromosome],
                                         ABC):
    @staticmethod
    def mutate(
            chromosome: IntPermutationChromosome) -> IntPermutationChromosome:
        new_chromosome = deepcopy(chromosome)
        IntPermutationSwapGeneRangeMutator.mutate_inplace(new_chromosome)
        return new_chromosome

    @staticmethod
    def mutate_inplace(chromosome: IntPermutationChromosome) -> None:
        chess_size = IntPermutationSwapGeneRangeMutator.custom_data[
            'chess_size']

        l = randint(0, chess_size - 1)
        r = randint(l, chess_size - 1)

        genes = chromosome.genotypes
        _range = genes[l:r + 1]
        _range.reverse()

        chromosome.genotypes = genes[:l] + _range + genes[r + 1:]
