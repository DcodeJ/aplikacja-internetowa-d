import secrets

from fastapi import Depends, Request

from db import get_db
from services import auth_service
from services.errors import Forbidden

def current_user(request: Request, db=Depends(get_db)):
    return auth_service.current(db, request.session.get("user_id"))

def csrf(request: Request, user=Depends(current_user)):
    expected = request.session.get("csrf", "")
    supplied = request.headers.get("X-CSRF-Token", "")
    if not expected or not secrets.compare_digest(
        supplied.encode(), expected.encode()
    ):
        raise Forbidden("Sesja formularza wygasła. Odśwież stronę i spróbuj ponownie.")
    return user