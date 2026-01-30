"""
Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.domain.models import TaskStatus


# ===== User Schemas =====

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator('password')
    def password_strength(cls, v):
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserResponse(UserBase):
    """User response schema."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===== Auth Schemas =====

class Token(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload schema."""
    sub: Optional[int] = None
    exp: Optional[int] = None
    type: Optional[str] = None


# ===== Note Schemas =====

class NoteBase(BaseModel):
    """Base note schema."""
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = Field(None, max_length=50000)


class NoteCreate(NoteBase):
    """Note creation schema."""
    pass


class NoteUpdate(BaseModel):
    """Note update schema."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, max_length=50000)


class NoteResponse(NoteBase):
    """Note response schema."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ===== Task Schemas =====

class TaskBase(BaseModel):
    """Base task schema."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)
    due_date: Optional[datetime] = None
    status: TaskStatus = TaskStatus.TODO


class TaskCreate(TaskBase):
    """Task creation schema."""
    pass


class TaskUpdate(BaseModel):
    """Task update schema."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None


class TaskResponse(TaskBase):
    """Task response schema."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ===== Calendar Event Schemas =====

class CalendarEventBase(BaseModel):
    """Base calendar event schema."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)
    start_time: datetime
    end_time: datetime
    linked_task_id: Optional[int] = None
    
    @field_validator('end_time')
    def validate_time_range(cls, v, info):
        """Validate that end_time is after start_time."""
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


class CalendarEventCreate(CalendarEventBase):
    """Calendar event creation schema."""
    pass


class CalendarEventUpdate(BaseModel):
    """Calendar event update schema."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    linked_task_id: Optional[int] = None


class CalendarEventResponse(CalendarEventBase):
    """Calendar event response schema."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ===== Pagination Schemas =====

class PaginationParams(BaseModel):
    """Pagination parameters."""
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)
