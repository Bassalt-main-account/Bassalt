from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# 🚀 Crear la aplicación FastAPI
app = FastAPI()

# 🛠 Crear las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

# 🔹 Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📍 Ruta principal para verificar que la API funciona
@app.get("/")
def read_root():
    return {"message": "API funcionando correctamente"}

# 📍 Endpoint para obtener todos los usuarios
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

