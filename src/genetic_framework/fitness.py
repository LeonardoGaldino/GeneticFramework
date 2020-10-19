from typing import Generic, Type
from abc import ABC, abstractmethod

from genetic_framework.chromosome import ChromosomeT
from genetic_framework.custom_data import CustomDataHolder


class FitnessComputer(Generic[ChromosomeT], CustomDataHolder, ABC):
    """Defines an abstract class for for types that knows how to compute the 
    fitness for a given type of Chromosome. Subclasses should specify
    through inheritance the kind of Chromosome it works for:

    class SubClassFitnessComputer(FitnessComputer[SubClassChromosome])...

    Then, fitness method can receive SubClassChromosome safely typechecked.
    """
    @classmethod
    @abstractmethod
    def fitness(cls: Type, chromosome: ChromosomeT) -> float:
        """Computes fitness for a given Chromosome. Subclasses should specify
        the correct type of Chromosome as parameter. 
        (Accordingly to the ChromosomeType specified at the class declaration)
        """
        ...
