import uuid
from sqlmodel import Field
from schemas.status import StatusBase


class Status(StatusBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
