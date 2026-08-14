import pprint
from fastapi import APIRouter

from dependencies import library_service


router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("/all-books")
def get_all_books():
    books = library_service.get_all_books()

    books = {
        "books": [
            {
                "id": row["id"],
                "title": row["title"],
                "author": row["author"],
                "isbn": row["isbn"],
            }
            for row in books
        ]
    }

    return {"message": books}


@router.get("/fetch-book")
def retrieve_one_book(id: str):
    result = library_service.get_singular_book(id)

    book = {
        "book": 
            {
                "id": result["id"],
                "title": result["title"],
                "author": result["author"],
                "isbn": result["isbn"],
            }
    }

    return {"message": book}


@router.post("/import")
def import_books(topic: str):
    count = library_service.import_books(topic)
  
    return {
        "topic": topic,
        "inserted": count
    }


@router.delete("/delete")
def import_books(id: str):
    library_service.delete_book(id)

    return {
        "status": "Book deleted"
    }
