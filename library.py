from collections import deque
import sys


class Library:
    def __init__(self, id: int, books, signup_process: int, book_ship: int, prority):
        self.id = id
        self.signup_process = signup_process
        self.book_chanels: int = book_ship
        self.books = books
        self.assignments = deque()

        self.sort_books(prority)

    def __repr__(self):
        return (
            "<Library: id:"
            + str(self.id)
            + " signup_process:"
            + str(self.signup_process)
            + " book_ship:"
            + str(self.book_chanels)
            + " number_of_books:"
            + str(len(self.books))
            + ">"
        )

    def sort_books(self, prority):
        self.books.sort(key=lambda x: prority[x], reverse=True)

    def print_assignments(self, file=sys.stdout):
        for book_id in self.assignments:
            file.write(str(book_id))
            file.write(" ")
        file.write("\n")
