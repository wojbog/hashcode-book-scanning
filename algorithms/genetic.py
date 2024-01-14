import random
import numpy.typing as npt
import numpy as np
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
    no_of_generations = 100

    mutation_probability = 0.8

    population, scores = generate_initial_population(
        population_size, libraries, get_score
    )

    for i in range(no_of_generations):
        sorted_indices = np.argsort(scores)[::-1]

        population = population[sorted_indices]
        scores = scores[sorted_indices]

        if check_time():
            return (scores[0], population[0])

        # if (i + 1) % 10 == 0:
        # print(f"Generation {i + 1}")
        # print(f"Best solution: {scores[0]}")

        for i in range(population_size // 2, population_size):
            parent1 = tournament_selection(population, scores)
            if random.random() < mutation_probability:
                mutate(parent1)

            parent2 = tournament_selection(population, scores)
            if random.random() < mutation_probability:
                mutate(parent2)

            child = crossover(parent1, parent2)

            if random.random() < mutation_probability:
                mutate(child)

            population[i] = child
            scores[i] = get_score(child)

    best_score_id = np.argmax(scores)
    best_score = scores[best_score_id]
    best_solution = population[best_score_id]

    return best_score, list(best_solution)


def generate_initial_population(
    population_size: int,
    libraries: list[Library],
    get_score: ScoreFunction,
) -> tuple[npt.NDArray[np.int32], npt.NDArray[np.int32]]:
    population = np.zeros((population_size, len(libraries)), dtype=np.int32)
    scores = np.zeros(population_size, dtype=np.int32)

    for i in range(population_size):
        population[i] = np.random.permutation(len(libraries))
        scores[i] = get_score(population[i])

    return population, scores


def mutate(solution: npt.NDArray) -> None:
    swapped = False
    for i in range(len(solution) - 1):
        if swapped:
            swapped = False
            continue

        if random.random() < 0.1:
            solution[i], solution[i + 1] = solution[i + 1], solution[i]


def crossover(solution1: Solution, solution2: Solution):
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


def tournament_selection(population: npt.NDArray, scores: npt.NDArray) -> npt.NDArray:
    tournament_size = 5

    best_solution_idx = random.randint(0, len(population) - 1)

    best_solution = population[best_solution_idx]
    best_score = scores[best_solution_idx]

    for _ in range(tournament_size - 1):
        solution_idx = random.randint(0, len(population) - 1)
        solution = population[solution_idx]
        score = scores[solution_idx]

        if score > best_score:
            best_solution = solution
            best_score = score

    return best_solution
