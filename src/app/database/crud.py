from sqlalchemy.orm import Session
from app.database.models import User, Consultation, Message, Feedback, ConsultationStatus, RiskLevel
from datetime import datetime
from typing import Optional, List

def get_or_create_user(db: Session, session_id: str) -> User:
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        user = User(session_id=session_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def create_consultation(db: Session, user_id: int, chief_complaint: str = None) -> Consultation:
    consultation = Consultation(
        user_id=user_id,
        chief_complaint=chief_complaint,
        status=ConsultationStatus.IN_PROGRESS
    )
    db.add(consultation)
    db.commit()
    db.refresh(consultation)
    return consultation

def add_message(db: Session, consultation_id: int, role: str, content: str) -> Message:
    message = Message(
        consultation_id=consultation_id,
        role=role,
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def update_consultation(
    db: Session,
    consultation_id: int,
    risk_level: Optional[RiskLevel] = None,
    medical_advice: Optional[str] = None,
    red_flags_detected: Optional[bool] = None,
    red_flags_content: Optional[str] = None,
    followup_questions: Optional[str] = None,
    initial_symptoms: Optional[str] = None
) -> Consultation:
    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
    if consultation:
        if risk_level is not None:
            consultation.risk_level = risk_level
        if medical_advice is not None:
            consultation.medical_advice = medical_advice
        if red_flags_detected is not None:
            consultation.red_flags_detected = red_flags_detected
        if red_flags_content is not None:
            consultation.red_flags_content = red_flags_content
        if followup_questions is not None:
            consultation.followup_questions = followup_questions
        if initial_symptoms is not None:
            consultation.initial_symptoms = initial_symptoms
        consultation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(consultation)
    return consultation

def complete_consultation(db: Session, consultation_id: int) -> Consultation:
    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
    if consultation:
        consultation.status = ConsultationStatus.COMPLETED
        consultation.completed_at = datetime.utcnow()
        consultation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(consultation)
    return consultation

def add_feedback(db: Session, consultation_id: int, rating: int, comment: str = None) -> Feedback:
    feedback = Feedback(
        consultation_id=consultation_id,
        rating=rating,
        comment=comment
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback

def get_consultation_messages(db: Session, consultation_id: int) -> List[Message]:
    return db.query(Message).filter(Message.consultation_id == consultation_id).order_by(Message.created_at).all()

def get_user_consultations(db: Session, user_id: int) -> List[Consultation]:
    return db.query(Consultation).filter(Consultation.user_id == user_id).order_by(Consultation.created_at.desc()).all()
