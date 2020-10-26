from abc import ABC
from typing import Type

from genetic_framework.recombiner import Recombiner
from ackley.chromosomes import FloatChromosome, AdaptiveStepFloatChromosome


class MidPointRecombiner(Recombiner[FloatChromosome], ABC):
    @classmethod
    def recombine(cls: Type, chromosome1: FloatChromosome,
                  chromosome2: FloatChromosome) -> FloatChromosome:
        new_chromosome = FloatChromosome(chromosome1.custom_data)
        new_genes = new_chromosome.genotypes
        genes1 = chromosome1.genotypes
        genes2 = chromosome2.genotypes

        for i in range(len(new_genes)):
            new_genes[i].data = (genes1[i].data + genes2[i].data) / 2

        new_chromosome.genotypes = new_genes
        return new_chromosome


class AdaptiveStepMidPointRecombiner(Recombiner[AdaptiveStepFloatChromosome],
                                     ABC):
    @classmethod
    def recombine(
        cls: Type, chromosome1: AdaptiveStepFloatChromosome,
        chromosome2: AdaptiveStepFloatChromosome
    ) -> AdaptiveStepFloatChromosome:
        new_chromosome = AdaptiveStepFloatChromosome(chromosome1.custom_data)
        new_genes = new_chromosome.genotypes
        genes1 = chromosome1.genotypes
        genes2 = chromosome2.genotypes

        for i in range(len(new_genes)):
            new_value = (genes1[i].data[0] + genes2[i].data[0]) / 2
            new_delta = (genes1[i].data[1] + genes2[i].data[1]) / 2
            new_genes[i].data = (new_value, new_delta)

        new_chromosome.genotypes = new_genes
        return new_chromosome
