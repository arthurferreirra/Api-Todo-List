from typing import Optional

from sqlalchemy.orm import Session
from app.models.todo import TodoModel
from app.schemas.todo import TodoCreate, TodoUpdate
from app.core.exceptions import ConflictException, NotFoundException

def get_all_todos(db: Session, skip: int = 0, limit: int = 10, completed: Optional[bool] = None):
    query = db.query(TodoModel)

    if completed is not None:
        query = query.filter(TodoModel.completed == completed)

    return query.offset(skip).limit(limit).all()

def create_todo(db: Session, todo_data: TodoCreate):
    existing = db.query(TodoModel).filter(TodoModel.task == todo_data.task).first()
    if existing:
        raise ConflictException("A todo with this task already exists.")

    db_todo = TodoModel(task=todo_data.task, completed=todo_data.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo_by_id(db: Session, todo_id: int):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise NotFoundException(f"Todo with id {todo_id} not found.")
    return todo

def delete_todo(db: Session, todo_id: int):
    todo = get_todo_by_id(db, todo_id)
    db.delete(todo)
    db.commit()
    return {"message": f"Todo with id {todo_id} has been deleted."}

def update_todo(db: Session, todo_id: int, todo_data: TodoUpdate):
    todo = get_todo_by_id(db,todo_id)
    update_data = todo_data.dict(exclude_unset=True)

    if "task" in update_data:
        if db.query(TodoModel).filter(TodoModel.task == update_data["task"], TodoModel.id != todo_id).first():
            raise ConflictException("A todo with this task already exists.")

    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo