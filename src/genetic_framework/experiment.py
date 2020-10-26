from typing import Type, Tuple, TypeVar, List, Dict, Optional, get_args
from collections import defaultdict

from genetic_framework.fitness import FitnessComputer
from genetic_framework.chromosome import Chromosome
from genetic_framework.mutator import Mutator
from genetic_framework.recombiner import Recombiner
from genetic_framework.selectors import SurvivorSelector, MatingSelector, SolutionSelector
from genetic_framework.individual import Individual
from genetic_framework.population import Population
from genetic_framework.statistics import StatisticsCollector

EPS = 1e-9


# Check if cls class works with the specified chromosome type
def is_correct_chromosome_type(cls: Type,
                               chromosome_cls: Type[Chromosome]) -> bool:
    if not hasattr(cls, '__orig_bases__'):
        return False

    for base in cls.__orig_bases__:
        args = get_args(base)

        for arg in args:
            if type(arg) == TypeVar:
                continue
            if issubclass(chromosome_cls, arg):
                return True

        if hasattr(base, '__origin__') \
            and is_correct_chromosome_type(base.__origin__, chromosome_cls):
            return True

    return False


class Experiment:
    def __init__(self,
                 population_size: int,
                 max_generations: int,
                 crossover_prob: float,
                 mutation_prob: float,
                 target_fitness: Optional[float],
                 num_solutions: int,
                 breed_size: int,
                 max_fitness_computations: int,
                 num_parent_pairs: int,
                 restart_zero_sd_tolerance: Optional[int],
                 chromosome_cls: Type[Chromosome],
                 fitness_computer_cls: Type[FitnessComputer],
                 maximize_fitness: bool,
                 mutator_cls: Type[Mutator],
                 recombiner_cls: Type[Recombiner],
                 mating_selector_cls: Type[MatingSelector],
                 survivor_selector_cls: Type[SurvivorSelector],
                 solution_selector_cls: Type[SolutionSelector],
                 stats_collector_types: List[Type[StatisticsCollector]],
                 custom_data: Dict = {}) -> None:
        self.population_size = population_size
        self.max_generations = max_generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.target_fitness = target_fitness
        self.num_solutions = num_solutions
        self.breed_size = breed_size
        self.max_fitness_computations = max_fitness_computations
        self.num_parent_pairs = num_parent_pairs
        self.restart_zero_sd_tolerance = restart_zero_sd_tolerance
        self.chromosome_cls = chromosome_cls

        self.fitness_computer_cls = fitness_computer_cls
        self.fitness_computer_cls.set_custom_data(custom_data)
        self.maximize_fitness = maximize_fitness

        self.mutator_cls = mutator_cls
        self.mutator_cls.set_custom_data(custom_data)

        self.recombiner_cls = recombiner_cls
        self.recombiner_cls.set_custom_data(custom_data)

        self.mating_selector_cls = mating_selector_cls
        self.mating_selector_cls.set_custom_data(custom_data)

        self.survivor_selector_cls = survivor_selector_cls
        self.survivor_selector_cls.set_custom_data(custom_data)

        self.solution_selector_cls = solution_selector_cls
        self.stats_collector_types = stats_collector_types
        self.custom_data = custom_data

        classes_to_be_validated = (
            (fitness_computer_cls, 'FitnessComputer'),
            (mutator_cls, 'Mutator'),
            (recombiner_cls, 'Recombiner'),
        )

        for (cls, name) in classes_to_be_validated:
            if not is_correct_chromosome_type(cls, chromosome_cls):
                raise TypeError(
                    '{} {} does not work with chromosome {}.'.format(
                        name, cls, chromosome_cls))

    def _generate_initial_individuals(self) -> List[Individual]:
        """Internal method used to generate individuals for the first 
        generation of the experiment"""
        return [
            Individual(self.chromosome_cls, self.fitness_computer_cls,
                       self.mutator_cls, self.recombiner_cls, 1,
                       self.custom_data).initialize()
            for i in range(self.population_size)
        ]

    def run_experiment(
            self) -> Tuple[List[Individual], List[StatisticsCollector]]:
        initial_individuals = self._generate_initial_individuals()
        population = Population(initial_individuals, self.crossover_prob,
                                self.mutation_prob, self.breed_size,
                                self.num_parent_pairs, self.maximize_fitness,
                                self.mating_selector_cls,
                                self.survivor_selector_cls)
        solution_selector = self.solution_selector_cls(self.num_solutions,
                                                       self.maximize_fitness,
                                                       self.custom_data)
        statistics_collectors = [
            collector_type(self.custom_data)
            for collector_type in self.stats_collector_types
        ]

        # Counts how many times fitness was called for each individual id
        individual_num_fitness_computed: Dict[int, int] = defaultdict(int)
        current_num_fitness_computations = 0
        # Count how many times sd was 0 in a row
        zero_sd_counter = 0

        while population.generation <= self.max_generations:
            print(
                "Evolving Generation {}: {} fitness computed, {:.3f} avg, {:.3f} standard deviation (fitness)."
                .format(population.generation,
                        current_num_fitness_computations,
                        population.avg_fitness(), population.sd_fitness()))

            population.evolve()
            solution_selector.update_individuals(population.population)
            for collector in statistics_collectors:
                collector.collect_data_point(population, solution_selector)

            for individual in population.population:
                if individual.num_fitness_computed != individual_num_fitness_computed[
                        id(individual)]:
                    individual_num_fitness_computed[id(
                        individual)] = individual.num_fitness_computed
            current_num_fitness_computations = sum(
                individual_num_fitness_computed.values())

            if current_num_fitness_computations >= self.max_fitness_computations:
                print(
                    "Max number of fitness computations achieved ({}).".format(
                        current_num_fitness_computations))
                break

            if self.target_fitness is not None \
                and float_less_equal(self.target_fitness,
                    solution_selector.best_individual.fitness()):
                print("Target fitness achieved ({}).".format(
                    solution_selector.best_individual.fitness()))
                break
            if float_equal(population.sd_fitness(), 0.0):
                zero_sd_counter += 1
            else:
                zero_sd_counter = 0

            if self.restart_zero_sd_tolerance is not None \
                and zero_sd_counter >= self.restart_zero_sd_tolerance:
                population.restart_population()
        else:
            print(
                "Maximum generations achieved: {:.3f} avg, {:.3f} standard deviation (fitness)."
                .format(population.avg_fitness(), population.sd_fitness()))

        return (solution_selector.best_individuals, statistics_collectors)


def float_equal(f1: float, f2: float) -> bool:
    return abs(f1 - f2) < EPS


def float_less_equal(f1: float, f2: float) -> bool:
    return float_equal(f1, f2) or f1 < f2
