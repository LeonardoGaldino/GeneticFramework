from typing import Dict, List
from random import randint
from functools import reduce

from eight_queens.phenotypes import QueenPositionPhenotype
from eight_queens.genotypes import BitStringGenotype, IntGenotype
from genetic_framework.chromosome import Chromosome


class BitStringChromosome(Chromosome[str, QueenPositionPhenotype, BitStringGenotype]):

    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data = ""

    def initialize(self) -> None:
        chess_size = self.custom_data['chess_size']

        self._data = ""
        for i in range(chess_size):
            self._data += "{:032b}".format(randint(0, chess_size - 1))

    @property
    def data(self) -> str:
        return self._data

    @data.setter
    def data(self, new_data: str) -> None:
        chess_size = self.custom_data['chess_size']
        genotype_size = BitStringGenotype.STRING_SIZE

        if (len(new_data) % genotype_size) != 0:
            raise ValueError('Tried to set BitStringChromosome data with string not multiple of {}. Was {}.'
                .format(genotype_size, len(new_data)))
        if len(new_data)//genotype_size != chess_size:
            raise ValueError('Tried to set BitStringChromosome data with wrong string length ({}). Expected {}.'
                .format(len(new_data), chess_size*genotype_size))

        values = [int(new_data[i*genotype_size : (i+1)*genotype_size], 2) \
            for i in range(chess_size)]

        for i in range(chess_size):
            if values[i] < 0 or values[i] >= chess_size:
                raise ValueError('Tried to set BitStringChromosome data with date out of boundaries ({}). Expected [{}, {}].'
                    .format(values[i], 0, chess_size - 1))

        self._data = new_data

    @staticmethod
    def genotype_to_phenotype(gene: BitStringGenotype, **kwargs) -> QueenPositionPhenotype:
        new_phenotype = QueenPositionPhenotype(gene.custom_data)
        new_phenotype.data = (int(gene.data, 2), kwargs['index'])
        return new_phenotype

    @property
    def genotypes(self) -> List[BitStringGenotype]:
        chess_size = self.custom_data['chess_size']
        genotype_size = BitStringGenotype.STRING_SIZE
        genes: List[BitStringGenotype] = []

        for i in range(chess_size):
            gene = BitStringGenotype(self.custom_data)
            gene.data = self.data[i*genotype_size : (i+1)*genotype_size]
            genes.append(gene)

        return genes

    @genotypes.setter
    def genotypes(self, genes: List[BitStringGenotype]) -> None:
        chess_size = self.custom_data['chess_size']
        self.data = reduce(lambda acc, gene: acc + gene.data, genes, '')

    @property
    def phenotypes(self) -> List[QueenPositionPhenotype]:
        chess_size = self.custom_data['chess_size']
        genos = self.genotypes
        phenos: List[QueenPositionPhenotype] = []

        for i in range(chess_size):
            phenos.append(BitStringChromosome.genotype_to_phenotype(genos[i], index=i))

        return phenos

    @phenotypes.setter
    def phenotypes(self, phenotypes: List[QueenPositionPhenotype]) -> None:
        chess_size = self.custom_data['chess_size']
        phenotypes.sort(key=lambda phenotype: phenotype.data[1])
        
        self.data = reduce(lambda acc, phenotype: 
            acc + "{:032b}".format(phenotype.data[0]), phenotypes, '')

    def __str__(self) -> str:
        return self.data

    def __repr__(self) -> str:
        return self.__str__()


class IntPermutationChromosome(Chromosome[List[int], QueenPositionPhenotype, IntGenotype]):

    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data = list(range(custom_data['chess_size']))

    def initialize(self) -> None:
        chess_size: int = self.custom_data['chess_size']

        self._data = list(range(chess_size))
        # Permute _data list: for each index i, choose an element after i 
        # (for exemple at r) and swap(i,r)
        for i in range(chess_size - 1):
            random_swap_position = randint(i+1, chess_size - 1)
            self._data[i], self._data[random_swap_position] = \
                self._data[random_swap_position], self._data[i]

    @property
    def data(self) -> List[int]:
        return self._data

    @data.setter
    def data(self, new_data: List[int]) -> None:
        chess_size = self.custom_data['chess_size']

        if len(new_data) != chess_size:
            raise ValueError('Tried to set IntPermutation data wrong size ({}). Expected {}.'
                .format(len(new_data), chess_size))

        for i in range(chess_size):
            if new_data.count(i) != 1:
                raise ValueError('Tried to set IntPermutationChromosome data not respecting permutation ({}).'
                    .format(new_data))

        self._data = new_data

    @staticmethod
    def genotype_to_phenotype(gene: IntGenotype, **kwargs) -> QueenPositionPhenotype:
        new_phenotype = QueenPositionPhenotype(gene.custom_data)
        new_phenotype.data = (gene.data, kwargs['index'])
        return new_phenotype

    @property
    def genotypes(self) -> List[IntGenotype]:
        chess_size = self.custom_data['chess_size']
        genes: List[IntGenotype] = []

        for cur_data in self.data:
            new_gene = IntGenotype(self.custom_data)
            new_gene.data = cur_data
            genes.append(new_gene)

        return genes

    @genotypes.setter
    def genotypes(self, genes: List[IntGenotype]) -> None:
        chess_size = self.custom_data['chess_size']
        
        self.data = list(map(lambda gene: gene.data, genes))

    @property
    def phenotypes(self) -> List[QueenPositionPhenotype]:
        chess_size = self.custom_data['chess_size']
        genos = self.genotypes
        phenos: List[QueenPositionPhenotype] = []

        for i in range(chess_size):
            phenos.append(IntPermutationChromosome.genotype_to_phenotype(genos[i], index=i))

        return phenos

    @phenotypes.setter
    def phenotypes(self, phenotypes: List[QueenPositionPhenotype]) -> None:
        phenotypes.sort(key=lambda phenotype: phenotype.data[1])
        self.data = list(map(lambda phenotype: phenotype.data[0], phenotypes))

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return self.__str__()