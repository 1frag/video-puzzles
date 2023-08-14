from pydantic import BaseModel


class VerifyingGame(BaseModel):
    duration_secs: int
    name: str
