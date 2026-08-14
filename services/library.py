from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from requests import get
from pprint import pprint

from repositories.books import BookRepository
from repositories.users import UserRepository
from repositories.loans import LoanRepository
from clients.open_library import retrieve_api_books



class BookUnavailableError(Exception):
    pass

class UserBorrowLimitExceeded(Exception):
    pass

class UnauthorizedReturnError(Exception):
    pass

class MaxLoansReachedError(Exception):
    pass






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


class LibraryService:
    MAX_BOOKS = 3
    def __init__(self, book_repository: BookRepository, user_repository: UserRepository, loan_repository: LoanRepository):
            self.book_repository = book_repository
            self.user_repository = user_repository
            self.loan_repository = loan_repository


    def get_all_books(self):
            return self.book_repository.fetch_all_books()

    def transform_books(self, books: list) -> list:
        books_cleaned = []
        for book in books:
            if not book.keys() >= {'title', 'author_name', 'cover_i', 'key'}:
                continue
            key = book["key"]
            id = key.split('/works/')[1]

            books_cleaned.append((id, book["title"], book["author_name"][0], book["cover_i"]))

        return books_cleaned

    def import_books(self, topic):
        books = retrieve_api_books(topic)
        cleaned_books = self.transform_books(books)
        returned_count = self.book_repository.populate_table(cleaned_books)
        return returned_count

    # def add_book(self, book: Book):
    #     self.books.append(book)


    # def find_all_books(self):
    #     return self.books

    # def is_user_permitted(self, user: User) -> bool:
    #     return len(self.get_active_loans_for_user(user)) < self.MAX_BOOKS
    

    # def get_active_loans(self) -> list[Loan]:
    #     return [loan for loan in self.loans if loan.is_active]


    # def borrow_book(self, book: Book, user: User):
    #     if self.get_active_loan_for_book(book) is None:
    #         if self.is_user_permitted(user):
    #             new_loan = Loan(book, user)
    #             self.loans.append(new_loan)
    #             self.store_user(user)
    #         else:
    #             raise MaxLoansReachedError(f"{user.name} currrently has {len(self.get_active_loans_for_user(user))} books borrowed. You can only borrow a maximum of {self.MAX_BOOKS} books at once.")
    #     else:
    #         raise BookUnavailableError(f"{book.title} is not available.")


    # def return_book(self, user: User, book: Book):
    #     current_loan = self.get_active_loan_for_book(book)
    #     if current_loan is None or current_loan.user != user:
    #         raise ValueError(f"{user.name} doesn't currently possess {book.title}.")
    #     else:
    #         current_loan._return_book()
    #         return f"{user.name} successfully returned {book.title}."

    
    # def get_active_loans_for_user(self, user: User) -> list[Loan]:
    #     return [loan for loan in self.get_active_loans() if loan.user == user]


    # def get_active_loan_for_book(self, book: Book) -> Loan | None:
    #     for loan in self.get_active_loans():
    #         if loan.book == book:
    #             return loan
    #     return None


    # def find_available_books(self) -> list[Book]:
    #     loaned_books = [loan.book for loan in self.get_active_loans()]
    #     return [book for book in self.books if book not in loaned_books]
    

    # def store_user(self, user: User):
    #     user_id = user.user_id
    #     if self.users.get(user_id) is None:
    #         self.users[user_id] = user
        

    # def get_all_users(self) -> list[User]:
    #     return [user for _, user in self.users.items()]
    

