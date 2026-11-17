import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

class AccountInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def valid_email(cls, value):
        value = value.strip().lower()
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
            raise ValueError("Podaj poprawny adres e-mail.")
        return value

class AccountOut(BaseModel):
    email: str

class SessionOut(AccountOut):
    csrf_token: str