import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from typing import List

app = FastAPI()

# 内存数据库
todos = [
    {"id": 1, "task": "Learn Knative", "completed": True},
    {"id": 2, "task": "Deploy with Generic Runner", "completed": False},
]

class TodoItem(BaseModel):
    task: str

@app.get("/api/todos")
def get_todos():
    return todos

@app.post("/api/todos")
def add_todo(item: TodoItem):
    new_id = max([t["id"] for t in todos], default=0) + 1
    new_todo = {"id": new_id, "task": item.task, "completed": False}
    todos.append(new_todo)
    return new_todo

@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return {"status": "ok"}

# 获取当前文件所在目录，确保静态文件路径正确
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")

# 挂载静态文件
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
