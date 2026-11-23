from pydantic import BaseModel, ConfigDict, Field

class NoteRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=30)
    content: str = Field(..., min_length=1, max_length=3000)
        

class Note(BaseModel): 
    id: int
    title: str
    content: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)