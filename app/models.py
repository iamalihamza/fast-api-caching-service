from typing import Optional
from sqlmodel import SQLModel, Field


class CachedTransform(SQLModel, table=True):
    __tablename__ = "cached_transform"

    id: Optional[int] = Field(default=None, primary_key=True)
    original_string: str = Field(unique=True, index=True)
    transformed_string: str


class Payload(SQLModel, table=True):
    __tablename__ = "payload"

    id: Optional[int] = Field(default=None, primary_key=True)
    final_string: str = Field(unique=True)  # The interleaved result
