from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from requests import get
from pprint import pprint



class BookUnavailableError(Exception):
    pass

class UserBorrowLimitExceeded(Exception):
    pass

class UnauthorizedReturnError(Exception):
    pass

class MaxLoansReachedError(Exception):
    pass

OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"

class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
    
    def __str__(self):
        return f"{self.title} by {self.author} - ISBN: {self.isbn}"


class User:
    
    def __init__(self, name: str, user_id: str):
        self.name = name
        self.user_id = user_id


class Loan:
    def __init__(self, book: Book, user: User, days=14):
        self.book = book
        self.user = user
        self.borrowed_at = datetime.now()
        self.due_date = self.borrowed_at + timedelta(days=days)
        self.returned_at: datetime | None = None

    @property
    def is_active(self) -> bool:
        return self.returned_at is None

    def _return_book(self):
        self.returned_at = datetime.now()


class Library:
    MAX_BOOKS = 3
    def __init__(self):
        self.books: list[Book] = []
        self.users: dict[str, User] = {}
        self.loans: list[Loan] = []

    def add_book(self, book: Book):
        self.books.append(book)


    def find_all_books(self):
        return self.books

    def is_user_permitted(self, user: User) -> bool:
        return len(self.get_active_loans_for_user(user)) < self.MAX_BOOKS
    

    def get_active_loans(self) -> list[Loan]:
        return [loan for loan in self.loans if loan.is_active]


    def borrow_book(self, book: Book, user: User):
        if self.get_active_loan_for_book(book) is None:
            if self.is_user_permitted(user):
                new_loan = Loan(book, user)
                self.loans.append(new_loan)
                self.store_user(user)
            else:
                raise MaxLoansReachedError(f"{user.name} currrently has {len(self.get_active_loans_for_user(user))} books borrowed. You can only borrow a maximum of {self.MAX_BOOKS} books at once.")
        else:
            raise BookUnavailableError(f"{book.title} is not available.")


    def return_book(self, user: User, book: Book):
        current_loan = self.get_active_loan_for_book(book)
        if current_loan is None or current_loan.user != user:
            raise ValueError(f"{user.name} doesn't currently possess {book.title}.")
        else:
            current_loan._return_book()
            return f"{user.name} successfully returned {book.title}."

    
    def get_active_loans_for_user(self, user: User) -> list[Loan]:
        return [loan for loan in self.get_active_loans() if loan.user == user]


    def get_active_loan_for_book(self, book: Book) -> Loan | None:
        for loan in self.get_active_loans():
            if loan.book == book:
                return loan
        return None


    def find_available_books(self) -> list[Book]:
        loaned_books = [loan.book for loan in self.get_active_loans()]
        return [book for book in self.books if book not in loaned_books]
    

    def store_user(self, user: User):
        user_id = user.user_id
        if self.users.get(user_id) is None:
            self.users[user_id] = user
        

    def get_all_users(self) -> list[User]:
        return [user for _, user in self.users.items()]
    
   

def retrieve_api_books(url: str, topic: str):
    response = get(f"{url}?q={topic}&limit=5")
    data = response.json()
    return data.get('docs')


# pprint(retrieve_api_books(OPEN_LIBRARY_URL, "football"))


# book1 = Book("Harry Potter 1", "JK Rowling", "12345")
# book2 = Book("Harry Potter 2", "JK Rowling", "52342")
# book3 = Book("Harry Potter 3", "JK Rowling", "97876")
# book4 = Book("Harry Potter 4", "JK Rowling", "67728")
# book5 = Book("Harry Potter 5", "JK Rowling", "00291")
# book6 = Book("Harry Potter 6", "JK Rowling", "54634")
# book7 = Book("Harry Potter 7", "JK Rowling", "64321")
# book8 = Book("Harry Potter 8", "JK Rowling", "23577")


# kayode = User("Kayode", "00001")
# shiloh = User("Shiloh", "00002")
# lanre = User("Lanre", "00003")


# my_library = Library()
# for book in [book1, book2, book3, book4, book5, book6, book7, book8]:
#     my_library.add_book(book)
# my_library.show_available_books()
# print("\n")

# for user in [kayode, shiloh, lanre]:
#     user.show_books_borrowed()
# print("\n")

# my_library.borrow_book(book1, kayode)
# my_library.borrow_book(book2, lanre)
# my_library.borrow_book(book3, shiloh)
# my_library.borrow_book(book5, kayode)
# print("\n")


# for user in [kayode, shiloh, lanre]:
#     user.show_books_borrowed()

# print("\n")
# my_library.show_available_books()
# print("\n")
# my_library.show_available_books()

# my_library.show_user_status("00001")
# print("\n")
# my_library.return_book(kayode, book5)
# print("\n")

# my_library.return_book(kayode, book4)
# print("\n")
# my_library.borrow_book(book6, kayode)
# my_library.borrow_book(book7, kayode)
# # my_library.borrow_book(book8, kayode)
# print("\n")

# my_library.show_user_status("00001")
# print("\n")

# my_users = my_library.users
# print(my_library.show_all_user_info())
# print("\n")

# my_library.show_available_books()

# print(book1)

    