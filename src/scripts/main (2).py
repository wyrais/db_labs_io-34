from fastapi import FastAPI, HTTPException
from typing import List
import logging
from improved_config import get_connection
from model_for import UserInDB, UserCreate, ProjectInDB, ProjectCreate

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Project Manager API")

# ===================== HELPERS =====================
def fetch_all(table: str):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Используем правильный регистр для таблиц
            query = f"SELECT * FROM {table}"
            logger.info(f"Executing query: {query}")
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error fetching from {table}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def fetch_by_id(table: str, key: str, value: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {table} WHERE {key} = %s"
            logger.info(f"Executing query: {query} with value: {value}")
            cursor.execute(query, (value,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail=f"{table.capitalize()} not found")
            return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching from {table}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def insert_data(query: str, values: tuple):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            logger.info(f"Executing query: {query}")
            cursor.execute(query, values)
            conn.commit()
            logger.info("Insert successful")
    except Exception as e:
        logger.error(f"Error inserting data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ===================== STARTUP EVENT =====================
@app.on_event("startup")
async def startup_event():
    """Проверка подключения к БД при запуске"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise

# ===================== USERS =====================
@app.get("/users", response_model=List[UserInDB], tags=["Users"])
def get_users():
    return fetch_all("users")

@app.get("/users/{user_id}", response_model=UserInDB, tags=["Users"])
def get_user(user_id: int):
    return fetch_by_id("users", "id", user_id)

@app.post("/users", status_code=201, tags=["Users"])
def create_user(user: UserCreate):
    insert_data(
        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
        (user.username, user.email, user.password_hash)
    )
    return {"message": "User created successfully"}

# ===================== PROJECTS =====================
@app.get("/projects", response_model=List[ProjectInDB], tags=["Projects"])
def get_projects():
    return fetch_all("projects")

@app.get("/projects/{project_id}", response_model=ProjectInDB, tags=["Projects"])
def get_project(project_id: int):
    return fetch_by_id("projects", "id", project_id)

@app.post("/projects", status_code=201, tags=["Projects"])
def create_project(project: ProjectCreate):
    insert_data(
        "INSERT INTO projects (title, description, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s)",
        (project.title, project.description, project.start_date, project.end_date, project.status)
    )
    return {"message": "Project created successfully"}

# ===================== HEALTH CHECK =====================
@app.get("/health", tags=["Health"])
def health_check():
    """Эндпоинт для проверки работоспособности API и БД"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}