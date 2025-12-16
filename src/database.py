from config import settings
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine


def create_db_engine(verbose: bool = False, **kwargs):
    """
    Create the SQLAlchemy engine for database interactions.

    Args:
        verbose (bool): If True, enables SQL query logging.
        **kwargs: Additional keyword arguments for the engine.
    Returns:
        engine: The SQLAlchemy engine instance.
    """
    # Using check_same_thread=False allows FastAPI to use the same SQLite database in different threads.
    connect_args = {
        "check_same_thread": False,
    }
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        **{
            "echo": verbose,
            "pool_use_lifo": True,  # Avoid many idle connections
            "pool_pre_ping": True,  # Gracefully handle connections closed by the server
            **kwargs,
        },
    )
    return engine


def create_db_and_tables(engine: Engine):
    """
    Create database tables based on the defined SQLModel models.
    """
    SQLModel.metadata.create_all(engine)


engine = create_db_engine()
