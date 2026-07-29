from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task = Column(String, index=True, nullable=False)
    completed = Column(Boolean, default=False)