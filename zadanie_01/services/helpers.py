from contextlib import contextmanager
from decimal import Decimal, ROUND_HALF_UP

from services.errors import NotFound

@contextmanager
def transaction(db):
    db.execute("BEGIN IMMEDIATE")
    try:
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise

def required(db, sql, args, field="form"):
    row = db.execute(sql, args).fetchone()
    if row is None:
        raise NotFound("Nie znaleziono wpisu.", field)
    return dict(row)

def money(value):
    return format(
        Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        ".2f",
    )

def zlote(grosze):
    return f"{grosze // 100}.{grosze % 100:02d}"