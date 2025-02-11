from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, select
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os

from database import SessionLocal, engine
import models
from models import User, Folder, File, Permission, FolderACL, FileACL

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

@app.get("/folders")
def get_folders(db: Session = Depends(get_db)):
    """ Devuelve una lista de todas las carpetas con sus IDs y nombres. """
    folders = db.query(Folder).all()
    return [{"id": folder.id, "name": folder.name, "parent_id": folder.parent_id} for folder in folders]

@app.get("/files")
def get_files(db: Session = Depends(get_db)):
    """ Devuelve una lista de todos los archivos con sus IDs, nombres y la carpeta a la que pertenecen. """
    files = db.query(File).all()
    return [{"id": file.id, "name": file.name, "folder_id": file.folder_id} for file in files]