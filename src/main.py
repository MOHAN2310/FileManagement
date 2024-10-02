from fastapi import FastAPI

from routers import ( users, files, folders)


app = FastAPI(title="File Management Operations")

app.include_router(users.router)
app.include_router(files.router)
app.include_router(folders.router)