from fastapi import FastAPI
from fastapi import Depends, Query
from sqlmodel import Session, select

from db.models.status import Status
from schemas.status import StatusCreate, StatusPublic
from db.settings import get_session
from db.settings import create_db_and_tables


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/statuses/", response_model=list[StatusPublic])
def read_statuses(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, le=10),
):
    statuses = session.exec(select(Status).offset(offset).limit(limit)).all()
    return statuses


@app.post("/statuses/", response_model=StatusPublic)
def create_status(
    *,
    session: Session = Depends(get_session),
    status: StatusCreate,
):
    db_status = Status.model_validate(status)
    session.add(db_status)
    session.commit()
    session.refresh(db_status)
    return db_status
