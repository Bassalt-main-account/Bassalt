from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, select
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

class Folder(Base):
    __tablename__ = "folders"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("folders.id", ondelete="CASCADE"), nullable=True)

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    folder_id = Column(Integer, ForeignKey("folders.id", ondelete="CASCADE"))

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class FolderACL(Base):
    __tablename__ = "folder_acl"
    id = Column(Integer, primary_key=True)
    folder_id = Column(Integer, ForeignKey("folders.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"))
    inherit = Column(Boolean, default=True)

class FileACL(Base):
    __tablename__ = "file_acl"
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("files.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"))

# ============================
# CREAR APP FASTAPI
# ============================

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================
# ENDPOINTS BÁSICOS
# ============================

@app.get("/user_exists/{username}")
def user_exists(username: str, db: Session = Depends(get_db)):
    """ Verifica si un usuario existe en la base de datos. """
    return {"exists": db.query(User).filter(User.username == username).first() is not None}

@app.get("/folder_exists/{folder_id}")
def folder_exists(folder_id: int, db: Session = Depends(get_db)):
    """ Verifica si una carpeta existe en la base de datos. """
    return {"exists": db.query(Folder).filter(Folder.id == folder_id).first() is not None}

@app.get("/file_exists/{file_id}")
def file_exists(file_id: int, db: Session = Depends(get_db)):
    """ Verifica si un archivo existe en la base de datos. """
    return {"exists": db.query(File).filter(File.id == file_id).first() is not None}

@app.get("/folder_has_permissions/{folder_id}")
def folder_has_permissions(folder_id: int, db: Session = Depends(get_db)):
    """ Verifica si una carpeta tiene permisos propios (no heredados). """
    exists = db.query(FolderACL).filter(FolderACL.folder_id == folder_id).first() is not None
    return {"folder_id": folder_id, "has_permissions": exists}

@app.get("/file_has_permissions/{file_id}")
def file_has_permissions(file_id: int, db: Session = Depends(get_db)):
    """ Verifica si un archivo tiene permisos propios (no heredados). """
    exists = db.query(FileACL).filter(FileACL.file_id == file_id).first() is not None
    return {"file_id": file_id, "has_permissions": exists}

@app.get("/user_has_permission_on_folder/{username}/{folder_id}/{permission_name}")
def user_has_permission_on_folder(username: str, folder_id: int, permission_name: str, db: Session = Depends(get_db)):
    """ Verifica si un usuario tiene un permiso directo en una carpeta. """
    user = db.query(User).filter(User.username == username).first()
    permission = db.query(Permission).filter(Permission.name == permission_name).first()
    if not user or not permission:
        return {"error": "Usuario o permiso no encontrado", "allowed": False}

    exists = db.query(FolderACL).filter(
        FolderACL.user_id == user.id,
        FolderACL.folder_id == folder_id,
        FolderACL.permission_id == permission.id
    ).first() is not None

    return {"allowed": exists}

@app.get("/user_has_permission_on_file/{username}/{file_id}/{permission_name}")
def user_has_permission_on_file(username: str, file_id: int, permission_name: str, db: Session = Depends(get_db)):
    """ Verifica si un usuario tiene un permiso directo en un archivo. """
    user = db.query(User).filter(User.username == username).first()
    permission = db.query(Permission).filter(Permission.name == permission_name).first()
    if not user or not permission:
        return {"error": "Usuario o permiso no encontrado", "allowed": False}

    exists = db.query(FileACL).filter(
        FileACL.user_id == user.id,
        FileACL.file_id == file_id,
        FileACL.permission_id == permission.id
    ).first() is not None

    return {"allowed": exists}

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

@app.get("/folder_by_name")
def get_folder_by_name(folder_name: str, db: Session = Depends(get_db)):
    """ Devuelve el ID de una carpeta dado su nombre, o False si no existe. """
    folder = db.query(Folder).filter(Folder.name == folder_name).first()
    return {"id": folder.id if folder else False}

@app.get("/file_by_name")
def get_file_by_name(file_name: str, db: Session = Depends(get_db)):
    """ Devuelve el ID de un archivo dado su nombre, o False si no existe. """
    file = db.query(File).filter(File.name == file_name).first()
    return {"id": file.id if file else False}

# ============================
# ENDPOINT DE PRUEBA
# ============================

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
