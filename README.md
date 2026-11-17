# fastapi-notes-api
A simple notes REST API built with FastAPI


## Purpose
A FastAPI REST API for managing notes, built as a learning project for addition to my resume. Supports CRUD operatiions and AI-powered summaries via Google Gemini API.


## Setup & Run
1. Create a virtual environment by typing in bash: 
    python -m venv .venv

2. Activate it:
    - Windows: .venv\Scripts\activate
    - Mac/Linux: source .venv/bin/activate

3. Install dependencies:
    pip install -r requirements.txt

4. Add a Gemini API key:
    - Get a key at https://aistudio.google.com/
    - Creat a .env file containing: GEMINI_API_KEY=your_key_here

5. Run with server:
    .venv\Scripts\python -m python uvicorn main:app --reload


**Endpoint Table**

| Method    | URL                   | Description           | Status Code               |
|-----------|-----------------------|-----------------------|---------------------------|
| POST      | /notes                | Create a note         | 201 Created               |
| GET       | /notes                | List all note         | 200 OK                    |
| GET       | /notes/{id}           | Get one note          | 200 OK or 404 Not Found   |
| PUT       | /notes/{id}           | Update a note         | 200 OK or 404 Not Found   |
| DELETE    | /notes/{id}           | Delete a note         | 204 No content            |
| POST      | /notes/{id}/summary   | AI summary via gemini | 200 OK or 502 Bad Gateway | 


**Tech/Tools Used**

- Fast API (web framework)
- SQLAlchemy (ORM with SQLite, potable to MySQL)
- Pydantic (data validation)
- pytest (testing)
- Git (version control)


**Design Decision**

1. SQLite first, then maybe MySQL later - I wanted to start development quickly without setting up a database server. SQLite is file-based and perfect for starting out. The code is written so switching to MySQL only requires changing the DATABASE_URL in database.py.

2. Error handling with status code e.g. 502/422/404 - I am trying to practice the production-quality behavior for this learning project. Invalid input would return 422 (FastAPI/Pydantic), missing notes return 404, Gemini errors return 502 instead of crashing the server and etc.

3. API key in .env, not main.py - I did'nt hardcode the Gemini key because that would be a security risk. This is a good practice since every developer should know to  use environment variables. THe key lives in .env and excluded from Git by .gitignore and the code reads it with os.getenv().


![FastAPI /docs](<Screenshot 2026-11-17 200008.png>)


This is a learning project built to demonstrate skills to potential employer/ It demonstrates FastAPI development, database integration, API consumption, and understanding of security best practices and error handling.