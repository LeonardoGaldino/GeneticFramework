from typing import List, Dict, Generic, TypeVar
from abc import ABC, abstractmethod


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

    @abstractmethod
    def __repr__(self) -> str:
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

    @abstractmethod
    def __repr__(self) -> str:
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

    @abstractmethod
    def __repr__(self) -> str:
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