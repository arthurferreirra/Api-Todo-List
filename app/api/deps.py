from app.database import sessionLocal

def get_db(): # Dependency function to get a database session, which can be used in FastAPI routes to interact with the database.

    db = sessionLocal() 
    try:
        yield db #yielding the database session to the caller, allowing them to use it within a context manager.
    finally:
        db.close()
