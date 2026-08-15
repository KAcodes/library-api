from datetime import datetime, timedelta

from database.db import get_connection
from models.models import Loan


class LoanRepository:

    def fetch_all_loans(self) -> list[Loan]:
        con = get_connection()
        cur = con.cursor()

        cur.execute("SELECT * FROM LOANS")
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


    def fetch_active_loans_for_user(self, user_id: str) -> list[Loan]:
        con = get_connection()
        cur = con.cursor()

        cur.execute("""
                    SELECT * FROM LOANS
                    WHERE user_id = (?)
                    AND returned_at IS NULL
                    """, (user_id, ))
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


    def fetch_active_loan_for_book(self, book_id: str) -> Loan:
        con = get_connection()
        cur = con.cursor()

        cur.execute("""
                    SELECT *
                    FROM LOANS
                    WHERE book_id = (?)
                    AND returned_at IS NULL
                    LIMIT 1
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

        con.commit()
        con.close()
