from requests import get

OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"


def retrieve_api_books(topic: str):
    response = get(f"{OPEN_LIBRARY_URL}?q={topic}&limit=5")
    data = response.json()
    return data.get('docs')


def transform_books(books: list) -> list:
    books_cleaned = []
    for book in books:
        if not book.keys() >= {'title', 'author_name', 'cover_i', 'key'}:
            continue
        key = book["key"]
        id = key.split('/works/')[1]

        books_cleaned.append((id, book["title"], book["author_name"][0], book["cover_i"]))

    return books_cleaned