from pydantic import BaseModel, Field

class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    isbn: str


class UserImportRequest(BaseModel):
    count: int = Field(
        default=5,
        ge=1,
        le=100,
    )

class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str | None


class BookImportRequest(BaseModel):
    topic: str


class LoanResponse(BaseModel):
    loan_id: int
    book_id: str
    user_id: str
    borrowed_at: str
    due_date: str
    returned_at: None | str


class CreateLoanRequest(BaseModel):
    user_id: str
    book_id: str