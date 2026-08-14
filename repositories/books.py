from database.db import get_connection
from models.models import Book


class BookRepository:

    def populate_table(self, books: list[tuple[str, str, str, str]]) -> int:
        con = get_connection()
        cur = con.cursor()
        cur.executemany("INSERT INTO BOOKS VALUES(?, ?, ?, ?)", books)
        
        inserted_count = cur.rowcount

        con.commit()
        con.close()

        return inserted_count


    def retrieve_book(self, id: str) -> Book | None:
        con = get_connection()
        cur = con.cursor()

        cur.execute("""
                    SELECT id, title, author, isbn FROM BOOKS
                    WHERE id = (?)
                    """, (id, ))
        item = cur.fetchone()
        con.close()

        if item is None:
            return None
        item = Book(
            id=item["id"],
            title=item["title"],
            author=item["author"],
            isbn=item["isbn"])
        
        return item


    def fetch_all_books(self) -> list[Book] | None:
        con = get_connection()
        cur = con.cursor()

        cur.execute("SELECT id, title, author, isbn FROM BOOKS")
        rows = cur.fetchall()

        con.close()
        if rows is None:
            return None

        rows = [
            Book(
                id=row["id"],
                title=row["title"],
                author=row["author"],
                isbn=row["isbn"]) 
            for row in rows
        ]
        return rows


    def insert_book(self, book: tuple[str, str]) -> int:
        con = get_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO BOOKS VALUES(?, ?, ?)", book)
        
        inserted_count = cur.rowcount

        con.commit()
        con.close()
        return inserted_count


    def delete_book(self, id: str):
        con = get_connection()
        cur = con.cursor()

        cur.execute("""
                    DELETE FROM BOOKS
                    WHERE id = (?)
                    """, (id, ))
        con.commit()
        con.close()
