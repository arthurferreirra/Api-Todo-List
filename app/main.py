from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.v1.routes import router as todo_router
from app.api.v1.auth_routes import router as auth_router

from app.database import Base, engine
from app.core.exceptions import AppException, NotFoundException, ConflictException
from sqlalchemy.exc import SQLAlchemyError

from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import router as todo_router

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API", version="1.0.0")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Handlers Globais

@app.exception_handler(AppException) #customize exception handler for AppException
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "error_type": exc.error_type}
    )
@app.exception_handler(RequestValidationError) #validation error handler for request validation schemas from pydantic
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Data sent to the server is invalid.",
            "error_type": "ValidationError",
            "error": exc.errors()
        }
    )

@app.exception_handler(SQLAlchemyError) #generic exception handler for unhandled exceptions
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error occurred while processing the request.",
            "error_type": "DatabaseError"
        }
    )

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
app.include_router(auth_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Api is ready to use!"}