from typing import List, Type, Callable, TypeVar
from functools import lru_cache
from copy import deepcopy
from random import random, randint
from math import sqrt
from statistics import mean, stdev

from genetic_framework.individual import Individual
from genetic_framework.selectors import SurvivorSelector, MatingSelector

T = TypeVar('T')


def clear_caches_after(fn: Callable[..., T]) -> Callable[..., T]:
    # Decorator for clearing Population cache after given method execution
    def wrapper(self, *args):
        res = fn(self, *args)
        self.avg_fitness.cache_clear()
        self.sd_fitness.cache_clear()

        return res

    return wrapper


class Population:
    def __init__(self, population: List[Individual], crossover_prob: float,
                 mutation_prob: float, breed_size: int, num_parent_pairs: int,
                 maximize_fitness: bool,
                 mating_selector_cls: Type[MatingSelector],
                 survivor_selector_cls: Type[SurvivorSelector]) -> None:
        self.population = population
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.breed_size = breed_size
        self.num_parent_pairs = num_parent_pairs
        self.maximize_fitness = maximize_fitness
        self.mating_selector_cls = mating_selector_cls
        self.survivor_selector_cls = survivor_selector_cls
        self.generation = 1

    def _offspring(self) -> List[Individual]:
        """Internal method used to create a list of new individuals (breed)
        from the current generation."""

        breed = []

        # if population has a single individual return a copies of it (may suffer mutation)
        if len(self.population) == 1:
            for _ in range(self.num_parent_pairs * self.breed_size):
                new_individual = deepcopy(self.population[0])

                mutation_r = random()
                if mutation_r < self.mutation_prob:
                    new_individual.self_mutate()

                new_individual.generation = self.generation
                breed.append(new_individual)

            return breed

        parents = self.mating_selector_cls.select_couples(
            self.population, self.num_parent_pairs, self.maximize_fitness)

        for (p1, p2) in parents:
            for _ in range(self.breed_size):
                # Generate child maybe cloned from parents
                crossover_r = random()
                if crossover_r < self.crossover_prob:
                    breed.append(p1.recombine(p2))
                else:
                    chosen_parent_clone = p1 if randint(0, 1) == 0 else p2
                    chosen_parent_clone = deepcopy(chosen_parent_clone)
                    breed.append(chosen_parent_clone)

                breed[-1].generation = self.generation

                # Maybe mutate generated child
                mutation_r = random()
                if mutation_r < self.mutation_prob:
                    breed[-1].self_mutate()

        return breed

    @clear_caches_after
    def evolve(self) -> None:
        """Method used to evolve the population into the next generation"""
        breed = self._offspring()
        survivors = self.survivor_selector_cls.select_survivors(
            len(self.population), self.population, breed,
            self.maximize_fitness)
        self.population = survivors
        self.generation += 1

    @clear_caches_after
    def restart_population(self) -> None:
        for individual in self.population:
            individual.initialize()

    @lru_cache
    def avg_fitness(self) -> float:
        return mean([individual.fitness() for individual in self.population])

    @lru_cache
    def sd_fitness(self) -> float:
        if (len(self.population) < 2):
            return 0

        return stdev([individual.fitness() for individual in self.population],
                     self.avg_fitness())
