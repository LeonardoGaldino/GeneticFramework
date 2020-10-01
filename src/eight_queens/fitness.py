from typing import Type, List, Tuple
from math import ceil, log2

from genetic_framework.fitness import FitnessComputer
from eight_queens.chromosomes import *


class QueenAttackCountFitnessComputer(FitnessComputer[BitStringChromosome]):
    
    @staticmethod
    def _is_horizontally_attacking(y1: int, y2: int) -> bool:
        return y1 == y2

    @staticmethod
    def _is_diagonally_attacking(x1: int, y1: int, x2: int, y2: int) -> bool:
        return abs(x1 - x2) == abs(y1 - y2)

    @staticmethod
    def fitness(chromosome: BitStringChromosome) -> float:
        phenotypes = chromosome.phenotypes()

        attacking_queens_count = 0.0
        for p1 in phenotypes:
            for p2 in phenotypes:
                if p1 == p2:
                    continue

                attacking_queens_count += \
                    QueenAttackCountFitnessComputer \
                        ._is_horizontally_attacking(p1.data[0], p2.data[0]) \
                    or QueenAttackCountFitnessComputer \
                        ._is_diagonally_attacking(p1.data[0], p1.data[1], p2.data[0], p2.data[1])

        return 1/(1+attacking_queens_count)

