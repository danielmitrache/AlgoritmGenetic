from converter import Converter
from operations import Operations
import copy

class Simulation:
    def __init__(self, dim_pop, dom_left, dom_right, a, b, c, prec, crossover_prob, mutation_prob, nr_steps):
        self.dim_pop = dim_pop
        self.dom_left = dom_left
        self.dom_right = dom_right
        self.a = a
        self.b = b
        self.c = c
        self.prec = prec
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.nr_steps = nr_steps


    def initialize(self):
        self.conv = Converter(self.dom_left, self.dom_right, self.prec)
        self.ops = Operations(self.crossover_prob, self.mutation_prob)
        self.population = self.ops.generate(self.dim_pop, self.conv.n)


    def __get_scores(self, population: list[str]) -> list[float]:
        scores = []
        for p in population:
            x = self.conv.decode(p)
            score = self.a * x ** 2 + self.b * x + self.c
            scores.append(score)
        return scores


    def __iterate(self):
        new_population = []
        scores = self.__get_scores(self.population)
        while len(new_population) < self.dim_pop:
            parent1 = self.ops.selection(self.population, scores)
            parent2 = self.ops.selection(self.population, scores)
            child1, child2 = self.ops.crossover(parent1, parent2)
            child1 = self.ops.mutation(child1)
            child2 = self.ops.mutation(child2)
            if len(new_population) == self.dim_pop - 1:
                new_population.append(child1)
            else:
                new_population.extend([child1, child2])
        self.population = copy.deepcopy(new_population)

    
    def run_simulation(self):
        for _ in range(self.nr_steps):
            self.__iterate()

    
    def get_best_solution(self) -> tuple[float, float]:
        scores = self.__get_scores(self.population)
        best_score = max(scores)
        for x, score in zip(self.population, scores):
            if score == best_score:
                sol = self.conv.decode(x)
                return (sol, score)