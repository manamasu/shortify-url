from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
import pyshorteners
from app.database import create_db_and_tables, get_session
from app.models import URL, URLPublic, URLUpdate


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(_: FastAPI):
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


@app.get("/api/v1/urls", response_model=list[URLPublic], tags=["urls"])
async def get_urls(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    url = session.exec(select(URL).offset(offset).limit(limit)).all()
    return url


@app.post("/api/v1/urls", response_model=URLPublic, tags=["urls"])
async def create_url(url: URL, session: SessionDep):
    db_url = URL.model_validate(url)
    url_dict = url.model_dump()

    # TODO Instead of pyshorteners get a ml_model or train a model myself to get unique names
    type_tiny = pyshorteners.Shortener()
    url_dict.update({"short_url": type_tiny.tinyurl.short(url_dict.get("long_url"))})

    db_url.sqlmodel_update(url_dict)
    session.add(db_url)
    session.commit()
    session.refresh(db_url)
    return db_url


# TODO wip, getting an argumenterror
@app.patch("/api/v1/urls/{url_id}", response_model=URLPublic, tags=["urls"])
def update_url(url_id: int, url: URLUpdate, session: SessionDep):
    url_db = session.get(url, url_id)
    if not url_db:
        raise HTTPException(status_code=404, detail="URL was not found")
    url_data = url.model_dump(exclude_unset=True)
    url.sqlmodel_update(url_data)
    return url


@app.delete("/api/v1/urls/{url_id}", tags=["urls"])
async def delete_url(url_id: int, session: SessionDep):
    url = session.get(URL, url_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL was not found")
    session.delete(url)
    session.commit()
    return {"ok": True}
