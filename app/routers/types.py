import uuid

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select

from app.db.settings import get_session
from app.db.models import Type
from app.schemas.type import TypeCreate, TypePublic, TypeUpdate


router = APIRouter(
    prefix="/types",
    tags=["types"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[TypePublic])
def read_types(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, le=10),
):
    types = session.exec(select(Type).offset(offset).limit(limit)).all()
    return types


@router.get("/{type_id}", response_model=TypePublic)
def read_type(
    *,
    session: Session = Depends(get_session),
    type_id: uuid.UUID,
):
    type = session.get(Type, type_id)
    if not type:
        raise HTTPException(status_code=404, detail="Type not found")
    return type


@router.post("/", response_model=TypePublic)
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


@router.patch("/{type_id}", response_model=TypePublic)
def update_type(
    *,
    session: Session = Depends(get_session),
    type_id: uuid.UUID,
    type: TypeUpdate,
):
    db_type = session.get(Type, type_id)
    if not db_type:
        raise HTTPException(status_code=404, detail="Type not found")
    type_data = type.model_dump(exclude_unset=True)
    db_type.sqlmodel_update(type_data)
    session.add(db_type)
    session.commit()
    session.refresh(db_type)
    return db_type


@router.delete("/{type_id}")
def delete_type(
    *,
    session: Session = Depends(get_session),
    type_id: uuid.UUID,
):
    type = session.get(Type, type_id)
    if not type:
        raise HTTPException(status_code=404, detail="Type not found")
    session.delete(type)
    session.commit()
    return {"ok": True}
