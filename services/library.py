from enum import Enum
from abc import ABC, abstractmethod

from repositories.books import BookRepository
from repositories.users import UserRepository
from repositories.loans import LoanRepository
from clients.open_library import retrieve_api_books, transform_books
from clients.random_user import retrieve_api_users, transform_users
from models.models import Book, User, Loan
from services.errors import *



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


    def get_loans(
        self,
        active: bool | None = None,
        user_id: str | None = None,
        book_id: str | None = None,
    ) -> list[Loan]:
        return self.loan_repository.fetch_loans(
            active=active,
            user_id=user_id,
            book_id=book_id,
        )


    def get_specific_loan(self, loan_id: int) -> Loan | None:
        loan = self.loan_repository.fetch_loan_by_id(loan_id)

        if loan is None:
            raise LoanNonExistent(f"Loan doesn't exist in our records.")   

        return loan 


    def borrow_book(self, book_id: str, user_id: str) -> Loan | None:
        book = self.book_repository.retrieve_book(book_id)
        user = self.user_repository.retrieve_user(user_id)

        if book is None:
            raise BookNotFoundError(f"Book ID {book_id} doesn't exist.")

        if user is None:
            raise UserNotFoundError(f"User ID {user_id} doesn't exist.")

        active_loan = self.loan_repository.fetch_active_loan_for_book(book_id)

        if active_loan is not None:
            raise BookUnavailableError(
                f"{book.title} is not available to loan."
            )

        active_loans_for_user = self.get_loans(active=True, user_id=user_id, book_id=None)

        if len(active_loans_for_user) >= self.MAX_BOOKS:
            raise MaxLoansReachedError(f"{user.first_name} currrently has {len(active_loans_for_user)} books borrowed. You can only borrow a maximum of {self.MAX_BOOKS} books at once.")

        return self.loan_repository.create_loan(
            book_id=book_id,
            user_id=user_id,
        )


    def return_book(self, loan_id: int) -> Loan | None:
        loan = self.loan_repository.fetch_loan_by_id(loan_id)

        if loan is None:
            raise LoanNonExistent(f"Loan doesn't exist in our records.")

        returned_loan = self.loan_repository.end_loan(loan_id)

        if returned_loan is None:
            raise BookAlreadyReturned(f"Book is not currently out on loan.")
        return returned_loan
        
       