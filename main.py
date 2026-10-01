import os
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")    

CONNECTION_STRING = (
    "mysql+pymysql://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:3306/{DB_NAME}"
)

engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI(title="SeguridadDeBaseDeDatos")

def retrieve_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()
class Country(Base):
    __tablename__ = "country"
    code = Column(String, primary_key=True)
    name = Column(String)

@app.get("/index")
async def index():
    return "Hola, el servidor esta funcionando"

@app.get("/country")
async def country(db = Depends(retrieve_db)):
    query = "SELECT * FROM country"
    resultado = db.execute(text(query))
    return resultado.fetchall()

@app.get("/country/{nombre}")
async def buscar_country(nombre: str, db = Depends(retrieve_db)):
    query = f"SELECT * FROM country WHERE Name = '{nombre}'"
    print(query)
    resultado = db.execute(text(query))
    return resultado.fetchall()

@app.get("/country/restricted/{nombre}")
async def buscar_country2(nombre: str, db = Depends(retrieve_db)):
    query = f"SELECT Name, Population, SurfaceArea FROM country WHERE Name = '{nombre}' AND Population >= 100000000"
    print(query)
    resultado = db.execute(text(query))
    return resultado.fetchall()
