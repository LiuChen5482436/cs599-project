from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class RiskLevel(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

class ConsultationStatus(enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), unique=True, index=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    medical_history = Column(Text, nullable=True)
    medication = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    consultations = relationship("Consultation", back_populates="user")

class Consultation(Base):
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(ConsultationStatus), default=ConsultationStatus.IN_PROGRESS)
    risk_level = Column(Enum(RiskLevel), nullable=True)
    chief_complaint = Column(Text, nullable=True)
    initial_symptoms = Column(Text, nullable=True)
    followup_questions = Column(Text, nullable=True)
    medical_advice = Column(Text, nullable=True)
    red_flags_detected = Column(Boolean, default=False)
    red_flags_content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="consultations")
    messages = relationship("Message", back_populates="consultation")
    feedback = relationship("Feedback", back_populates="consultation", uselist=False)

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id"))
    role = Column(String(20))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    consultation = relationship("Consultation", back_populates="messages")

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id"), unique=True)
    rating = Column(Integer)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    consultation = relationship("Consultation", back_populates="feedback")
