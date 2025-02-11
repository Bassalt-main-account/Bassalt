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

@app.delete("/delete_user/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    """ Elimina un usuario y sus permisos en cascada. """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {"error": "Usuario no encontrado"}

    # Eliminar permisos en archivos y carpetas
    db.query(FolderACL).filter(FolderACL.user_id == user.id).delete()
    db.query(FileACL).filter(FileACL.user_id == user.id).delete()

    # Eliminar usuario
    db.delete(user)
    db.commit()
    
    return {"message": f"Usuario {username} eliminado correctamente"}

@app.delete("/delete_folder/{folder_id}")
def delete_folder(folder_id: int, db: Session = Depends(get_db)):
    """ Elimina una carpeta, sus subcarpetas, archivos y permisos en cascada. """
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    if not folder:
        return {"error": "Carpeta no encontrada"}

    # Buscar y eliminar archivos en la carpeta
    db.query(FileACL).filter(FileACL.file_id.in_(
        db.query(File.id).filter(File.folder_id == folder_id)
    )).delete()
    db.query(File).filter(File.folder_id == folder_id).delete()

    # Buscar y eliminar permisos de la carpeta
    db.query(FolderACL).filter(FolderACL.folder_id == folder_id).delete()

    # Buscar y eliminar subcarpetas de manera recursiva
    def delete_subfolders(parent_id):
        subfolders = db.query(Folder).filter(Folder.parent_id == parent_id).all()
        for subfolder in subfolders:
            delete_subfolders(subfolder.id)  # Llamada recursiva
            db.query(FolderACL).filter(FolderACL.folder_id == subfolder.id).delete()
            db.delete(subfolder)

    delete_subfolders(folder_id)

    # Eliminar la carpeta principal
    db.delete(folder)
    db.commit()

    return {"message": f"Carpeta {folder.name} eliminada correctamente"}

@app.delete("/delete_file/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    """ Elimina un archivo y sus permisos en cascada. """
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        return {"error": "Archivo no encontrado"}

    # Eliminar permisos
    db.query(FileACL).filter(FileACL.file_id == file_id).delete()

    # Eliminar archivo
    db.delete(file)
    db.commit()

    return {"message": f"Archivo {file.name} eliminado correctamente"}

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    """ Devuelve una lista de todos los usuarios con sus IDs y nombres. """
    users = db.query(User).all()
    return [{"id": user.id, "username": user.username} for user in users]


@app.get("/user/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """ Devuelve todos los datos de un usuario dado su ID, o error si no existe. """
    user = db.query(User).filter(User.id == user_id).first()
    return user.__dict__ if user else {"error": "Usuario no encontrado"}

@app.get("/folder/{folder_id}")
def get_folder_by_id(folder_id: int, db: Session = Depends(get_db)):
    """ Devuelve todos los datos de una carpeta dado su ID, o error si no existe. """
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    return folder.__dict__ if folder else {"error": "Carpeta no encontrada"}

@app.get("/file/{file_id}")
def get_file_by_id(file_id: int, db: Session = Depends(get_db)):
    """ Devuelve todos los datos de un archivo dado su ID, o error si no existe. """
    file = db.query(File).filter(File.id == file_id).first()
    return file.__dict__ if file else {"error": "Archivo no encontrado"}

@app.get("/user_by_name")
def get_user_by_name(username: str, db: Session = Depends(get_db)):
    """ Devuelve el ID de un usuario dado su nombre, o False si no existe. """
    user = db.query(User).filter(User.username == username).first()
    return {"id": user.id} if user else {"error": "Usuario no encontrado"}


# ============================
# ENDPOINT DE PRUEBA
# ============================

@app.get("/")
def root():
    return {"message": "DB + API up and running"}

#TODO: REORGANIZAR ESTA GUARRERIA