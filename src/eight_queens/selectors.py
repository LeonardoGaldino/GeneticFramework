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
        # TODO: Implement this method
        return parents


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
                