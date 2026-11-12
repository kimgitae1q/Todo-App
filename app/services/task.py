from sqlalchemy.orm import Session

from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskSchema, TaskUpdate


class TaskNotFoundError(Exception):
    pass


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = TaskRepository(db)

    def list_tasks(self) -> list[TaskSchema]:
        tasks = self.repository.get_all()
        return [TaskSchema.model_validate(task) for task in tasks]

    def create_task(self, payload: TaskCreate) -> TaskSchema:
        task = self.repository.create(title=payload.title)
        self.db.commit()
        return TaskSchema.model_validate(task)

    def update_task(self, task_id: str, payload: TaskUpdate) -> TaskSchema:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError

        task.title = payload.title if payload.title is not None else task.title
        task.completed = (
            payload.completed if payload.completed is not None else task.completed
        )

        self.db.commit()
        return TaskSchema.model_validate(task)

    def delete_task(self, task_id: str) -> None:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError

        self.repository.delete(task)
        self.db.commit()
