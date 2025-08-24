import uuid

from sqlmodel import Field, SQLModel

from app.schemas.status import StatusPublic
from app.schemas.type import TypePublic


class TaskBase(SQLModel):
    summary: str = Field(max_length=255, index=True)
    description: str | None = Field(default=None)

    status_id: uuid.UUID = Field(foreign_key="status.id")
    type_id: uuid.UUID = Field(foreign_key="type.id")


class TaskCreate(TaskBase):
    pass


class TaskPublic(TaskBase):
    id: uuid.UUID


class TaskUpdate(SQLModel):
    summary: str | None = None
    description: str | None = None
    status_id: uuid.UUID | None = None
    type_id: uuid.UUID | None = None


class TaskPublicWithStatusAndType(TaskPublic):
   status: StatusPublic
   type: TypePublic
