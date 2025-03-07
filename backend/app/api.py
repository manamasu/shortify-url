from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from app.database import create_db_and_tables, get_session
from app.models import URL


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


origins = ["http://localhost:5173", "localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
async def root() -> dict:
    return {"message": "Welcome to your Backend of Shortify."}


@app.get("/api/v1/urls", tags=["urls"])
async def get_urls() -> list[dict]:
    return [{"message": "success"}]


@app.post("/api/v1/urls", tags=["urls"])
def create_url(url: URL, session: SessionDep) -> URL:
    session.add(url)
    session.commit()
    session.refresh(url)
    return url


@app.put("/api/v1/urls/{url_id}")
async def update_url(url_id: int):
    return url_id


@app.delete("/api/v1/urls/{url_id}")
async def delete_url(url_id: int, session: SessionDep):
    url = session.get(URL, url_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL was not found")
    session.delete(url)
    session.commit()
    return {"ok": True}
