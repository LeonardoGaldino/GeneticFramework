"""Module responsible for the learning process of the function minimization problem.

This module instantiate genetic algorithm framework to find solutions for the
function minimization problem.
"""
from argparse import ArgumentParser, Action
from typing import Type, Any
from enum import Enum

import matplotlib.pyplot as plt # type: ignore
import matplotlib.patches as mpatches # type: ignore

from function_minimization.chromosomes import FloatVectorChromosome
from function_minimization.phenotypes import FloatPhenotype
from function_minimization.genotypes import FloatGenotype
from function_minimization.fitness import ChallengeFitnessComputer
from function_minimization.mutators import RandomizeGeneMutator
from function_minimization.recombiners import RandomInterpolationRecombiner
from function_minimization.selectors import MinimizeFitnessMatingSelector, MinimizeFitnessSurvivorSelector, KLowerFitnessSolutionSelector
from genetic_framework.experiment import Experiment
from genetic_framework.statistics import *


PROGRAM_DESCRIPTION = "Minimizes a function through genetic algorithm"

""" Enums for choosing classes for tunning the algorithm
If new classes are implemented, add them in the corresponding enum
to make it available as CLI argument.
"""
class FitnessComputerEnum(Enum):
    CHALLENGE = ChallengeFitnessComputer

class ChromosomeEnum(Enum):
    FLOAT_VECTOR = FloatVectorChromosome

class MutatorEnum(Enum):
    RANDOMIZE_GENE = RandomizeGeneMutator

class RecombinerEnum(Enum):
    RANDOM_INTERPOLATION = RandomInterpolationRecombiner

class SurvivorSelectorEnum(Enum):
    MINIMIZE_FITNESS = MinimizeFitnessSurvivorSelector

class MatingSelectorEnum(Enum):
    MINIMIZE_FITNESS = MinimizeFitnessMatingSelector

class SolutionSelectorEnum(Enum):
    K_LOWER_FITNESS = KLowerFitnessSolutionSelector

class CLIArgumentDescription:
    # Class designed to model the fields that an CLI Argument should define

    def __init__(self, _type: Type, default_value: Any, short_name: str, 
        full_name: str, value_name: str, help_message: str, action_cls: Type[Action]) -> None:
        self.type = _type
        self.default_value = default_value
        self.short_name = '-{}'.format(short_name)
        self.full_name = '--{}'.format(full_name)
        self.value_name = value_name
        self.help_message = help_message.replace('\n', '').replace('\td', '') + \
            " (default={}).".format(default_value)
        self.action_cls = action_cls


# argparse.Actions for validating CLI arguments.
class EnumConstraintAction(Action):
    """Class responsible for sanitizing enum CLI inputs 
    (making sure value is a valid enum)"""

    def __init__(self, **kwargs):
        enum = kwargs.pop("type", None)
        kwargs['type'] = str

        if enum is None:
            raise ValueError("type must be assigned an Enum when using EnumAction")
        if not issubclass(enum, Enum):
            raise TypeError("type must be an Enum when using EnumAction")

        # Generate choices from the Enum
        choices = tuple(e.name for e in enum)
        kwargs.setdefault("choices", choices)
        kwargs['help'] += ' Choices: {}'.format(choices)

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

class NoConstraintAction(Action):
    """Dummy Action for arguments with no constraints"""
    
    def __call__(self, parser, namespace, values, option_string = None) -> None:
        setattr(namespace, self.dest, values)


# Every CLI Argument this script takes
ARGS = [
    CLIArgumentDescription(_type=int, default_value=2, 
        short_name='vs', full_name='vector_size', value_name='VECTOR_SIZE',
        help_message="""Specify the number of parameters the function will have""",
        action_cls=CheckPositiveIntegerConstraintAction),

    CLIArgumentDescription(_type=float, default_value=-2.048, 
        short_name='plb', full_name='parameter_lower_bound', value_name='LOWER_BOUND',
        help_message="""Specify the minimum value the funcion's parameter is allowed to have""",
        action_cls=NoConstraintAction),

    CLIArgumentDescription(_type=float, default_value=2.048, 
        short_name='pub', full_name='parameter_upper_bound', value_name='UPPER_BOUND',
        help_message="""Specify the maximum value the funcion's parameter is allowed to have""",
        action_cls=NoConstraintAction),

    CLIArgumentDescription(_type=int, default_value=100, 
        short_name='ps', full_name='population_size', value_name='POP_SIZE',
        help_message="""Specify the size of the population that the algorithm 
            will evolve to find solutions.""",
        action_cls=CheckPositiveIntegerConstraintAction),
        
    CLIArgumentDescription(_type=int, default_value=50, 
        short_name='mg', full_name='max_generations', value_name='MAX_GENS',
        help_message="""Specify the maximum number of generations the 
            algorithm should evolve to find solutions.""",
        action_cls=CheckPositiveIntegerConstraintAction),

    CLIArgumentDescription(_type=int, default_value=5, 
        short_name='ns', full_name='number_solutions', value_name='NUM_SOLUTIONS',
        help_message="""Specify the number of solutions the algorithm should 
            find.""",
        action_cls=CheckPositiveIntegerConstraintAction),

    CLIArgumentDescription(_type=int, default_value=2, 
        short_name='bs', full_name='breed_size', value_name='BREED_SIZE',
        help_message="""Specify the number of children that should be created 
            for each pair or parents.""",
        action_cls=CheckPositiveIntegerConstraintAction),

    CLIArgumentDescription(_type=int, default_value=10000, 
        short_name='mfc', full_name='max_fitness_comp', value_name='MAX_FIT_COMPS',
        help_message="""Maximum number of fitness computations allowed to be 
            done before algorithm stops.""",
        action_cls=CheckPositiveIntegerConstraintAction),

    CLIArgumentDescription(_type=int, default_value=30, short_name='npp', 
        full_name='num_parent_pairs', value_name='NUM_PAR_PAIRS',
        help_message="""Number of parents pairs returned from mating selector 
            algorithm for generating new individual through recombination.""",
        action_cls=CheckPositiveIntegerConstraintAction),

    CLIArgumentDescription(_type=float, default_value=None, 
        short_name='tf', full_name='target_fitness', value_name='TARGET_FITNESS',
        help_message="""Specify the fitness of a good enough solution, so that 
            the algorithm can stop.""",
        action_cls=NoConstraintAction),

    CLIArgumentDescription(_type=float, default_value=0.4, 
        short_name='mp', full_name='mutation_probability', value_name='MUTATION_PROB',
        help_message="""Specify the probability that a mutation will occur 
            when new individual is generated.""",
        action_cls=CheckProbabilityConstraintAction),

    CLIArgumentDescription(_type=float, default_value=0.9, 
        short_name='cp', full_name='crossover_probability', value_name='CROSS_PROB',
        help_message="""Specify the probability that two given individuals 
            will recombine.""",
        action_cls=CheckProbabilityConstraintAction),

    CLIArgumentDescription(_type=FitnessComputerEnum, 
        default_value=FitnessComputerEnum.CHALLENGE.value, 
        short_name='fc', full_name='fitness_computer', value_name='FITNESS_COMPUTER',
        help_message="""Specify the class responsible for computing individuals 
            fitness.""",
        action_cls=EnumConstraintAction),

    CLIArgumentDescription(_type=ChromosomeEnum, 
        default_value=ChromosomeEnum.FLOAT_VECTOR.value, 
        short_name='chr', full_name='chromosome', value_name='CHROMOSOME',
        help_message="""Specify the chromosome class. Will define how solutions
            are encoded and manipulated.""",
        action_cls=EnumConstraintAction),

    CLIArgumentDescription(_type=MutatorEnum, 
        default_value=MutatorEnum.RANDOMIZE_GENE.value, 
        short_name='mut', full_name='mutator', value_name='MUTATOR',
        help_message="""Specify the mutator class. Will define how solutions
            are mutated during evolution.""",
        action_cls=EnumConstraintAction),

    CLIArgumentDescription(_type=RecombinerEnum, 
        default_value=RecombinerEnum.RANDOM_INTERPOLATION.value, 
        short_name='rec', full_name='recombiner', value_name='RECOMBINER',
        help_message="""Specify the recombiner class. Will define how solutions
            are recombined together to generate new ones during evolution.""",
        action_cls=EnumConstraintAction),

    CLIArgumentDescription(_type=SurvivorSelectorEnum, 
        default_value=SurvivorSelectorEnum.MINIMIZE_FITNESS.value, 
        short_name='susel', full_name='survivor_selector', value_name='SURVIVOR_SEL',
        help_message="""Specify Survivor Selector class. Will define how 
            individuals are chosen to go on to next generation.""",
        action_cls=EnumConstraintAction),

    CLIArgumentDescription(_type=MatingSelectorEnum, 
        default_value=MatingSelectorEnum.MINIMIZE_FITNESS.value, 
        short_name='msel', full_name='mating_selector', value_name='MATING_SEL',
        help_message="""Specify Mating Selector class. Will define how 
            individuals are chosen to generate children for next generation.""",
        action_cls=EnumConstraintAction),

    CLIArgumentDescription(_type=SolutionSelectorEnum, 
        default_value=SolutionSelectorEnum.K_LOWER_FITNESS.value, 
        short_name='sosel', full_name='solution_selector', value_name='SOLUTION_SEL',
        help_message="""Specify Solution Selector class. Will define how 
            best individuals are chosen as solution to the problem after the
            experiment.""",
        action_cls=EnumConstraintAction),
]

STATISTICS_COLLECTOR_TYPES = [
    AvgFitnessPerGenerationStatisticsCollector,
    BestFitnessPerGenerationStatisticsCollector,
    FitnessSDPerGenerationStatisticsCollector,
]

def main(**kwargs) -> None:
    print('Using these CLI arguments: {}\n'.format(kwargs))

    experiment = Experiment(kwargs['population_size'], kwargs['max_generations'], 
        kwargs['crossover_probability'], kwargs['mutation_probability'],
        kwargs['target_fitness'], kwargs['number_solutions'], kwargs['breed_size'], 
        kwargs['max_fitness_comp'], kwargs['num_parent_pairs'], 
        kwargs['chromosome'], kwargs['fitness_computer'], 
        kwargs['mutator'], kwargs['recombiner'],
        kwargs['mating_selector'], kwargs['survivor_selector'], 
        kwargs['solution_selector'], STATISTICS_COLLECTOR_TYPES,
        dict(parameter_lower_bound=kwargs['parameter_lower_bound'], 
            parameter_upper_bound=kwargs['parameter_upper_bound'],
            vector_size=kwargs['vector_size']))
    best_individuals, stats_collectors = experiment.run_experiment()

    print('\nSolutions:')
    for individual in best_individuals:
        print('Gen: {}, Fitness: {}'.format(individual.generation, individual.fitness()))
        print(individual)
        print('\n')

    avg_fitness_per_generation = stats_collectors[0]
    best_fitness_per_generation = stats_collectors[1]
    sd_fitness_per_generation = stats_collectors[2]

    x_all, y_avg, y_best, y_sd, y_sdinv = [], [], [], [], []

    for i, (x, y) in enumerate(avg_fitness_per_generation.data):
        x_all.append(x)
        y_avg.append(y)
        y_best.append(best_fitness_per_generation.data[i][1])
        y_sd.append(y + sd_fitness_per_generation.data[i][1])
        y_sdinv.append(y - sd_fitness_per_generation.data[i][1])

        if sd_fitness_per_generation.data[i][1] == 0.0:
            for elem in [x_all, y_avg, y_best, y_sd, y_sdinv]:
                elem = elem[:i + 1]
            
            break

    plt.fill_between(x_all, y_sd, color='lightcoral')
    plt.fill_between(x_all, y_sdinv, color='white')
    sd = mpatches.Patch(color='lightcoral', label='Standard Deviation')

    best, = plt.plot(x_all, y_best, color='limegreen', label='Best Individual')
    avg, = plt.plot(x_all, y_avg, color='crimson', label='Average')

    plt.legend(handles=[sd, avg, best])

    plt.xlabel('Generations')
    plt.ylabel('Fitness')

    plt.show()


if __name__ == '__main__':
    parser = ArgumentParser(description=PROGRAM_DESCRIPTION)

    for arg in ARGS:
        parser.add_argument(arg.short_name, arg.full_name, 
            help=arg.help_message, action=arg.action_cls, type=arg.type, 
            metavar=arg.value_name, default=arg.default_value)
    args = parser.parse_args()

    main(**args.__dict__)