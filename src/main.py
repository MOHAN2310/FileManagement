from fastapi import FastAPI
import uvicorn
from database import Base, engine
from routers import ( users, files, folders, search)


app = FastAPI(title="File Management Operations",
        description="This project is a backend API built using FastAPI and SQLAlchemy that allows users to manage files and folders "
    "in a hierarchical structure. Users can create, rename, move, and delete files and folders, as well as list folder "
    "contents. Folders can be nested within other folders, and files cannot contain other items.",
        version="1.0.0"
    )

app.include_router(users.router)
app.include_router(search.router)
app.include_router(folders.router)
app.include_router(files.router)


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
   uvicorn.run("main:routes", host="127.0.0.1", port=8000, reload=True)