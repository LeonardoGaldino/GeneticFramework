from typing import Dict, List
from random import randint
from functools import reduce
from copy import deepcopy

from ackley.phenotypes import FloatPhenotype, FloatPairPhenotype
from ackley.genotypes import FloatGenotype, FloatPairGenotype
from ackley.util import DataType
from genetic_framework.chromosome import Chromosome


class FloatChromosome(Chromosome[FloatPhenotype, FloatGenotype]):
    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)

        n: int = self.custom_data['n']
        self._genotypes = [FloatGenotype(self.custom_data) for _ in range(n)]

    def initialize(self) -> None:
        n: int = self.custom_data['n']

        self._genotypes = [FloatGenotype(self.custom_data) for _ in range(n)]
        for genotype in self._genotypes:
            genotype.initialize()

    @staticmethod
    def genotype_to_phenotype(gene: FloatGenotype, **_) -> FloatPhenotype:
        new_phenotype = FloatPhenotype(gene.custom_data)
        new_phenotype.data = gene.data
        return new_phenotype

    @staticmethod
    def phenotype_to_genotype(phenotype: FloatPhenotype, **_) -> FloatGenotype:
        new_gene = FloatGenotype(phenotype.custom_data)
        new_gene.data = phenotype.data
        return new_gene

    @property
    def genotypes(self) -> List[FloatGenotype]:
        return self._genotypes

    @genotypes.setter
    def genotypes(self, genes: List[FloatGenotype]) -> None:
        n: int = self.custom_data['n']
        if len(genes) != n:
            raise ValueError(
                'Tried to assign genotypes to FloatChromosome with wrong number of genes ({}). Expected {}.'
                .format(len(genes), n))

        self._genotypes = deepcopy(genes)

    @property
    def phenotypes(self) -> List[FloatPhenotype]:
        genes = self._genotypes

        return [self.genotype_to_phenotype(gene) for gene in self._genotypes]

    @phenotypes.setter
    def phenotypes(self, phenotypes: List[FloatPhenotype]) -> None:
        self._genotypes = [
            self.phenotype_to_genotype(phenotype) for phenotype in phenotypes
        ]

    def __str__(self) -> str:
        return str(self._genotypes)

    def __repr__(self) -> str:
        return self.__str__()


class AdaptiveStepFloatChromosome(Chromosome[FloatPairPhenotype,
                                             FloatPairGenotype]):
    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        n: int = self.custom_data['n']

        self._genotypes = [
            FloatPairGenotype(self.custom_data) for _ in range(n)
        ]

    def initialize(self) -> None:
        n: int = self.custom_data['n']

        self._genotypes = [
            FloatPairGenotype(self.custom_data) for _ in range(n)
        ]
        for genotype in self._genotypes:
            genotype.initialize()

    @staticmethod
    def genotype_to_phenotype(gene: FloatPairGenotype,
                              **_) -> FloatPairPhenotype:
        new_phenotype = FloatPairPhenotype(gene.custom_data)
        new_phenotype.data = gene.data
        return new_phenotype

    @staticmethod
    def phenotype_to_genotype(phenotype: FloatPairPhenotype,
                              **_) -> FloatPairGenotype:
        new_gene = FloatPairGenotype(phenotype.custom_data)
        new_gene.data = phenotype.data
        return new_gene

    @property
    def genotypes(self) -> List[FloatPairGenotype]:
        return self._genotypes

    @genotypes.setter
    def genotypes(self, genes: List[FloatPairGenotype]) -> None:
        n: int = self.custom_data['n']
        if len(genes) != n:
            raise ValueError(
                'Tried to assign genotypes to AdaptiveStepFloatChromosome with wrong number of genes ({}). Expected {}.'
                .format(len(genes), n))

        self._genotypes = deepcopy(genes)

    @property
    def phenotypes(self) -> List[FloatPairPhenotype]:
        genes = self._genotypes

        return [self.genotype_to_phenotype(gene) for gene in self._genotypes]

    @phenotypes.setter
    def phenotypes(self, phenotypes: List[FloatPairPhenotype]) -> None:
        self._genotypes = [
            self.phenotype_to_genotype(phenotype) for phenotype in phenotypes
        ]

    def __str__(self) -> str:
        return str(self._genotypes)

    def __repr__(self) -> str:
        return self.__str__()


class CovarianceFloatChromosome(Chromosome[FloatPhenotype, FloatGenotype]):
    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)

        n: int = self.custom_data['n']
        k: int = int(n * (n - 1) / 2)
        size: int = 2 * n + k

        self._genotypes = [
            FloatGenotype(self.custom_data) for _ in range(size)
        ]
        for i in range(size):
            if i < n:
                self._genotypes[i].type = DataType.VARIABLE
            elif i < 2 * n:
                self._genotypes[i].type = DataType.STEP_SIZE
            else:
                self._genotypes[i].type = DataType.ROTATION_ANGLE

    def initialize(self) -> None:
        n: int = self.custom_data['n']
        k: int = int(n * (n - 1) / 2)
        size: int = 2 * n + k

        self._genotypes = [
            FloatGenotype(self.custom_data) for _ in range(size)
        ]
        for i in range(size):
            if i < n:
                self._genotypes[i].type = DataType.VARIABLE
            elif i < 2 * n:
                self._genotypes[i].type = DataType.STEP_SIZE
            else:
                self._genotypes[i].type = DataType.ROTATION_ANGLE

            self._genotypes[i].initialize()

    @staticmethod
    def genotype_to_phenotype(gene: FloatGenotype, **_) -> FloatPhenotype:
        new_phenotype = FloatPhenotype(gene.custom_data)
        new_phenotype.type = gene.type
        new_phenotype.data = gene.data
        return new_phenotype

    @staticmethod
    def phenotype_to_genotype(phenotype: FloatPhenotype, **_) -> FloatGenotype:
        new_gene = FloatGenotype(phenotype.custom_data)
        new_gene.type = phenotype.type
        new_gene.data = phenotype.data
        return new_gene

    @property
    def genotypes(self) -> List[FloatGenotype]:
        return self._genotypes

    @genotypes.setter
    def genotypes(self, genes: List[FloatGenotype]) -> None:
        n: int = self.custom_data['n']
        k: int = int(n * (n - 1) / 2)
        size: int = 2 * n + k

        if len(genes) != size:
            raise ValueError(
                'Tried to assign genotypes to CovarianceFloatChromosome with wrong number of genes ({}). Expected {}.'
                .format(len(genes), size))

        self._genotypes = deepcopy(genes)

    @property
    def phenotypes(self) -> List[FloatPhenotype]:
        genes = self._genotypes

        return [self.genotype_to_phenotype(gene) for gene in self._genotypes]

    @phenotypes.setter
    def phenotypes(self, phenotypes: List[FloatPhenotype]) -> None:
        self._genotypes = [
            self.phenotype_to_genotype(phenotype) for phenotype in phenotypes
        ]

    def __str__(self) -> str:
        return str(self._genotypes)

    def __repr__(self) -> str:
        return self.__str__()
