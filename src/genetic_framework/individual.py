from typing import Generic, Dict, Type
from functools import lru_cache

from genetic_framework.chromosome import ChromosomeT
from genetic_framework.fitness import FitnessComputer
from genetic_framework.mutator import Mutator
from genetic_framework.recombiner import Recombiner


class Individual(Generic[ChromosomeT]):
    """Class representing a Individual.

    chromosome_cls: The individual's chromosome type
    fitness_computer_cls: Class for computing fitness.
    mutator_cls: Class for mutating the individual.
    recombiner_cls: Class for recombining individual with another one.
    """
    
    def __init__(self, chromosome_cls: Type[ChromosomeT],
            fitness_computer_cls: Type[FitnessComputer],
            mutator_cls: Type[Mutator], 
            recombiner_cls: Type[Recombiner],
            generation: int = 1,
            custom_data: Dict = {}) -> None:
        self.chromosome_cls = chromosome_cls
        self.fitness_computer_cls = fitness_computer_cls
        self.mutator_cls = mutator_cls
        self.recombiner_cls = recombiner_cls
        self.generation = generation
        self.custom_data = custom_data
        
        self._chromosome = self.chromosome_cls(custom_data)

    def initialize(self) -> 'Individual':
        self.chromosome.initialize()
        return self

    @property
    def chromosome(self) -> ChromosomeT:
        return self._chromosome

    @chromosome.setter
    def chromosome(self, new_chromosome: ChromosomeT) -> None:
        self.fitness.cache_clear()
        self._chromosome = new_chromosome

    # Caches fitness computation to avoid wasting CPU time
    @lru_cache
    def fitness(self) -> float:
        return self.fitness_computer_cls.fitness(self.chromosome)

    def self_mutate(self) -> 'Individual':
        """Use mutator to change this individual chromosome and return itself"""
        self.mutator_cls.mutate_inplace(self.chromosome)
        self.fitness.cache_clear()
        return self

    def recombine(self, other: 'Individual') -> 'Individual':
        """Use recombiner to combine this individual with other argument
        to generate a new individual"""
        new_chromosome = self.recombiner_cls.recombine(self.chromosome,\
                other.chromosome)

        return self.new_individual(new_chromosome, self.generation + 1)
            
    def new_individual(self, chromosome: ChromosomeT, generation: int = 1) -> 'Individual':
        """Returns a new individual with the given gene using the same fitness
        computer, genemutator, recombiner of this individual"""
        new_individual = Individual(self.chromosome_cls, self.fitness_computer_cls, 
            self.mutator_cls, self.recombiner_cls, generation, self.custom_data)
        new_individual.chromosome = chromosome

        return new_individual

    def __str__(self) -> str:
        return str(self.chromosome)

    def __repr__(self) -> str:
        return self.__str__()
