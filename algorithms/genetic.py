from main import check_time
import random
from library import Library
from typing import Callable, List, Optional, Tuple


ScoreFunction = Callable[[List[int]], int]

Solution = List[int]
SolutionWithScore = tuple[int, Solution]


def genetic(
    libraries: list[Library],
    get_score: ScoreFunction,
) -> tuple[int, Solution]:
    population_size = 200
    no_of_generations = 100

    mutation_probability = 0.8
    # crossover_probability = 0.2

    population = generate_initial_population(population_size, libraries, get_score)

    for i in range(no_of_generations):
        sorted_population = sorted(population, key=lambda x: x[0], reverse=True)

        if check_time():
            return sorted_population[0]

        if (i + 1) % 10 == 0:
            print(f"Generation {i + 1}: {sorted_population[0][0]}")

        population = sorted_population[: population_size // 2]

        for _ in range(population_size // 2):
            # if random.random() < crossover_probability:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)

            child1, child2 = crossover(parent1[1], parent2[1])

            if random.random() < mutation_probability:
                mutate(child1)

            if random.random() < mutation_probability:
                mutate(child2)

            population.append((get_score(child1), child1))
            population.append((get_score(child2), child2))


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


def crossover(solution1: Solution, solution2: Solution) -> Tuple[Solution, Solution]:
    new_solution1 = solution1.copy()
    new_solution2 = solution2.copy()

    p1 = random.randint(0, len(solution1) - 4)
    p2 = random.randint(p1 + 1, len(solution1) - 3)

    q1 = random.randint(p2 + 1, len(solution1) - 2)
    q2 = random.randint(q1 + 1, len(solution1) - 1)

    for i in range(0, p1):
        new_solution1[i] = solution2[i]
        new_solution2[i] = solution1[i]

    for i in range(p2, q1):
        new_solution1[i] = solution2[i]
        new_solution2[i] = solution1[i]

    for i in range(q2, len(solution1)):
        new_solution1[i] = solution2[i]
        new_solution2[i] = solution1[i]

    return new_solution1, new_solution2


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
