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