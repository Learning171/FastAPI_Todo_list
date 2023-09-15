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


# SQLAlchemy Database Model


class CarDB(Base):
    __tablename__ = "cars_table"
    car_company = Column(String, primary_key=True, index=True)
    car_model = Column(String, index=True)
    specifications = Column(String, index=True)
    price = Column(Float, default=False)


class BikeDB(Base):
    __tablename__ = "bike_table"
    bike_id = Column(Integer, primary_key=True)
    bike_company = Column(String, index=True)
    bike_model = Column(String, index=True)
    specification = Column(String, index=True)
    price = Column(Float, default=False)


Base.metadata.create_all(bind=engine)  # Create Database Tables

app = FastAPI()  # Initialize app instance


# Pydentic Models declarations for Database Table

class CarBase(BaseModel):
    car_company: str
    car_model: str
    specifications: str
    price: float


class BikeBase(BaseModel):
    bike_id: int
    bike_company: str
    bike_model: str
    specification: str
    price: float


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""APIs For POST"""


@app.post("/bikes")  # Add new Bike object
async def create_bike(bike: BikeBase, db=Depends(get_db)):
    db_bike = BikeDB(**bike.dict())
    db.add(db_bike)
    db.commit()
    db.refresh(db_bike)
    return db_bike


@app.post("/cars/")  # Add new Car object
async def create_car(car: CarBase, db=Depends(get_db)):
    db_car = CarDB(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


"""APIs for GET"""


@app.get("/cars/{car_model}")  # GET single car object
async def read_car(car_model: str, db=Depends(get_db)):
    db_car = db.query(CarDB).filter(CarDB.car_model == car_model).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="car not found")
    return db_car


@app.get("/cars/")  # GET all cars object
async def read_cars(skip: int = 0, limit: int = 10, db=Depends(get_db)):
    cars = db.query(CarDB).offset(skip).limit(limit).all()
    return cars


@app.get("/bikes/{bike_id}")  # GET single bike object
async def read_bike(bike_id: int, db=Depends(get_db)):
    db_bike = db.query(BikeDB).filter(BikeDB.bike_id == bike_id).first()
    if db_bike is None:
        raise HTTPException(status_code=404, detail="bike not found")
    return db_bike


@app.get("/bikes")  # GET all bike object
async def read_bikes(skip: int = 0, limit: int = 10, db=Depends(get_db)):
    bikes = db.query(BikeDB).offset(skip).limit(limit).all()
    return bikes


"""APIs for PUT"""


@app.put("/cars/{car_model}")  # Update existing records of car
async def update_car(car_model: str, car: CarBase, db=Depends(get_db)):
    db_car = db.query(CarDB).filter(CarDB.car_model == car_model).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="car not found")
    for key, value in car.dict().items():
        setattr(db_car, key, value)
    db.commit()
    db.refresh(db_car)
    return db_car


@app.put("/bikes/{bike_id}")  # Update existing records of Bike
async def update_bike(bike_id: int, bike: BikeBase, db=Depends(get_db)):
    db_bike = db.query(BikeDB).filter(BikeDB.bike_id == bike_id).first()
    if db_bike is None:
        raise HTTPException(status_code=404, detail="bike not found")
    for key, value in bike.dict().items():
        setattr(db_bike, key, value)
    db.commit()
    db.refresh(db_bike)
    return db_bike


"""APIs for DELETE"""


@app.delete("/cars/{car_model}")  # Delete existing records of Car.
async def delete_car(car_model: str, db=Depends(get_db)):
    db_car = db.query(CarDB).filter(CarDB.car_model == car_model).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="car not found")
    db.delete(db_car)
    db.commit()
    return db_car


@app.delete("/bikes/{bike_id}")  # Delete existing records of bike.
async def delete_bike(bike_id: int, db=Depends(get_db)):
    db_bike = db.query(BikeDB).filter(BikeDB.bike_id == bike_id).first()
    if db_bike is None:
        raise HTTPException(status_code=404, detail="bike not found")
    db.delete(db_bike)
    db.commit()
    return db_bike
