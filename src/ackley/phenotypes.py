from typing import Dict, Tuple

from genetic_framework.chromosome import Phenotype
from ackley.util import DataType


class FloatPhenotype(Phenotype[float]):
    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data: float = 0.0
        self.type: DataType = DataType.VARIABLE

    @property
    def data(self) -> float:
        return self._data

    @data.setter
    def data(self, new_data: float) -> None:
        lower_bound: float = self.custom_data['lower_bound']
        upper_bound: float = self.custom_data['upper_bound']

        if self.type == DataType.VARIABLE and (new_data < lower_bound or new_data > upper_bound):
            raise ValueError(
                'Tried to set FloatPhenotype data with ({}). Should be [{}, {}]'
                .format(new_data, lower_bound, upper_bound))

        self._data = new_data

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return self.__str__()


class FloatPairPhenotype(Phenotype[Tuple[float, float]]):
    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data: Tuple[float, float] = (0.0, 0.0)

    @property
    def data(self) -> Tuple[float, float]:
        return self._data

    @data.setter
    def data(self, new_data: Tuple[float, float]) -> None:
        lower_bound: float = self.custom_data['lower_bound']
        upper_bound: float = self.custom_data['upper_bound']

        if new_data[0] < lower_bound or new_data[0] > upper_bound:
            raise ValueError(
                'Tried to set FloatPairPhenotype data with ({}). Should be [{}, {}]'
                .format(new_data[0], lower_bound, upper_bound))

        self._data = new_data

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return self.__str__()
