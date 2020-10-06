from typing import Type, List, Tuple
from abc import ABC

from genetic_framework.fitness import FitnessComputer
from function_minimization.genotypes import FloatGenotype
from function_minimization.chromosomes import FloatVectorChromosome

class ChallengeFitnessComputer(FitnessComputer[FloatVectorChromosome], ABC):

    @staticmethod
    def fitness(chromosome: FloatVectorChromosome) -> float:
        vector_size = ChallengeFitnessComputer.custom_data['vector_size']
        data: List[float] = [gene.data for gene in chromosome.genotypes]

        total = 0.0
        for i in range(vector_size - 1):
            x1 = data[i]
            x2 = data[i + 1]
            left = x2 - (x1 ** 2)
            right = (x1 - 1)
            total += (100.0 * (left ** 2)) + (right ** 2)
        return total