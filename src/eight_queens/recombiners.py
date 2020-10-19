from random import randint
from typing import List, Type
from abc import ABC

from genetic_framework.recombiner import Recombiner
from eight_queens.chromosomes import *
from eight_queens.genotypes import IntGenotype


class BitStringCutCrossfillRecombiner(Recombiner[BitStringChromosome], ABC):
    @classmethod
    def recombine(cls: Type, chromosome1: BitStringChromosome,
                  chromosome2: BitStringChromosome) -> BitStringChromosome:
        chess_size = cls.custom_data['chess_size']

        new_chromosome = BitStringChromosome(chromosome1.custom_data)
        genes1 = chromosome1.genotypes
        genes2 = chromosome2.genotypes

        cut_point = randint(0, chess_size)
        mixed_genes = genes1[:cut_point] + genes2[cut_point:]

        new_chromosome.genotypes = mixed_genes
        return new_chromosome


class IntPermutationRecombiner(Recombiner[IntPermutationChromosome], ABC):
    # PMX crossover algorithm

    @classmethod
    def _find_index(cls: Type['IntPermutationRecombiner'], idx: int, left: int,
                    right: int, genes1: List[int], genes2: List[int]) -> int:
        target = genes1[idx]
        target_idx_p2 = genes2.index(target)

        if target_idx_p2 >= left and target_idx_p2 <= right:
            return cls._find_index(target_idx_p2, left, right, genes1, genes2)

        return target_idx_p2

    @classmethod
    def recombine(
            cls: Type['IntPermutationRecombiner'],
            chromosome1: IntPermutationChromosome,
            chromosome2: IntPermutationChromosome) -> IntPermutationChromosome:
        chess_size = cls.custom_data['chess_size']

        new_chromosome = IntPermutationChromosome(chromosome1.custom_data)
        chromo1_data = list(map(lambda gene: gene.data, chromosome1.genotypes))
        chromo2_data = list(map(lambda gene: gene.data, chromosome2.genotypes))

        # Randomize who is going to be the parent1 and parent2
        if randint(0, 1) == 0:
            chromo1_data, chromo2_data = chromo2_data, chromo1_data

        new_data = [-1] * chess_size

        # Defines the range to be copied to the son
        left_r = randint(0, chess_size - 1)
        right_r = randint(left_r, chess_size - 1)
        new_data[left_r:right_r + 1] = chromo1_data[left_r:right_r + 1]

        for i in range(left_r, right_r + 1):
            if chromo2_data[i] in new_data:
                continue

            idx = cls._find_index(i, left_r, right_r, chromo1_data,
                                  chromo2_data)
            new_data[idx] = chromo2_data[i]

        for i in range(0, chess_size):
            new_data[i] = new_data[i] if new_data[i] != -1 else chromo2_data[i]

        new_genes: List[IntGenotype] = []
        for data in new_data:
            new_gene = IntGenotype(chromosome1.custom_data)
            new_gene.data = data
            new_genes.append(new_gene)

        new_chromosome.genotypes = new_genes
        return new_chromosome
