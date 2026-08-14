from repositories.books import BookRepository
from repositories.users import UserRepository
from repositories.loans import LoanRepository
from services.library import LibraryService



book_repository = BookRepository()
user_repository = UserRepository()
loan_repository = LoanRepository()

library_service = LibraryService(
    book_repository=book_repository,
    user_repository=user_repository,
    loan_repository=loan_repository,
)
