from fastapi import FastAPI, status, HTTPException
from uuid import uuid4
from fastapi.params import Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, Mapped, mapped_column
from contextlib import asynccontextmanager

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker[Session](bind=engine)

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class TaskORM(Base):
    __tablename__ = "tasks"
    title: Mapped[str]
    completed: Mapped[bool]

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

class Category(BaseModel):
    id: str
    name: str

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str | None = None

class Task(BaseModel):
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
categories: list[Category] = []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def task_orm_to_model(task_orm: TaskORM):
    return Task(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)

@app.get("/books", tags=["Книги"])
def get_book():
    return f"Любимая книга: {book}"

@app.post("/books", tags=["Книги"])
def add_book(payload: BookCreate):
    global book
    book = payload.book
    return book

@app.get("/tasks",  response_model=list[Task], tags=["Задачи"])
def get_tasks(db: Session = Depends(get_db)):
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in tasks_from_db]

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Задачи"])
def create_task(payload: TaskCreate,db: Session = Depends(get_db)):
    task = TaskORM(title=payload.title, completed=False)
    db.add(task)
    db.commit()
    return task_orm_to_model(task)

@app.patch("/tasks/{task_id}", response_model=Task, tags=["Задачи"])
def update_task(task_id: str, payload: TaskUpdate,db: Session = Depends(get_db)):
    task_for_update = db.get(TaskORM, task_id)
    if payload.title:
        task_for_update.title = payload.title
    if payload.completed:
        task_for_update.completed = payload.completed
    db.commit()
    return task_for_update

@app.delete("/tasks/{task_id}",status_code=status.HTTP_204_NO_CONTENT, tags=["Задачи"])
def delete_task(task_id: str,db: Session = Depends(get_db)):
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()

@app.get("/categories",response_model=list[Category],tags = ["Категории"])
def get_categories(db: Session = Depends(get_db)):
    return categories

@app.post("/categories", status_code=status.HTTP_200_OK, response_model=Category,tags = ["Категории"])
def create_category(payload: CategoryCreate,db: Session = Depends(get_db)):
    category1 = Category(id=str(uuid4()), name = payload.name)
    categories.append(category1)
    return category1

@app.patch("/categories/{category_id}", status_code=status.HTTP_200_OK, response_model=Category,tags = ["Категории"])
def update_category(category_id: str, payload: CategoryUpdate,db: Session = Depends(get_db)):
    for category in categories:
        if category.id == category_id:
            if payload.name is not None:
                category.name = payload.name
            return category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")

@app.delete("/categories/{category_id}",status_code=status.HTTP_204_NO_CONTENT,tags = ["Категории"])
def delete_category(category_id: str,db: Session = Depends(get_db)):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")