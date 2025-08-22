from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Query
from sqlmodel import Session, select

from db.models.status import Status
from db.models.type import Type
from db.settings import create_db_and_tables, get_session
from schemas.status import StatusCreate, StatusPublic
from schemas.type import TypeCreate, TypePublic


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield create_db_and_tables()


app = FastAPI(lifespan=lifespan)


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


@app.get("/types/", response_model=list[TypePublic])
def read_types(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, le=10),
):
    types = session.exec(select(Type).offset(offset).limit(limit)).all()
    return types


@app.post("/types/", response_model=TypePublic)
def create_type(
    *,
    session: Session = Depends(get_session),
    type: TypeCreate,
):
    db_type = Type.model_validate(type)
    session.add(db_type)
    session.commit()
    session.refresh(db_type)
    return db_type
