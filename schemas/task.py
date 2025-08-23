import uuid

from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    summary: str = Field(max_length=255, index=True)
    description: str | None = Field(default=None)

    status: uuid.UUID = Field(default="new", foreign_key="status.id")
    type: uuid.UUID = Field(default="task", foreign_key="type.id")


class TaskCreate(TaskBase):
    pass


class TaskPublic(TaskBase):
    id: uuid.UUID
