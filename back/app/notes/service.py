from app.database import NoteModel, SessionDep
from fastapi import Depends
from typing import Annotated
from sqlalchemy import select

class NotesService:
    def __init__(self, session):
        self.session = session

    def create_note(self, note: NoteModel) -> NoteModel:
        try:
            self.session.add(note)
            self.session.commit()
            self.session.refresh(note)
            return note
        except Exception as e:
            self.session.rollback()
            raise e

    def get_note_by_id(self, note_id: int) -> NoteModel | None:
        return self.session.execute(select(NoteModel).where(NoteModel.id == note_id)).scalar_one_or_none()

    def get_all_notes(self) -> list[NoteModel]:
        return self.session.execute(select(NoteModel)).scalars().all()

    def update_note(self, note_id: int, updated_note: NoteModel) -> NoteModel | None:
        note = self.get_note_by_id(note_id)
        if note:
            note.title = updated_note.title
            note.content = updated_note.content
            self.session.commit()
            self.session.refresh(note)
            return note
        return None

    def delete_note(self, note_id: int) -> bool:
        note = self.get_note_by_id(note_id)
        if note:
            self.session.delete(note)
            self.session.commit()
            return True
        return False

def get_notes_service(session: SessionDep) -> NotesService:
    return NotesService(session)

NotesServiceDep = Annotated[NotesService, Depends(get_notes_service)]