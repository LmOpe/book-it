"""The database module"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from api.core.settings import settings

DATABASE_URL=settings.DATABASE_URL


def get_db_engine() -> create_engine:
    """
    Get the database engine.
    
    This function creates a database engine using the SQLAlchemy library.
    The engine is used to connect to the database and execute SQL queries.

    Returns:
        create_engine: The SQLAlchemy engine object.
    """

    return create_engine(DATABASE_URL)


engine = get_db_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = scoped_session(SessionLocal)

Base = declarative_base()


def create_database():
    """
    Create the database tables.

    This function creates the database tables defined in the SQLAlchemy models.

    Returns:
        Base.metadata: The metadata object containing the database schema.
    """
    return Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency to get the database session.

    The function provides a database session for the FastAPI application.
    It is used as a dependency in the API routes to interact with the database.

    Yields:
        Session: The database session object.
    
    Finally, it closes the session after use.
    """
    db = db_session()
    try:
        yield db
    finally:
        db.close()
