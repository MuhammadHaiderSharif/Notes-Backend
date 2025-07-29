from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

users = {}
notes = {}
note_id_counter = 1

class User(BaseModel):
    username: str
    password: str


class Note(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    username: str 

@app.post("/signup")
def signup(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[user.username] = user.password
    return {"message": "User registered successfully!"}


@app.post("/login")
def login(user: User):
    if user.username not in users or users[user.username] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful!"}


@app.post("/notes")
def add_note(note: Note):
    global note_id_counter
    note.id = note_id_counter
    note_id_counter += 1
    notes[note.id] = note
    return {"message": "Note added", "note": note}


@app.get("/notes/{username}", response_model=List[Note])
def get_notes(username: str):
    user_notes = [n for n in notes.values() if n.username == username]
    return user_notes


@app.put("/notes/{note_id}")
def update_note(note_id: int, note: Note):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    if notes[note_id].username != note.username:
        raise HTTPException(status_code=403, detail="Not allowed")
    note.id = note_id
    notes[note_id] = note
    return {"message": "Note updated", "note": note}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, username: str):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    if notes[note_id].username != username:
        raise HTTPException(status_code=403, detail="Not allowed")
    del notes[note_id]
    return {"message": "Note deleted"}
