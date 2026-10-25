from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.models.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Все нужные модели должны быть импортированы перед запуском
    from app.models.task import TaskORM
    Base.metadata.create_all(bind=engine)
    yield


settings = get_settings()
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(api_router)



# from fastapi import FastAPI, status, HTTPException, Depends
# from pydantic import BaseModel
# from uuid import uuid4
# from fastapi.middleware.cors import  CORSMiddleware
# from contextlib import asynccontextmanager
# from sqlalchemy import create_engine, select
# from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

# DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)

# class Base(DeclarativeBase):
#     id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

# class CategoryORM(Base):
#     __tablename__ = "categories"
#     name: Mapped[str]
    
# class TaskORM(Base):
#     __tablename__ = "tasks"
#     title: Mapped[str]
#     completed: Mapped[bool] = mapped_column(default=False)

# class Task(BaseModel):
#     id: str
#     title: str
#     completed: bool

# class TaskCreate(BaseModel):
#     title: str

# class TaskUpdate(BaseModel):
#     title: str | None = None
#     completed: bool | None = None

# class Category(BaseModel):
#     id: str
#     name: str

# class CategoryCreate(BaseModel):
#     name: str

# class CategoryUpdate(BaseModel):
#     name: str | None = None

# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     Base.metadata.create_all(bind=engine)
#     yield

# app = FastAPI(lifespan=lifespan)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_methods=["*"],
#     allow_headers=["*"],
#     allow_credentials=True,
# )

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def task_to_model(task: TaskORM):
#     return Task(id=task.id, title=task.title, completed=task.completed)

# def category_to_model(category: CategoryORM):
#     return Category(id=category.id, name=category.name)



# @app.get("/categories", response_model = list[Category],tags=["Категории"])
# def get_category(db: Session = Depends(get_db)):
#     categories = db.scalars(select(CategoryORM)).all()
#     return [category_to_model(category) for category in categories]

# @app.post("/categories", response_model = Category, status_code = status.HTTP_201_CREATED,tags=["Категории"])
# def create_category(payload: CategoryCreate,  db: Session = Depends(get_db)):
#     category = CategoryORM(name = payload.name)
#     db.add(category)
#     db.commit()
#     return category_to_model(category)

# @app.patch("/categories/{category_id}", response_model = Category,tags=["Категории"])
# def update_category(category_id: str, payload: CategoryUpdate, db: Session = Depends(get_db)):
#     category = db.get(CategoryORM, category_id)
#     if category is None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
#     if payload.name is not None:
#         category.name = payload.name
#     db.commit()
#     return category_to_model(category)
    
# @app.delete("/categories/{category_id}", status_code = status.HTTP_204_NO_CONTENT,tags=["Категории"])
# def delete_category(category_id: str, db: Session = Depends(get_db)):
#     category = db.get(CategoryORM, category_id)
#     if category is None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
#     db.delete(category)
#     db.commit()
    

# @app.get("/tasks", response_model = list[Task], tags=["Задачи"])
# def get_tasks(db: Session = Depends(get_db)):
#     tasks = db.scalars(select(TaskORM)).all()
#     return [task_to_model(task) for task in tasks]

# @app.post("/tasks", response_model = Task, status_code = status.HTTP_201_CREATED, tags=["Задачи"])
# def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
#     task = TaskORM(title=payload.title, completed=False)
#     db.add(task)
#     db.commit()
#     return task_to_model(task)
    

# @app.patch("/tasks/{task_id}", response_model = Task, tags=["Задачи"])
# def update_task(task_id: str, payload: TaskUpdate, db: Session = Depends(get_db)):
#     task = db.get(TaskORM, task_id)
#     if task is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    
#     task.title = payload.title if payload.title is not None else task.title
#     task.completed = payload.completed if payload.completed is not None else task.completed
#     db.commit()
#     return task_to_model(task)
    


# @app.delete("/tasks/{task_id}", status_code = status.HTTP_204_NO_CONTENT, tags=["Задачи"])
# def delete_task(task_id: str, db: Session = Depends(get_db)):
#     task = db.get(TaskORM, task_id)
#     if task is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
#     db.delete(task)
#     db.commit()
    
