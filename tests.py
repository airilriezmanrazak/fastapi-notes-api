import pytest
from fastapi.testclient import TestClient
from main import app

# same imports as main.py
from database import SessionLocal, engine 
from models import Note as SQLNote
from schemas import NoteCreate, Note

client = TestClient(app)

# Initializing databse for tests
def setup_module(module):
    from database import Base
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
    from database import Base
    Base.metadata.drop_all(bind=engine)

# TEST 1: create a note (POST /notes, 201 aka Created)
def test_create_note():
    response = client.post("/notes", json = {"title": "Test Note", "content": "This is a test content"},)
    assert response.status_code == 201
    data = response.json()
    assert data ["title"] == "Test Note"
    assert data ["content"] == "This is a test content"
    assert "id" in data
    assert "created_at" in data

# TEST 2: List all notes (GET /notes)
def test_read_all_notes():
    response = client.get("/notes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance (data, list)
    assert len(data) >= 1

# TEST 3: Get one note (GET /notes/{id}, 200 aka OK)
def test_read_note():
    create_response = client.post("/notes", json={"title": "Read a note", "content": "Content for reading"})
    note_id = create_response.json()["id"]

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Read a note"

# TEST 4: Get one note (404 aka Not found)
def test_read_note_404():
    response = client.get("/notes/999999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

#TEST 5: Update a note (PUT /notes/{id})
def test_update_note():
    # Create a note first
    create_response = client.post("/notes", json={"title": "To be updated", "content": "1.0"})
    note_id = create_response.json()["id"]

    # Update the note
    response = client.put(f"/notes/{note_id}", json={"title": "Updated", "content": "2.0"})
    assert response.status_code == 200 
    data = response.json()
    assert data["title"] == "Updated"
    assert data["content"] == "2.0"

# TEST 6: Delete a note (DELETE /notes/{id}, 204 aka no content)
def test_delete_note():
    # Create a note first
    create_response = client.post("/notes", json={"title": "To be deleted", "content": "delete me"})
    note_id = create_response.json()["id"]

    # Delete the note
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 204

# TEST 7: Invalid input to return 422 aka Unprocessable Content
def test_create_note_invalid_input():
    response = client.post("/notes", json={"title": 123, "content": "The title should be string"})
    assert response.status_code == 422

# TEST 8: Gemini summary endpoint (mocked so no working key is needed) 200 aka OK or 502 aka Bad Gateway
def test_generate_summary_mocked():
    # Create a note first
    create_response = client.post("/notes", json={"title": "Gemini summary test", "content": "Hello World test content"})
    note_id = create_response.json()["id"]

    # This test should not crash even without Gemini API key
    response = client.post(f"/notes/{note_id}/summary")
    # Return 502 if the Gemini API key is not configured
    assert response.status_code in (200,502)