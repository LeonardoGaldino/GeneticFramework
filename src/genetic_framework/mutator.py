from typing import Generic
from abc import ABC, abstractmethod

from genetic_framework.chromosome import ChromosomeT
from genetic_framework.custom_data import CustomDataHolder


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
