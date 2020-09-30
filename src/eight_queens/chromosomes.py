from typing import Generic, Tuple
from random import randint
from math import log2, ceil

from genetic_framework.core import *


class QueenPositionPhenotype(Phenotype[Tuple[int, int]]):

    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data: Tuple[int, int] = (-1, -1)

    @property
    def data(self) -> Tuple[int, int]:
        return self._data

    @data.setter
    def data(self, new_data: Tuple[int, int]) -> None:
        chess_size = self.custom_data['chess_size']

        if new_data[0] < 0 or new_data[0] >= chess_size:
            raise ValueError("""Tried to set QueenPositionPhenotype data[0] with ({}). Should be [{}, {}]"""
                .format(new_data[0], 0, chess_size - 1))

        if new_data[1] < 0 or new_data[1] >= chess_size:
            raise ValueError("""Tried to set QueenPositionPhenotype data[1] with ({}). Should be [{}, {}]"""
                .format(new_data[1], 0, chess_size - 1))
                
        self._data = new_data

    def __str__(self) -> str:
        return '({}, {})'.format(self.data[0], self.data[1])


class BitStringGenotype(Genotype[str]):

    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data: str = ""


    def initialize(self) -> None:
        chess_size = self.custom_data['chess_size']
        column = randint(0, chess_size - 1)
        self._data = "{:032b}".format(column)

    @property
    def data(self) -> str:
        return self._data

    @data.setter
    def data(self, new_data: str) -> None:
        chess_size = self.custom_data['chess_size']
        integer_data = int(new_data, 2)

        if integer_data < 0 or integer_data >= chess_size:
            raise ValueError("""Tried to set StringGenotype data with ({}). Should be [{}, {}]"""
                .format(integer_data, 0, chess_size - 1))

        self._data = new_data
    
    def __str__(self) -> str:
        return str(self.data)


class BitStringChromosome(Chromosome[str, QueenPositionPhenotype, BitStringGenotype]):

    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data = ""

    def initialize(self) -> None:
        # TODO: make it random and generic according to tab size
        self._data = ""

    @property
    def data(self) -> str:
        return self._data

    @data.setter
    def data(self, new_data: str) -> None:
        # TODO: Check if new_data is valid
        self._data = new_data
    
    @staticmethod
    def genotype_to_phenotype(gene: BitStringGenotype) -> QueenPositionPhenotype:
        # TODO: correctly populate phenotype instead of dumping -1
        p = QueenPositionPhenotype()
        p.data = (-1, -1)
        return p

    def genotypes(self) -> List[BitStringGenotype]:
        # TODO: correctly create genotypes instead of creating empty genes
        return list(map(lambda v: BitStringGenotype(), self.data))

    def phenotypes(self) -> List[QueenPositionPhenotype]:
        return list(map(lambda gene: BitStringChromosome \
            .genotype_to_phenotype(gene), self.genotypes()))

    def __str__(self) -> str:
        return self.data