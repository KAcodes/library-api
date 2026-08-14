from database.db import get_connection
from models.models import User



class UserRepository:


    def populate_table(
        self,
        users: list[tuple[str, str, str, str, str | None]],
    ) -> int:

        con = get_connection()
        cur = con.cursor()

        cur.executemany(
            """
            INSERT OR IGNORE INTO USERS (
                id,
                first_name,
                last_name,
                email,
                phone
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            users,
        )

        inserted_count = cur.rowcount

        con.commit()
        con.close()

        return inserted_count

    
    def retrieve_user(self, user_id: str) -> User | None:
        con = get_connection()
        cur = con.cursor()

        cur.execute("""
                    SELECT * FROM USERS
                    WHERE id = (?)
                    """, (user_id, ))
        item = cur.fetchone()
        con.close()

        if item is None:
            return None
        item = User(
                id=item["id"],
                first_name=item["first_name"],
                last_name=item["last_name"],
                email=item["email"],
                phone=item["phone"]
            )
        
        return item
    
    
    def fetch_all_users(self) -> list[User] | None:
        con = get_connection()
        cur = con.cursor()

        cur.execute("SELECT * FROM USERS")
        rows = cur.fetchall()
        con.close()

        rows = [
            User(
                id=row["id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                phone=row["phone"]
            )
            for row in rows
        ]
        return rows


    def delete_user(self, id: str):
        con = get_connection()
        cur = con.cursor()

        cur.execute("""
                    DELETE FROM USERS
                    WHERE id = (?)
                    """, (id, ))
        con.commit()
        con.close()