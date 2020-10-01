from copy import deepcopy
from typing import List, Tuple, Dict

from genetic_framework.selectors import SurvivorSelector, MatingSelector, SolutionSelector
from genetic_framework.individual import Individual


class BestFitnessMatingSelector(MatingSelector):

    @staticmethod
    def select_couples(population: List[Individual]) -> List[Tuple[Individual, Individual]]:
        population.sort(key=lambda individual: -individual.fitness())
        pairs: List[Tuple[Individual, Individual]] = []
        size = len(population)

        if size <= 1:
            return []

        i = 0
        while i < size - 1:
            pairs.append((population[i], population[i+1]))
            i += 2
        if (size % 2) != 0:
            pairs.append((population[i-1], population[i]))

        return pairs


class BestFitnessSurvivorSelector(SurvivorSelector):

    @staticmethod
    def select_survivors(population_size: int, parents: List[Individual],
            breed: List[Individual]) -> List[Individual]:
        parents.sort(key=lambda individual: -individual.fitness())
        breed.sort(key=lambda individual: -individual.fitness())
        new_generation_individuals = []

        i, j = 0, 0
        while i + j < population_size:
            if i == len(parents) and j == len(breed):
                break
            if i == len(parents) or parents[i].fitness() < breed[j].fitness():
                new_generation_individuals.append(breed[j])
                j += 1
            elif j == len(breed) or parents[i].fitness() > breed[j].fitness():
                new_generation_individuals.append(parents[i])
                i += 1
            else:
                # The same fitness
                new_generation_individuals.append(parents[i])
                i += 1

        return new_generation_individuals


class KBestFitnessSolutionSelector(SolutionSelector):

    def __init__(self, number_solutions: int, custom_data: Dict = {}) -> None:
        super().__init__(number_solutions, custom_data)
        self._best_individuals: List[Individual] = []
    
    @property
    def best_individual(self) -> Individual:
        return self._best_individuals[-1]

    @property
    def best_individuals(self) -> List[Individual]:
        return self._best_individuals

    def update_individuals(self, population: List[Individual]) -> None:
        population.sort(key=lambda individual: individual.fitness())
        size = len(population)
    
        if not self._best_individuals:
            # if no best individuals have been stored yet: 
            # copy <number_solutions> best individuals from population
            self._best_individuals = deepcopy(population[size - self.number_solutions:])
            return

        i = 0
        while i < self.number_solutions and \
                population[size - 1 - i].fitness() > self._best_individuals[i].fitness():
            self._best_individuals[i] = deepcopy(population[size - 1 - i])
            i += 1
        if i > 0:
            # elements have been added to the beginning: resort individuals
            self._best_individuals.sort(key=lambda individual: individual.fitness())
        
                