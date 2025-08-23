import uuid

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select

from app.db.settings import get_session
from app.db.models import Status
from app.schemas.status import StatusCreate, StatusPublic, StatusUpdate


router = APIRouter(
    prefix="/statuses",
    tags=["statuses"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[StatusPublic])
def read_statuses(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, le=10),
):
    statuses = session.exec(select(Status).offset(offset).limit(limit)).all()
    return statuses


@router.get("/{status_id}", response_model=StatusPublic)
def read_status(
    *,
    session: Session = Depends(get_session),
    status_id: uuid.UUID,
):
    status = session.get(Status, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return status


@router.post("/", response_model=StatusPublic)
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


@router.patch("/{status_id}", response_model=StatusPublic)
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


@router.delete("/{status_id}")
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
