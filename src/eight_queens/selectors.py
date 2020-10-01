from copy import copy

from genetic_framework.core import *


class BestFitnessMatingSelector(MatingSelector):

    @staticmethod
    def select_couples(population: List[Individual]) \
            -> List[Tuple[Individual, Individual]]:
        # TODO: implement this method
        return [(individual, individual) for individual in population]


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


class KBestFitnessIndividualSelector(IndividualSelector):

    def __init__(self, number_solutions: int, custom_data: Dict = {}) -> None:
        super().__init__(number_solutions, custom_data)
        self._best_individuals: List[Individual] = []
    
    @property
    def best_individuals(self) -> List[Individual]:
        return self._best_individuals

    @abstractmethod
    def update_individuals(self, population: List[Individual]) -> None:
        population.sort(key=lambda individual: individual.fitness())
        lower_bound = len(population) - self.number_solutions
    
        if not self._best_individuals:
            self._best_individuals = copy(population[lower_bound:])
            return

        i = lower_bound
        while i < len(population) and \
                population[i].fitness() > self.best_individuals[i - lower_bound].fitness():
            self._best_individuals[i - lower_bound] = population[i]
            i += 1
                