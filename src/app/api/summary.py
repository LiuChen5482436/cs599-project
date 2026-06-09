from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.consultation import ConsultationResponse, ConsultationDetailResponse
from app.database.session import get_db
from app.database import crud
from app.agents.summary_writer import SummaryWriter
from app.utils.logger import setup_logger

router = APIRouter(prefix="/summary", tags=["summary"])
logger = setup_logger(__name__)
summary_writer = SummaryWriter()

@router.get("/{consultation_id}", response_model=dict)
async def get_summary(consultation_id: int, db: Session = Depends(get_db)):
    logger.info(f"Generating summary for consultation: {consultation_id}")
    
    consultation = db.query(crud.Consultation).filter(
        crud.Consultation.id == consultation_id
    ).first()
    
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    
    messages = crud.get_consultation_messages(db, consultation_id)
    
    consultation_data = {
        "consultation_id": consultation.id,
        "status": consultation.status.value,
        "risk_level": consultation.risk_level.value if consultation.risk_level else None,
        "chief_complaint": consultation.chief_complaint,
        "initial_symptoms": consultation.initial_symptoms,
        "messages": [
            {"role": msg.role, "content": msg.content, "created_at": msg.created_at.isoformat()}
            for msg in messages
        ],
        "created_at": consultation.created_at.isoformat(),
        "completed_at": consultation.completed_at.isoformat() if consultation.completed_at else None
    }
    
    summary = summary_writer.generate_summary(consultation_data)
    
    return {
        "consultation_id": consultation_id,
        "summary": summary,
        "consultation_data": consultation_data
    }

@router.get("/{consultation_id}/brief")
async def get_brief_summary(consultation_id: int, db: Session = Depends(get_db)):
    consultation = db.query(crud.Consultation).filter(
        crud.Consultation.id == consultation_id
    ).first()
    
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    
    return {
        "consultation_id": consultation_id,
        "risk_level": consultation.risk_level.value if consultation.risk_level else None,
        "status": consultation.status.value,
        "created_at": consultation.created_at.isoformat()
    }
