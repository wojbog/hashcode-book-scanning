from library import Library
from functools import partial

from time import perf_counter
from score_result import print_solution
from algorithms.local_search import local_search_iteration
from algorithms.genetic_lists import genetic

from algorithms.heuristic_solution_generator import *
import cProfile
import pstats


def check_time():
    global start_time

    if perf_counter() - start_time > 60 * 4.5:
        return True
    return False


def read_data():
    tab = input().split()

    library_number = int(tab[1])
    no_of_days = int(tab[2])

    tab = input().split()
    book_score = [int(el) for el in tab]

    from library import Library

    libraries = []

    for i in range(library_number):
        tab = input().split()
        temp = input().split()
        libraries.append(
            Library(i, [int(el) for el in temp], int(tab[1]), int(tab[2]), book_score)
        )

    return no_of_days, book_score, libraries


################################################################


def get_score(
    order_of_signup: list[int],
    books_scores: list[int],
    no_of_days: int,
    libraries: list[Library],
) -> int:
    scored = [False] * len(books_scores)

    score = 0
    total_days = no_of_days

    for library_id in order_of_signup:
        total_days -= libraries[library_id].signup_process
        days_left = total_days
        available_slots = days_left * libraries[library_id].book_chanels

        if available_slots <= 0:
            continue

        for book_id in libraries[library_id].books:
            if scored[book_id]:
                continue

            if available_slots <= 0:
                break

            score += books_scores[book_id]
            scored[book_id] = True
            available_slots -= 1

    return score


def assign_books(
    order_of_signup: list[int],
    books_scores: list[int],
    no_of_days: int,
    libraries: list[Library],
):
    scored = [False] * len(books_scores)

    total_days = no_of_days

    for library_id in order_of_signup:
        library = libraries[library_id]

        total_days -= libraries[library_id].signup_process
        days_left = total_days
        available_slots = days_left * libraries[library_id].book_chanels

        for book_id in libraries[library_id].books:
            if scored[book_id]:
                continue

            if available_slots <= 0:
                break

            library.assignments.append(book_id)

            scored[book_id] = True
            available_slots -= 1


def solve():
    no_of_days, book_scores, libraries = read_data()

    for lib in libraries:
        lib.sort_books(book_scores)

    _, solution = algorithm(libraries, book_scores, no_of_days)

    print_solution(libraries, solution)


def algorithm(libraries, book_scores, no_of_days):
    global start_time

    gain_function = partial(
        get_score, books_scores=book_scores, no_of_days=no_of_days, libraries=libraries
    )
    # score, solution = genetic(libraries, gain_function)

    solution = heuristic_solution_generator2(libraries, book_scores, no_of_days)
    # _, solution = genetic(libraries, gain_function)
    start_time -= 15

    solution = local_search_iteration(
        libraries, gain_function, initial_solution=solution
    )

    assign_books(solution, book_scores, no_of_days, libraries)

    # print("score:", gain_function(solution))

    return gain_function(solution), solution


start_time = perf_counter()
if __name__ == "__main__":
    with cProfile.Profile() as pr:
        solve()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)

    # stats to be visualized by ```snakeviz profile.prof```
    stats.dump_stats(f"profile.prof")
