# Algoritm genetic de determinare al maximului unei functii pe un domeniu
from simulation import Simulation
import yaml

input_vars = None
with open("input.yaml") as input:
    try:
        input_vars = yaml.safe_load(input)
    except yaml.YAMLError as exc:
        print(exc)

dim_pop = input_vars['population_size']
dom_left = input_vars['domain_left']
dom_right = input_vars['domain_right']
a = input_vars['a']
b = input_vars['b']
c = input_vars['c']
prec = input_vars['prec']
crossover_prob = input_vars['crossover_prob']
mutation_prob = input_vars['mutation_prob']
nr_steps = input_vars['num_steps']
use_elitism = input_vars['use_elitism']

simulation = Simulation(dim_pop, dom_left, dom_right, a, b, c, prec, crossover_prob, mutation_prob, nr_steps, use_elitism)

simulation.initialize()
simulation.run_simulation()
print(simulation.get_best_solution())