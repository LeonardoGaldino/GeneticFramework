from typing import Dict
from random import uniform

from genetic_framework.chromosome import Genotype


class FloatGenotype(Genotype[float]):

    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data: float = 0.0


    def initialize(self) -> None:
        lower_bound = self.custom_data['parameter_lower_bound']
        upper_bound = self.custom_data['parameter_upper_bound']
        self._data = uniform(lower_bound, upper_bound)

    @property
    def data(self) -> float:
        return self._data

    @data.setter
    def data(self, new_data: float) -> None:
        lower_bound = self.custom_data['parameter_lower_bound']
        upper_bound = self.custom_data['parameter_upper_bound']
        
        if self.data < lower_bound or self.data > upper_bound:
            raise ValueError('Tried to set FloatGenotype data with ({}). Should be [{}, {}]'
                .format(new_data, lower_bound, upper_bound))

        self._data = new_data
    
    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return self.__str__()