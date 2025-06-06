"""CRUD helpers for tasks and sections."""


from typing import Iterable
from .models import Task


class Repository:
    """Simple repository wrapping list-based storage."""

    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def add_task(self, name: str) -> Task:
        task = Task(id=len(self._tasks) + 1, name=name)
        self._tasks.append(task)
        return task

    def list_tasks(self) -> Iterable[Task]:
        return list(self._tasks)
