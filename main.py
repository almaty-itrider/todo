from contextlib import asynccontextmanager
import uuid

from fastapi import Depends, FastAPI, Query
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from db.models.status import Status
from db.models.type import Type
from db.settings import create_db_and_tables, get_session
from schemas.status import StatusCreate, StatusPublic, StatusUpdate
from schemas.type import TypeCreate, TypePublic


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield create_db_and_tables()


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/statuses/", response_model=list[StatusPublic])
def read_statuses(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, le=10),
):
    statuses = session.exec(select(Status).offset(offset).limit(limit)).all()
    return statuses


@app.get("/status/{status_id}", response_model=StatusPublic)
def read_status(
    *,
    session: Session = Depends(get_session),
    status_id: uuid.UUID,
):
    status = session.get(Status, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return status


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


@app.patch("/status/{status_id}", response_model=StatusPublic)
def update_status(
    *,
    session: Session = Depends(get_session),
    status_id: uuid.UUID,
    status: StatusUpdate,
):
    db_status = session.get(Status, status_id)
    if not db_status:
        raise HTTPException(status_code=404, detail="Status not found")
    status_data = status.model_dump(exclude_unset=True)
    db_status.sqlmodel_update(status_data)
    session.add(db_status)
    session.commit()
    session.refresh(db_status)
    return db_status


@app.delete("/status/{status_id}")
def delete_status(
    *,
    session: Session = Depends(get_session),
    status_id: uuid.UUID,
):
    status = session.get(Status, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    session.delete(status)
    session.commit()
    return {"ok": True}


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
