from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)

    root_folder = relationship(
        "Folder",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=False)
    parent_folder_id = Column(Integer, ForeignKey('folders.id'), nullable=True)
    parent_folder = relationship(
        "Folder",
        remote_side=[id],
        back_populates="subfolders",
        foreign_keys=[parent_folder_id]
    )
    subfolders = relationship(
        "Folder",
        back_populates="parent_folder",
        cascade="all, delete-orphan",
        foreign_keys=[parent_folder_id]
    )
    files = relationship(
        "File",
        back_populates="folder",
        cascade="all, delete-orphan"
    )
    user = relationship(
        "User",
        back_populates="root_folder"
    )

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    folder_id = Column(Integer, ForeignKey('folders.id'), nullable=False)
    folder = relationship(
        "Folder",
        back_populates="files"
    )

