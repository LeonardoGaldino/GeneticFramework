from random import randint

from genetic_framework.core import *
from eight_queen.genes import BitStringGene


class BitStringFlipBitMutator(GeneMutator):

    @staticmethod
    def gene_cls() -> Type[BitStringGene]:
        return BitStringGene

    @staticmethod
    def _mutate(gene: BitStringGene):
        chosen_bit = randint(0, 8*len(gene.data) - 1)
        gene.flip_bit(chosen_bit)

    @classmethod
    @validate_gene_args
    def mutate(cls: Type[GeneMutator], gene: BitStringGene) -> BitStringGene:
        new_gene = BitStringGene(gene)
        BitStringFlipBitMutator._mutate(new_gene)
        return new_gene

    @classmethod
    @validate_gene_args
    def mutate_inplace(cls: Type[GeneMutator], gene: Gene):
        BitStringFlipBitMutator._mutate(gene)

