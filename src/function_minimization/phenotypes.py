from typing import Dict

from genetic_framework.chromosome import Phenotype


class FloatPhenotype(Phenotype[float]):
    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data: float = 0.0

    @property
    def data(self) -> float:
        return self._data

    @data.setter
    def data(self, new_data: float) -> None:
        lower_bound = self.custom_data['parameter_lower_bound']
        upper_bound = self.custom_data['parameter_upper_bound']

        if new_data < lower_bound or new_data > upper_bound:
            raise ValueError(
                'Tried to set FloatPhenotype data with ({}). Should be [{}, {}]'
                .format(new_data, lower_bound, upper_bound))

        self._data = new_data

    def __str__(self) -> str:
        return '{}'.format(self.data)

    def __repr__(self) -> str:
        return self.__str__()
