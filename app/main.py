from fastapi import FastAPI
from app.api.v1.routes import router as todo_router

from app.database import Base, engine
from app.models.todo import TodoModel

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API", version="1.0.0")

app.include_router(todo_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to the Todo API!"}