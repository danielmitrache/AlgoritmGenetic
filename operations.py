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


    def selection(self, population: list[str], scores: list[int | float]):
        probs = [0]
        curr_total = 0
        min_score = min(scores)
        if min_score < 0:
            scores = [score + abs(min_score) + 0.001 for score in scores]
        total = sum(scores)
        for score in scores:
            curr_total += score
            probs.append(curr_total / total)
        selected = random.random()
        idx = 0 
        while idx < len(population) - 1 and not probs[idx] <= selected <= probs[idx + 1]:
            idx += 1
        return population[idx] 


    def crossover(self, parent1: str, parent2: str, idx: int | None = None) -> tuple[str, str]:
        """If idx is None, then a random cut point will be chosen."""
        if random.random() > self.crossover_prob:
            return (parent1, parent2)
        
        if idx is None:
            idx = random.randint(1, len(parent1) - 1)

        child1 = parent1[:idx] + parent2[idx:]
        child2 = parent1[idx:] + parent2[:idx]
        return (child1, child2)


    def mutation(self, parent: str) -> str:
        child = ""
        for bit in parent:
            if random.random() > self.mutation_prob:
                child += bit
            else:
                child += str(1 - int(bit))
        return child