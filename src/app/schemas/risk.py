from pydantic import BaseModel
from typing import Optional

class RiskAssessmentRequest(BaseModel):
    symptoms: str
    age: Optional[int] = None
    medical_history: Optional[str] = None
    special_condition: Optional[str] = None
    temperature: Optional[float] = None

class RiskAssessmentResponse(BaseModel):
    risk_level: str
    risk_name: str
    risk_description: str
    score: float
    factors: list[str]
    advice: str

class RedFlagDetectionResponse(BaseModel):
    has_red_flags: bool
    detected_flags: list[str]
    emergency_response: Optional[str] = None
