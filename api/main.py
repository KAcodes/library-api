from fastapi import FastAPI
from requests import get
from pprint import pprint
from library import *

app = FastAPI()

OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"


def retrieve_api_books(url: str, topic: str) -> list:
    response = get(f"{url}?q={topic}&limit=5")
    data = response.json()
    return data.get('docs')


my_library = Library()

books = retrieve_api_books(OPEN_LIBRARY_URL, "football")
for book in books:
    new_book = Book(book["title"], book["author_name"][0], book["cover_i"])
    my_library.add_book(new_book)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/books/all-books")
def get_all_books():
    books = my_library.find_all_books()
    return {"message": books}