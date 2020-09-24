"""Module containing core classes for genetic algorithms."""
from abc import ABC, abstractmethod
from typing import Any, Type, List, Tuple
from functools import lru_cache


class Gene(ABC):
    """Defines an abstract class for holding information about individuals."""

    @abstractmethod
    def initialize(self):
        """Initialize itself with random values possibly following some policy.
        This method doesn't return another instance, just modifies the current."""
        pass

    @property
    @abstractmethod
    def data(self) -> Any:
        """Property containing the gene's data. Type should not be specified."""
        pass

    @data.setter
    @abstractmethod
    def data(self, new_data: Any) -> Any:
        """Set data property (contains the gene's data). Type should not be specified."""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass


class GeneTypeSpecifier(ABC):
    """Class used to specify subclasses that must define the type of gene it
    works with."""

    @staticmethod
    @abstractmethod
    def gene_cls() -> Type[Gene]:
        """Defines the type of gene the subclass will work for. Subclasses
        should return the Gene CLASS, not an instance of Gene.
        """
        pass


# Decorator for validating each gene parameter for the specified class gene type
def validate_gene_args(m):
    def wrapper(*args):
        # args[0] should be 'cls': the class reference.
        # it should contain gene_cls method: be instance of GeneTypeSpecifier
        if not hasattr(args[0], 'gene_cls') or not callable(args[0].gene_cls):
             raise AttributeError(
                'Decorated method with validate_gene_cls should be in GeneTypeSpecifier subclass.'
                )

        # Validate each gene parameter
        gene_cls = args[0].gene_cls()
        for i in range(1, len(args)):
            if not isinstance(args[i], gene_cls):
                raise TypeError("Gene '{}' is not a supported type for class '{}'."
                    .format(args[i].__class__.__name__, args[0].__name__))

        return m(*args)
    return wrapper


class FitnessComputer(GeneTypeSpecifier, ABC):
    """Defines an abstract class for for types that knows how to compute fitness
    for a given type of Gene.
    """

    @classmethod
    @abstractmethod
    def fitness(cls: Type['FitnessComputer'], gene: Gene) -> float:
        """Computes fitness for a given Gene. Implementations should use
        @validate_gene_args to ensure gene arg has correct type.
        """
        pass


class GeneMutator(GeneTypeSpecifier, ABC):
    """Abstract class that models Mutators. Subclasses should specify the 
    type of gene it works with through gene_cls() static method."""

    @classmethod
    @abstractmethod
    def mutate(cls: Type['GeneMutator'], gene: Gene) -> Gene:
        """Mutate a given gene into a new one. Implementations should use
        @validate_gene_args to ensure gene arg has correct type.
        """
        pass

    @classmethod
    @abstractmethod
    def mutate_inplace(cls: Type['GeneMutator'], gene: Gene):
        """Mutate a given gene modifying the argument. Implementations should use
        @validate_gene_args to ensure gene arg has correct type.
        """
        pass


class GeneRecombiner(GeneTypeSpecifier, ABC):
    """Abstract class that models Recombiners. Subclasses should specify the 
    type of gene it works with through gene_cls() static method."""
    
    @classmethod
    @abstractmethod
    def recombine(cls: Type['GeneRecombiner'], gene1: Gene, gene2: Gene) -> List[Gene]:
        """Recombines two genes into a list (possible singleton) of new genes.
        Implementations should use @validate_gene_args to ensure gene arg has 
        correct type.
        """
        pass


class Individual:
    """Class representing a Individual.

        gene_cls: The individual's gene class.
        fitness_computer_cls: Class for computing fitness.
        gene_mutator_cls: Class for mutating the individual.
        gene_recombiner_cls: Class for recombining individual with another one.
    """
    
    def __init__(self, gene_cls: Type[Gene],
            fitness_computer_cls: Type[FitnessComputer],
            gene_mutator_cls: Type[GeneMutator], 
            gene_recombiner_cls: Type[GeneRecombiner]):
        self.gene_cls = gene_cls
        self.fitness_computer_cls = fitness_computer_cls
        self.gene_mutator_cls = gene_mutator_cls
        self.gene_recombiner_cls = gene_recombiner_cls
        
        self.gene = self.gene_cls()

    def initialize_gene(self) -> 'Individual':
        self.gene.initialize()
        return self

    def set_gene(self, gene: Gene) -> 'Individual':
        self.gene = gene
        return self

    # Caches fitness computation to avoid wasting CPU time
    @lru_cache
    def fitness(self) -> float:
        return self.fitness_computer_cls.fitness(self.gene)

    def self_mutate(self) -> 'Individual':
        self.gene_mutator_cls.mutate_inplace(self.gene)
        self.fitness.cache_clear()
        return self

    def recombine(self, other: 'Individual') -> List['Individual']:
        return list(map(lambda gene: self.new_individual(gene), 
            self.gene_recombiner_cls.recombine(self.gene, other.gene)))

    def new_individual(self, gene: Gene) -> 'Individual':
        return Individual(self.gene_cls, self.fitness_computer_cls, 
            self.gene_mutator_cls, self.gene_recombiner_cls).set_gene(gene)

    def __str__(self) -> str:
        return self.gene.__str__()


class MatingSelector(ABC):
    
    @staticmethod
    @abstractmethod
    def select_couples(List[Individual]) -> List[Tuple(Individual)]:
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
        # Use mating_selector to choose parents and recombine them
        pass 

    def _kill_population(self):
        # Use survivor_selector to choose parents and recombine them
        pass

    def evolve(self):
        """ Update the object with new individuals: use internal methods
        _offspring and _kill_population"""
        pass


"""
Responsible for best individuals selection logic on a running experiment
"""
class IndividualSelector(ABC):
    
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
        breed_size: int, gene_cls: Type[Gene], 
        fitness_computer_cls: Type[FitnessComputer], 
        mutator_cls: Type[GeneMutator],
        recombiner_cls: Type[GeneRecombiner],
        mating_selector_cls: Type[MatingSelector],
        survivor_selector_cls: Type[SurvivorSelector],
        individual_selector_cls: Type[IndividualSelector]):
        pass