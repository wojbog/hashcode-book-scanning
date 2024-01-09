class Library():
    def __init__(self,id :int, books, signup_process :int,book_ship:int):
        self.id = id
        self.signup_process = signup_process
        self.book_ship = book_ship
        self.books = books

    def __repr__(self):
        return "<Library: id:" + str(self.id) + " signup_process:" +str(self.signup_process) + " book_ship:" +str(self.book_ship) + " books: " + self.books+ ">"