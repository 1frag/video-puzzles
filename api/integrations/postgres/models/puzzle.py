from pydantic import BaseModel


class Puzzle(BaseModel):
    id: str
    name: str
    preview: str
    metadata: str
