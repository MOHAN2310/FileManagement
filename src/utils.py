from sqlalchemy.orm import Session
from model import Folder, User, File


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_name(db: Session, user_name: int):
    return db.query(User).filter(User.username == user_name).first()

def get_folder(db: Session, folder_id: int):
    return db.query(Folder).filter(Folder.id == folder_id).first()

def get_folder_by_name(db: Session, folder_name: int):
    return db.query(Folder).filter(Folder.name == folder_name).first()

def get_file(db: Session, file_id: int):
    return db.query(File).filter(File.id == file_id).first()

def get_file_by_name(db: Session, file_name: int):
    return db.query(File).filter(File.name == file_name).first()