from typing import Generic, Type
from abc import ABC, abstractmethod
from copy import deepcopy
from random import randint

from genetic_framework.chromosome import ChromosomeT, Chromosome
from genetic_framework.custom_data import CustomDataHolder


class Mutator(Generic[ChromosomeT], CustomDataHolder, ABC):
    """Abstract class that represents Mutators. Mutators can modify Genotypes.
    Subclasses should specify through inheritance the kind of Chromosome it 
    works for: 

    class SubClassMutator(Mutator[SubClassChromosome])...

    Then, mutate and mutate_inplace methods can receive SubClassChromosome 
    safely typechecked.
    """
    @classmethod
    def mutate(cls: Type, chromosome: ChromosomeT) -> ChromosomeT:
        """Mutate a given chromosome into a new one. Subclasses should specify
        the correct type of Chromosome as parameter. 
        (Accordingly to the ChromosomeType specified at the class declaration)
        """
        new_chromosome = deepcopy(chromosome)
        cls.mutate_inplace(new_chromosome)
        return new_chromosome

    @classmethod
    @abstractmethod
    def mutate_inplace(cls: Type, chromosome: ChromosomeT) -> None:
        """Mutate a given chromosome (modifying it, not returning a new one). 
        Subclasses should specify the correct type of Chromosome as parameter. 
        (Accordingly to the ChromosomeType specified at the class declaration)
        """
        ...


class SwapGeneMutator(Mutator[Chromosome], ABC):
    @classmethod
    def mutate_inplace(cls: Type, chromosome: Chromosome) -> None:
        number_genes = len(chromosome.genotypes)

        r1 = randint(0, number_genes - 1)
        r2 = randint(0, number_genes - 1)
        while r1 == r2:
            r2 = randint(0, number_genes - 1)

        genes = chromosome.genotypes

        # Swap genes
        genes[r1], genes[r2] = genes[r2], genes[r1]
        chromosome.genotypes = genes  # type: ignore


class SwapGeneRangeMutator(Mutator[Chromosome], ABC):
    @classmethod
    def mutate_inplace(cls: Type, chromosome: Chromosome) -> None:
        number_genes = len(chromosome.genotypes)

        l = randint(0, number_genes - 1)
        r = randint(l, number_genes - 1)

        genes = chromosome.genotypes
        _range = genes[l:r + 1]
        _range.reverse()

        chromosome.genotypes = genes[:l] + _range + genes[r +  # type: ignore
                                                          1:]
