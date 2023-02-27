from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
    title: str = Field(title="The title of the note.", max_length=50)
    description: str


class NoteDB(NoteSchema):
    id: int
