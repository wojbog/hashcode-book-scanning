from library import Library


def print_solution(libraries: list[Library], order_of_signup: list[int]):
    print(str(len(order_of_signup)))
    for library_id in order_of_signup:
        print(f"{library_id} {len(libraries[library_id].assignments)}")
        libraries[library_id].print_assignments()
