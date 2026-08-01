from sqlalchemy.orm import Session
from app.models.todo import TodoModel
from app.schemas.todo import TodoCreate

def get_all_todos(db: Session):
    return db.query(TodoModel).all()

def create_todo(db: Session, todo_data: TodoCreate):
    existing = db.query(TodoModel).filter(TodoModel.task == todo_data.task).first()
    if existing:
        raise ValueError("A todo with this task already exists.")

    db_todo = TodoModel(task=todo_data.task, completed=False)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        return False  # Todo not found
    db.delete(todo)
    db.commit()
    return True