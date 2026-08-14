from database.db import get_connection


class BookRepository:

    def populate_table(self, books: list[tuple[str, str, str, str]]):
        con = get_connection()
        cur = con.cursor()
        cur.executemany("INSERT INTO BOOKS VALUES(?, ?, ?, ?)", books)
        
        inserted_count = cur.rowcount

        con.commit()
        con.close()

        return inserted_count


    def insert_book():
        pass


    def fetch_all_books(self) -> list:
        con = get_connection()
        cur = con.cursor()

        cur.execute("SELECT id, title, author, isbn FROM BOOKS")
        rows = cur.fetchall()

        con.close()
        return rows


    def retrieve_book(self, id: str):
        con = get_connection()
        cur = con.cursor()

        cur.execute("""
                    SELECT id, title, author, isbn FROM BOOKS
                    WHERE id = (?)
                    """, (id, ))
        rows = cur.fetchone()

        con.close()
        return rows


    def delete_book(self, id: str):
        con = get_connection()
        cur = con.cursor()

        cur.execute("""
                    DELETE FROM BOOKS
                    WHERE id = (?)
                    """, (id, ))
        con.commit()
        con.close()
