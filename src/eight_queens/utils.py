from typing import List
from random import random, randint

from eight_queens.chromosomes import *
from genetic_framework.individual import Individual


class Roulette:
    def __init__(self,
                 population: List[Individual],
                 replacement: bool = False):
        population.sort(key=lambda individual: individual.fitness(),
                        reverse=True)
        self.replacement = replacement
        self._items: List[Roulette.Item] = list(
            map(
                lambda individual: Roulette.Item(individual,
                                                 individual.fitness()),
                population))

        for i in range(1, len(self._items)):
            self._items[i].acc_probability += self._items[i -
                                                          1].acc_probability

    def get_individual(self) -> Individual:
        r = random() * self._items[-1].acc_probability
        try:
            selected_item = next(item for item in self._items
                                 if r <= item.acc_probability)
        except StopIteration:
            # When everyone has fitness 0.0, just take random one
            r2 = randint(0, len(self._items) - 1)
            selected_item = self._items[r2]
        self._items.remove(selected_item)
        return selected_item.individual

    class Item:
        def __init__(self, individual: Individual,
                     acc_probability: float) -> None:
            self.individual = individual
            self.acc_probability = acc_probability


def print_chess_board(chromosome: BitStringChromosome) -> None:
    chess_size = chromosome.custom_data['chess_size']
    queen_positions = [(pheno.data[0], pheno.data[1])
                       for pheno in chromosome.phenotypes]

    board: List[List[str]] = []
    for i in range(chess_size):
        board.append([])
        for j in range(chess_size):
            board[i].append('*' if (i, j) in queen_positions else '_')

    final_str = '\n'.join([' '.join(row) for row in board])
    print(final_str)
