from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.api.v1.routes import router as todo_router

from app.database import Base, engine
from app.core.exceptions import NotFoundException, ConflictException
from sqlalchemy.exc import SQLAlchemyError

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API", version="1.0.0")

#Handlers Globais

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc), "error_type": "NotFoundException"}
    )

@app.exception_handler(ConflictException)
async def conflict_exception_handler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc), "error_type": "ConflictException"}
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    # Logar o erro internamente se necessário
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno no banco de dados.", "error_type": "DatabaseError"}
    )

app.include_router(todo_router, prefix="/api/v1")
