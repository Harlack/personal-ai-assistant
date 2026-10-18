from app.database import NoteModel, SessionDep
from fastapi import Depends
from typing import Annotated
from sqlalchemy import select

class NotesService:
    def __init__(self, session):
        self.session = session

    def create_note(self, note: NoteModel):
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        return note

    def get_note_by_id(self, note_id: int):
        return self.session.execute(select(NoteModel).where(NoteModel.id == note_id)).scalar_one_or_none()

    def get_all_notes(self):
        return self.session.execute(select(NoteModel)).scalars().all()

def get_notes_service(session: SessionDep):
    return NotesService(session)

NotesServiceDep = Annotated[NotesService, Depends(get_notes_service)]