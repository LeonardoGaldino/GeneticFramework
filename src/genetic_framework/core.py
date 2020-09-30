"""Module containing core classes for genetic algorithms."""
from abc import ABC, abstractmethod
from typing import Any, Type, List, Tuple
from functools import lru_cache


class Phenotype(ABC):

    @abstractmethod
    def __init__(self, **custom_data):
        self.custom_data = custom_data

    # (https://github.com/python/mypy/issues/4165)
    @property # type:ignore
    @abstractmethod
    def data(self) -> Any:
        pass

    # (https://github.com/python/mypy/issues/4165)
    @data.setter # type:ignore
    @abstractmethod
    def data(self, new_data: Any):
        pass 

    @abstractmethod
    def __str__(self) -> str:
        pass


class Genotype(ABC):
    """Defines an abstract class for holding information about individuals."""

    @abstractmethod
    def __init__(self, **custom_data):
        self.custom_data = custom_data

    @abstractmethod
    def initialize(self):
        """Initialize itself with random values possibly following some policy.
        This method doesn't return another instance, just modifies the current."""
        pass

    # (https://github.com/python/mypy/issues/4165)
    @property # type:ignore
    @abstractmethod
    def data(self) -> Any:
        """Property containing the gene's data. Type should not be specified."""
        pass

    # (https://github.com/python/mypy/issues/4165)
    @data.setter # type:ignore
    @abstractmethod
    def data(self, new_data: Any):
        """Set data property (contains the gene's data). Type should not be specified."""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass


class Chromosome(ABC):

    @abstractmethod
    def __init__(self, **custom_data):
        self.custom_data = custom_data

    @staticmethod
    @abstractmethod
    def genotype_to_phenotype(gene: Genotype) -> Phenotype:
        pass

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def genotypes(self) -> List[Genotype]:
        pass

    @abstractmethod
    def phenotypes(self) -> List[Phenotype]:
        pass

    # (https://github.com/python/mypy/issues/4165)
    @property # type:ignore
    @abstractmethod
    def data(self) -> Any:
        pass

    # (https://github.com/python/mypy/issues/4165)
    @data.setter # type:ignore
    @abstractmethod
    def data(self, new_data: Any):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class FitnessComputer(ABC):
    """Defines an abstract class for for types that knows how to compute fitness
    for a given type of Gene.
    """

    @staticmethod
    @abstractmethod
    def fitness(chromosome: Chromosome) -> float:
        """Computes fitness for a given Gene. Implementations should use
        @validate_gene_args to ensure gene arg has correct type.
        """
        pass


class Mutator(ABC):
    """Abstract class that models Mutators. Subclasses should specify the 
    type of gene it works with through gene_cls() static method."""

    @staticmethod
    @abstractmethod
    def mutate(chromosome: Chromosome) -> Chromosome:
        """Mutate a given gene into a new one. Implementations should use
        @validate_gene_args to ensure gene arg has correct type.
        """
        pass

    @staticmethod
    @abstractmethod
    def mutate_inplace(chromosome: Chromosome):
        """Mutate a given gene modifying the argument. Implementations should use
        @validate_gene_args to ensure gene arg has correct type.
        """
        pass


class Recombiner(ABC):
    """Abstract class that models Recombiners. Subclasses should specify the 
    type of gene it works with through gene_cls() static method."""
    
    @staticmethod
    @abstractmethod
    def recombine(chromosome1: Chromosome, chromosome2: Chromosome) -> Chromosome:
        """Recombines two genes into a new genes. Implementations should use 
        @validate_gene_args to ensure gene arg has correct type.
        """
        pass


class Individual:
    """Class representing a Individual.

        gene_clchromosome_clss: The individual's chromosome type
        fitness_computer_cls: Class for computing fitness.
        gene_mutator_cls: Class for mutating the individual.
        gene_recombiner_cls: Class for recombining individual with another one.
    """
    
    def __init__(self, chromosome_cls: Type[Chromosome],
            fitness_computer_cls: Type[FitnessComputer],
            mutator_cls: Type[Mutator], 
            recombiner_cls: Type[Recombiner],
            **chromosome_custom_data):
        self.chromosome_cls = chromosome_cls
        self.fitness_computer_cls = fitness_computer_cls
        self.mutator_cls = mutator_cls
        self.recombiner_cls = recombiner_cls
        
        self._chromosome = self.chromosome_cls(**chromosome_custom_data)

    def initialize(self) -> 'Individual':
        self.chromosome.initialize()
        return self

    @property
    def chromosome(self) -> Chromosome:
        return self._chromosome

    @chromosome.setter
    def chromosome(self, new_chromosome: Chromosome):
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

        return self.new_individual(new_chromosome)
            
    def new_individual(self, chromosome: Chromosome) -> 'Individual':
        """Returns a new individual with the given gene using the same fitness
        computer, genemutator, recombiner of this individual"""
        new_individual = Individual(self.chromosome_cls, self.fitness_computer_cls, 
            self.mutator_cls, self.recombiner_cls)
        new_individual.chromosome = chromosome

        return new_individual

    def __str__(self) -> str:
        return str(self.chromosome)


class MatingSelector(ABC):
    
    @staticmethod
    @abstractmethod
    def select_couples(population: List[Individual]) -> List[Tuple[Individual, Individual]]:
        """Pairs individuals to mate and produce children. Subclass should
        implement this logic of selecting individual to mate."""
        pass


class SurvivorSelector(ABC):
    """Class responsible for selecting survivors for the following
    generation. Subclasses should implement this logic."""


    @staticmethod
    @abstractmethod
    def select_survivors(population_size: int, parents: List[Individual],
        breed: List[Individual]) -> List[Individual]:
        """Implements logic of choosing which individuals will survive to next
        generation."""
        pass


class Population:

    def __init__(self, population: List[Individual], crossover_prob: float,
            mutation_prob: float, breed_size: int, 
            mating_selector_cls: Type[MatingSelector], 
            survivor_selector_cls: Type[SurvivorSelector]):
        self.population = population
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.breed_size = breed_size
        self.mating_selector_cls = mating_selector_cls
        self.survivor_selector_cls = survivor_selector_cls

    def _offspring(self) -> List[Individual]:
        """Internal method used to create a list of new individuals (breed)
        from the current generation."""
        parents = self.mating_selector_cls.select_couples(self.population)
        breed = [p1.recombine(p2) for i in range(self.breed_size) for (p1, p2)\
            in parents]

        return breed

    def evolve(self):
        """Method used to evolve the population into the next generation"""
        breed = self._offspring()
        survivors = self.survivor_selector_cls.select_survivors(len(self.population),
            self.population, breed)
        self.population = survivors
        self.avg_fitness.cache_clear()

    @lru_cache
    def avg_fitness(self) -> float:
        return sum(map(lambda individual: individual.fitness(), 
            self.population))/len(self.population)


"""
Responsible for best individuals selection logic on a running experiment
"""
class IndividualSelector(ABC):

    @abstractmethod
    def __init__(self, number_solutions: int):
        pass
    
    @property
    @abstractmethod
    def best_individuals(self) -> List[Individual]:
        """Returns the best individuals selected and stored so far."""
        pass

    @abstractmethod
    def update_individuals(self, population: Population):
        """Updates (if necessary) the list of best individuals with 
        individuals from the specified population."""
        pass


class Experiment:
    
    def __init__(self, population_size: int, max_generations: int, 
        crossover_prob: float, mutation_prob: float, num_solutions: int, 
        breed_size: int, chromosome_cls: Type[Chromosome], 
        fitness_computer_cls: Type[FitnessComputer], 
        mutator_cls: Type[Mutator],
        recombiner_cls: Type[Recombiner],
        mating_selector_cls: Type[MatingSelector],
        survivor_selector_cls: Type[SurvivorSelector],
        individual_selector_cls: Type[IndividualSelector],
        **custom_data):
        self.population_size = population_size
        self.max_generations = max_generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.num_solutions = num_solutions
        self.breed_size = breed_size
        self.chromosome_cls = chromosome_cls
        self.fitness_computer_cls = fitness_computer_cls
        self.mutator_cls = mutator_cls
        self.recombiner_cls = recombiner_cls
        self.mating_selector_cls = mating_selector_cls
        self.survivor_selector_cls = survivor_selector_cls
        self.individual_selector_cls = individual_selector_cls
        self.custom_data = custom_data

    def _generate_initial_individuals(self) -> List[Individual]:
        """Internal method used to generate individuals for the first 
        generation of the experiment"""
        return [Individual(self.chromosome_cls, self.fitness_computer_cls, 
            self.mutator_cls, self.recombiner_cls, **self.custom_data).initialize()
                for i in range(self.population_size)]

    def run_experiment(self) -> List[Individual]:
        initial_individuals = self._generate_initial_individuals()
        population = Population(initial_individuals, self.crossover_prob, 
            self.mutation_prob, self.breed_size, self.mating_selector_cls,
            self.survivor_selector_cls)
        solution_selector = self.individual_selector_cls(self.num_solutions)

        for i in range(self.max_generations):
            print("Evolving Generation {}: {} average fitness..."
                .format(i+1, population.avg_fitness()))
            population.evolve()
            solution_selector.update_individuals(population)
        print("Maximum generations achieved: {} average fitness."
            .format(population.avg_fitness()))

        return solution_selector.best_individuals
            
