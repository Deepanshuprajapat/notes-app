from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import sqlite3

app = FastAPI()

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Database Connection
conn = sqlite3.connect("notes.db", check_same_thread=False)
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL
)
""")
conn.commit()

# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "notes": notes
        }
    )

# Add Note
@app.post("/add")
async def add_note(note: str = Form(...)):

    cursor.execute(
        "INSERT INTO notes (content) VALUES (?)",
        (note,)
    )

    conn.commit()

    return RedirectResponse("/", status_code=303)

# Delete Note
@app.get("/delete/{note_id}")
async def delete_note(note_id: int):

    cursor.execute(
        "DELETE FROM notes WHERE id=?",
        (note_id,)
    )

    conn.commit()

    return RedirectResponse("/", status_code=303)