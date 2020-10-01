"""Module responsible for the learning process of the eight queen problem.

This module instantiate genetic algorithm framework to find solutions for the
eight queen problem.
"""
from argparse import ArgumentParser, Action
from typing import Type, Any
from enum import Enum

from genetic_framework.core import *
from eight_queens.chromosomes import *
from eight_queens.fitness import *
from eight_queens.mutators import *
from eight_queens.recombiners import *
from eight_queens.selectors import *
from eight_queens.utils import *


PROGRAM_DESCRIPTION = "Learns eight queens puzzle through genetic algorithm"


class FitnessComputerEnum(Enum):
    QUEEN_ATTACK_COUNT = QueenAttackCountFitnessComputer


class ChromosomeEnum(Enum):
    BIT_STRING = BitStringChromosome


class MutatorEnum(Enum):
    RANDOMIZE_GENE = RandomizeGeneMutator


class RecombinerEnum(Enum):
    CUT_CROSS_FILL = CutCrossFillRecombiner


class SurvivorSelectorEnum(Enum):
    BEST_FITNESS = BestFitnessSurvivorSelector


class MatingSelectorEnum(Enum):
    BEST_FITNESS = BestFitnessMatingSelector    


class IndividualSelectorEnum(Enum):
    K_BEST_FITNESS = KBestFitnessIndividualSelector


class CLIArgumentDescription:

    def __init__(self, _type: Type, default_value: Any, short_name: str, 
        full_name: str, help_message: str, action_cls: Type[Action]) -> None:
        self.type = _type
        self.default_value = default_value
        self.short_name = '-{}'.format(short_name)
        self.full_name = '--{}'.format(full_name)
        self.help_message = help_message.replace('\n', '').replace('\td', '') + \
            " (default={})".format(default_value)
        self.action_cls = action_cls


class EnumConstraintAction(Action):
    """Class responsible for sanitizing probability CLI inputs' range [0, 1]"""

    def __init__(self, **kwargs):
        enum = kwargs.pop("type", None)
        kwargs['type'] = str

        if enum is None:
            raise ValueError("type must be assigned an Enum when using EnumAction")
        if not issubclass(enum, Enum):
            raise TypeError("type must be an Enum when using EnumAction")

        # Generate choices from the Enum
        kwargs.setdefault("choices", tuple(e.name for e in enum))

        super().__init__(**kwargs)

        self._enum = enum

    def __call__(self, parser, namespace, values, option_string = None) -> None:
        setattr(namespace, self.dest, self._enum[values].value)


class CheckProbabilityConstraintAction(Action):
    """Class responsible for sanitizing probability CLI inputs' range [0, 1]"""

    def __call__(self, parser, namespace, values, option_string = None) -> None:
        if values < 0 or values > 1.0:
            raise ValueError(
                "{} flag has a value out of probability boundaries [0, 1.0]: {}"
                    .format(option_string, values))
        setattr(namespace, self.dest, values)


class CheckPositiveIntegerConstraintAction(Action):
    """Class responsible for sanitizing positive integers"""
    
    def __call__(self, parser, namespace, values, option_string = None) -> None:
        if values <= 0:
            raise ValueError(
                "{} flag has non positive value which is not allowed: {}"
                    .format(option_string, values))
        setattr(namespace, self.dest, values)


ARGS = [
    CLIArgumentDescription(_type=int, default_value=8, 
        short_name='cs', full_name='chess_size', 
        help_message="""Specify the size of the chess board in which the puzzle 
            takes place.""", action_cls=CheckPositiveIntegerConstraintAction),

    CLIArgumentDescription(_type=int, default_value=100, 
        short_name='ps', full_name='population_size', 
        help_message="""Specify the size of the population that the algorithm 
            will evolve to find solutions.""",
        action_cls=CheckPositiveIntegerConstraintAction),
        
    CLIArgumentDescription(_type=int, default_value=50, 
        short_name='mg', full_name='max_generations', 
        help_message="""Specify the maximum number of generations the 
            algorithm should evolve to find solutions.""",
        action_cls=CheckPositiveIntegerConstraintAction),

    CLIArgumentDescription(_type=int, default_value=5, 
        short_name='ns', full_name='number_solutions', 
        help_message="""Specify the number of solutions the algorithm should 
            find.""",
        action_cls=CheckPositiveIntegerConstraintAction),

    CLIArgumentDescription(_type=int, default_value=2, 
        short_name='bs', full_name='breed_size', 
        help_message="""Specify the number of children that should be created 
            for each pair or parents.""",
        action_cls=CheckPositiveIntegerConstraintAction),

    CLIArgumentDescription(_type=float, default_value=0.4, 
        short_name='mp', full_name='mutation_probability', 
        help_message="""Specify the probability that a mutation will occur 
            when new individual is generated.""",
        action_cls=CheckProbabilityConstraintAction),

    CLIArgumentDescription(_type=float, default_value=0.9, 
        short_name='cp', full_name='crossover_probability', 
        help_message="""Specify the probability that two given individuals 
            will recombine.""",
        action_cls=CheckProbabilityConstraintAction),

    CLIArgumentDescription(_type=FitnessComputerEnum, 
        default_value=FitnessComputerEnum.QUEEN_ATTACK_COUNT.value, 
        short_name='fc', full_name='fitness_computer', 
        help_message="""Specify the class responsible for computing individuals 
            fitness.""",
        action_cls=EnumConstraintAction),

    CLIArgumentDescription(_type=ChromosomeEnum, 
        default_value=ChromosomeEnum.BIT_STRING.value, 
        short_name='chr', full_name='chromosome', 
        help_message="""Specify the chromosome class. Will define how solutions
            are encoded and manipulated.""",
        action_cls=EnumConstraintAction),

    CLIArgumentDescription(_type=MutatorEnum, 
        default_value=MutatorEnum.RANDOMIZE_GENE.value, 
        short_name='mut', full_name='mutator', 
        help_message="""Specify the mutator class. Will define how solutions
            are mutated during evolution.""",
        action_cls=EnumConstraintAction),

    CLIArgumentDescription(_type=RecombinerEnum, 
        default_value=RecombinerEnum.CUT_CROSS_FILL.value, 
        short_name='rec', full_name='recombiner', 
        help_message="""Specify the recombiner class. Will define how solutions
            are recombined together to generate new ones during evolution.""",
        action_cls=EnumConstraintAction),

    CLIArgumentDescription(_type=SurvivorSelectorEnum, 
        default_value=SurvivorSelectorEnum.BEST_FITNESS.value, 
        short_name='ssel', full_name='survivor_selector', 
        help_message="""Specify Survivor Selector class. Will define how 
            individuals are chosen to go on to next generation.""",
        action_cls=EnumConstraintAction),

    CLIArgumentDescription(_type=MatingSelectorEnum, 
        default_value=MatingSelectorEnum.BEST_FITNESS.value, 
        short_name='msel', full_name='mating_selector', 
        help_message="""Specify Mating Selector class. Will define how 
            individuals are chosen to generate children for next generation.""",
        action_cls=EnumConstraintAction),

    CLIArgumentDescription(_type=IndividualSelectorEnum, 
        default_value=IndividualSelectorEnum.K_BEST_FITNESS.value, 
        short_name='isel', full_name='individual_selector', 
        help_message="""Specify Individual Selector class. Will define how 
            best individuals are chosen as solution to the problem after the
            experiment.""",
        action_cls=EnumConstraintAction),
]


def main(**kwargs) -> None:
    print('Using these CLI arguments: {}'.format(kwargs))
    experiment = Experiment(kwargs['population_size'], kwargs['max_generations'], 
        kwargs['crossover_probability'], kwargs['mutation_probability'],
        kwargs['number_solutions'], kwargs['breed_size'], 
        kwargs['chromosome'], kwargs['fitness_computer'], 
        kwargs['mutator'], kwargs['recombiner'],
        kwargs['mating_selector'], kwargs['survivor_selector'], 
        kwargs['individual_selector'], dict(chess_size=kwargs['chess_size']))
    best_individuals = experiment.run_experiment()

    print('\nSolutions:')
    for individual in best_individuals:
        print('Fitness: {}'.format(individual.fitness()))
        print_chess_board(individual.chromosome)
        print('\n')


if __name__ == '__main__':
    parser = ArgumentParser(description=PROGRAM_DESCRIPTION)

    for arg in ARGS:
        parser.add_argument(arg.short_name, arg.full_name, 
            help=arg.help_message, action=arg.action_cls, type=arg.type, 
            default=arg.default_value)
    args = parser.parse_args()

    main(**args.__dict__)