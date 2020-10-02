from random import randint
from typing import List

from genetic_framework.recombiner import Recombiner
from eight_queens.chromosomes import *


class BitStringCutCrossfillRecombiner(Recombiner[BitStringChromosome]):

    @staticmethod
    def recombine(chromosome1: BitStringChromosome, chromosome2: BitStringChromosome) -> BitStringChromosome:
        chess_size = BitStringCutCrossfillRecombiner.custom_data['chess_size']

        new_chromosome = BitStringChromosome(chromosome1.custom_data)
        genes1 = chromosome1.genotypes
        genes2 = chromosome2.genotypes

        cut_point = randint(0, chess_size)
        mixed_genes = genes1[:cut_point] + genes2[cut_point:]

        new_chromosome.genotypes = mixed_genes
        return new_chromosome


class IntPermutationRecombiner(Recombiner[IntPermutationChromosome]):
    # PMX crossover algorithm

    @staticmethod
    def _find_index(idx: int, left: int, right: int, genes1: List[int],
            genes2: List[int]) -> int:
        target = genes1[idx]
        target_idx_p2 = genes2.index(target)

        if target_idx_p2 >= left and target_idx_p2 <= right:
            return IntPermutationRecombiner \
                ._find_index(target_idx_p2, left, right, genes1, genes2)

        return target_idx_p2

    @staticmethod
    def recombine(chromosome1: IntPermutationChromosome, 
            chromosome2: IntPermutationChromosome) -> IntPermutationChromosome:
        chess_size = IntPermutationRecombiner.custom_data['chess_size']

        new_chromosome = IntPermutationChromosome(chromosome1.custom_data)
        genes1 = list(map(lambda chromo: chromo.data, chromosome1.genotypes))
        genes2 = list(map(lambda chromo: chromo.data, chromosome2.genotypes))

        # Randomize who is going to be the parent1 and parent2
        if randint(0, 1) == 0:
            genes1, genes2 = genes2, genes1

        # TODO: implement recombination
        new_data = [-1]*chess_size

        # Defines the range to be copied to the son
        left_r = randint(0, chess_size - 1)
        right_r = randint(left_r, chess_size - 1)
        new_data[left_r : right_r + 1] = genes1[left_r : right_r + 1]

        for i in range(left_r, right_r + 1):
            if genes2[i] in new_data:
                continue

            idx = IntPermutationRecombiner._find_index(i, left_r, right_r, genes1, genes2)
            new_data[idx] = genes2[i]

        for i in range(0, chess_size):
            new_data[i] = new_data[i] if new_data[i] != -1 else genes2[i]
            
        new_chromosome.data = new_data
        return new_chromosome