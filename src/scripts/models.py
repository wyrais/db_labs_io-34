from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


# === USERS ===
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password_hash: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    last_login: Optional[datetime] = None


class UserInDB(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

# === PROJECTS ===
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    status: str

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel): # Додано для можливості оновлення
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None

class ProjectInDB(ProjectBase):
    id: int

    class Config:
        from_attributes = True

# === TASKS ===
class TaskBase(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    priority: Optional[int] = None
    status: str
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel): # Додано для можливості оновлення
    project_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    due_date: Optional[date] = None

class TaskInDB(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True