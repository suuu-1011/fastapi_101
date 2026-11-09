from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from . import models, schemas
from .dependencies import get_current_user, require_teacher


router = APIRouter(prefix="/pms/tasks", tags=["PMS Tasks"])


# TEACHER: Create and assign a task
@router.post("/", response_model=schemas.TaskResponse, status_code=201)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_teacher)
):
    student = db.query(models.User).filter(
        models.User.id == task.user_id,
        models.User.role == "student",
        models.User.status == "active"
    ).first()

    if not student:
        raise HTTPException(404, detail="Active student not found")

    new_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=task.user_id,
        teacher_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# TEACHER: View all tasks
@router.get("/", response_model=list[schemas.TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_teacher)
):
    return db.query(models.Task).all()


# STUDENT: View own tasks
@router.get("/my", response_model=list[schemas.TaskResponse])
def get_my_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "student":
        raise HTTPException(403, detail="Student access required")

    return db.query(models.Task).filter(
        models.Task.user_id == current_user.id
    ).all()


# TEACHER: View task progress summary
@router.get("/progress/")
def get_task_progress(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_teacher)
):
    total_tasks = db.query(models.Task).count()

    pending = db.query(models.Task).filter(
        models.Task.status == "pending"
    ).count()

    in_progress = db.query(models.Task).filter(
        models.Task.status == "in progress"
    ).count()

    done = db.query(models.Task).filter(
        models.Task.status == "done"
    ).count()

    return {
        "total_tasks": total_tasks,
        "pending": pending,
        "in_progress": in_progress,
        "done": done
    }

# TEACHER: Filter tasks by status
@router.get("/filter/")
def filter_tasks(
    status: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_teacher)
):
    allowed_statuses = ["pending", "in progress", "done"]

    if status not in allowed_statuses:
        raise HTTPException(400, detail="Invalid task status")

    return db.query(models.Task).filter(
        models.Task.status == status
    ).all()


# STUDENT: Update own task status and work notes
@router.patch("/{task_id}/work")
def update_my_task(
    task_id: int,
    task_data: schemas.StudentTaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "student":
        raise HTTPException(403, detail="Student access required")

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(404, detail="Task not found")

    updates = task_data.dict(exclude_unset=True)

    if not updates:
        raise HTTPException(400, detail="No update data provided")

    for key, value in updates.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# TEACHER: View a specific task
@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_teacher)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(404, detail="Task not found")

    return task


# TEACHER: Update a task
@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_teacher)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(404, detail="Task not found")

    updates = task_data.dict(exclude_unset=True)

    if not updates:
        raise HTTPException(400, detail="No update data provided")

    if "user_id" in updates:
        student = db.query(models.User).filter(
            models.User.id == updates["user_id"],
            models.User.role == "student",
            models.User.status == "active"
        ).first()

        if not student:
            raise HTTPException(404, detail="Active student not found")

    for key, value in updates.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# TEACHER: Delete a task
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_teacher)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}

