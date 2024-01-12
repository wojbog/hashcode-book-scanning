from collections.abc import Callable
from library import Library
from functools import partial

from typing import Optional
from time import perf_counter
import random
from score_result import get_answer_from_file, print_solution
import os
import sys
from algorithms.local_search import local_search, local_search_iteration
from algorithms.heuristic_solution_generator import heuristic_solution_generator
import cProfile
import pstats

from dataclasses import dataclass


@dataclass
class Solution:
    no_of_libraries: int
    library_order: list[int]
    books_to_library: list[int]


def read_data(file_name: str):
    file = open(file_name, "r")
    tab = file.readline().split()

    book_number = int(tab[0])
    library_number = int(tab[1])
    no_of_days = int(tab[2])

    tab = file.readline().split()
    book_score = [int(el) for el in tab]

    from library import Library

    libraries = []

    for i in range(library_number):
        tab = file.readline().split()
        temp = file.readline().split()
        libraries.append(
            Library(i, [int(el) for el in temp], int(tab[1]), int(tab[2]), book_score)
        )

    file.close()
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

    score = 0
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


def solve(intput_file: str, output_file: Optional[str]):
    no_of_days, book_scores, libraries = read_data(input_file)

    for lib in libraries:
        lib.sort_books(book_scores)

    start_time = perf_counter()
    score, solution = algorithm(libraries, book_scores, no_of_days)
    end_time = perf_counter()
    print(f"Score: {score}")
    print(f"Solution: {solution[:100]}")
    print(f"Time: {(end_time - start_time) / 60} minutes")
    # in minutes

    if output_file is not None:
        rscore, rsolution = get_answer_from_file(intput_file, output_file)
        print(f"Correct Score: {rscore}")
        print(f"Correct Solution: {rsolution[:100]}")
        print(f"Same?: {solution == rsolution}")

    print_solution(libraries, solution)


def algorithm(libraries, book_scores, no_of_days):
    heuristic_solution = heuristic_solution_generator(
        libraries, book_scores, no_of_days
    )

    gain_function = partial(
        get_score, books_scores=book_scores, no_of_days=no_of_days, libraries=libraries
    )

    solution = local_search_iteration(
        libraries, gain_function, initial_solution=heuristic_solution
    )

    assign_books(solution, book_scores, no_of_days, libraries)

    return gain_function(solution), solution


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = None
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    with cProfile.Profile() as pr:
        solve(input_file, output_file)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)

    # # stats to be visualized by ```snakeviz profile.prof```
    stats.dump_stats("profile.prof")

# no_of_days, book_score, libraries = read_data(input_file)

# score, solution = local_search(libraries, get_score)


# if output_file is not None:
#     print(get_answer_from_file(input_file, output_file))
