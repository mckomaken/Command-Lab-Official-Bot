from pydantic import BaseModel


class PatchNoteImage(BaseModel):
    url: str
    title: str


class PatchNoteEntry(BaseModel):
    title: str
    type: str
    version: str
    image: PatchNoteImage
    body: str


class PatchNote(BaseModel):
    entries: list[PatchNoteEntry]
    version: int
