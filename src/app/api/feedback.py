from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import FeedbackRequest, FeedbackResponse
from app.database.session import get_db
from app.database import crud
from app.utils.logger import setup_logger

router = APIRouter(prefix="/feedback", tags=["feedback"])
logger = setup_logger(__name__)

@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    logger.info(f"Feedback for consultation: {request.consultation_id}")
    
    consultation = db.query(crud.Consultation).filter(
        crud.Consultation.id == request.consultation_id
    ).first()
    
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    
    existing_feedback = db.query(crud.Feedback).filter(
        crud.Feedback.consultation_id == request.consultation_id
    ).first()
    
    if existing_feedback:
        raise HTTPException(status_code=400, detail="Feedback already submitted")
    
    feedback = crud.add_feedback(
        db,
        request.consultation_id,
        request.rating,
        request.comment
    )
    
    return FeedbackResponse(
        success=True,
        message="反馈提交成功，感谢您的反馈！"
    )

@router.get("/{consultation_id}")
async def get_feedback(consultation_id: int, db: Session = Depends(get_db)):
    feedback = db.query(crud.Feedback).filter(
        crud.Feedback.consultation_id == consultation_id
    ).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    return {
        "consultation_id": feedback.consultation_id,
        "rating": feedback.rating,
        "comment": feedback.comment,
        "created_at": feedback.created_at.isoformat()
    }
