import uuid

from datetime import datetime
from sqlmodel import Field, Relationship

from app.schemas.task import TaskBase
from .status import Status
from .type import Type


class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    status: Status = Relationship(back_populates="tasks")
    type: Type = Relationship(back_populates="tasks")
