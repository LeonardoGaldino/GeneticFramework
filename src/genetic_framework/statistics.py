from abc import ABC, abstractmethod
from typing import Dict, TypeVar, Generic, List, Tuple

from genetic_framework.population import Population
from genetic_framework.selectors import SolutionSelector


DataPoint = TypeVar('DataPoint')


class StatisticsCollector(Generic[DataPoint], ABC):

    @abstractmethod
    def __init__(self, custom_data: Dict = {}) -> None:
        self.custom_data = custom_data

    @abstractmethod
    def collect_data_point(self, population: Population, \
            solution_selector: SolutionSelector) -> None:
        ...

    @property
    @abstractmethod
    def data(self) -> List[DataPoint]:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...


class AvgFitnessPerGenerationStatisticsCollector(StatisticsCollector[Tuple[int, float]]):
    
    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data: List[Tuple[int, float]] = []

    def collect_data_point(self, population: Population, \
            _: SolutionSelector) -> None:
        self._data.append((population.generation, population.avg_fitness()))
    
    @property
    def data(self) -> List[Tuple[int, float]]:
        return self._data

    def __str__(self) -> str:
        return str(self.data)
    
    def __repr__(self) -> str:
        return str(self)


class FitnessSDPerGenerationStatisticsCollector(StatisticsCollector[Tuple[int, float]]):
    
    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data: List[Tuple[int, float]] = []

    def collect_data_point(self, population: Population, \
            _: SolutionSelector) -> None:
        self._data.append((population.generation, 
            population.sd_fitness()))
    
    @property
    def data(self) -> List[Tuple[int, float]]:
        return self._data

    def __str__(self) -> str:
        return str(self.data)
    
    def __repr__(self) -> str:
        return str(self)
        

class BestFitnessPerGenerationStatisticsCollector(StatisticsCollector[Tuple[int, float]]):
    
    def __init__(self, custom_data: Dict = {}) -> None:
        super().__init__(custom_data)
        self._data: List[Tuple[int, float]] = []

    def collect_data_point(self, population: Population, \
            solution_selector: SolutionSelector) -> None:
        self._data.append((population.generation, 
            solution_selector.best_individual.fitness()))
    
    @property
    def data(self) -> List[Tuple[int, float]]:
        return self._data

    def __str__(self) -> str:
        return str(self.data)
    
    def __repr__(self) -> str:
        return str(self)