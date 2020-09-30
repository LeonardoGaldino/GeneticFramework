from typing import Generic, Tuple

from genetic_framework.core import *


class QueenPhenotype(Phenotype[Tuple[int, int]]):

    def __init__(self, **custom_data) -> None:
        super().__init__(**custom_data)
        self._data: Tuple[int, int] = (-1, -1)

    @property
    def data(self) -> Tuple[int, int]:
        return self._data

    @data.setter
    def data(self, new_data: Tuple[int, int]) -> None:
        # TODO: Validate if new data is within boundaries
        self._data = new_data

    def __str__(self) -> str:
        return '({}, {})'.format(self.data[0], self.data[1])


class BytesGenotype(Genotype[int]):

    def __init__(self, **custom_data) -> None:
        super().__init__(**custom_data)
        self._data: int = 0

    def initialize(self) -> None:
        # TODO: randomize a valid column number (within boundaries)
        self._data = 1

    @property
    def data(self) -> int:
        return self._data

    @data.setter
    def data(self, new_data: int) -> None:
        # TODO: Validate if new data is within boundaries
        self._data = new_data
    
    def __str__(self) -> str:
        return str(self.data)


class BitStringChromosome(Chromosome[bytearray, QueenPhenotype, BytesGenotype]):

    def __init__(self, **custom_data) -> None:
        super().__init__(custom_data)
        # TODO: calculate and instatiate bytearray with correct size
        self._data: bytearray = bytearray(3)

    def initialize(self) -> None:
        # TODO: make it random and generic according to tab size
        for i in len(self.data):
            self._data[i] = 0

    @property
    def data(self) -> bytearray:
        return self._data

    @data.setter
    def data(self, new_data: bytearray) -> None:
        self._data = new_data
    
    @staticmethod
    def genotype_to_phenotype(gene: BytesGenotype) -> QueenPhenotype:
        # TODO: correctly populate phenotype instead of dumping genotype data
        p = QueenPhenotype()
        p.data = (gene.data, gene.data)
        return p

    def genotypes(self) -> List[BytesGenotype]:
        # TODO: correctly create genotypes instead of creating empty genes
        return list(map(lambda v: BytesGenotype(), self.data))

    def phenotypes(self) -> List[QueenPhenotype]:
        return list(map(lambda gene: BitStringChromosome \
            .genotype_to_phenotype(gene), self.genotypes()))

    def __str__(self) -> str:
        return str(list(self._data))