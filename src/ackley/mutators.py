from random import gauss
from abc import ABC
from typing import Type
from math import sqrt, exp, radians, tan, pi
from numpy.random import multivariate_normal  #type: ignore
import numpy as np  #type: ignore

from genetic_framework.mutator import Mutator
from genetic_framework.fitness import FitnessComputer
from ackley.chromosomes import FloatChromosome, AdaptiveStepFloatChromosome, CovarianceFloatChromosome
from ackley.util import clamp, sign


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
        n: int = cls.custom_data['n']
        lr_multiplier: float = cls.custom_data['learning_rate_multiplier']
        return lr_multiplier / sqrt(n)

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


class CovarianceMutator(Mutator[CovarianceFloatChromosome], ABC):
    @classmethod
    def learning_rate(cls: Type) -> float:
        generation: int = cls.custom_data['generation']
        lr_multiplier: float = cls.custom_data['learning_rate_multiplier']
        return lr_multiplier / sqrt(generation)

    @classmethod
    def mutate_inplace(cls: Type,
                       chromosome: CovarianceFloatChromosome) -> None:
        n: int = cls.custom_data['n']
        lower_bound: float = cls.custom_data['lower_bound']
        upper_bound: float = cls.custom_data['upper_bound']
        lr = cls.learning_rate()

        variables = chromosome.genotypes[:n]
        step_sizes = chromosome.genotypes[n:(2 * n)]
        rotation_angles = chromosome.genotypes[(2 * n):]

        for gene in step_sizes:
            gene.data = gene.data * exp(lr * gauss(0, 1))

        for gene in rotation_angles:
            gene.data = gene.data * radians(5) * gauss(0, 1)
            if gene.data > pi:
                gene.data = gene.data - 2 * pi * sign(gene.data)

        means = np.zeros((n))
        covariance_matrix = np.zeros((n, n))

        k = 0
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    covariance_matrix[i][j] = step_sizes[i].data**2
                else:
                    value = 0.5 * (step_sizes[i].data**2 - step_sizes[j].data**
                                   2) * tan(rotation_angles[k].data)
                    covariance_matrix[i][j] = covariance_matrix[j][i] = value
                    k += 1

        offsets = multivariate_normal(means, covariance_matrix)
        for i in range(n):
            variables[i].data = variables[i].data + offsets[i]
            variables[i].data = clamp(variables[i].data, lower_bound,
                                      upper_bound)
