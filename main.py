#!/usr/bin/env python3

from models.todo import TodoItem
from sqlmodel import Session, create_engine

import typer

APP_NAME = "An Over-engineered Todo App"
cli = typer.Typer()


@cli.command()
def migrate(db_url: str = typer.Option("sqlite:///:memory:", envvar="DB_URL", help="Database URL")):
    engine = create_engine(db_url)
    TodoItem.metadata.create_all(engine)


@cli.command()
def create(db_url: str = typer.Option("sqlite:///:memory:", envvar="DB_URL", help="Database URL")):
    engine = create_engine(db_url)
    TodoItem.metadata.create_all(engine)
    with Session(engine) as session:
        todo = TodoItem(title="Todo 1")
        session.add(todo)
        session.commit()
        session.refresh(todo)
        print(todo)


if __name__ == "__main__":
    cli()
