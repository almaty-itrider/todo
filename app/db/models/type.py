import uuid

from sqlmodel import Field

from app.schemas.type import TypeBase


class Type(TypeBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
