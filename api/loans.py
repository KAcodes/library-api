from fastapi import APIRouter, Query, HTTPException
from typing import Annotated

from dependencies import library_service
from schemas.schema import LoanResponse, CreateLoanRequest
from services.errors import *

router = APIRouter(
    prefix="/loans",
    tags=["loans"]
)

@router.get("/", response_model=list[LoanResponse])
def get_loans(
        active: Annotated[bool | None, Query()] = None,
        user_id: Annotated[str | None, Query(min_length=1)] = None,
        book_id: Annotated[str | None, Query(min_length=1)] = None,
    ):
    loans = library_service.get_loans(active, user_id, book_id)

    return [
        LoanResponse(
            loan_id=loan.id,
            book_id=loan.book_id,
            user_id=loan.user_id,
            borrowed_at=loan.borrowed_at,
            due_date=loan.due_date,
            returned_at=loan.returned_at
        )
        for loan in loans
    ]


@router.get("/{loan_id}/", response_model=LoanResponse)
def get_specific_loan(loan_id: str):
    try:   
        loan = library_service.get_specific_loan(loan_id)

    except LoanNonExistent as e:
            raise HTTPException(
            status_code=404,
            detail="Loan not found"
        )
    
    return LoanResponse(
            loan_id=loan.id,
            book_id=loan.book_id,
            user_id=loan.user_id,
            borrowed_at=loan.borrowed_at,
            due_date=loan.due_date,
            returned_at=loan.returned_at
        )


@router.post("/", response_model=LoanResponse)
def create_loan_for_user(request: CreateLoanRequest):
    try:
        loan = library_service.borrow_book(request.book_id, request.user_id)

    except (BookNotFoundError, UserNotFoundError) as e:
        raise HTTPException(
        status_code=404,
        detail=str(e),
    )

    except (BookUnavailableError, MaxLoansReachedError) as e:
        raise HTTPException(
        status_code=409,
        detail=str(e),
    )
    
    return LoanResponse(
        loan_id=loan.id,
        book_id=loan.book_id,
        user_id=loan.user_id,
        borrowed_at=loan.borrowed_at,
        due_date=loan.due_date,
        returned_at=loan.returned_at
    )


@router.patch("/{loan_id}/return", response_model=LoanResponse)
def return_for_user(loan_id: str):

    try:
        loan = library_service.return_book(loan_id)

    except LoanNonExistent as e:
        raise HTTPException(
        status_code=404,
        detail=str(e)
    )

    except BookAlreadyReturned as e:
        raise HTTPException(
        status_code=404,
        detail=str(e)
    )
    
    return LoanResponse(
        loan_id=loan.id,
        book_id=loan.book_id,
        user_id=loan.user_id,
        borrowed_at=loan.borrowed_at,
        due_date=loan.due_date,
        returned_at=loan.returned_at
    )
