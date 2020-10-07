from typing import Tuple, Dict

from genetic_framework.chromosome import Phenotype


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
            raise ValueError(
                'Tried to set QueenPositionPhenotype data[0] with ({}). Should be [{}, {}]'
                .format(new_data[0], 0, chess_size - 1))

        if new_data[1] < 0 or new_data[1] >= chess_size:
            raise ValueError(
                'Tried to set QueenPositionPhenotype data[1] with ({}). Should be [{}, {}]'
                .format(new_data[1], 0, chess_size - 1))

        self._data = new_data

    def __str__(self) -> str:
        return '({}, {})'.format(self.data[0], self.data[1])

    def __repr__(self) -> str:
        return self.__str__()
