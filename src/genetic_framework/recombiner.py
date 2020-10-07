from typing import Generic
from abc import ABC, abstractmethod

from genetic_framework.chromosome import ChromosomeT
from genetic_framework.custom_data import CustomDataHolder


class Recombiner(Generic[ChromosomeT], CustomDataHolder, ABC):
    """Abstract class that represents Recombiners. Recombiners knows how to
    combine two Chromosomes into a new one. Subclasses should specify 
    through inheritance the kind of Chromosome it works for:

    class SubClassRecombiner(Recombiner[SubClassChromosome])...

    Then, recombine method can receive SubClassChromosome safely typechecked.
    """
    @staticmethod
    @abstractmethod
    def recombine(chromosome1: ChromosomeT,
                  chromosome2: ChromosomeT) -> ChromosomeT:
        """Recombines two Chromosomes into a new one. Subclasses should 
        specify the correct type of Chromosome as parameter.
        (Accordingly to the ChromosomeType specified at the class declaration)
        """
        ...
