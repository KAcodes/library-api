from datetime import datetime, timedelta

from database.db import get_connection
from models.models import Loan


class LoanRepository:

    def fetch_loans(self,
        active: bool | None = None,
        user_id: str | None = None,
        book_id: str | None = None
        ) -> list[Loan]:
        
        con = get_connection()
        cur = con.cursor()

        query = "SELECT * FROM LOANS WHERE id IS NOT NULL"
        params = []

        if active is True:
            query += " AND returned_at IS NULL"
        elif active is False:
            query += " AND returned_at IS NOT NULL"

        if user_id is not None:
            query += " AND user_id = ?"
            params.append(user_id)

        if book_id is not None:
            query += " AND book_id = ?"
            params.append(book_id)

        cur.execute(query, params)

        rows = cur.fetchall()
        con.close()


        rows = [
            Loan(
                id=row["id"],
                user_id=row["user_id"],
                book_id=row["book_id"],
                borrowed_at=row["borrowed_at"],
                due_date=row["due_date"],
                returned_at=row["returned_at"]
            )
            for row in rows
        ]
        return rows


    def fetch_loan_by_id(self, loan_id: int) -> Loan | None:
        con = get_connection()
        cur = con.cursor()
 
        cur.execute("""
                    SELECT *
                    FROM LOANS
                    WHERE id = (?)
                    """, (loan_id, ))
        item = cur.fetchone()
        con.close()

        if item is None:
            return None
        item = Loan(
            id=item["id"],
            user_id=item["user_id"],
            book_id=item["book_id"],
            borrowed_at=item["borrowed_at"],
            due_date=item["due_date"],
            returned_at=item["returned_at"]
        )

        return item


    def fetch_active_loan_for_book(self, book_id: str) -> Loan | None:
        con = get_connection()
        cur = con.cursor()
    
        cur.execute("""
                    SELECT *
                    FROM LOANS
                    WHERE book_id = (?)
                    """, (book_id, ))
        item = cur.fetchone()
        con.close()

        if item is None:
            return None
        item = Loan(
            id=item["id"],
            user_id=item["user_id"],
            book_id=item["book_id"],
            borrowed_at=item["borrowed_at"],
            due_date=item["due_date"],
            returned_at=item["returned_at"]
        )

        return item

    def create_loan(self, book_id: str, user_id: str):
        borrowed_at = datetime.now()
        due_date = borrowed_at + timedelta(days=14)

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            """
            INSERT INTO LOANS (
                user_id,
                book_id,
                borrowed_at,
                due_date,
                returned_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                book_id,
                borrowed_at.isoformat(),
                due_date.isoformat(),
                None,
            ),
        )

        loan_id = cur.lastrowid

        con.commit()
        con.close()

        return Loan(
            id=loan_id,
            user_id=user_id,
            book_id=book_id,
            borrowed_at=borrowed_at.isoformat(),
            due_date=due_date.isoformat(),
            returned_at=None,
        )


    def end_loan(self, loan_id: int):
        returned_at = datetime.now()
        con = get_connection()
        cur = con.cursor()

        cur.execute(
            """
            UPDATE LOANS
            SET returned_at = (?)
            WHERE id = (?)
            AND returned_at IS NULL
            RETURNING *
            """,
            (
                returned_at.isoformat(),
                loan_id,
            )
        )
        row = cur.fetchone()

        con.commit()
        con.close()

        if row is None:
            return None
            
        return Loan(
            id=row["id"],
            user_id=row["user_id"],
            book_id=row["book_id"],
            borrowed_at=row["borrowed_at"],
            due_date=row["due_date"],
            returned_at=row["returned_at"]
        )

