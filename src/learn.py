"""Module responsible for the learning process of the eight queen problem.

This module instantiate genetic algorithm framework to find solutions for the
eight queen problem.
"""
from argparse import ArgumentParser, Action
from typing import Type, Any


PROGRAM_DESCRIPTION = "Learns eight queens puzzle through genetic algorithm"


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
            in each generation.""",
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
]


def main(**kwargs) -> None:
    print('CLI Arguments: {}'.format(kwargs))

if __name__ == '__main__':
    parser = ArgumentParser(description=PROGRAM_DESCRIPTION)

    for arg in ARGS:
        parser.add_argument(arg.short_name, arg.full_name, 
            help=arg.help_message, action=arg.action_cls, type=arg.type, 
            default=arg.default_value)
    args = parser.parse_args()

    main(**args.__dict__)