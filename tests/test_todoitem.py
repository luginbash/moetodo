from collections import namedtuple

from models.todo import TodoItem
from sqlmodel import Session, create_engine, inspect


class TestTodoItem:
    db_url = "sqlite:///:memory:"

    def test_migrate(self):
        engine = create_engine(self.db_url)
        TodoItem.metadata.create_all(engine)
        inspector = inspect(engine)
        assert TodoItem.__tablename__ in inspector.get_table_names()

    def test_create(self):
        engine = create_engine(self.db_url)
        TodoItem.metadata.create_all(engine)
        with Session(engine) as session:
            todo = TodoItem()
            session.add(todo)
            session.commit()
            session.refresh(todo)

            assert session.get(TodoItem, todo.todoitem_id) == todo

