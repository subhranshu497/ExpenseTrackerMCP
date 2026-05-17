import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "expenses.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                expense_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                category     TEXT    NOT NULL,
                sub_category TEXT,
                amount       REAL    NOT NULL,
                date         TEXT    NOT NULL,
                comments     TEXT
            )
        """)
        conn.commit()
