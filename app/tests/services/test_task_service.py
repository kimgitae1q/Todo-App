from unittest.mock import Mock

from app.models.task import TaskORM
from app.schemas.task import TaskRead
from app.services.task import TaskService


def test_list_tasks_returns_pydantic_models(
    service: TaskService,
    repository_mock: Mock,
) -> None:
    repository_mock.get_all.return_value = [
        TaskORM(id="task-1", title="Изучить pytest", completed=False),
        TaskORM(id="task-2", title="Написать первый тест", completed=True),
    ]

    result = service.list_tasks()

    assert result == [
        TaskRead(id="task-1", title="Изучить pytest", completed=False),
        TaskRead(id="task-2", title="Написать первый тест", completed=True),
    ]
