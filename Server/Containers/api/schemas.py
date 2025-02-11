from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

class TokenData(BaseModel):
    access_token: str
    token_type: str

# 📍 Modelo para crear una carpeta
class FolderCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None

# 📍 Modelo para crear un archivo
class FileCreate(BaseModel):
    name: str
    folder_id: int

# 📍 Modelo para crear un permiso
class PermissionCreate(BaseModel):
    name: str

# 📍 Modelo para asignar permisos a carpetas
class FolderACLCreate(BaseModel):
    folder_id: int
    user_id: int
    permission_id: int
    inherit: Optional[bool] = True

# 📍 Modelo para asignar permisos a archivos
class FileACLCreate(BaseModel):
    file_id: int
    user_id: int
    permission_id: int
