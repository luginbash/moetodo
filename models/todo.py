from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import HSTORE


class TodoItem(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    kvs: dict = Field(default=None, sa_column=Column(HSTORE))
    urgency: int = 0
    context: str = None
    project: str = None
    tags: List[str] = []
    created_at: datetime = datetime.now()
    completed_at: datetime = None
    due_at: datetime = None


class Tenant(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted_at: datetime = None
    users: List["User"] = Relationship(back_populates="tenant")


class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    email: str
    password: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted_at: datetime = None
    tenant_id: Optional[UUID] = Field(default=None, foreign_key="tenant.id")
    tenant: Optional[Tenant] = Relationship(back_populates="users")



