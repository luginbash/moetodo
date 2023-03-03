import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import HSTORE


class Tenant(SQLModel, table=True):
    tenant_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    name: str = Field(index=True)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted_at: datetime = None
    projects: List["Project"] = Relationship(back_populates="tenant")
    users: List["User"] = Relationship(back_populates="tenant")


class User(SQLModel, table=True):
    user_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    name: str = Field(index=True)
    email: str
    password: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted_at: datetime = None
    tenant_id: List[UUID] = Field(default=None, foreign_key="tenant.tenant_id")
    tenant: List["Tenant"] = Relationship(back_populates="users")
    journals: Optional["Journal"] = Relationship(back_populates="user")


class Project(SQLModel, table=True):
    project_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    name: str = Field(index=True)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted_at: datetime = None
    tenant_id: List[UUID] = Field(default=None, foreign_key="tenant.tenant_id")
    tenant: Optional["Tenant"] = Relationship(back_populates="projects")
    todoitem: Optional["TodoItem"] = Relationship(back_populates="project")
    journals: Optional["Journal"] = Relationship(back_populates="project")


class Journal(SQLModel, table=True):
    journal_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    todoitem_id: Optional[UUID] = Field(default=None, foreign_key="todoitem.todoitem_id")
    todoitem: Optional["TodoItem"] = Relationship(back_populates="journals")
    user_id: UUID = Field(default=None, foreign_key="user.user_id")
    user: Optional["User"] = Relationship(back_populates="journals")
    project_id: UUID = Field(default=None, foreign_key="project.project_id")
    project: Optional["Project"] = Relationship(back_populates="journals")
    created_at: datetime = datetime.now()
    edited_at: datetime = None
    content: str = None


class Tag(SQLModel, table=True):
    tag_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    name: str = Field(index=True)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted_at: datetime = None
    todoitem: Optional["TodoItem"] = Relationship(back_populates="tags")


class TodoItem(SQLModel, table=True):
    todoitem_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    project_id: Optional[UUID] = Field(default=None, foreign_key="project.project_id")
    project: Optional["Project"] = Relationship(back_populates="todoitem")
    parent: UUID = Field(default_factory=uuid4, index=True)  # Subtasks
    journals: Optional["Journal"] = Relationship(back_populates="todoitem")
    description: str = Field(default=None, index=True)
    summary: str = Field(default=None, index=True)
    urgency: int = Field(default=-1, index=True)
    context: str = Field(default=None, index=True)
    tag_ids: List[UUID] = Field(default=None, foreign_key="tag.tag_id")
    tags: List["Tag"] = Relationship(back_populates="todoitem")
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: datetime = Field(default=None)
    due_at: datetime = Field(default=None)
