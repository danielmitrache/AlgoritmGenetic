from converter import Converter
from operations import Operations

class Simulation:
    def __init__(self, dim_pop, dom_left, dom_right, a, b, c, prec, crossover_prob, mutation_prob, nr_steps, use_elitism):
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
        self.use_elitism = use_elitism


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


    def __write_pop(self, population: list[str], scores: list[float]):
        for i, (chrom, score) in enumerate(zip(population, scores)):
            x = self.conv.decode(chrom)
            self.f.write(f"{i+1}: {chrom} x={x} f={score}\n")


    def iterate(self, verbose: bool = False):
        scores = self.__get_scores(self.population)
        best_idx = scores.index(max(scores))
        elite = self.population[best_idx]

        if verbose:
            self.f.write("Populatia initiala\n")
            self.__write_pop(self.population, scores)

            total = sum(scores)
            self.f.write("\nProbabilitati selectie \n")
            for i, score in enumerate(scores):
                self.f.write(f"cromozom {i+1} probabilitate {score / total}\n")

            self.f.write("\nIntervale probabilitati selectie \n")
            self.f.write(" ".join(str(q) for q in self.ops.get_probs_from_scores(scores)) + " \n\n")

        # Selectie
        new_pop = []
        for _ in range(self.dim_pop):
            chrom, u, idx = self.ops.selection(self.population, scores)
            new_pop.append(chrom)
            if verbose:
                self.f.write(f"u={u} selectam cromozomul {idx} \n")

        if verbose:
            self.f.write("\nDupa selectie:\n")
            self.__write_pop(new_pop, self.__get_scores(new_pop))

        # Incrucisare
        if verbose:
            self.f.write(f"\nProbabilitatea de incrucisare {self.crossover_prob}\n")

        participation = self.ops.crossover_participation(self.dim_pop)

        if verbose:
            for i, (u, participates) in enumerate(participation):
                if participates:
                    self.f.write(f"{i+1}: {new_pop[i]} u={u}<{self.crossover_prob} participa \n")
                else:
                    self.f.write(f"{i+1}: {new_pop[i]} u={u}\n")

        participant_idx = [i for i, (_, p) in enumerate(participation) if p]
        post_crossover = new_pop[:]

        limit = len(participant_idx)
        if limit % 2 == 1:
            if limit >= 3:
                limit -= 3 
            else:
                limit = 0  # singur participant, nu poate face crossover

        for k in range(0, limit, 2):
            i, j = participant_idx[k], participant_idx[k + 1]
            c1, c2, bp = self.ops.crossover(new_pop[i], new_pop[j])
            post_crossover[i] = c1
            post_crossover[j] = c2
            if verbose:
                self.f.write(f"\nRecombinare dintre cromozomul {i+1} cu cromozomul {j+1}:\n")
                self.f.write(f"{new_pop[i]} {new_pop[j]} punct {bp}\n")
                self.f.write(f"Rezultat {c1} {c2}\n")

        if len(participant_idx) % 2 == 1 and len(participant_idx) >= 3:
            i, j, k = participant_idx[-3], participant_idx[-2], participant_idx[-1]
            c1, c2, c3, bp1, bp2 = self.ops.crossover3(new_pop[i], new_pop[j], new_pop[k])
            post_crossover[i] = c1
            post_crossover[j] = c2
            post_crossover[k] = c3
            if verbose:
                self.f.write(f"\nRecombinare dintre cromozomii {i+1}, {j+1}, {k+1}:\n")
                self.f.write(f"{new_pop[i]} {new_pop[j]} {new_pop[k]} puncte {bp1} {bp2}\n")
                self.f.write(f"Rezultat {c1} {c2} {c3}\n")

        if verbose:
            self.f.write("\nDupa recombinare:\n")
            self.__write_pop(post_crossover, self.__get_scores(post_crossover))

        # Mutatie
        if verbose:
            self.f.write(f"\nProbabilitate de mutatie pentru fiecare gena {self.mutation_prob}\n")

        post_mutation = []
        mutated = []
        for i, chrom in enumerate(post_crossover):
            new_chrom, changed = self.ops.mutation(chrom)
            post_mutation.append(new_chrom)
            if changed:
                mutated.append(i + 1)

        if verbose:
            self.f.write("Au fost modificati cromozomii:\n")
            for idx in mutated:
                self.f.write(f"{idx}\n")
            self.f.write("\nDupa mutatie:\n")
            self.__write_pop(post_mutation, self.__get_scores(post_mutation))
            self.f.write("\n")

        # Elitism: inlocuim cel mai slab cu elita
        if self.use_elitism:
            final_scores = self.__get_scores(post_mutation)
            worst_idx = final_scores.index(min(final_scores))
            post_mutation[worst_idx] = elite
        self.population = post_mutation


    def run_simulation(self):
        with open("Evolutie.txt", "w") as f:
            self.f = f
            max_values = []
            mean_values = []

            for step in range(self.nr_steps):
                self.iterate(step == 0)
                scores = self.__get_scores(self.population)
                max_values.append(max(scores))
                mean_values.append(sum(scores) / len(scores))

            f.write("\nEvolutia maximului \n")
            for mv in max_values:
                f.write(f"{mv}\n")

            f.write("\nEvolutia mediei \n")
            for mv in mean_values:
                f.write(f"{mv}\n")


    def get_best_solution(self) -> tuple[float, float]:
        scores = self.__get_scores(self.population)
        best_score = max(scores)
        for x, score in zip(self.population, scores):
            if score == best_score:
                sol = self.conv.decode(x)
                return (sol, score)


    def get_all_solutions(self) -> list[tuple[float, float]]:
        return list(zip(list(map(self.conv.decode, self.population)), self.__get_scores(self.population)))
