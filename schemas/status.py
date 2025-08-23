import uuid

from sqlmodel import Field, SQLModel


class StatusBase(SQLModel):
    name: str = Field(default="new", index=True)


class StatusCreate(StatusBase):
    pass


class StatusPublic(StatusBase):
    id: uuid.UUID


class StatusUpdate(SQLModel):
    name: str | None = None
