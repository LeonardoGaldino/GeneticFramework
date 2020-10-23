from random import gauss
from abc import ABC
from typing import Type
from math import cos, exp, sqrt, e

from genetic_framework.mutator import Mutator
from genetic_framework.fitness import FitnessComputer
from ackley.chromosomes import FloatChromosome


class DeltaMutator(Mutator[FloatChromosome], ABC):
    step_multiplier = 0.99
    total_mutations: int = 0
    successful_mutations: int = 0
    current_step_size: float = 0

    @classmethod
    def mutate_inplace(cls: Type, chromosome: FloatChromosome) -> None:
        # Initialize step_size
        if (cls.current_step_size == 0):
            cls.current_step_size = cls.custom_data['step_size']

        lower_bound: float = cls.custom_data['lower_bound']
        upper_bound: float = cls.custom_data['upper_bound']
        fitness_computer: Type[FitnessComputer] = cls.custom_data[
            'fitness_computer']

        old_fitness: float = fitness_computer.fitness(chromosome)
        cls.total_mutations += 1

        if 5 * cls.successful_mutations > cls.total_mutations:
            cls.current_step_size *= cls.step_multiplier
        elif 5 * cls.successful_mutations < cls.total_mutations:
            cls.current_step_size /= cls.step_multiplier

        for gene in chromosome.genotypes:
            delta = gauss(0, cls.current_step_size)
            new_val = gene.data + delta

            # Avoid moving gene data outside boundaries
            new_val = min(upper_bound, max(lower_bound, new_val))
            gene.data = new_val

        new_fitness: float = fitness_computer.fitness(chromosome)

        if (new_fitness > old_fitness):
            cls.successful_mutations += 1
