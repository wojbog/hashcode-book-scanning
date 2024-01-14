import random
from typing import Callable, List

from library import Library


ScoreFunction = Callable[[List[int]], int]


def local_search(
    libraries: list[Library],
    get_score: ScoreFunction,
) -> tuple[int, list[int]]:
    no_of_iterations = 1

    best_score = -1
    best_solution = []
    for i in range(no_of_iterations):
        solution = local_search_iteration(libraries, get_score)
        score = get_score(solution)
        if score > best_score:
            best_score = score
            best_solution = solution

    return get_score(best_solution), best_solution


def local_search_iteration(
    libraries: list[Library],
    get_score: ScoreFunction,
    initial_solution: list[int] | None = None,
) -> list[int]:
    from main import check_time

    enhancments = 0

    if initial_solution is None:
        current_solution = list(range(len(libraries)))
        random.shuffle(current_solution)
    else:
        current_solution = initial_solution

    best_solution = current_solution
    best_score = get_score(best_solution)
    while True:
        for neighbour in get_neighbours(current_solution):
            if check_time():
                return best_solution

            current_score = get_score(neighbour)
            if current_score > best_score:
                best_solution = neighbour
                best_score = current_score
                break

        if best_solution == current_solution:
            break
        else:
            enhancments += 1

        current_solution = best_solution

        if check_time():
            return best_solution

    return best_solution


def get_neighbours(solution: list[int]):  # -> Generator[List[int]]]:
    for i in range(len(solution) - 1):
        new_solution = solution.copy()
        new_solution[i], new_solution[i + 1] = new_solution[i + 1], new_solution[i]

        yield new_solution
