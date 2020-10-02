from typing import Dict
from random import randint

from genetic_framework.chromosome import Genotype


class BitStringGenotype(Genotype[str]):
    STRING_SIZE = 32

    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data: str = ""


    def initialize(self) -> None:
        chess_size = self.custom_data['chess_size']
        row = randint(0, chess_size - 1)
        self._data = "{:032b}".format(row)

    @property
    def data(self) -> str:
        return self._data

    @data.setter
    def data(self, new_data: str) -> None:
        chess_size = self.custom_data['chess_size']
        integer_data = int(new_data, 2)

        if integer_data < 0 or integer_data >= chess_size:
            raise ValueError('Tried to set BitStringGenotype data with ({}). Should be [{}, {}]'
                .format(integer_data, 0, chess_size - 1))

        self._data = new_data
    
    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return self.__str__()


class IntGenotype(Genotype[int]):

    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data: int = -1

    def initialize(self) -> None:
        chess_size = self.custom_data['chess_size']
        self._data = randint(0, chess_size - 1)

    @property
    def data(self) -> int:
        return self._data

    @data.setter
    def data(self, new_data: int) -> None:
        chess_size = self.custom_data['chess_size']

        if new_data < 0 or new_data >= chess_size:
            raise ValueError('Tried to set IntGenotype data with ({}). Should be [{}, {}]'
                .format(new_data, 0, chess_size - 1))

        self._data = new_data
    
    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return self.__str__()