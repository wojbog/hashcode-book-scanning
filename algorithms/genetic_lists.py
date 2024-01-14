import random
from library import Library
from typing import Callable, List


ScoreFunction = Callable[[List[int]], int]

Solution = List[int]
SolutionWithScore = tuple[int, Solution]


def genetic(
    libraries: list[Library],
    get_score: ScoreFunction,
) -> tuple[int, Solution]:
    from main import check_time

    population_size = 200

    mutation_probability = 0.8

    population = generate_initial_population(population_size, libraries, get_score)

    generation = 0

    while not check_time():
        population.sort(key=lambda x: x[0], reverse=True)

        if check_time():
            return population[0]

        # if (generation + 1) % 10 == 0:
        #     print(f"Generation {generation + 1}: {population[0][0]}")
        #     print(f"Best solution: {population[0][0]}")

        for i in range(population_size // 2, population_size):
            parent1 = tournament_selection(population)
            if random.random() < mutation_probability:
                mutate(parent1[1])

            parent2 = tournament_selection(population)
            if random.random() < mutation_probability:
                mutate(parent2[1])

            child = crossover(parent1[1], parent2[1])

            if random.random() < mutation_probability:
                mutate(child)

            population[i] = (get_score(child), child)

        generation += 1

    return max(population, key=lambda x: x[0])


def generate_initial_population(
    population_size: int,
    libraries: list[Library],
    get_score: ScoreFunction,
) -> list[SolutionWithScore]:
    initial_population = []

    for _ in range(population_size):
        solution = list(range(len(libraries)))
        random.shuffle(list(range(len(libraries))))

        initial_population.append((get_score(solution), solution))

    return initial_population


def mutate(solution: Solution) -> None:
    swapped = False
    for i in range(len(solution) - 1):
        if swapped:
            swapped = False
            continue

        if random.random() < 0.1:
            solution[i], solution[i + 1] = solution[i + 1], solution[i]


def crossover(solution1: Solution, solution2: Solution) -> Solution:
    p1 = random.randint(0, len(solution1) - 4)
    p2 = random.randint(p1 + 1, len(solution1) - 3)

    q1 = random.randint(p2 + 1, len(solution1) - 2)
    q2 = random.randint(q1 + 1, len(solution1) - 1)

    child = solution1.copy()
    missing = set()
    for i in range(0, p1):
        missing.add(solution1[i])
    for i in range(p2 + 1, q1):
        missing.add(solution1[i])
    for i in range(q2 + 1, len(solution1)):
        missing.add(solution1[i])

    i2 = 0
    for i in range(0, p1):
        while not solution2[i2] in missing:
            i2 += 1
        child[i] = solution2[i2]
        i2 += 1

    for i in range(p2 + 1, q1):
        while not solution2[i2] in missing:
            i2 += 1
        child[i] = solution2[i2]
        i2 += 1

    for i in range(q2 + 1, len(solution1)):
        while not solution2[i2] in missing:
            i2 += 1
        child[i] = solution2[i2]
        i2 += 1

    return child


def tournament_selection(population: list[SolutionWithScore]) -> SolutionWithScore:
    tournament_size = 5

    best_solution = random.choice(population)
    best_score = best_solution[0]

    for _ in range(tournament_size - 1):
        solution = random.choice(population)

        if solution[0] > best_score:
            best_solution = solution
            best_score = solution[0]

    return best_solution
