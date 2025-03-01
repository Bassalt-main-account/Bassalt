from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, select
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)  
    mail = Column(String, nullable=False)  # Nuevo campo de correo renombrado
    birthday = Column(String, nullable=True) 
    default_role = Column(Integer, ForeignKey("permissions.id", ondelete="SET NULL"), nullable=True)  # Nuevo campo de rol


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