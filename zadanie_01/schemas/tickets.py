from typing import Literal

from pydantic import BaseModel, Field

from schemas.base import Input

Status = Literal["new", "in_progress", "closed", "rejected"]

class Create(Input):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=10)
    priority: Literal["low", "medium", "high"]

class Change(Input):
    status: Status

class Record(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    created_date: str
    closed_date: str | None
    days_open: int
    allowed_transitions: list[str]