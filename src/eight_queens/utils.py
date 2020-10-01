from typing import List

from eight_queens.chromosomes import *


def print_chess_board(chromosome: BitStringChromosome) -> None:
    chess_size = chromosome.custom_data['chess_size']
    queen_positions = [(pheno.data[0], pheno.data[1]) 
        for pheno in chromosome.phenotypes()]
    
    board: List[List[str]] = []
    for i in range(chess_size):
        board.append([])
        for j in range(chess_size):
            board[i].append('*' if (i, j) in queen_positions else '_')

    final_str = '\n'.join([' '.join(row) for row in board])
    print(final_str)
