from datetime import date
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict

class Input(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

def not_future(value):
    if value > date.today():
        raise ValueError("Data nie może być z przyszłości.")
    return value

def not_past(value):
    if value < date.today():
        raise ValueError("Data nie może być z przeszłości.")
    return value

def future(value):
    if value <= date.today():
        raise ValueError("Data musi być późniejsza niż dziś.")
    return value

PastDate = Annotated[date, AfterValidator(not_future)]
FutureDate = Annotated[date, AfterValidator(not_past)]
StrictFutureDate = Annotated[date, AfterValidator(future)]