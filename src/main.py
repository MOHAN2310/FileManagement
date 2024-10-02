from fastapi import FastAPI
from database import Base, engine
from routers import ( users, files, folders)


app = FastAPI(title="File Management Operations")

app.include_router(users.router)
app.include_router(files.router)
app.include_router(folders.router)


Base.metadata.create_all(bind=engine)