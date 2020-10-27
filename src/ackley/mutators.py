from random import gauss
from abc import ABC
from typing import Type
from math import sqrt, exp

from genetic_framework.mutator import Mutator
from genetic_framework.fitness import FitnessComputer
from ackley.chromosomes import FloatChromosome, AdaptiveStepFloatChromosome
from ackley.util import clamp


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
            new_val = clamp(new_val, lower_bound, upper_bound)
            gene.data = new_val

        new_fitness: float = fitness_computer.fitness(chromosome)

        if (new_fitness > old_fitness):
            cls.successful_mutations += 1


class AdaptiveStepMutator(Mutator[AdaptiveStepFloatChromosome], ABC):
    @classmethod
    def learning_rate(cls: Type) -> float:
        generation: int = cls.custom_data['generation']
        lr_multiplier: float = cls.custom_data['learning_rate_multiplier']
        return lr_multiplier / sqrt(generation)

    @classmethod
    def mutate_inplace(cls: Type,
                       chromosome: AdaptiveStepFloatChromosome) -> None:
        lower_bound: float = cls.custom_data['lower_bound']
        upper_bound: float = cls.custom_data['upper_bound']
        lr = cls.learning_rate()

        for gene in chromosome.genotypes:
            new_delta = gene.data[1] * exp(lr * gauss(0, 1))
            new_value = gene.data[0] + new_delta * gauss(0, 1)
            new_value = clamp(new_value, lower_bound, upper_bound)
            gene.data = (new_value, new_delta)
