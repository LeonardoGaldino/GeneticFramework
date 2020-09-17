"""Module responsible for the learning process of the eight queen problem.

This module instantiate genetic algorithm framework to find solutions for the
eight queen problem.
"""
from argparse import ArgumentParser, Action


PROGRAM_DESCRIPTION = "Learns eight queens puzzle through genetic algorithm"
DEFAULTS = {
    'chess_size': 8,
    'pop_size': 100,
    'max_gen': 50,
    'crossover_prob': 0.9,
    'mutation_prob': 0.4,
}


class CheckProbabilityConstraintAction(Action):
    """Class responsible for sanitizing probability CLI inputs' range [0, 1]"""
    
    def __call__(self, parser, namespace, values, option_string):
        if values < 0 or values > 1.0:
            raise ValueError(
                "{} flag has a value out of probability boundaries [0, 1.0]: {}"
                    .format(option_string, values))
        setattr(namespace, self.dest, values)


class CheckPositiveIntegerConstraintAction(Action):
    """Class responsible for sanitizing positive integers"""
    
    def __call__(self, parser, namespace, values, option_string):
        if values <= 0:
            raise ValueError(
                "{} flag has non positive value which is not allowed: {}"
                    .format(option_string, values))
        setattr(namespace, self.dest, values)


def main(chess_size: int, population_size: int, max_generations: int, 
        crossover_prob: float, mutation_prob: float):
    print('Hello, world: {} - {} - {} - {} - {}'
        .format(chess_size, population_size, max_generations, crossover_prob, 
            mutation_prob))

if __name__ == '__main__':
    parser = ArgumentParser(description=PROGRAM_DESCRIPTION)

    parser.add_argument('-cs', '--chess_size', 
        help="""Specify the size of the chess board in which the puzzle takes 
            place (default={})""".format(DEFAULTS['chess_size']),
        action=CheckPositiveIntegerConstraintAction, type=int,
        default=DEFAULTS['chess_size'])

    parser.add_argument('-ps', '--pop_size', 
        help="""Specify the size of the population that the algorithm will 
            evolve to find solutions (default={})""".format(DEFAULTS['pop_size']),
        action=CheckPositiveIntegerConstraintAction, type=int,
        default=DEFAULTS['pop_size'])

    parser.add_argument('-mg', '--max_gen',
        help="""Specify the maximum number of generations the algorithm should 
            evolve to find solutions (default={})""".format(DEFAULTS['max_gen']),
        action=CheckPositiveIntegerConstraintAction, type=int,
        default=DEFAULTS['max_gen'])

    parser.add_argument('-cp', '--crossover_prob', 
        help="""Specify the probability that a given individual will recombine 
            (default={})""".format(DEFAULTS['crossover_prob']),
        action=CheckProbabilityConstraintAction, type=float, 
        default=DEFAULTS['crossover_prob'])

    parser.add_argument('-mp', '--mutation_prob',
        help="""Specify the probability that a mutation will occur in a new  
            individual (default={})""".format(DEFAULTS['mutation_prob']),
        action=CheckProbabilityConstraintAction, type=float, 
        default=DEFAULTS['mutation_prob'])

    args = parser.parse_args()
    main(args.chess_size, args.pop_size, args.max_gen, args.crossover_prob, args.mutation_prob)
