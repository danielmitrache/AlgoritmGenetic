# Algoritm genetic de determinare al maximului unei functii pe un domeniu
from simulation import Simulation

lines = []
with open("input.txt", "r") as infile:
    lines = infile.readlines()

problem_input = []
for line in lines:
    line = list(map(float, line.strip().split()))
    problem_input.extend(line)

dim_pop, dom_left, dom_right, a, b, c, prec, crossover_prob, mutation_prob, nr_steps = problem_input
dim_pop = int(dim_pop)
prec = int(prec)
nr_steps = int(nr_steps)

simulation = Simulation(dim_pop, dom_left, dom_right, a, b, c, prec, crossover_prob, mutation_prob, nr_steps)

simulation.initialize()
simulation.run_simulation()
print(simulation.get_best_solution())
