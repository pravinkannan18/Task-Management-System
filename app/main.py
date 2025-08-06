from fastapi import FastAPI
from app.routes import projects, tasks, auth
from app.database import create_db_and_tables

app = FastAPI(title="Task Management API")

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()