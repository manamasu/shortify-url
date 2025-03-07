from sqlmodel import Field, SQLModel


class URL(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    long_url: str = Field(index=True)
    short_url: str | None = Field(default=None, index=True)
