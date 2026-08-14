from enum import Enum
from abc import ABC, abstractmethod

from repositories.books import BookRepository
from repositories.users import UserRepository
from repositories.loans import LoanRepository
from clients.open_library import retrieve_api_books, transform_books
from clients.random_user import retrieve_api_users, transform_users
from models.models import Book, User



class BookUnavailableError(Exception):
    pass

class UserBorrowLimitExceeded(Exception):
    pass

class UnauthorizedReturnError(Exception):
    pass

class MaxLoansReachedError(Exception):
    pass


class LibraryService:
    MAX_BOOKS = 3
    def __init__(self, book_repository: BookRepository, user_repository: UserRepository, loan_repository: LoanRepository):
        self.book_repository = book_repository
        self.user_repository = user_repository
        self.loan_repository = loan_repository


    def get_singular_book(self, id: str) -> Book | None:
        return self.book_repository.retrieve_book(id) 


    def get_all_books(self) -> list[Book] | None:
        return self.book_repository.fetch_all_books()


    def import_singular_book():
        pass


    def import_books(self, topic: str):
        books = retrieve_api_books(topic)
        cleaned_books = transform_books(books)
        returned_count = self.book_repository.populate_table(cleaned_books)
        return returned_count


    def delete_book(self, id: str):
        return self.book_repository.delete_book(id) 

    # def add_book(self, book: Book):
    #     self.books.append(book)


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

    def import_users(self, count: int = 5) -> int:
        users = retrieve_api_users(count)
        cleaned_users = transform_users(users)

        return self.user_repository.populate_table(cleaned_users)
        
    def get_user(self, id: str) -> User | None:
        return self.user_repository.retrieve_user(id)


    def get_all_users(self) -> list[User]:
        return self.user_repository.fetch_all_users()
    

    def delete_user(self, id: str) -> User | None:
        return self.user_repository.delete_user(id)