import enum

from pydantic import BaseModel


class NextActionIdent(str, enum.Enum):
    PUBLISH_RESULT = 'publish_result'


class NextAction(BaseModel):
    ident: NextActionIdent
