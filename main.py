from collections.abc import Callable

from typing import Optional
from time import perf_counter
import random
from score_result import get_answer_from_file
import os
import sys
from algorithms.local_search import local_search
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
        libraries.append(Library(i, [int(el) for el in temp], int(tab[1]), int(tab[2])))

    file.close()
    return no_of_days, book_score, libraries


################################################################


def get_score(order_of_signup: list[int]) -> int:
    scored = [False] * len(book_score)

    score = 0
    total_days = no_of_days
    for library_id in order_of_signup:
        total_days -= libraries[library_id].signup_process
        days_left = total_days
        slots = days_left * libraries[library_id].book_chanels

        for slot_id in range(slots):
            if slot_id >= len(libraries[library_id].books):
                break

            book_id = libraries[library_id].books[slot_id]
            if scored[book_id]:
                continue

            score += book_score[book_id]
            scored[book_id] = True
    return score


def solve(intput_file: str, output_file: Optional[str], algorithm: Callable):
    global no_of_days, book_score, libraries

    no_of_days, book_score, libraries = read_data(input_file)

    for lib in libraries:
        lib.sort_books(book_score)
    start_time = perf_counter()
    score, solution = algorithm(libraries, get_score)
    end_time = perf_counter()
    print(f"Score: {score}")
    print(f"Solution: {solution}")
    print(f"Time: {end_time - start_time}")

    if output_file is not None:
        score, solution = get_answer_from_file(intput_file, output_file)
        print(f"Correct Score: {score}")
        print(f"Correct Solution: {solution}")


input_file = sys.argv[1]
output_file = None
if len(sys.argv) > 2:
    output_file = sys.argv[2]


with cProfile.Profile() as pr:
    solve(input_file, output_file, local_search)

stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)

# stats to be visualized by ```snakeviz profile.prof```
stats.dump_stats("profile.prof")

# no_of_days, book_score, libraries = read_data(input_file)

# score, solution = local_search(libraries, get_score)


# if output_file is not None:
#     print(get_answer_from_file(input_file, output_file))
