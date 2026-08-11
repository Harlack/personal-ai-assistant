from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

engine = create_engine("sqlite:///notes.db")

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class NoteModel(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, type_= String(30))
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False)


with Session() as session:
    pass

Base.metadata.create_all(engine)