from sqlalchemy.orm import Session
from model import Folder, User, File


async def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

async def get_user_by_name(db: Session, user_name: int):
    return db.query(User).filter(User.username == user_name).first()

async def get_folder(db: Session, folder_id: int):
    return db.query(Folder).filter(Folder.id == folder_id).first()

async def get_folder_by_name(db: Session, folder_name: int):
    return db.query(Folder).filter(Folder.name == folder_name).first()

async def get_file(db: Session, file_id: int):
    return db.query(File).filter(File.id == file_id).first()

async def get_file_by_name(db: Session, file_name: int):
    return db.query(File).filter(File.name == file_name).first()

async def get_folder_hierarchy(folder_id: int, db: Session):
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    if not folder:
        return None

    hierarchy = []
    current_folder = folder

    while current_folder:
        hierarchy.insert(0, current_folder)
        current_folder = current_folder.parent_folder

    def build_nested_structure(folders):
        if not folders:
            return None
        root = folders[0]
        current = root
        for next_folder in folders[1:]:
            current.subfolders = [next_folder]
            current = next_folder
        return root

    nested_structure = build_nested_structure(hierarchy)
    return nested_structure