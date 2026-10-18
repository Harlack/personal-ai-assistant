from datetime import datetime
from fastapi import HTTPException, FastAPI
from app.notes.service import NotesServiceDep
from sqlalchemy import select
from pydantic import BaseModel, ConfigDict
from app.database import NoteModel, SessionDep

class NoteRequest(BaseModel):
    title: str
    content: str

class Note(BaseModel): 
    id: int
    title: str
    content: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)

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

@app.post("/notes", response_model=Note)
async def create_note(note: NoteRequest, service: NotesServiceDep):
    new_note = NoteModel(title=note.title, content=note.content, created_at=datetime.now().isoformat())
    note = service.create_note(new_note)
    return Note.model_validate(note)

@app.get("/notes", response_model=list[Note])
async def get_notes(service: NotesServiceDep) -> list[Note]:
    notes = service.get_all_notes()
    return [Note.model_validate(note) for note in notes]

@app.get("/notes/{note_id}", response_model=Note)
async def get_note(note_id: int, service: NotesServiceDep):
    note = service.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return Note.model_validate(note)

