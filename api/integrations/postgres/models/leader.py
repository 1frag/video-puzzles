from pydantic import BaseModel


class Leader(BaseModel):
    name: str
    duration_secs: int
