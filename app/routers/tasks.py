import uuid

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select

from app.db.settings import get_session
from app.db.models import Task
from app.schemas.task import TaskCreate, TaskPublic, TaskPublicWithStatusAndType, TaskUpdate


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[TaskPublic])
def read_tasks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, le=10),
):
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
    return tasks


@router.get("/{task_id}", response_model=TaskPublicWithStatusAndType)
def read_task(
    *,
    session: Session = Depends(get_session),
    task_id: uuid.UUID,
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=TaskPublic)
def create_task(
    *,
    session: Session = Depends(get_session),
    task: TaskCreate,
):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.patch("/{task_id}", response_model=TaskPublic)
def update_task(
    *,
    session: Session = Depends(get_session),
    task_id: uuid.UUID,
    task: TaskUpdate,
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/{task_id}")
def delete_task(
    *,
    session: Session = Depends(get_session),
    task_id: uuid.UUID,
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}
