from typing import Type, List, Dict, Optional

from genetic_framework.fitness import FitnessComputer
from genetic_framework.chromosome import Chromosome
from genetic_framework.mutator import Mutator
from genetic_framework.recombiner import Recombiner
from genetic_framework.selectors import SurvivorSelector, MatingSelector, SolutionSelector
from genetic_framework.individual import Individual
from genetic_framework.population import Population


EPS = 1e-9


class Experiment:
    
    def __init__(self, population_size: int, max_generations: int, 
        crossover_prob: float, mutation_prob: float, target_fitness: Optional[float],
        num_solutions: int, breed_size: int, 
        chromosome_cls: Type[Chromosome], 
        fitness_computer_cls: Type[FitnessComputer], 
        mutator_cls: Type[Mutator],
        recombiner_cls: Type[Recombiner],
        mating_selector_cls: Type[MatingSelector],
        survivor_selector_cls: Type[SurvivorSelector],
        solution_selector_cls: Type[SolutionSelector],
        custom_data: Dict = {}) -> None:
        self.population_size = population_size
        self.max_generations = max_generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.target_fitness = target_fitness
        self.num_solutions = num_solutions
        self.breed_size = breed_size
        self.chromosome_cls = chromosome_cls

        self.fitness_computer_cls = fitness_computer_cls
        self.fitness_computer_cls.set_custom_data(custom_data)

        self.mutator_cls = mutator_cls
        self.mutator_cls.set_custom_data(custom_data)
        
        self.recombiner_cls = recombiner_cls
        self.recombiner_cls.set_custom_data(custom_data)
        
        self.mating_selector_cls = mating_selector_cls
        self.mating_selector_cls.set_custom_data(custom_data)

        self.survivor_selector_cls = survivor_selector_cls
        self.survivor_selector_cls.set_custom_data(custom_data)

        self.solution_selector_cls = solution_selector_cls
        self.custom_data = custom_data

    def _generate_initial_individuals(self) -> List[Individual]:
        """Internal method used to generate individuals for the first 
        generation of the experiment"""
        return [Individual(self.chromosome_cls, self.fitness_computer_cls, 
            self.mutator_cls, self.recombiner_cls, 1, self.custom_data).initialize()
                for i in range(self.population_size)]

    def run_experiment(self) -> List[Individual]:
        initial_individuals = self._generate_initial_individuals()
        population = Population(initial_individuals, self.crossover_prob, 
            self.mutation_prob, self.breed_size, self.mating_selector_cls,
            self.survivor_selector_cls)
        solution_selector = self.solution_selector_cls(self.num_solutions, self.custom_data)

        while population.generation <= self.max_generations:
            print("Evolving Generation {}: {:.3f} avg, {:.3f} standard deviation (fitness)."
                .format(population.generation, population.avg_fitness(),
                     population.sd_fitness()))

            population.evolve()
            solution_selector.update_individuals(population.population)

            if self.target_fitness is not None \
                and float_less_equal(self.target_fitness, 
                    solution_selector.best_individual.fitness()):
                    print("Target fitness achieved ({})."
                        .format(solution_selector.best_individual.fitness()))
                    break
        else:
            print("Maximum generations achieved: {:.3f} avg, {:.3f} standard deviation (fitness)."
                .format(population.avg_fitness(), population.sd_fitness()))

        return solution_selector.best_individuals
            

def float_less_equal(f1: float, f2: float) -> bool:
    return abs(f1-f2) < EPS or f1 < f2
    