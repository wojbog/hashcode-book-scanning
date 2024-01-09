from library import Library
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

no_of_days, book_score, libraries = read_data()

file = open("./output/a_example.txt","r")

number_of_libraries = int(file.readline())
solution = []
for _ in range(number_of_libraries):
    id_library, number_of_books = file.readline().split()
    solution.append(int(id_library))
    books = [int(el) for el in file.readline().split()]
    libraries[int(id_library)].books = books

file.close()

print(get_score(solution))