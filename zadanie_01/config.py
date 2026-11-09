import os
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parent
SECRET_KEY = os.environ["SECRET_KEY"]
DATABASE_PATH = os.environ["DATABASE_PATH"]
COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "0") == "1"
CURRENT_YEAR = date.today().year
TITLE = "Rejestr zgłoszeń serwisowych"

TRANSITIONS = {
    "new": ("in_progress", "rejected"),
    "in_progress": ("closed", "rejected"),
    "closed": (),
    "rejected": (),
}

UI = {
    "fields": [
        {
            "name": "title",
            "label": "Tytuł",
            "type": "text",
            "minlength": 5,
            "maxlength": 100,
        },
        {
            "name": "description",
            "label": "Opis",
            "type": "textarea",
            "minlength": 10,
        },
        {
            "name": "priority",
            "label": "Priorytet",
            "type": "select",
            "options": ["low", "medium", "high"],
        },
    ],
    "columns": [
        ["id", "#"],
        ["title", "Tytuł"],
        ["description", "Opis"],
        ["priority", "Priorytet"],
        ["status", "Status"],
        ["days_open", "Dni otwarcia"],
    ],
    "filters": [
        {
            "name": "status",
            "label": "Status",
            "type": "select",
            "options": ["new", "in_progress", "closed", "rejected"],
            "required": False,
        }
    ],
    "title": "Rejestr zgłoszeń serwisowych",
    "number": 1,
    "domain": "tickets",
    "summary": "stats",
    "mode": "tickets",
}