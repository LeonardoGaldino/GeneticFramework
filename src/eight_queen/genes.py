from random import randint
from copy import copy

from genetic_framework.core import *

class BitStringGene(Gene):

    def __init__(self, gene_copy_from: 'BitStringGene' = None):
        if gene_copy_from is None:
            self._data = bytearray(3)
        else:
            self._data = copy(gene_copy_from.data)

    def initialize(self):
        for i in len(self.data):
            self.data[i] = randint(0, 7)

    @property
    def data(self) -> Any:
        return self._data

    @data.setter
    def data(self, new_data: Any):
        self.data = new_data

    def flip_bit(self, bit_index: int):
        if bit_index >= 8*len(self.data):
            raise ValueError('Tried to access BitString invalid bit index ({})'
                .format(bit_index))
        # ^ operator is bitwise xor. It flips the specified bit.
        self.data[bit_index/8] ^= (1 << (bit_index % 8))
    
    def __str__(self) -> str:
        return '[{}, {}, {}]'.format(*self.data)

