import pprint
from fastapi import APIRouter, HTTPException, status

from dependencies import library_service
from schemas.schema import BookResponse, BookImportRequest

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("/", response_model=list[BookResponse])
def get_all_books():
    books = library_service.get_all_books()

    return [
        BookResponse(
            id=book.id,
            title=book.title,
            author=book.author,
            isbn=book.isbn
        )
        for book in books
    ]


@router.get("/{id}", response_model=BookResponse)
def retrieve_one_book(id: str):
    book = library_service.get_singular_book(id)

    if book is None:
        raise HTTPException(
        status_code=404,
        detail="Book not found"
    )

    return BookResponse(
        id=book.id,
        title=book.title,
        author=book.author,
        isbn=book.isbn
    )


@router.post("/import")
def import_books(request: BookImportRequest):
    count = library_service.import_books(request.topic)
    if not count:
            raise HTTPException(
            status_code=404,
            detail="No books found on topic"
        )
    
    return {
        "topic": request.topic,
        "inserted": count
    }


@router.delete("/delete/{id}")
def import_books(id: str):
    library_service.delete_book(id)

    return {
        "status": "Book deleted"
    }
