from datetime import datetime
from sqlalchemy import select
from fastapi import FastAPI
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
async def create_note(note: NoteRequest, session: SessionDep):
    new_note = NoteModel(title=note.title, content=note.content, created_at=datetime.now().isoformat())
    session.add(new_note)
    session.commit()
    session.refresh(new_note)
    return Note.model_validate(new_note)

@app.get("/notes", response_model=list[Note])
async def get_notes(session: SessionDep) -> list[Note]:
    notes = session.execute(select(NoteModel)).scalars().all()
    return [Note.model_validate(note) for note in notes]
