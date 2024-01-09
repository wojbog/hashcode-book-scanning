import random


def read_data():
    tab = input().split()

    book_number = int(tab[0])
    library_number = int(tab[1])
    no_of_days = int(tab[2])

    # print(book_number, library_number, no_of_days)

    tab = input().split()
    book_score = [int(el) for el in tab]

    # print(book_score)

    from library import Library

    libraries = []

    for i in range(library_number):
        tab = input().split()
        temp = input().split()
        libraries.append(Library(i, [int(el) for el in temp], int(tab[1]), int(tab[2])))

    # print(libraries)
    return no_of_days, book_score, libraries


################################################################
# algorithm
no_of_days, book_score, libraries = read_data()
# print(libraries[0].books)
# libraries[0].sort_books(book_score)
# print(libraries[0].books)


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


def local_search():
    initial_solution = list(range(len(libraries)))

    random.shuffle(initial_solution)

    best_solution = initial_solution
    while True:
        better_found = False
        for neighbour in get_neighbours(initial_solution):
            if get_score(neighbour) > get_score(best_solution):
                best_solution = neighbour
                better_found = True
        if not better_found:
            return best_solution


def get_neighbours(solution: list[int]) -> list[list[int]]:
    neighbours = []

    for i in range(len(solution) - 1):
        new_solution = solution.copy()
        new_solution[i], new_solution[i + 1] = new_solution[i + 1], new_solution[i]

        neighbours.append(new_solution)

    return neighbours


def solve():
    for library in libraries:
        library.sort_books(book_score)

    no_of_iterations = 100

    best_solution = max((local_search() for _ in range(no_of_iterations)))

    print(get_score(best_solution))
    print(best_solution)


if __name__ == "__main__":
    solve()
