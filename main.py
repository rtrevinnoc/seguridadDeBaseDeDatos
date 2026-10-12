import os
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, text
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "world")
DB_PORT = os.getenv("DB_PORT", "3306")
USE_SSL = os.getenv("USE_SSL", "false").lower() in ("true", "1", "yes")

CONNECTION_STRING = (
    "mysql+pymysql://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Capa 4: Conexión cifrada (TLS/X509)
connect_args = {}
if USE_SSL:
    ca_path = os.getenv("SSL_CA", "certs/ca.pem")
    cert_path = os.getenv("SSL_CERT", "certs/client-cert.pem")
    key_path = os.getenv("SSL_KEY", "certs/client-key.pem")
    connect_args["ssl"] = {
        "ca": ca_path,
        "cert": cert_path,
        "key": key_path,
        "check_hostname": False,
    }

engine = create_engine(CONNECTION_STRING, connect_args=connect_args)
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

class BusquedaPais(BaseModel):
    nombre: str = Field(
                min_length=1,
                max_length=200#,
                #pattern=r'^[a-zA-Z\s]+$'
            )

@app.get("/index")
async def index():
    return "Hola, el servidor esta funcionando"

@app.get("/country")
async def country(db = Depends(retrieve_db)):
    query = "SELECT * FROM country"
    resultado = db.execute(text(query))
    return resultado.mappings().all()

#@app.get("/country/{nombre}")
#async def buscar_country(nombre: str, db = Depends(retrieve_db)):
#    query = f"SELECT * FROM country WHERE Name = '{nombre}'"
#    print(query)
#    resultado = db.execute(text(query))
#    return resultado.mappings().all()

@app.get("/country/restricted")
async def buscar_country2(params: BusquedaPais = Depends(), db = Depends(retrieve_db)):
    query = f"SELECT Name FROM country WHERE Name = '{params.nombre}' AND Population >= 100000000"
    print(query)
    resultado = db.execute(text(query))
    return len(resultado.fetchall()) > 0
