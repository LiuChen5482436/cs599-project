from pydantic import BaseModel, Field
from typing import Optional, Literal

class UserInfo(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[Literal["男", "女", "其他"]] = None
    medical_history: Optional[str] = None
    medication: Optional[str] = None
    allergies: Optional[str] = None

class ChatRequest(BaseModel):
    session_id: str
    message: str = Field(..., min_length=1, max_length=2000)
    user_info: Optional[UserInfo] = None

class ChatResponse(BaseModel):
    response: str
    consultation_id: int
    is_complete: bool
    needs_followup: bool
    followup_question: Optional[str] = None

class FeedbackRequest(BaseModel):
    consultation_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    success: bool
    message: str
