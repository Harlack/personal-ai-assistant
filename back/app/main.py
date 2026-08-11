from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from app.database import NoteModel, Session


class NoteRequest(BaseModel):
    title: str
    content: str

class Note(BaseModel): 
    id: int
    title: str
    content: str
    created_at: str

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/info")
async def read_info():
    return {
                "name": "Personal AI Assistant",
                "version": "0.1.0"
    }

@app.get("/health")
async def read_health():
    return {"status": "healthy"}

@app.post("/notes")
async def create_note(note: NoteRequest):
    with Session() as session:
        new_note = NoteModel(title=note.title, content=note.content, created_at=datetime.now().isoformat())
        session.add(new_note)
        session.commit()
        session.refresh(new_note)
    return {"id": new_note.id, "title": new_note.title, "content": new_note.content, "created_at": new_note.created_at}