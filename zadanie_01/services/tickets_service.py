from datetime import date

from config import TRANSITIONS
from services.errors import Conflict
from services.helpers import required, transaction

def enrich(row):
    row = dict(row)
    end_date = (
        date.fromisoformat(row["closed_date"])
        if row["closed_date"]
        else date.today()
    )
    row["days_open"] = (
        end_date - date.fromisoformat(row["created_date"])
    ).days
    row["allowed_transitions"] = TRANSITIONS[row["status"]]
    return row

def listing(db, uid, status=None):
    rows = db.execute(
        "SELECT * FROM tickets "
        "WHERE user_id = ? AND (? IS NULL OR status = ?) "
        "ORDER BY created_date DESC, id DESC",
        (uid, status, status),
    ).fetchall()
    return [enrich(row) for row in rows]

def create(db, uid, data):
    with db:
        ticket_id = db.execute(
            "INSERT INTO tickets(user_id, title, description, priority) "
            "VALUES (?, ?, ?, ?)",
            (uid, data.title, data.description, data.priority),
        ).lastrowid
    return enrich(
        required(
            db,
            "SELECT * FROM tickets WHERE id = ? AND user_id = ?",
            (ticket_id, uid),
        )
    )

def change(db, uid, id, data):
    with transaction(db):
        row = required(
            db,
            "SELECT * FROM tickets WHERE id = ? AND user_id = ?",
            (id, uid),
        )
        if data.status not in TRANSITIONS[row["status"]]:
            raise Conflict("Niedozwolona zmiana statusu.", "status")

        closed = (
            date.today().isoformat()
            if not TRANSITIONS[data.status]
            else row["closed_date"]
        )
        db.execute(
            "UPDATE tickets SET status = ?, closed_date = ? "
            "WHERE id = ? AND user_id = ?",
            (data.status, closed, id, uid),
        )

    return enrich(
        required(
            db,
            "SELECT * FROM tickets WHERE id = ? AND user_id = ?",
            (id, uid),
        )
    )

def summary(db, uid):
    counts = {status: 0 for status in TRANSITIONS}
    for row in db.execute(
        "SELECT status, COUNT(*) AS n FROM tickets "
        "WHERE user_id = ? GROUP BY status",
        (uid,),
    ):
        counts[row["status"]] = row["n"]
    return counts