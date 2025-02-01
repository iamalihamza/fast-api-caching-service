from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = "sqlite:///./caching.db"

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    """
    Create the database tables if they don't already exist.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Yields a database session that can be used in endpoints.
    """
    with Session(engine) as session:
        yield session
