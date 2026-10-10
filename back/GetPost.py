from fastapi import FastAPI, status
from uuid import uuid4
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

class Task(BaseModel):
    """Модель задач"""
    id: str
    title: str
    completed: bool

class TaskCreate(BaseModel):
    title: str

tasks: list[Task] = []

@app.get("/tasks",  response_model=list[Task])
def get_tasks():
    return tasks


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    """Создать новую задачу"""
    task = Task(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(task)
    return task