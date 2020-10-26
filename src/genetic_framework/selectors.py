from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from random import random, shuffle, randint
from statistics import mean
from copy import deepcopy
from operator import le, ge

from genetic_framework.custom_data import CustomDataHolder
from genetic_framework.individual import Individual
from genetic_framework.utils import Roulette


class MatingSelector(CustomDataHolder, ABC):
    @staticmethod
    @abstractmethod
    def select_couples(
            population: List[Individual], num_parent_pairs: int,
            maximize_fitness: bool) -> List[Tuple[Individual, Individual]]:
        """Pairs individuals to mate and produce children. Subclass should
        implement this logic of selecting individual to mate."""


class SurvivorSelector(CustomDataHolder, ABC):
    """Class responsible for selecting survivors for the following
    generation. Subclasses should implement this logic."""
    @staticmethod
    @abstractmethod
    def select_survivors(population_size: int, parents: List[Individual],
                         breed: List[Individual],
                         maximize_fitness: bool) -> List[Individual]:
        """Implements logic of choosing which individuals will survive to next
        generation."""


class SolutionSelector(ABC):
    """
    Responsible for best individuals selection logic on a running experiment
    """
    @abstractmethod
    def __init__(self,
                 number_solutions: int,
                 maximize_fitness: bool,
                 custom_data: Dict = {}) -> None:
        self.number_solutions = number_solutions
        self.maximize_fitness = maximize_fitness
        self.custom_data = custom_data

    @property
    @abstractmethod
    def best_individual(self) -> Individual:
        """Returns the best individual selected and stored so far."""

    @property
    @abstractmethod
    def best_individuals(self) -> List[Individual]:
        """Returns the best individuals selected and stored so far."""

    @abstractmethod
    def update_individuals(self, population: List[Individual]) -> None:
        """Updates (if necessary) the list of best individuals with 
        individuals from the specified population."""


class BestFitnessMatingSelector(MatingSelector, ABC):
    @staticmethod
    def select_couples(
            population: List[Individual], num_pairs: int,
            maximize_fitness: bool) -> List[Tuple[Individual, Individual]]:
        population.sort(key=lambda individual: individual.fitness(),
                        reverse=maximize_fitness)
        pairs: List[Tuple[Individual, Individual]] = []
        size = len(population)

        if size <= 1:
            return []

        i = 0
        for i in range(0, 2 * num_pairs, 2):
            pairs.append((population[i], population[i + 1]))

        return pairs


class RandomMatingSelector(MatingSelector, ABC):
    @staticmethod
    def select_couples(population: List[Individual], num_pairs: int,
                       __: bool) -> List[Tuple[Individual, Individual]]:
        pairs: List[Tuple[Individual, Individual]] = []
        size = len(population)

        if size <= 1:
            return []

        for _ in range(num_pairs):
            p1 = randint(0, size - 1)
            p2 = randint(0, size - 1)
            while p1 == p2:
                p2 = randint(0, size - 1)
            pairs.append((population[p1], population[p2]))

        return pairs


class RouletteMatingSelector(MatingSelector, ABC):
    @staticmethod
    def select_couples(
            population: List[Individual], num_pairs: int,
            maximize_fitness: bool) -> List[Tuple[Individual, Individual]]:
        pairs: List[Tuple[Individual, Individual]] = []
        roulette = Roulette(population, maximize_fitness)

        if len(population) <= 1:
            return []

        for _ in range(num_pairs):
            mate1 = roulette.get_individual()
            mate2 = roulette.get_individual()

            while mate2 == mate1:
                mate2 = roulette.get_individual()
            pairs.append((mate1, mate2))

        return pairs


class BestFromRandomMatingSelector(MatingSelector, ABC):
    @staticmethod
    def select_couples(
            population: List[Individual], num_pairs: int,
            maximize_fitness: bool) -> List[Tuple[Individual, Individual]]:
        pairs: List[Tuple[Individual, Individual]] = []

        if len(population) <= 1:
            return []

        random_count = min(5, len(population))

        for _ in range(num_pairs):
            shuffle(population)
            possible_mates = population[:random_count]
            selected_mates = sorted(
                possible_mates,
                key=lambda individual: individual.fitness(),
                reverse=maximize_fitness)[:2]
            pairs.append((selected_mates[0], selected_mates[1]))

        return pairs


class BestFitnessSurvivorSelector(SurvivorSelector, ABC):
    @staticmethod
    def select_survivors(population_size: int, parents: List[Individual],
                         breed: List[Individual],
                         maximize_fitness: bool) -> List[Individual]:
        parents.sort(key=lambda individual: individual.fitness(),
                     reverse=maximize_fitness)
        breed.sort(key=lambda individual: individual.fitness(),
                   reverse=maximize_fitness)
        new_generation_individuals = []

        i, j = 0, 0
        while i + j < population_size:
            if i == len(parents) and j == len(breed):
                break
            if i == len(parents):
                new_generation_individuals.append(breed[j])
                j += 1
            elif j == len(breed):
                new_generation_individuals.append(parents[i])
                i += 1
            elif parents[i].fitness() < breed[j].fitness():
                new_generation_individuals.append(breed[j])
                j += 1
            elif parents[i].fitness() > breed[j].fitness():
                new_generation_individuals.append(parents[i])
                i += 1
            else:
                # The same fitness
                new_generation_individuals.append(breed[j])
                i += 1

        return new_generation_individuals


class RouletteSurvivorSelector(SurvivorSelector, ABC):
    @staticmethod
    def select_survivors(population_size: int, parents: List[Individual],
                         breed: List[Individual],
                         maximize_fitness: bool) -> List[Individual]:
        new_generation_individuals: List[Individual] = []
        roulette = Roulette(parents + breed, maximize_fitness)

        return [roulette.get_individual() for _ in range(population_size)]


class GenerationalSurvivorSelector(SurvivorSelector, ABC):
    @staticmethod
    def select_survivors(population_size: int, parents: List[Individual],
                         breed: List[Individual],
                         maximize_fitness: bool) -> List[Individual]:
        new_generation_individuals = parents + breed

        avg_gen = mean([
            individual.generation for individual in new_generation_individuals
        ])
        avg_gen = 1.0 if avg_gen == 0.0 else avg_gen

        avg_fitness = mean([
            individual.fitness() for individual in new_generation_individuals
        ])
        avg_fitness = 1.0 if avg_fitness == 0.0 else avg_fitness

        def score(ind: Individual) -> float:
            fitness = ind.fitness()
            gen = ind.generation

            return (fitness / avg_fitness) * (gen / avg_gen)

        new_generation_individuals.sort(key=score, reverse=maximize_fitness)
        return new_generation_individuals[:population_size]


class KBestFitnessSolutionSelector(SolutionSelector, ABC):
    def __init__(self,
                 number_solutions: int,
                 maximize_fitness: bool,
                 custom_data: Dict = {}) -> None:
        super().__init__(number_solutions, maximize_fitness, custom_data)
        self._best_individuals: List[Individual] = []

    @property
    def best_individual(self) -> Individual:
        return self._best_individuals[-1]

    @property
    def best_individuals(self) -> List[Individual]:
        return self._best_individuals

    def update_individuals(self, population: List[Individual]) -> None:
        self.best_individuals.sort(key=lambda individual: individual.fitness(),
                                   reverse=self.maximize_fitness)
        population.sort(key=lambda individual: individual.fitness(),
                        reverse=self.maximize_fitness)
        new_best_individuals: List[Individual] = []
        comparison = ge if self.maximize_fitness else le

        i, j = 0, 0
        while len(new_best_individuals) < self.number_solutions:
            if i == len(population) and j == len(self.best_individuals):
                break
            elif i == len(population):
                new_best_individuals.append(self.best_individuals[j])
                j += 1
            elif j == len(self.best_individuals):
                new_best_individuals.append(deepcopy(population[i]))
                i += 1
            elif comparison(self.best_individuals[j].fitness(),
                            population[i].fitness()):
                new_best_individuals.append(self.best_individuals[j])
                j += 1
            else:
                new_best_individuals.append(deepcopy(population[i]))
                i += 1

        self.best_individuals.clear()
        self.best_individuals.extend(new_best_individuals)
