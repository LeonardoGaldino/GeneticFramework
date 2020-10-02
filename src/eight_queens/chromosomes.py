from typing import Dict, List
from random import randint
from functools import reduce
from copy import deepcopy

from eight_queens.phenotypes import QueenPositionPhenotype
from eight_queens.genotypes import BitStringGenotype, IntGenotype
from genetic_framework.chromosome import Chromosome


class BitStringChromosome(Chromosome[QueenPositionPhenotype, BitStringGenotype]):

    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._genotypes: List[BitStringGenotype] = []

    def initialize(self) -> None:
        chess_size = self.custom_data['chess_size']

        self._genotypes = []
        for i in range(chess_size):
            new_gene = BitStringGenotype(self.custom_data)
            new_data = randint(0, chess_size - 1)
            new_gene.data = "{:032b}".format(new_data)
            self._genotypes.append(new_gene) 

    @staticmethod
    def genotype_to_phenotype(gene: BitStringGenotype, **kwargs) -> QueenPositionPhenotype:
        new_phenotype = QueenPositionPhenotype(gene.custom_data)
        new_phenotype.data = (int(gene.data, 2), kwargs['index'])
        return new_phenotype

    @staticmethod
    def phenotype_to_genotype(phenotype: QueenPositionPhenotype, **kwargs) -> BitStringGenotype:
        new_genotype = BitStringGenotype(phenotype.custom_data)
        new_genotype.data = "{:032b}".format(phenotype.data[0])
        return new_genotype

    @property
    def genotypes(self) -> List[BitStringGenotype]:
        return self._genotypes

    @genotypes.setter
    def genotypes(self, genes: List[BitStringGenotype]) -> None:
        chess_size = self.custom_data['chess_size']

        if len(genes) != chess_size:
            raise ValueError('Tried to set BitStringChromosome genotypes with wrong number of genes ({}). Expected {}.'
                .format(len(genes), chess_size))

        values = [int(gene.data, 2) for gene in genes]

        for value in values:
            if value < 0 or value >= chess_size:
                raise ValueError('Tried to set BitStringChromosome genes with gene out of boundaries ({}). Expected [{}, {}].'
                    .format(value, 0, chess_size - 1))
        self._genotypes = deepcopy(genes)

    @property
    def phenotypes(self) -> List[QueenPositionPhenotype]:
        return [BitStringChromosome
            .genotype_to_phenotype(self.genotypes[i], index=i)
            for i in range(len(self.genotypes))]

    @phenotypes.setter
    def phenotypes(self, _phenotypes: List[QueenPositionPhenotype]) -> None:
        _phenotypes.sort(key=lambda phenotype: phenotype.data[1])
        
        self._genotypes = [BitStringChromosome
            .phenotype_to_genotype(phenotype)
            for phenotype in _phenotypes]

    def __str__(self) -> str:
        return str(self.genotypes)

    def __repr__(self) -> str:
        return self.__str__()


class IntPermutationChromosome(Chromosome[QueenPositionPhenotype, IntGenotype]):

    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._genotypes: List[IntGenotype] = []

    def initialize(self) -> None:
        chess_size: int = self.custom_data['chess_size']
        self._genotypes = []

        for i in range(chess_size):
            new_gene = IntGenotype(self.custom_data)
            new_gene.data = i
            self._genotypes.append(new_gene)

        # Permute _data list: for each index i, choose an element after i 
        # (for exemple at r) and swap(i,r)
        for i in range(chess_size - 1):
            random_swap_position = randint(i+1, chess_size - 1)
            self._genotypes[i], self._genotypes[random_swap_position] = \
                self._genotypes[random_swap_position], self._genotypes[i]

    @staticmethod
    def genotype_to_phenotype(gene: IntGenotype, **kwargs) -> QueenPositionPhenotype:
        new_phenotype = QueenPositionPhenotype(gene.custom_data)
        new_phenotype.data = (gene.data, kwargs['index'])
        return new_phenotype

    @staticmethod
    def phenotype_to_genotype(phenotype: QueenPositionPhenotype, **kwargs) -> IntGenotype:
        new_gene = IntGenotype(phenotype.custom_data)
        new_gene.data = phenotype.data[0]
        return new_gene

    @property
    def genotypes(self) -> List[IntGenotype]:
        return self._genotypes

    @genotypes.setter
    def genotypes(self, genes: List[IntGenotype]) -> None:
        chess_size = self.custom_data['chess_size']
        if len(genes) != chess_size:
            raise ValueError(
                'Tried to assign genotypes to IntPermutationChromosome with wrog number of genes ({}). Expected {}.'
                .format(len(genes), chess_size))

        values = list(map(lambda gene: gene.data, genes))
        for i in range(chess_size):
            if values.count(i) != 1:
                raise ValueError(
                    'Tried to set IntPermutation genes with bad permutation ({}).'
                    .format(values))
        
        self._genotypes = deepcopy(genes)

    @property
    def phenotypes(self) -> List[QueenPositionPhenotype]:
        genes = self.genotypes

        return [IntPermutationChromosome.genotype_to_phenotype(genes[i], index=i)
            for i in range(len(genes))]

    @phenotypes.setter
    def phenotypes(self, phenotypes: List[QueenPositionPhenotype]) -> None:
        phenotypes.sort(key=lambda phenotype: phenotype.data[1])

        self._genotypes = [IntPermutationChromosome
            .phenotype_to_genotype(phenotypes[i]) 
            for i in range(len(phenotypes))]

    def __str__(self) -> str:
        return str(self._genotypes)

    def __repr__(self) -> str:
        return self.__str__()