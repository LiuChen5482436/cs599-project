from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = None
    medical_history: Optional[str] = None
    medication: Optional[str] = None
    allergies: Optional[str] = None

class UserCreate(UserBase):
    session_id: str

class UserResponse(UserBase):
    id: int
    session_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConsultationBase(BaseModel):
    chief_complaint: Optional[str] = None

class ConsultationCreate(ConsultationBase):
    user_id: int

class ConsultationResponse(ConsultationBase):
    id: int
    user_id: int
    status: str
    risk_level: Optional[str] = None
    red_flags_detected: bool
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ConsultationDetailResponse(ConsultationResponse):
    messages: list[MessageResponse] = []
    user: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True
