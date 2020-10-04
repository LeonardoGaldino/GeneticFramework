from abc import ABC, abstractmethod
from typing import List, Tuple, Dict

from genetic_framework.custom_data import CustomDataHolder
from genetic_framework.individual import Individual


class MatingSelector(CustomDataHolder, ABC):
    
    @staticmethod
    @abstractmethod
    def select_couples(population: List[Individual], num_parent_pairs: int) \
            -> List[Tuple[Individual, Individual]]:
        """Pairs individuals to mate and produce children. Subclass should
        implement this logic of selecting individual to mate."""
        ...


class SurvivorSelector(CustomDataHolder, ABC):
    """Class responsible for selecting survivors for the following
    generation. Subclasses should implement this logic."""


    @staticmethod
    @abstractmethod
    def select_survivors(population_size: int, parents: List[Individual],
        breed: List[Individual]) -> List[Individual]:
        """Implements logic of choosing which individuals will survive to next
        generation."""
        ...


class SolutionSelector(ABC):
    """
    Responsible for best individuals selection logic on a running experiment
    """

    @abstractmethod
    def __init__(self, number_solutions: int, custom_data: Dict = {}) -> None:
        self.number_solutions = number_solutions
        self.custom_data = custom_data

    @property
    @abstractmethod
    def best_individual(self) -> Individual:
        """Returns the best individual selected and stored so far."""
        ...
    
    @property
    @abstractmethod
    def best_individuals(self) -> List[Individual]:
        """Returns the best individuals selected and stored so far."""
        ...

    @abstractmethod
    def update_individuals(self, population: List[Individual]) -> None:
        """Updates (if necessary) the list of best individuals with 
        individuals from the specified population."""
        ...