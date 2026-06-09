from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.risk import RiskAssessmentRequest, RiskAssessmentResponse, RedFlagDetectionResponse
from app.agents.safety_gate import SafetyGate
from app.agents.risk_classifier import RiskClassifier
from app.database.session import get_db
from app.utils.logger import setup_logger

router = APIRouter(prefix="/triage", tags=["triage"])
logger = setup_logger(__name__)

safety_gate = SafetyGate()
risk_classifier = RiskClassifier()

@router.post("/risk", response_model=RiskAssessmentResponse)
async def assess_risk(request: RiskAssessmentRequest, db: Session = Depends(get_db)):
    logger.info(f"Risk assessment request: {request.symptoms[:50]}...")
    
    user_info = {
        "symptoms": request.symptoms,
        "age": request.age,
        "medical_history": request.medical_history,
        "special_condition": request.special_condition,
        "temperature": request.temperature
    }
    
    risk_report = risk_classifier.generate_risk_report(user_info)
    
    return RiskAssessmentResponse(
        risk_level=risk_report["risk_level"],
        risk_name=risk_report["risk_name"],
        risk_description=risk_report["risk_description"],
        score=risk_report["score"],
        factors=risk_report["factors"],
        advice=risk_report["advice"]
    )

@router.post("/red-flags", response_model=RedFlagDetectionResponse)
async def detect_red_flags(request: dict, db: Session = Depends(get_db)):
    message = request.get("message", "")
    logger.info(f"Red flag detection for: {message[:50]}...")
    
    has_red_flags, detected_flags = safety_gate.detect_red_flags(message)
    
    response = RedFlagDetectionResponse(
        has_red_flags=has_red_flags,
        detected_flags=detected_flags
    )
    
    if has_red_flags:
        response.emergency_response = safety_gate.get_emergency_response(detected_flags)
    
    return response
