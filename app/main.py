from fastapi import FastAPI
from app.api.v1 import router as todo_router

app = FastAPI(title="Todo API", version="1.0.0")

app.include_router(todo_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Todo API!"}