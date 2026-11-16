from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Note as SQLNote
from schemas import NoteCreate, Note
from dotenv import load_dotenv
import os 
from google.genai import Client
load_dotenv()

app = FastAPI()

# Create tables on startup
Base.metadata.create_all(bind=engine)

# Dependency: Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ENDPOINT 1: POST /notes - Create a note
@app.post("/notes", response_model=Note, status_code=201)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = SQLNote(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# ENDPOINT 2: GET /notes - List all notes
@app.get("/notes", response_model=list[Note])
def read_notes(db: Session = Depends(get_db)):
    notes = db.query(SQLNote).all()
    return notes

# ENDPOINT 3: GET /notes/{id} - Get one note (404 if not found)
@app.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(SQLNote).filter(SQLNote.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# ENDPOINT 4: PUT /notes/{id} - Update a note
@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    db_note = db.query(SQLNote).filter(SQLNote.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db_note.title = note.title #type: ignore
    db_note.content = note.content #type: ignore
    db.commit()
    db.refresh(db_note)
    return db_note

# ENDPOINT 5: DELETE /notes/{id} - Delete a note
@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(SQLNote).filter(SQLNote.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note  not found")
    db.delete(db_note)
    db.commit()
    return None

# ENDPOINT 6 post /NOTES/{id} - Gemini summary
API_KEY = os.getenv("GEMINI_API_KEY")

@app.post("/notes/{note_id}/summary")
def generate_summary(note_id: int, db: Session = Depends(get_db)):
    note = db.query(SQLNote).filter(SQLNote.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    if not API_KEY:
        raise HTTPException(status_code=500, detail=":Gemini API key not configured")

    try:
        client = Client(api_key=API_KEY)
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"Summarize this note: {note.content}"
        )
        return {"Summary": response.text, "note_id": note.id}
    except Exception as e:
        print(f"DEBUG: Error = {e}")  # <-- Add this
        raise HTTPException(status_code=502, detail="Gemini API error")
