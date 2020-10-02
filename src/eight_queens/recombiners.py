from random import randint

from genetic_framework.recombiner import Recombiner
from eight_queens.chromosomes import *


class CutCrossFillRecombiner(Recombiner[BitStringChromosome]):

    @staticmethod
    def recombine(chromosome1: BitStringChromosome, chromosome2: BitStringChromosome) -> BitStringChromosome:
        chess_size = CutCrossFillRecombiner.custom_data['chess_size']

        new_chromosome = BitStringChromosome(chromosome1.custom_data)
        genes1 = chromosome1.genotypes
        genes2 = chromosome2.genotypes

        cut_point = randint(0, chess_size)
        mixed_genes = genes1[:cut_point] + genes2[cut_point:]

        new_chromosome.genotypes = mixed_genes
        return new_chromosome