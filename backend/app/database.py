import os
import pathlib
from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv(dotenv_path=f"{pathlib.Path().resolve()}/.env")

# Build flexible
sqlite_url = (
    f"{os.getenv("SQLITE_BASE_URL").replace("FILENAME", os.getenv("SQLITE_FILE_NAME"))}"
)

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# This is for creating the tables for all the table models
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# A session is what stores the object in memory
def get_session():
    with Session(engine) as session:
        yield session
