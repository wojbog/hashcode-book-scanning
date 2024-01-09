from library import Library


def get_answer_from_file(input_file: str, answer_file: str) -> tuple[int, list[int]]:
    from main import read_data, get_score

    no_of_days, book_score, libraries = read_data(input_file)
    with open(answer_file, "r") as file:
        number_of_libraries = int(file.readline())
        solution = []
        for _ in range(number_of_libraries):
            id_library, number_of_books = file.readline().split()
            solution.append(int(id_library))
            books = [int(el) for el in file.readline().split()]
            libraries[int(id_library)].books = books

    return get_score(solution), solution
