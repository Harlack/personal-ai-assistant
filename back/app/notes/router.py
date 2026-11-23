from fastapi import APIRouter
from app.notes.schemas import Note, NoteRequest
from app.notes.service import NotesServiceDep
from app.database import NoteModel
from datetime import datetime

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("", response_model=Note)
async def create_note(note: NoteRequest, service: NotesServiceDep):
    new_note = NoteModel(title=note.title, content=note.content, created_at=datetime.now().isoformat())
    note = service.create_note(new_note)
    return Note.model_validate(note)

@router.get("", response_model=list[Note])
async def get_notes(service: NotesServiceDep) -> list[Note]:
    notes = service.get_all_notes()
    return [Note.model_validate(note) for note in notes]

@router.get("/{note_id}", response_model=Note)
async def get_note(note_id: int, service: NotesServiceDep):
    note = service.get_note_by_id(note_id)
    return Note.model_validate(note)

@router.put("/{note_id}", response_model=Note)
async def update_note(note_id: int, note_request: NoteRequest, service: NotesServiceDep):
    updated_note = NoteModel(title=note_request.title, content=note_request.content)
    note = service.update_note(note_id, updated_note)
    return Note.model_validate(note)

@router.delete("/{note_id}")
async def delete_note(note_id: int, service: NotesServiceDep):
    result = service.delete_note(note_id)
    return "Note deleted successfully" if result else "Failed to delete note"