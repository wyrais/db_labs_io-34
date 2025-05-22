from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# === USERS ===
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password_hash: str

class UserInDB(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True  # для Pydantic v2
        # orm_mode = True  # для Pydantic v1

# === PROJECTS ===
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    status: str

class ProjectCreate(ProjectBase):
    pass

class ProjectInDB(ProjectBase):
    id: int

    class Config:
        from_attributes = True  # для Pydantic v2
        # orm_mode = True  # для Pydantic v1

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

class TaskInDB(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # для Pydantic v2
        # orm_mode = True  # для Pydantic v1

# === COMMENTS ===
class CommentBase(BaseModel):
    task_id: int
    user_id: int
    content: str

class CommentCreate(CommentBase):
    pass

class CommentInDB(CommentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # для Pydantic v2
        # orm_mode = True  # для Pydantic v1

# === USER TASKS (Many-to-Many) ===
class UserTaskCreate(BaseModel):
    user_id: int
    task_id: int

class UserTaskInDB(UserTaskCreate):
    assigned_at: datetime

    class Config:
        from_attributes = True  # для Pydantic v2
        # orm_mode = True  # для Pydantic v1

# === ATTACHMENTS ===
class AttachmentBase(BaseModel):
    task_id: int
    filename: str
    filepath: str
    filetype: str
    filesize: int

class AttachmentCreate(AttachmentBase):
    pass

class AttachmentInDB(AttachmentBase):
    id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True  # для Pydantic v2
        # orm_mode = True  # для Pydantic v1