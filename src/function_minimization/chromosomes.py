from typing import Dict, List
from random import uniform
from copy import deepcopy

from function_minimization.phenotypes import FloatPhenotype
from function_minimization.genotypes import FloatGenotype
from genetic_framework.chromosome import Chromosome


class FloatVectorChromosome(Chromosome[FloatPhenotype, FloatGenotype]):
    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._genotypes: List[FloatGenotype] = []

    def initialize(self) -> None:
        vector_size = self.custom_data['vector_size']
        lower_bound = self.custom_data['parameter_lower_bound']
        upper_bound = self.custom_data['parameter_upper_bound']

        self._genotypes = []
        for _ in range(vector_size):
            new_gene = FloatGenotype(self.custom_data)
            new_gene.data = uniform(lower_bound, upper_bound)
            self._genotypes.append(new_gene)

    @staticmethod
    def genotype_to_phenotype(gene: FloatGenotype, **kwargs) -> FloatPhenotype:
        new_phenotype = FloatPhenotype(gene.custom_data)
        new_phenotype.data = gene.data
        return new_phenotype

    @staticmethod
    def phenotype_to_genotype(phenotype: FloatPhenotype,
                              **kwargs) -> FloatGenotype:
        new_genotype = FloatGenotype(phenotype.custom_data)
        new_genotype.data = phenotype.data
        return new_genotype

    @property
    def genotypes(self) -> List[FloatGenotype]:
        return self._genotypes

    @genotypes.setter
    def genotypes(self, genes: List[FloatGenotype]) -> None:
        vector_size = self.custom_data['vector_size']
        lower_bound = self.custom_data['parameter_lower_bound']
        upper_bound = self.custom_data['parameter_upper_bound']

        if len(genes) != vector_size:
            raise ValueError(
                'Tried to set FloatParameterChromosome genotypes with wrong number of genes ({}). Expected {}.'
                .format(len(genes), vector_size))

        values = [gene.data for gene in genes]

        for value in values:
            if value < lower_bound or value > upper_bound:
                raise ValueError(
                    'Tried to set FloatParameterChromosome genes with gene out of boundaries ({}). Expected [{}, {}].'
                    .format(value, lower_bound, upper_bound))

        self._genotypes = deepcopy(genes)

    @property
    def phenotypes(self) -> List[FloatPhenotype]:
        return [
            FloatVectorChromosome.genotype_to_phenotype(self.genotypes[i])
            for i in range(len(self.genotypes))
        ]

    @phenotypes.setter
    def phenotypes(self, _phenotypes: List[FloatPhenotype]) -> None:
        self._genotypes = [
            FloatVectorChromosome.phenotype_to_genotype(phenotype)
            for phenotype in _phenotypes
        ]

    def __str__(self) -> str:
        return str(self.genotypes)

    def __repr__(self) -> str:
        return self.__str__()
