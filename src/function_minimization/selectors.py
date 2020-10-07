from copy import deepcopy
from typing import List, Tuple, Dict
from random import random, randint, shuffle
from abc import ABC
from statistics import mean

from genetic_framework.selectors import SurvivorSelector, MatingSelector, SolutionSelector
from genetic_framework.individual import Individual


class MinimizeFitnessMatingSelector(MatingSelector, ABC):
    @staticmethod
    def select_couples(population: List[Individual],
                       num_pairs: int) -> List[Tuple[Individual, Individual]]:
        population.sort(key=lambda individual: individual.fitness())
        pairs: List[Tuple[Individual, Individual]] = []
        size = len(population)

        if size <= 1:
            return []

        i = 0
        for i in range(0, 2 * num_pairs, 2):
            pairs.append((population[i], population[i + 1]))

        return pairs


class MinimizeFitnessSurvivorSelector(SurvivorSelector, ABC):
    @staticmethod
    def select_survivors(population_size: int, parents: List[Individual],
                         breed: List[Individual]) -> List[Individual]:
        new_generation_individuals = parents + breed
        new_generation_individuals.sort(
            key=lambda individual: individual.fitness())
        return new_generation_individuals[:population_size]


class KLowerFitnessSolutionSelector(SolutionSelector, ABC):
    def __init__(self, number_solutions: int, custom_data: Dict = {}) -> None:
        super().__init__(number_solutions, custom_data)
        self._best_individuals: List[Individual] = []

    @property
    def best_individual(self) -> Individual:
        return self._best_individuals[0]

    @property
    def best_individuals(self) -> List[Individual]:
        return self._best_individuals

    def update_individuals(self, population: List[Individual]) -> None:
        self._best_individuals.extend(population)
        self._best_individuals.sort(
            key=lambda individual: individual.fitness())
        self._best_individuals = self.best_individuals[:self.number_solutions]
