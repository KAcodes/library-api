from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime, timedelta



class BookStatus(Enum):
    AVAILABLE = 'available'
    CHECKED_OUT = 'checked out'
    RESERVED = 'reserved'

class Book:
    def __init__(self, title: str, author: str, isbn: str, status=BookStatus.AVAILABLE):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def check_out_book(self):
        self.status = BookStatus.CHECKED_OUT
    
    def return_book(self):
        self.status = BookStatus.AVAILABLE

    def is_book_available(self) -> bool:
        return self.status == BookStatus.AVAILABLE
    
    def __str__(self):
        return f"{self.title} by {self.author} - ISBN: {self.isbn}"


class User:
    MAX_BOOKS = 3
    def __init__(self, name: str, user_id: str):
        self.name = name
        self.user_id = user_id
        self._borrowed_books: list[Book] = []

    @property
    def borrowed_books(self):
        return tuple(self._borrowed_books)

    def _add_book(self, book: Book):
        self._borrowed_books.append(book)

    def _remove_book(self, book: Book):
        self._borrowed_books.remove(book)

    def is_user_permitted(self) -> bool:
        number_books_borrowed = len(self._borrowed_books)
        return number_books_borrowed < self.MAX_BOOKS

    def show_books_borrowed(self):
        print(f"{self.name} currrently has these books borrowed:")
        for book in self._borrowed_books:
            print(book)  


class Library:
    def __init__(self):
        self.books: list[Book] = []
        self.users = {}

    def add_book(self, book: Book):
        self.books.append(book)

    def register_user(self, user: User):
        self.users[user.user_id] = user

    def borrow_book(self, book: Book, user: User):
        if book.is_book_available():
            if user.is_user_permitted():
                book.check_out_book()
                user._add_book(book)
                self.users[user.user_id] = user
            else:
                raise f"{user.name} currrently has {len(user.borrowed_books)} books borrowed. You can only borrow a maximum of 3 books at once."
        else:
            raise f"Sorry {user.name} {book.title} is currently unavailable."

    def return_book(self, user: User, book: Book):
        if book not in user.borrowed_books:
            print(f"You doesn't currently possess {book.title}.")
        else:
            user._remove_book(book)
            book.return_book()
            print(f"{user.name} successfully returned {book.title}.")

            self.users[user.user_id] = user
    
    def show_available_books(self):
        books_status = [book for book in self.books if book.status == BookStatus.CHECKED_OUT]
        if not self.books:
            print("No Books In Library")
        elif len(books_status) == len(self.books):
            print("All Books Currently Checked Out")
        else:
            print("Books currently available in our library:")
        for book in self.books:
            if book.status == BookStatus.AVAILABLE:
                print(book.title)

    def show_user_status(self, user_id: str):
        user = self.users.get(user_id)
        if user is not None:
            user.show_books_borrowed()
        else:
            print("User not in our database")

    def show_all_user_info(self):
        for user_id, user in self.users.items():
            # print(f"{user.name} - {user_id}:")
            user.show_books_borrowed()
            print("\n")



class Loan:
    def __init__(self, book, user, days=14):
        self.book = book
        self.user = user
        self.borrowed_at = datetime.now()
        self.due_date = self.borrowed_at + timedelta(days=days)
        self.returned_at = None

    @property
    def is_active(self) -> bool:
        return self.returned_at is None

    def return_book(self):
        self.returned_at = datetime.now()



book1 = Book("Harry Potter 1", "JK Rowling", "12345")
book2 = Book("Harry Potter 2", "JK Rowling", "52342")
book3 = Book("Harry Potter 3", "JK Rowling", "97876")
book4 = Book("Harry Potter 4", "JK Rowling", "67728")
book5 = Book("Harry Potter 5", "JK Rowling", "00291")
book6 = Book("Harry Potter 6", "JK Rowling", "54634")
book7 = Book("Harry Potter 7", "JK Rowling", "64321")
book8 = Book("Harry Potter 8", "JK Rowling", "23577")


kayode = User("Kayode", "00001")
shiloh = User("Shiloh", "00002")
lanre = User("Lanre", "00003")


my_library = Library()
for book in [book1, book2, book3, book4, book5, book6, book7, book8]:
    my_library.add_book(book)
my_library.show_available_books()
print("\n")

for user in [kayode, shiloh, lanre]:
    user.show_books_borrowed()
print("\n")

my_library.borrow_book(book1, kayode)
my_library.borrow_book(book2, lanre)
my_library.borrow_book(book3, shiloh)
my_library.borrow_book(book5, kayode)
print("\n")


for user in [kayode, shiloh, lanre]:
    user.show_books_borrowed()

print("\n")
my_library.show_available_books()
print("\n")
my_library.show_available_books()

my_library.show_user_status("00001")
print("\n")
my_library.return_book(kayode, book5)
print("\n")

my_library.return_book(kayode, book4)
print("\n")
my_library.borrow_book(book6, kayode)
my_library.borrow_book(book7, kayode)
# my_library.borrow_book(book8, kayode)
print("\n")

my_library.show_user_status("00001")
print("\n")

my_users = my_library.users
print(my_library.show_all_user_info())
print("\n")

my_library.show_available_books()

print(book1)

    