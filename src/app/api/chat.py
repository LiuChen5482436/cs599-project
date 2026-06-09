from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import ChatRequest, ChatResponse
from app.schemas.consultation import MessageResponse
from app.database.session import get_db
from app.database import crud
from app.agents.orchestrator import Orchestrator
from app.utils.logger import setup_logger
from typing import List

router = APIRouter(prefix="/chat", tags=["chat"])
logger = setup_logger(__name__)
orchestrator = Orchestrator()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    logger.info(f"Chat request for session: {request.session_id}")
    
    user = crud.get_or_create_user(db, request.session_id)
    
    if request.user_info:
        if request.user_info.age:
            user.age = request.user_info.age
        if request.user_info.gender:
            user.gender = request.user_info.gender
        if request.user_info.medical_history:
            user.medical_history = request.user_info.medical_history
        if request.user_info.medication:
            user.medication = request.user_info.medication
        if request.user_info.allergies:
            user.allergies = request.user_info.allergies
        db.commit()
    
    consultations = crud.get_user_consultations(db, user.id)
    consultation = consultations[0] if consultations else None
    
    if not consultation:
        consultation = crud.create_consultation(db, user.id, request.message)
    else:
        crud.add_message(db, consultation.id, "user", request.message)
    
    user_info_dict = {
        "age": user.age,
        "gender": user.gender,
        "medical_history": user.medical_history,
        "medication": user.medication,
        "allergies": user.allergies,
        "conversation_history": [
            {"content": msg.content}
            for msg in crud.get_consultation_messages(db, consultation.id)
        ]
    }
    
    if request.user_info:
        user_info_dict.update(request.user_info.model_dump())
    
    result = await orchestrator.process_message(
        request.message,
        user_info_dict,
        consultation.id
    )
    
    crud.add_message(db, consultation.id, "assistant", result["response"])
    
    if result.get("risk_report"):
        crud.update_consultation(
            db, consultation.id,
            risk_level=result["risk_report"]["risk_level"],
            medical_advice=result["response"]
        )
    
    return ChatResponse(
        response=result["response"],
        consultation_id=consultation.id,
        is_complete=result.get("is_complete", False),
        needs_followup=result.get("needs_followup", False),
        followup_question=result.get("followup_question")
    )

@router.get("/history/{session_id}", response_model=List[MessageResponse])
async def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    user = crud.get_or_create_user(db, session_id)
    consultations = crud.get_user_consultations(db, user.id)
    
    if not consultations:
        return []
    
    messages = crud.get_consultation_messages(db, consultations[0].id)
    return [
        MessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at
        )
        for msg in messages
    ]
