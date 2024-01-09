tab=input().split()

book_number = int(tab[0])
library_number = int(tab[1])
scanning_number = int(tab[2])

print(book_number, library_number, scanning_number)

tab=input().split()
book_score = [int(el) for el in tab]

print(book_score)

from library import Library

libraries = []

for i in range(library_number):
    tab=input().split()
    temp = input().split()
    libraries.append(Library(i,[int(el) for el in temp],int(tab[1]),int(tab[2])))

print(libraries)


