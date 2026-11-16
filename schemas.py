from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteCreate(BaseModel):
    title: str
    content: str

class Note(NoteCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True