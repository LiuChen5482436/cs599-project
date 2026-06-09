from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class UserInfoValidator(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = Field(None, pattern="^(男|女|其他)$")
    medical_history: Optional[str] = None
    medication: Optional[str] = None
    allergies: Optional[str] = None
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        if v is not None and (v < 0 or v > 150):
            raise ValueError('年龄必须在0-150之间')
        return v

class SymptomValidator(BaseModel):
    symptom_text: str = Field(..., min_length=1, max_length=2000)
    
    @field_validator('symptom_text')
    @classmethod
    def validate_symptom_text(cls, v):
        if not v or not v.strip():
            raise ValueError('症状描述不能为空')
        dangerous_patterns = ['自杀', '自残', '他杀']
        for pattern in dangerous_patterns:
            if pattern in v:
                raise ValueError('检测到需要专业心理干预的内容，请拨打心理援助热线')
        return v

def validate_phone_number(phone: str) -> bool:
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_id_card(id_card: str) -> bool:
    pattern = r'^\d{17}[\dXx]$'
    return bool(re.match(pattern, id_card))
