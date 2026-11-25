import sqlite3

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

from services.errors import Conflict, Unauthorized

hasher = PasswordHasher()

def register(db, data):
    password_hash = hasher.hash(data.password)
    try:
        with db:
            db.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (data.email, password_hash),
            )
    except sqlite3.IntegrityError:
        raise Conflict("Ten e-mail jest już zajęty.", "email")
    return {"email": data.email}

def login(db, data):
    row = db.execute(
        "SELECT id, email, password_hash FROM users WHERE email = ?",
        (data.email,),
    ).fetchone()
    if row is None:
        raise Unauthorized("Nieprawidłowy e-mail lub hasło.", "password")
    try:
        hasher.verify(row["password_hash"], data.password)
    except (VerificationError, InvalidHashError):
        raise Unauthorized("Nieprawidłowy e-mail lub hasło.", "password")
    return {"id": row["id"], "email": row["email"]}

def current(db, user_id):
    row = db.execute(
        "SELECT id, email FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    if row is None:
        raise Unauthorized("Zaloguj się aby kontynuować.")
    return dict(row)