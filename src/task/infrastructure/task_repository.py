from sqlite3 import Connection
from typing import List, Optional
from uuid import UUID

from src.task.domain.entity import Task
from src.task.domain.repository.task_repository import TaskRepository


class TaskSqliteRepository(TaskRepository):
    def __init__(self, session: Connection):
        self.session = session

    def save(self, task: Task) -> Task:
        c = self.session.cursor()
        c.execute(
            "INSERT INTO tasks (id, description, status, \
            created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (
                str(task.id),
                task.description,
                task.status.value,
                task.created_at,
                task.updated_at,
            ),
        )
        self.session.commit()
        self.session.close()
        return c.lastrowid

    def get_by_id(self, id: UUID) -> Task:
        return None

    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    def update(self, task: Task) -> None:
        raise NotImplementedError

    def list(
        self,
        search: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Task]:
        raise NotImplementedError
