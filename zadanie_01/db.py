import sqlite3
from decimal import Decimal
from pathlib import Path

from config import BASE_DIR, DATABASE_PATH

sqlite3.register_adapter(Decimal, str)

def connect():
    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False,
        timeout=15,
    )
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def init_db():
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    with connect() as connection:
        connection.executescript(
            (BASE_DIR / "schema.sql").read_text(encoding="utf-8")
        )

def get_db():
    connection = connect()
    try:
        yield connection
    finally:
        connection.close()