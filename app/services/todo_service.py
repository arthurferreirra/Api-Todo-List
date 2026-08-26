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

def create_todo(db: Session, todo_data: TodoCreate, owner_id: int):
    # Cria a tarefa já vinculada ao dono logado
    db_todo = TodoModel(
        task=todo_data.task,
        completed=False,
        owner_id=owner_id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todos_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10, completed: Optional[bool] = None):
    # Lista apenas as tarefas do usuário logado, aplicando filtros se houver
    query = db.query(TodoModel).filter(TodoModel.owner_id == user_id)
    
    if completed is not None:
        query = query.filter(TodoModel.completed == completed)
        
    return query.offset(skip).limit(limit).all()

def get_todo_by_id_and_user(db: Session, todo_id: int, user_id: int):
    # Busca uma tarefa específica garantindo que ela pertence ao usuário
    todo = db.query(TodoModel).filter(
        TodoModel.id == todo_id, 
        TodoModel.owner_id == user_id
    ).first()
    
    if not todo:
        raise NotFoundException(f"Tarefa com ID {todo_id} não encontrada.")
    return todo


def delete_todo(db: Session, todo_id: int, user_id: int):
    todo = get_todo_by_id_and_user(db, todo_id, user_id)
    db.delete(todo)
    db.commit()
    return {"message": f"Todo with id {todo_id} has been deleted."}

def update_todo(db: Session, todo_id: int, user_id: int, todo_data: TodoUpdate):
    todo = get_todo_by_id_and_user(db, todo_id, user_id)
    update_data = todo_data.model_dump(exclude_unset=True)

    if "task" in update_data:
        if db.query(TodoModel).filter(TodoModel.task == update_data["task"], TodoModel.id != todo_id).first():
            raise ConflictException("A todo with this task already exists.")

    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo