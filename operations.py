import random


class Operations:
    def __init__(self, crossover_prob: float, mutation_prob: float):
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob


    def generate(self, dim_pop: int, length: int) -> list[str]:
        generated = []
        for _ in range(dim_pop):
            num_of_ones = random.randint(0, length)
            indexes = random.sample(range(0, length), num_of_ones)
            gen_num = ["0"] * length
            for idx in indexes:
                gen_num[idx] = "1"
            gen_num = "".join(gen_num)
            generated.append(gen_num)
        return generated


    def get_probs_from_scores(self, scores: list[int | float]) -> list[float]:
        probs = [0.0]
        total = sum(scores)
        curr_total = 0.0
        for score in scores:
            curr_total += score
            probs.append(curr_total / total)
        return probs


    def selection(self, population: list[str], scores: list[int | float]) -> tuple[str, float, int]:
        """Roulette wheel selection with binary search.
        Returns (chromosome, u_value, 1-based index)."""
        probs = self.get_probs_from_scores(scores)
        # Cautam intervalul folosind cautare binara
        u = random.random()
        l, r = 0, len(probs) - 1
        while l < r - 1:
            mid = (l + r) // 2
            if probs[mid] <= u:
                l = mid
            else:
                r = mid
        return population[l], u, l + 1


    def crossover_participation(self, n: int) -> list[tuple[float, bool]]:
        """Returns (u, participates) for each of n chromosomes."""
        result = []
        for _ in range(n):
            u = random.random()
            result.append((u, u < self.crossover_prob))
        return result


    def crossover(self, parent1: str, parent2: str) -> tuple[str, str, int]:
        """Single-point crossover. Returns (child1, child2, break_point).
        break_point=0 means no exchange."""
        break_point = random.randint(0, len(parent1) - 1)
        if break_point == 0:
            return parent1, parent2, 0
        child1 = parent1[:break_point] + parent2[break_point:]
        child2 = parent2[:break_point] + parent1[break_point:]
        return child1, child2, break_point


    def mutation(self, parent: str) -> tuple[str, bool]:
        """Bit-flip mutation. Returns (mutated_chromosome, was_changed)."""
        child = ""
        changed = False
        for bit in parent:
            if random.random() < self.mutation_prob:
                child += str(1 - int(bit))
                changed = True
            else:
                child += bit
        return child, changed
