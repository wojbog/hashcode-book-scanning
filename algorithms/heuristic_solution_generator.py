from library import Library


def heuristic_solution_generator(
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

    return [library.id for library in libraries_sorted]
