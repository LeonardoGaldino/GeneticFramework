from typing import Dict, List
from random import randint
from functools import reduce
from copy import deepcopy

from ackley.phenotypes import FloatPhenotype
from ackley.genotypes import FloatGenotype
from genetic_framework.chromosome import Chromosome


class FloatChromosome(Chromosome[FloatPhenotype, FloatGenotype]):
    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._genotypes: List[FloatGenotype] = []

    def initialize(self) -> None:
        lower_bound = self.custom_data['lower_bound']
        upper_bound = self.custom_data['upper_bound']
        n = self.custom_data['n']

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
        n = self.custom_data['n']
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
