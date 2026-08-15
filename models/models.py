from datetime import datetime, timedelta


class Book:
    def __init__(self, id: str, title: str, author: str, isbn: str):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
    
    def __str__(self):
        return f"{self.title} by {self.author} - ISBN: {self.isbn}"


class User:
    
    def __init__(
        self,
        id: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str | None = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


class Loan:
    def __init__(self, id: str, book_id: str, user_id: str, borrowed_at: str, due_date: str, returned_at: str | None):
        self.id = id
        self.book_id = book_id
        self.user_id = user_id
        self.borrowed_at = borrowed_at
        self.due_date = due_date
        self.returned_at = returned_at

    @property
    def is_active(self) -> bool:
        return self.returned_at is None

    def _return_book(self):
        self.returned_at = datetime.now()