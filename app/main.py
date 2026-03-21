from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Tasks API")

tasks = []


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task):
    for t in tasks:
        if t.id == task.id:
            raise HTTPException(status_code=400, detail="Task already exists")
    tasks.append(task)
    return task
