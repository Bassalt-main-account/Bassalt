from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os

# ============================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ============================
# DEFINICIÓN DE MODELOS
# ============================

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)

# ============================
# CREAR APP FASTAPI
# ============================

app = FastAPI()

# Dependencia para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================
# ENDPOINT PARA LISTAR USUARIOS
# ============================

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": user.id, "username": user.username} for user in users]

# ============================
# ENDPOINT DE PRUEBA
# ============================

@app.get("/")
def root():
    return {"message": "DB & API up and running! "}
