from library import Library


def heuristic_solution_generator1(
    libraries: list[Library], book_scores: list[int], no_of_days: int
) -> list[int]:
    def library_score(library: Library) -> float:
        slots = (no_of_days - library.signup_process) * library.book_chanels
        score = 0
        for slot_id in range(slots):
            if slot_id >= len(library.books):
                break

            book_id = library.books[slot_id]

            score += book_scores[book_id]

        return score

    libraries_sorted = sorted(libraries, key=library_score, reverse=True)

    print("heuristic done")

    return [library.id for library in libraries_sorted]


def heuristic_solution_generator2(
    libraries: list[Library], book_scores: list[int], no_of_days: int
) -> list[int]:
    book_is_added = [False] * len(book_scores)
    library_is_taken = [False] * len(libraries)
    library_score = [0] * len(libraries)

    solution = []

    days_left = no_of_days

    for _ in libraries:
        calculate_library_scores(
            days_left,
            book_scores,
            library_score,
            libraries,
            book_is_added,
            library_is_taken,
        )

        best_library = get_best_lib(libraries, library_is_taken, library_score)

        library_is_taken[best_library.id] = True

        days_left -= best_library.signup_process
        if days_left <= 0:
            days_left += best_library.signup_process
            continue

        empty_library = append_books(days_left, best_library, book_is_added)

        if not empty_library:
            solution.append(best_library.id)
        else:
            days_left += best_library.signup_process

    return solution


def calculate_library_scores(
    days_left: int,
    book_scores: list[int],
    library_score: list[int],
    libraries: list[Library],
    book_is_added: list[bool],
    library_is_taken: list[bool],
):
    for library in libraries:
        if library_is_taken[library.id]:
            library_score[library.id] = 0
            continue

        available_slots = (days_left - library.signup_process) * library.book_chanels

        if available_slots <= 0:
            library_score[library.id] = 0
            continue

        for book_id in library.books:
            if book_is_added[book_id]:
                continue

            if available_slots <= 0:
                break

            available_slots -= 1

            library_score[library.id] += book_scores[book_id]


def get_best_lib(
    libraries: list[Library], library_is_taken: list[bool], library_score: list[int]
):
    best_library = Library(-1, [], -1, -1, -1)
    best_library_score = -1

    for library in libraries:
        if library_is_taken[library.id]:
            continue

        current_library_score = library_score[library.id] / library.signup_process

        if current_library_score > best_library_score:
            best_library = library
            best_library_score = current_library_score

    return best_library


def append_books(days_left: int, best_library: Library, book_is_added: list[bool]):
    available_slots = days_left * best_library.book_chanels

    empty_library = True
    for book_id in best_library.books:
        if book_is_added[book_id]:
            continue

        if available_slots <= 0:
            break

        available_slots -= 1

        best_library.assignments.append(book_id)
        book_is_added[book_id] = True
        empty_library = False

    return empty_library
