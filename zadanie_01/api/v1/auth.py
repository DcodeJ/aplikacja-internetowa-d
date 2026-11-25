import secrets

from fastapi import APIRouter, Depends, Request, Response

from api.deps import csrf, current_user
from db import get_db
from schemas.account import AccountInput, AccountOut, SessionOut
from services import auth_service

router = APIRouter(tags=["Konto"])

@router.post("/register", status_code=201, response_model=AccountOut)
def register(data: AccountInput, db=Depends(get_db)):
    return auth_service.register(db, data)

@router.post("/login", response_model=SessionOut)
def login(data: AccountInput, request: Request, db=Depends(get_db)):
    user = auth_service.login(db, data)
    request.session.clear()
    request.session.update(user_id=user["id"], csrf=secrets.token_urlsafe(32))
    return {"email": user["email"], "csrf_token": request.session["csrf"]}

@router.get("/me", response_model=SessionOut)
def me(request: Request, user=Depends(current_user)):
    return {"email": user["email"], "csrf_token": request.session["csrf"]}

@router.post("/logout", status_code=204, response_class=Response)
def logout(request: Request, user=Depends(csrf)):
    request.session.clear()
    return None