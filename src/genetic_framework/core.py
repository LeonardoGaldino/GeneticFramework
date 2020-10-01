"""Module containing core classes for genetic algorithms."""
from abc import ABC, abstractmethod
from typing import Type, List, Tuple, TypeVar, Generic, Dict
from functools import lru_cache


""" TypeVariable for Generic types Chromosome, Phenotype, Genotype since each
subclass of these will use its own data type to represent its internal data.
"""
T = TypeVar('T')


class Phenotype(Generic[T], ABC):

    @abstractmethod
    def __init__(self, custom_data: Dict = {}) -> None:
        self.custom_data = custom_data

    # (https://github.com/python/mypy/issues/4165)
    @property # type:ignore
    @abstractmethod
    def data(self) -> T:
        ...

    # (https://github.com/python/mypy/issues/4165)
    @data.setter # type:ignore
    @abstractmethod
    def data(self, new_data: T) -> None:
        ... 

    @abstractmethod
    def __str__(self) -> str:
        ...


class Genotype(Generic[T], ABC):
    """Defines an abstract class for holding information about Genes."""

    @abstractmethod
    def __init__(self, custom_data: Dict = {}) -> None:
        self.custom_data = custom_data

    @abstractmethod
    def initialize(self) -> None:
        """Initialize itself with random values possibly following some policy.
        This method doesn't return another instance, just modifies the current."""
        ...

    # (https://github.com/python/mypy/issues/4165)
    @property # type:ignore
    @abstractmethod
    def data(self) -> T:
        """Property containing the gene's data."""
        ...

    # (https://github.com/python/mypy/issues/4165)
    @data.setter # type:ignore
    @abstractmethod
    def data(self, new_data: T) -> None:
        """Set data property (contains the gene's data)."""
        ...
    
    @abstractmethod
    def __str__(self) -> str:
        ...


""" Python's method override is invariant, hence we cannot override methods 
with specific types of Pheno/GenoTypes, only with their base class. For more
details on why this is a problem and why the below TypeVars addresses this,
check details on top of ChromosomeT TypeVar (right below Chromosome class
definition).
"""
PhenotypeT = TypeVar('PhenotypeT', bound=Phenotype)
GenotypeT = TypeVar('GenotypeT', bound=Genotype)

class Chromosome(Generic[T, PhenotypeT, GenotypeT], ABC):

    @abstractmethod
    def __init__(self, custom_data: Dict = {}) -> None:
        self.custom_data = custom_data

    @staticmethod
    @abstractmethod
    def genotype_to_phenotype(gene: GenotypeT, **kwargs) -> PhenotypeT:
        ...

    @abstractmethod
    def initialize(self) -> None:
        ...

    @abstractmethod
    def genotypes(self) -> List[GenotypeT]:
        ...

    @abstractmethod
    def phenotypes(self) -> List[PhenotypeT]:
        ...

    # (https://github.com/python/mypy/issues/4165)
    @property # type:ignore
    @abstractmethod
    def data(self) -> T:
        ...

    # (https://github.com/python/mypy/issues/4165)
    @data.setter # type:ignore
    @abstractmethod
    def data(self, new_data: T) -> None:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

""" Python's method override is invariant, hence we cannot override methods 
with specific types of Chromosome, only with Chromosome base class. This is
a problem, because we want a subclass of FitnessComputer, for example, to be
able to compute fitness method over a specific subclass of Chromosome, not 
against Chromosome base class. For this we create a TypeVar to use with
Generics and make it Covariant. That way, subclasses of FitnessComputer will
specify which type of Chromosome they work with.
"""
ChromosomeT = TypeVar('ChromosomeT', bound=Chromosome)


class CustomDataHolder:
    """Class that defines custom_data: data that some subclasses need to have
    in its class object, not in an instance.
    """
    custom_data: Dict = {}

    @classmethod
    def set_custom_data(cls, custom_data: Dict) -> None:
        cls.custom_data = custom_data


class FitnessComputer(Generic[ChromosomeT], CustomDataHolder, ABC):
    """Defines an abstract class for for types that knows how to compute the 
    fitness for a given type of Chromosome. Subclasses should specify
    through inheritance the kind of Chromosome it works for:

    class SubClassFitnessComputer(FitnessComputer[SubClassChromosome])...

    Then, fitness method can receive SubClassChromosome safely typechecked.
    """

    @staticmethod
    @abstractmethod
    def fitness(chromosome: ChromosomeT) -> float:
        """Computes fitness for a given Chromosome. Subclasses should specify
        the correct type of Chromosome as parameter. 
        (Accordingly to the ChromosomeType specified at the class declaration)
        """
        ...


class Mutator(Generic[ChromosomeT], CustomDataHolder, ABC):
    """Abstract class that represents Mutators. Mutators can modify Genotypes.
    Subclasses should specify through inheritance the kind of Chromosome it 
    works for: 

    class SubClassMutator(Mutator[SubClassChromosome])...

    Then, mutate and mutate_inplace methods can receive SubClassChromosome 
    safely typechecked.
    """

    @staticmethod
    @abstractmethod
    def mutate(chromosome: ChromosomeT) -> ChromosomeT:
        """Mutate a given chromosome into a new one. Subclasses should specify
        the correct type of Chromosome as parameter. 
        (Accordingly to the ChromosomeType specified at the class declaration)
        """
        ...

    @staticmethod
    @abstractmethod
    def mutate_inplace(chromosome: ChromosomeT) -> None:
        """Mutate a given chromosome (modifying it, not returning a new one). 
        Subclasses should specify the correct type of Chromosome as parameter. 
        (Accordingly to the ChromosomeType specified at the class declaration)
        """
        ...


class Recombiner(Generic[ChromosomeT], CustomDataHolder, ABC):
    """Abstract class that represents Recombiners. Recombiners knows how to
    combine two Chromosomes into a new one. Subclasses should specify 
    through inheritance the kind of Chromosome it works for:

    class SubClassRecombiner(Recombiner[SubClassChromosome])...

    Then, recombine method can receive SubClassChromosome safely typechecked.
    """
    
    @staticmethod
    @abstractmethod
    def recombine(chromosome1: ChromosomeT, chromosome2: ChromosomeT) -> ChromosomeT:
        """Recombines two Chromosomes into a new one. Subclasses should 
        specify the correct type of Chromosome as parameter.
        (Accordingly to the ChromosomeType specified at the class declaration)
        """
        ...


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
            custom_data: Dict = {}) -> None:
        self.chromosome_cls = chromosome_cls
        self.fitness_computer_cls = fitness_computer_cls
        self.mutator_cls = mutator_cls
        self.recombiner_cls = recombiner_cls
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

        return self.new_individual(new_chromosome)
            
    def new_individual(self, chromosome: ChromosomeT) -> 'Individual':
        """Returns a new individual with the given gene using the same fitness
        computer, genemutator, recombiner of this individual"""
        new_individual = Individual(self.chromosome_cls, self.fitness_computer_cls, 
            self.mutator_cls, self.recombiner_cls, self.custom_data)
        new_individual.chromosome = chromosome

        return new_individual

    def __str__(self) -> str:
        return str(self.chromosome)


class MatingSelector(CustomDataHolder, ABC):
    
    @staticmethod
    @abstractmethod
    def select_couples(population: List[Individual]) -> List[Tuple[Individual, Individual]]:
        """Pairs individuals to mate and produce children. Subclass should
        implement this logic of selecting individual to mate."""
        ...


class SurvivorSelector(CustomDataHolder, ABC):
    """Class responsible for selecting survivors for the following
    generation. Subclasses should implement this logic."""


    @staticmethod
    @abstractmethod
    def select_survivors(population_size: int, parents: List[Individual],
        breed: List[Individual]) -> List[Individual]:
        """Implements logic of choosing which individuals will survive to next
        generation."""
        ...


class Population:

    def __init__(self, population: List[Individual], crossover_prob: float,
            mutation_prob: float, breed_size: int, 
            mating_selector_cls: Type[MatingSelector], 
            survivor_selector_cls: Type[SurvivorSelector]) -> None:
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

    def evolve(self) -> None:
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



class IndividualSelector(ABC):
    """
    Responsible for best individuals selection logic on a running experiment
    """

    @abstractmethod
    def __init__(self, number_solutions: int, custom_data: Dict = {}) -> None:
        self.number_solutions = number_solutions
        self.custom_data = custom_data
    
    @property
    @abstractmethod
    def best_individuals(self) -> List[Individual]:
        """Returns the best individuals selected and stored so far."""
        ...

    @abstractmethod
    def update_individuals(self, population: Population) -> None:
        """Updates (if necessary) the list of best individuals with 
        individuals from the specified population."""
        ...


class Experiment(Generic[ChromosomeT]):
    
    def __init__(self, population_size: int, max_generations: int, 
        crossover_prob: float, mutation_prob: float, num_solutions: int, 
        breed_size: int, chromosome_cls: Type[ChromosomeT], 
        fitness_computer_cls: Type[FitnessComputer], 
        mutator_cls: Type[Mutator],
        recombiner_cls: Type[Recombiner],
        mating_selector_cls: Type[MatingSelector],
        survivor_selector_cls: Type[SurvivorSelector],
        individual_selector_cls: Type[IndividualSelector],
        custom_data: Dict = {}) -> None:
        self.population_size = population_size
        self.max_generations = max_generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.num_solutions = num_solutions
        self.breed_size = breed_size
        self.chromosome_cls = chromosome_cls

        self.fitness_computer_cls = fitness_computer_cls
        self.fitness_computer_cls.set_custom_data(custom_data)

        self.mutator_cls = mutator_cls
        self.mutator_cls.set_custom_data(custom_data)
        
        self.recombiner_cls = recombiner_cls
        self.recombiner_cls.set_custom_data(custom_data)
        
        self.mating_selector_cls = mating_selector_cls
        self.mating_selector_cls.set_custom_data(custom_data)

        self.survivor_selector_cls = survivor_selector_cls
        self.survivor_selector_cls.set_custom_data(custom_data)

        self.individual_selector_cls = individual_selector_cls
        self.custom_data = custom_data

    def _generate_initial_individuals(self) -> List[Individual]:
        """Internal method used to generate individuals for the first 
        generation of the experiment"""
        return [Individual(self.chromosome_cls, self.fitness_computer_cls, 
            self.mutator_cls, self.recombiner_cls, self.custom_data).initialize()
                for i in range(self.population_size)]

    def run_experiment(self) -> List[Individual]:

        initial_individuals = self._generate_initial_individuals()
        population = Population(initial_individuals, self.crossover_prob, 
            self.mutation_prob, self.breed_size, self.mating_selector_cls,
            self.survivor_selector_cls)
        solution_selector = self.individual_selector_cls(self.num_solutions, self.custom_data)

        for i in range(self.max_generations):
            print("Evolving Generation {}: {} average fitness..."
                .format(i+1, population.avg_fitness()))
            population.evolve()
            solution_selector.update_individuals(population)
        print("Maximum generations achieved: {} average fitness."
            .format(population.avg_fitness()))

        return solution_selector.best_individuals
            
