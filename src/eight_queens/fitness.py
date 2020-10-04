from typing import Type, List, Tuple
from abc import ABC

from genetic_framework.fitness import FitnessComputer
from eight_queens.phenotypes import QueenPositionPhenotype
from eight_queens.chromosomes import *


def is_horizontally_attacking(y1: int, y2: int) -> bool:
    return y1 == y2

def is_diagonally_attacking(x1: int, y1: int, x2: int, y2: int) -> bool:
    return abs(x1 - x2) == abs(y1 - y2)

def count_queen_attacks(phenotypes: List[QueenPositionPhenotype]) -> int:
    attacking_queens_count = 0
    for p1 in phenotypes:
        for p2 in phenotypes:
            if p1 == p2:
                continue

            attacking_queens_count += \
                is_horizontally_attacking(p1.data[0], p2.data[0]) \
                or is_diagonally_attacking(p1.data[0], p1.data[1],
                    p2.data[0], p2.data[1])

    return attacking_queens_count//2


class BitStringFitnessComputer(FitnessComputer[BitStringChromosome], ABC):

    @staticmethod
    def fitness(chromosome: BitStringChromosome) -> float:
        attacks = count_queen_attacks(chromosome.phenotypes)
        return 1/(1 + float(attacks))


class BooleanBitStringFitnessComputer(FitnessComputer[BitStringChromosome], ABC):

    @staticmethod
    def fitness(chromosome: BitStringChromosome) -> float:
        attacks = count_queen_attacks(chromosome.phenotypes)
        return 1.0 if attacks == 0 else 0.0


class IntPermutationFitnessComputer(FitnessComputer[IntPermutationChromosome], ABC):
    
    @staticmethod
    def fitness(chromosome: IntPermutationChromosome) -> float:
        attacks = count_queen_attacks(chromosome.phenotypes)
        return 1/(1 + float(attacks))


class BooleanIntPermutationFitnessComputer(FitnessComputer[IntPermutationChromosome], ABC):

    @staticmethod
    def fitness(chromosome: IntPermutationChromosome) -> float:
        attacks = count_queen_attacks(chromosome.phenotypes)
        return 1.0 if attacks == 0 else 0.0