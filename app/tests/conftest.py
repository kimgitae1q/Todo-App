from unittest.mock import Mock

import pytest
from services.task import TaskService
from sqlalchemy.orm import Session

from app.repositories.task import TaskRepository


@pytest.fixture
def db_mock() -> Mock:
    return Mock(spec=Session)


@pytest.fixture
def repository_mock() -> Mock:
    return Mock(spec=TaskRepository)


@pytest.fixture
def service(db_mock: Mock, repository_mock: Mock) -> TaskService:
    task_service = TaskService(db_mock)
    task_service.repository = repository_mock
    return task_service
