from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# SQLite database configuration
DATABASE_URL = "sqlite:///./car.db"  # SQLite database file
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy Model
class CarDB(Base):
    __tablename__ = "cars_table"
    car_company = Column(String, primary_key=True, index=True)
    car_model = Column(String, index=True)
    specifications = Column(String, index=True)
    price = Column(Float, default=False)


Base.metadata.create_all(bind=engine)

app = FastAPI()


class CarBase(BaseModel):
    car_company: str
    car_model: str
    specifications: str
    price: float


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cars/")
def create_car(car: CarBase, db=Depends(get_db)):
    db_car = CarDB(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


@app.get("/cars/{car_model}")
def read_car(car_model: str, db=Depends(get_db)):
    db_car = db.query(CarDB).filter(CarDB.car_model == car_model).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="car not found")
    return db_car


@app.get("/cars/")
def read_cars(skip: int = 0, limit: int = 10, db=Depends(get_db)):
    cars = db.query(CarDB).offset(skip).limit(limit).all()
    return cars


@app.put("/cars/{car_model}")
def update_car(car_model: str, car: CarBase, db=Depends(get_db)):
    db_car = db.query(CarDB).filter(CarDB.car_model == car_model).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="car not found")
    for key, value in car.dict().items():
        setattr(db_car, key, value)
    db.commit()
    db.refresh(db_car)
    return db_car


@app.delete("/cars/{car_model}")
def delete_car(car_model: str, db=Depends(get_db)):
    db_car = db.query(CarDB).filter(CarDB.car_model == car_model).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="car not found")
    db.delete(db_car)
    db.commit()
    return db_car