from fastapi import FastAPI, status, HTTPException
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

class Category(BaseModel):
    """Модель каатегории"""
    id: str
    name: str

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str | None = None


class Task(BaseModel):
    """Модель задач"""
    id: str
    title: str
    completed: bool

class TaskCreate(BaseModel):
    title: str

class BookCreate(BaseModel):
    book: str

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

book = ""
tasks: list[Task] = []
categories: list[Category] = []



@app.get("/books", tags=["Книги"])
def get_book():
    return f"Любимая книга: {book}"

@app.post("/books", tags=["Книги"])
def add_book(payload: BookCreate):
    global book
    book = payload.book
    return book


@app.get("/tasks",  response_model=list[Task], tags=["Задачи"])
def get_tasks():
    return tasks


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Задачи"])
def create_task(payload: TaskCreate):
    """Создать новую задачу"""
    task = Task(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(task)
    return task

@app.patch("/tasks/{task_id}", response_model=Task, tags=["Задачи"])
def update_task(task_id: str, payload: TaskUpdate):
    """
    Обновить существующую задачу
    task_id получаем из url
    payload получаем из тела запроса
    """
    for task in tasks:
        if task.id == task_id:
            if payload.title is not None:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

@app.delete("/tasks/{task_id}",status_code=status.HTTP_204_NO_CONTENT, tags=["Задачи"])
def delete_task(task_id: str):
    """Удалить задачу"""
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")


@app.get("/categories",response_model=list[Category],tags = ["Категории"])
def get_categories():
    return categories

@app.post("/categories", status_code=status.HTTP_200_OK, response_model=Category,tags = ["Категории"])
def create_category(payload: CategoryCreate):
    category1 = Category(id=str(uuid4()), name = payload.name)
    categories.append(category1)
    return category1

@app.patch("/categories/{category_id}", status_code=status.HTTP_200_OK, response_model=Category,tags = ["Категории"])
def update_category(category_id: str, payload: CategoryUpdate):
    for category in categories:
        if category.id == category_id:
            if payload.name is not None:
                category.name = payload.name
            return category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")

@app.delete("/categories/{category_id}",status_code=status.HTTP_204_NO_CONTENT,tags = ["Категории"])
def delete_category(category_id: str):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")


