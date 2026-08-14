from requests import get

OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"


def retrieve_api_books(topic: str):
    response = get(f"{OPEN_LIBRARY_URL}?q={topic}&limit=5")
    data = response.json()
    return data.get('docs')
