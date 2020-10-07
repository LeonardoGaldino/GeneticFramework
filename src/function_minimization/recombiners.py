from random import random
from abc import ABC

from genetic_framework.recombiner import Recombiner
from function_minimization.chromosomes import FloatVectorChromosome
from function_minimization.genotypes import FloatGenotype


class RandomInterpolationRecombiner(Recombiner[FloatVectorChromosome], ABC):
    @staticmethod
    def recombine(chromosome1: FloatVectorChromosome,
                  chromosome2: FloatVectorChromosome) -> FloatVectorChromosome:
        vector_size = RandomInterpolationRecombiner.custom_data['vector_size']

        new_chromosome = FloatVectorChromosome(chromosome1.custom_data)
        genes1 = chromosome1.genotypes
        genes2 = chromosome2.genotypes

        alpha = random()
        mixed_genes = genes1[:]
        for i in range(vector_size):
            mixed_genes[i].data = alpha * genes1[i].data + (
                1 - alpha) * genes2[i].data

        new_chromosome.genotypes = mixed_genes
        return new_chromosome
