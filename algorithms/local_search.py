import random
from typing import Callable, List

# from algorithms.types import ScoreFunction
from library import Library


ScoreFunction = Callable[[List[int]], int]

visited = set()


def local_search(
    libraries: list[Library], get_score: ScoreFunction
) -> tuple[int, list[int]]:
    no_of_iterations = 1

    # best_solution = max(
    #     (local_search_iteration(libraries, get_score) for _ in range(no_of_iterations)),
    #     key=get_score,
    # )

    best_score = -1
    best_solution = []
    for i in range(no_of_iterations):
        print(f"iteration {i}")
        solution = local_search_iteration(libraries, get_score)
        score = get_score(solution)
        if score > best_score:
            best_score = score
            best_solution = solution

    return get_score(best_solution), best_solution


def local_search_iteration(
    libraries: list[Library], get_score: ScoreFunction
) -> list[int]:
    current_solution = list(range(len(libraries)))
    random.shuffle(current_solution)

    best_solution = current_solution
    while True:
        print("new iteration")
        better_found = False
        for neighbour in get_neighbours(current_solution):
            if get_score(neighbour) > get_score(best_solution):
                best_solution = neighbour
                better_found = True

        if not better_found:
            print("no better found")
            return best_solution

        print(f"{best_solution=} {get_score(best_solution)=}")
        current_solution = best_solution


def get_neighbours(solution: list[int]):
    neighbours = []

    for i in range(len(solution) - 1):
        new_solution = solution.copy()
        new_solution[i], new_solution[i + 1] = new_solution[i + 1], new_solution[i]

        yield new_solution
