from sqlmodel import Field, SQLModel


class URLBase(SQLModel):
    long_url: str = Field(index=True)


class URL(URLBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_url: str | None = Field(default=None)


class URLPublic(URLBase):
    id: int
    short_url: str


class URLUpdate(URLBase):
    long_url: str | None = None
