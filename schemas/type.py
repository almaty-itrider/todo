import uuid

from sqlmodel import Field, SQLModel


class TypeBase(SQLModel):
    name: str = Field(default="task", index=True)


class TypeCreate(TypeBase):
    pass


class TypePublic(TypeBase):
    id: uuid.UUID
