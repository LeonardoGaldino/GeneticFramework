from typing import List, Type
from functools import lru_cache
from random import random, randint
from math import sqrt
from statistics import mean, stdev

from genetic_framework.individual import Individual
from genetic_framework.selectors import SurvivorSelector, MatingSelector


class Population:

    def __init__(self, population: List[Individual], crossover_prob: float,
            mutation_prob: float, breed_size: int, num_parent_pairs: int,
            mating_selector_cls: Type[MatingSelector], 
            survivor_selector_cls: Type[SurvivorSelector]) -> None:
        self.population = population
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.breed_size = breed_size
        self.num_parent_pairs = num_parent_pairs
        self.mating_selector_cls = mating_selector_cls
        self.survivor_selector_cls = survivor_selector_cls
        self.generation = 1

    def _offspring(self) -> List[Individual]:
        """Internal method used to create a list of new individuals (breed)
        from the current generation."""
        parents = self.mating_selector_cls \
            .select_couples(self.population, self.num_parent_pairs)
        breed = []

        for (p1, p2) in parents:
            for i in range(self.breed_size):
                # Generate child maybe cloned from parents
                crossover_r = random()
                if crossover_r < self.crossover_prob:
                    breed.append(p1.recombine(p2))
                else:
                    chosen_parent_clone = p1 if randint(0, 1) == 0 else p2
                    breed.append(chosen_parent_clone)

                breed[-1].generation = self.generation

                # Maybe mutate generated child
                mutation_r = random()
                if mutation_r < self.mutation_prob:
                    breed[-1].self_mutate()

        return breed

    def evolve(self) -> None:
        """Method used to evolve the population into the next generation"""
        breed = self._offspring()
        survivors = self.survivor_selector_cls.select_survivors(len(self.population),
            self.population, breed)
        self.population = survivors
        self.generation += 1
        self.avg_fitness.cache_clear()
        self.sd_fitness.cache_clear()

    @lru_cache
    def avg_fitness(self) -> float:
        return mean([individual.fitness() for individual in self.population])

    @lru_cache
    def sd_fitness(self) -> float:
        return stdev([individual.fitness() for individual
            in self.population], self.avg_fitness())
