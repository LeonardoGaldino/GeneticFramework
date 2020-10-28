from typing import Dict, Tuple
from random import uniform
from enum import Enum
from math import pi

from genetic_framework.chromosome import Genotype


class FloatGenotype(Genotype[float]):
    class Type(Enum):
        VARIABLE = 0
        STEP_SIZE = 1
        ROTATION_ANGLE = 2

    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self.type: FloatGenotype.Type = FloatGenotype.Type.VARIABLE
        self._data: float = 0.0

    def initialize(self) -> None:
        lower_bound: float = self.custom_data['lower_bound']
        upper_bound: float = self.custom_data['upper_bound']
        step_size: float = self.custom_data['step_size']

        if self.type == FloatGenotype.Type.VARIABLE:
            self._data = uniform(lower_bound, upper_bound)
        elif self.type == FloatGenotype.Type.STEP_SIZE:
            self._data = step_size
        else:
            self._data = uniform(0, 2 * pi)

    @property
    def data(self) -> float:
        return self._data

    @data.setter
    def data(self, new_data: float) -> None:
        lower_bound: float = self.custom_data['lower_bound']
        upper_bound: float = self.custom_data['upper_bound']

        if self.type == FloatGenotype.Type.VARIABLE and (
                new_data < lower_bound or new_data > upper_bound):
            raise ValueError(
                'Tried to set FloatGenotype data with ({}). Should be [{}, {}]'
                .format(new_data, lower_bound, upper_bound))

        self._data = new_data

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return self.__str__()


class FloatPairGenotype(Genotype[Tuple[float, float]]):
    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data: Tuple[float, float] = (0.0, 0.0)

    def initialize(self) -> None:
        lower_bound: float = self.custom_data['lower_bound']
        upper_bound: float = self.custom_data['upper_bound']
        delta: float = self.custom_data['step_size']
        x: float = uniform(lower_bound, upper_bound)
        self._data = (x, delta)

    @property
    def data(self) -> Tuple[float, float]:
        return self._data

    @data.setter
    def data(self, new_data: Tuple[float, float]) -> None:
        lower_bound: float = self.custom_data['lower_bound']
        upper_bound: float = self.custom_data['upper_bound']

        if new_data[0] < lower_bound or new_data[0] > upper_bound:
            raise ValueError(
                'Tried to set FloatPairGenotype data with ({}). Should be [{}, {}]'
                .format(new_data[0], lower_bound, upper_bound))

        self._data = new_data

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return self.__str__()
