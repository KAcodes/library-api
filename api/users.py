from fastapi import APIRouter, HTTPException, status

from dependencies import library_service
from schemas.schema import UserImportRequest, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=list[UserResponse])
def get_all_users():
    users = library_service.get_all_users()

    return [
        UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone
        )
        for user in users
    ]


@router.get("/{id}", response_model=UserResponse)
def retrieve_user(id: str):
    user = library_service.get_user(id)

    if user is None:
        raise HTTPException(
        status_code=404,
        detail="User not found"
    )

    return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
        )


@router.post("/import")
def import_users(request: UserImportRequest):
    count = library_service.import_users(request.count)
    if not count:
            raise HTTPException(
            status_code=404,
            detail="Couldn't import Users"
        )
    
    return {
        "requested": request.count,
        "inserted": count
    }


@router.delete("/delete/{id}")
def import_books(id: str):
    library_service.delete_user(id)

    return {
        "status": "User deleted"
    }

