from fastapi import APIRouter

from dependencies import library_service
from schemas.schema import LoanResponse, CreateLoanRequest

router = APIRouter(
    prefix="/loans",
    tags=["loans"]
)

@router.get("/", response_model=list[LoanResponse])
def get_all_loans():
    loans = library_service.get_all_loans()

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


@router.get("/{user_id}", response_model=list[LoanResponse])
def get_active_loans_for_user(user_id: str):
    loans = library_service.get_active_loans_for_user(user_id)

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


@router.post("/")
def create_loan_for_user(request: CreateLoanRequest):
    loan = library_service.borrow_book(request.book_id, request.user_id)

    # if not count:
    #         raise HTTPException(
    #         status_code=404,
    #         detail="Couldn't import Users"
    #     )
    
    return f"Successful Loan to {request.user_id}"