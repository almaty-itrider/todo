import uuid

from datetime import datetime
from sqlmodel import Field, Relationship

from app.schemas.status import StatusBase


class Status(StatusBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    tasks: list["Task"] = Relationship(back_populates="status")
