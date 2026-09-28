from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def initialize_database():
    Base.metadata.create_all(bind=engine)
    if "owners" in inspect(engine).get_table_names():
        columns = {column["name"] for column in inspect(engine).get_columns("owners")}
        if "user_id" not in columns:
            with engine.begin() as connection:
                connection.execute(
                    text("ALTER TABLE owners ADD COLUMN user_id INTEGER REFERENCES users(id)")
                )
                connection.execute(
                    text("CREATE UNIQUE INDEX IF NOT EXISTS ix_owners_user_id ON owners(user_id)")
                )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()