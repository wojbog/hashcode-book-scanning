from library import Library


def get_answer_from_file(input_file: str, answer_file: str) -> tuple[int, list[int]]:
    from main import read_data, get_score

    no_of_days, book_scores, libraries = read_data(input_file)
    with open(answer_file, "r") as file:
        number_of_libraries = int(file.readline())
        solution = []
        for _ in range(number_of_libraries):
            id_library, number_of_books = file.readline().split()
            solution.append(int(id_library))
            books = [int(el) for el in file.readline().split()]
            libraries[int(id_library)].books = books

    return get_score(solution, book_scores, no_of_days, libraries), solution


def print_solution(libraries: list[Library], order_of_signup: list[int]):
    with open("output.txt", "w") as file:
        file.write(str(len(order_of_signup)))
        file.write("\n")
        for library_id in order_of_signup:
            file.write(f"{library_id} {len(libraries[library_id].assignments)}\n")
            libraries[library_id].print_assignments(file=file)
    # print(len(libraries))
    # for library_id in order_of_signup:
    #     print(f"{library_id} {len(libraries[library_id].assignments)}")
    #     libraries[library_id].print_assignments()
