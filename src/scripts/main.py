from fastapi import FastAPI, HTTPException
from typing import List, Optional
from config import get_connection
from datetime import datetime, date

from models import (
    UserInDB, UserCreate, UserUpdate,
    ProjectInDB, ProjectCreate, ProjectUpdate,
    TaskInDB, TaskCreate, TaskUpdate
)

app = FastAPI(title="Lab6 DAO with Users, Projects, Tasks")


# ======== HELPER FUNCTIONS ==========\

def fetch_all(table: str):
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table}")
        return cursor.fetchall()


def fetch_by_id(table: str, key: str, value: int):
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table} WHERE {key} = %s", (value,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail=f"{table.capitalize()} not found")
        return result


def insert_data(query: str, values: tuple):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid # Повертаємо ID новоствореного запису
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))


def update_data(table: str, key: str, value: int, update_data: dict):
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")
    fields = ', '.join(f"{k} = %s" for k in update_data)
    query = f"UPDATE {table} SET {fields} WHERE {key} = %s"
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, list(update_data.values()) + [value])
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"{table.capitalize()} not found")
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))


def delete_by_id(table: str, key: str, value: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM {table} WHERE {key} = %s", (value,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"{table.capitalize()} not found")
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))


# ========== USER ENDPOINTS ===========
@app.get("/users", response_model=List[UserInDB], tags=["Users"])
async def get_all_users():
    return fetch_all("Users")

@app.get("/users/{user_id}", response_model=UserInDB, tags=["Users"])
async def get_user(user_id: int):
    return fetch_by_id("Users", "id", user_id)

@app.post("/users", response_model=dict, status_code=201, tags=["Users"])
async def create_user(user: UserCreate):
    # Додаємо поточний час для created_at та last_login при створенні
    now = datetime.now()
    user_id = insert_data(
        "INSERT INTO Users (username, email, password_hash, created_at, last_login) VALUES (%s, %s, %s, %s, %s)",
        (user.username, user.email, user.password_hash, now, now)
    )
    return {"message": f"User added with ID: {user_id}"}

@app.put("/users/{user_id}", response_model=UserInDB, tags=["Users"])
async def update_user(user_id: int, user_update: UserUpdate):
    update_data("Users", "id", user_id, user_update.model_dump(exclude_unset=True))
    return await get_user(user_id)

@app.delete("/users/{user_id}", response_model=dict, tags=["Users"])
async def delete_user(user_id: int):
    delete_by_id("Users", "id", user_id)
    return {"message": f"User with id {user_id} deleted"}


# ========== PROJECT ENDPOINTS ===========
@app.get("/projects", response_model=List[ProjectInDB], tags=["Projects"])
async def get_all_projects():
    return fetch_all("Projects")

@app.get("/projects/{project_id}", response_model=ProjectInDB, tags=["Projects"])
async def get_project(project_id: int):
    return fetch_by_id("Projects", "id", project_id)

@app.post("/projects", response_model=dict, status_code=201, tags=["Projects"])
async def create_project(project: ProjectCreate):
    project_id = insert_data(
        "INSERT INTO Projects (title, description, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s)",
        (project.title, project.description, project.start_date, project.end_date, project.status)
    )
    return {"message": f"Project added with ID: {project_id}"}

@app.put("/projects/{project_id}", response_model=ProjectInDB, tags=["Projects"])
async def update_project(project_id: int, project_update: ProjectUpdate):
    update_data("Projects", "id", project_id, project_update.model_dump(exclude_unset=True))
    return await get_project(project_id)

@app.delete("/projects/{project_id}", response_model=dict, tags=["Projects"])
async def delete_project(project_id: int):
    delete_by_id("Projects", "id", project_id)
    return {"message": f"Project with id {project_id} deleted"}


# ========== TASK ENDPOINTS ===========
@app.get("/tasks", response_model=List[TaskInDB], tags=["Tasks"])
async def get_all_tasks():
    return fetch_all("Tasks")

@app.get("/tasks/{task_id}", response_model=TaskInDB, tags=["Tasks"])
async def get_task(task_id: int):
    return fetch_by_id("Tasks", "id", task_id)

@app.post("/tasks", response_model=dict, status_code=201, tags=["Tasks"])
async def create_task(task: TaskCreate):
    # Додаємо поточний час для created_at при створенні
    now = datetime.now()
    task_id = insert_data(
        "INSERT INTO Tasks (project_id, title, description, priority, status, due_date, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (task.project_id, task.title, task.description, task.priority, task.status, task.due_date, now)
    )
    return {"message": f"Task added with ID: {task_id}"}

@app.put("/tasks/{task_id}", response_model=TaskInDB, tags=["Tasks"])
async def update_task(task_id: int, task_update: TaskUpdate):
    update_data("Tasks", "id", task_id, task_update.model_dump(exclude_unset=True))
    return await get_task(task_id)

@app.delete("/tasks/{task_id}", response_model=dict, tags=["Tasks"])
async def delete_task(task_id: int):
    delete_by_id("Tasks", "id", task_id)
    return {"message": f"Task with id {task_id} deleted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)