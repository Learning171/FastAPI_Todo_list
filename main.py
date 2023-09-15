from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# SQLite database configuration
DATABASE_URL = "sqlite:///./test.db"  # Use a local SQLite database file
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Model
class TodoItemDB(Base):
    __tablename__ = "todo_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    done = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Connecting Fast API with React
origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Pydantic model for your to-do item

class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    done: bool = False

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations
@app.post("/todos/", response_model=TodoItem)
def create_todo(todo: TodoItem, db = Depends(get_db)):
    db_todo = TodoItemDB(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
# http://localhost:8000/todos/
@app.get("/todos/{todo_id}", response_model=TodoItem)
def read_todo(todo_id: int, db = Depends(get_db)):
    db_todo = db.query(TodoItemDB).filter(TodoItemDB.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.get("/todos/", response_model=list[TodoItem])
def read_todos(skip: int = 0, limit: int = 10, db = Depends(get_db)):
    todos = db.query(TodoItemDB).offset(skip).limit(limit).all() 
    return todos

@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, todo: TodoItem, db = Depends(get_db)):
    db_todo = db.query(TodoItemDB).filter(TodoItemDB.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}", response_model=TodoItem)
def delete_todo(todo_id: int, db = Depends(get_db)):
    db_todo = db.query(TodoItemDB).filter(TodoItemDB.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return db_todo


