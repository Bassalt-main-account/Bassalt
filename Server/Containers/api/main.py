from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, select
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
import jwt
import auth
from passlib.context import CryptContext
from datetime import datetime, timedelta
from database import SessionLocal, engine
import models
from models import User, Folder, File, Permission, FolderACL, FileACL
import schemas


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#################################### 
#   EXAMPLE
####################################
@app.get("/")
def read_root():
    return {"message": "DB + API up and running"}

#################################### 
#   AUTENTICACIÓN
####################################

@app.post("/register/", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """ Permite a los usuarios registrarse con username y password """
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    hashed_password = auth.hash_password(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login/", response_model=schemas.TokenData)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """ Permite a los usuarios iniciar sesión y obtener un token JWT """
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectos")
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

#################################### 
#   BASICS
####################################

# 📍 Endpoint para obtener todos los usuarios
@app.get("/users/", dependencies=[Depends(auth.oauth2_scheme)])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/folders", dependencies=[Depends(auth.oauth2_scheme)])
def get_folders(db: Session = Depends(get_db)):
    """ Devuelve una lista de todas las carpetas con sus IDs y nombres. """
    folders = db.query(Folder).all()
    return [{"id": folder.id, "name": folder.name, "parent_id": folder.parent_id} for folder in folders]

@app.get("/files", dependencies=[Depends(auth.oauth2_scheme)])
def get_files(db: Session = Depends(get_db)):
    """ Devuelve una lista de todos los archivos con sus IDs, nombres y la carpeta a la que pertenecen. """
    files = db.query(File).all()
    return [{"id": file.id, "name": file.name, "folder_id": file.folder_id} for file in files]

#################################### 
#   GET BY ID
####################################

@app.get("/user/{user_id}", dependencies=[Depends(auth.oauth2_scheme)])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """ Devuelve todos los datos de un usuario dado su ID, o error si no existe. """
    user = db.query(User).filter(User.id == user_id).first()
    return user.__dict__ if user else {"error": "Usuario no encontrado"}

@app.get("/folder/{folder_id}", dependencies=[Depends(auth.oauth2_scheme)])
def get_folder_by_id(folder_id: int, db: Session = Depends(get_db)):
    """ Devuelve todos los datos de una carpeta dado su ID, o error si no existe. """
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    return folder.__dict__ if folder else {"error": "Carpeta no encontrada"}

@app.get("/file/{file_id}", dependencies=[Depends(auth.oauth2_scheme)])
def get_file_by_id(file_id: int, db: Session = Depends(get_db)):
    """ Devuelve todos los datos de un archivo dado su ID, o error si no existe. """
    file = db.query(File).filter(File.id == file_id).first()
    return file.__dict__ if file else {"error": "Archivo no encontrado"}


#################################### 
#   GET ID BY NAME
####################################

@app.get("/user_by_name", dependencies=[Depends(auth.oauth2_scheme)])
def get_user_by_name(username: str, db: Session = Depends(get_db)):
    """ Devuelve el ID de un usuario dado su nombre, o False si no existe. """
    user = db.query(User).filter(User.username == username).first()
    return {"id": user.id} if user else {"error": "Usuario no encontrado"}


@app.get("/folder_by_name", dependencies=[Depends(auth.oauth2_scheme)])
def get_folder_by_name(folder_name: str, db: Session = Depends(get_db)):
    """ Devuelve el ID de una carpeta dado su nombre, o False si no existe. """
    folder = db.query(Folder).filter(Folder.name == folder_name).first()
    return {"id": folder.id if folder else False}

@app.get("/file_by_name", dependencies=[Depends(auth.oauth2_scheme)])
def get_file_by_name(file_name: str, db: Session = Depends(get_db)):
    """ Devuelve el ID de un archivo dado su nombre, o False si no existe. """
    file = db.query(File).filter(File.name == file_name).first()
    return {"id": file.id if file else False}

#################################### 
#   EXIST BY ID
####################################

@app.get("/user_exists/{user_id}", dependencies=[Depends(auth.oauth2_scheme)])
def user_exists(user_id: int, db: Session = Depends(get_db)):
    """ Verifica si un usuario existe en la base de datos por ID. """
    return {"exists": db.query(User).filter(User.id == user_id).first() is not None}

@app.get("/folder_exists/{folder_id}", dependencies=[Depends(auth.oauth2_scheme)])
def folder_exists(folder_id: int, db: Session = Depends(get_db)):
    """ Verifica si una carpeta existe en la base de datos. """
    return {"exists": db.query(Folder).filter(Folder.id == folder_id).first() is not None}

@app.get("/file_exists/{file_id}", dependencies=[Depends(auth.oauth2_scheme)])
def file_exists(file_id: int, db: Session = Depends(get_db)):
    """ Verifica si un archivo existe en la base de datos. """
    return {"exists": db.query(File).filter(File.id == file_id).first() is not None}


#################################### 
#   EXTRA PERMISSIONS?
####################################

@app.get("/folder_has_permissions/{folder_id}", dependencies=[Depends(auth.oauth2_scheme)])
def folder_has_permissions(folder_id: int, db: Session = Depends(get_db)):
    """ Verifica si una carpeta tiene permisos propios (no heredados). """
    exists = db.query(FolderACL).filter(FolderACL.folder_id == folder_id).first() is not None
    return {"folder_id": folder_id, "has_permissions": exists}

@app.get("/file_has_permissions/{file_id}", dependencies=[Depends(auth.oauth2_scheme)])
def file_has_permissions(file_id: int, db: Session = Depends(get_db)):
    """ Verifica si un archivo tiene permisos propios (no heredados). """
    exists = db.query(FileACL).filter(FileACL.file_id == file_id).first() is not None
    return {"file_id": file_id, "has_permissions": exists}

#################################### 
#   USER HAS PERMISIONS?
####################################

@app.get("/user_has_permission_on_folder/{username}/{folder_id}/{permission_name}", dependencies=[Depends(auth.oauth2_scheme)])
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

@app.get("/user_has_permission_on_file/{username}/{file_id}/{permission_name}", dependencies=[Depends(auth.oauth2_scheme)])
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


#################################### 
#   DELETE
####################################

@app.delete("/delete_user/{user_id}", dependencies=[Depends(auth.oauth2_scheme)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """ Elimina un usuario y sus permisos en cascada. """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "Usuario no encontrado"}

    # Eliminar permisos en archivos y carpetas
    db.query(FolderACL).filter(FolderACL.user_id == user.id).delete()
    db.query(FileACL).filter(FileACL.user_id == user.id).delete()

    # Eliminar usuario
    db.delete(user)
    db.commit()
    
    return {"message": f"Usuario con ID {user_id} eliminado correctamente"}


@app.delete("/delete_folder/{folder_id}", dependencies=[Depends(auth.oauth2_scheme)])
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

@app.delete("/delete_file/{file_id}", dependencies=[Depends(auth.oauth2_scheme)])
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


#################################### 
#   CREATE 
####################################

@app.post("/create_user/", dependencies=[Depends(auth.oauth2_scheme)])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """ Crea un nuevo usuario """
    db_user = User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/create_folder/", dependencies=[Depends(auth.oauth2_scheme)])
def create_folder(folder: schemas.FolderCreate, db: Session = Depends(get_db)):
    """ Crea una nueva carpeta """
    db_folder = Folder(name=folder.name, parent_id=folder.parent_id)
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return db_folder

@app.post("/create_file/", dependencies=[Depends(auth.oauth2_scheme)])
def create_file(file: schemas.FileCreate, db: Session = Depends(get_db)):
    """ Crea un nuevo archivo dentro de una carpeta """
    db_file = File(name=file.name, folder_id=file.folder_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

@app.post("/create_permission/", dependencies=[Depends(auth.oauth2_scheme)])
def create_permission(permission: schemas.PermissionCreate, db: Session = Depends(get_db)):
    """ Crea un nuevo permiso """
    db_permission = Permission(name=permission.name)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

@app.post("/assign_folder_permission/", dependencies=[Depends(auth.oauth2_scheme)])
def assign_folder_permission(folder_acl: schemas.FolderACLCreate, db: Session = Depends(get_db)):
    """ Asigna un permiso a un usuario en una carpeta """
    db_acl = FolderACL(
        folder_id=folder_acl.folder_id,
        user_id=folder_acl.user_id,
        permission_id=folder_acl.permission_id,
        inherit=folder_acl.inherit
    )
    db.add(db_acl)
    db.commit()
    db.refresh(db_acl)
    return db_acl

@app.post("/assign_file_permission/", dependencies=[Depends(auth.oauth2_scheme)])
def assign_file_permission(file_acl: schemas.FileACLCreate, db: Session = Depends(get_db)):
    """ Asigna un permiso a un usuario en un archivo """
    db_acl = FileACL(
        file_id=file_acl.file_id,
        user_id=file_acl.user_id,
        permission_id=file_acl.permission_id
    )
    db.add(db_acl)
    db.commit()
    db.refresh(db_acl)
    return db_acl
