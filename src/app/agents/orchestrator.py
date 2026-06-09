from app.agents.safety_gate import SafetyGate
from app.agents.symptom_extractor import SymptomExtractor
from app.agents.followup_agent import FollowupAgent
from app.agents.risk_classifier import RiskClassifier
from app.agents.advice_generator import AdviceGenerator
from app.agents.summary_writer import SummaryWriter
from app.agents.rag_agent import RAGAgent
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class Orchestrator:
    def __init__(self):
        self.safety_gate = SafetyGate()
        self.symptom_extractor = SymptomExtractor()
        self.followup_agent = FollowupAgent()
        self.risk_classifier = RiskClassifier()
        self.advice_generator = AdviceGenerator()
        self.summary_writer = SummaryWriter()
        self.rag_agent = RAGAgent()
        logger.info("Orchestrator initialized")
    
    async def process_message(self, message: str, user_info: dict, consultation_id: int) -> dict:
        logger.info(f"Processing message for consultation {consultation_id}")
        
        has_red_flags, detected_flags = self.safety_gate.detect_red_flags(message)
        
        if has_red_flags:
            logger.warning(f"Red flags detected in consultation {consultation_id}: {detected_flags}")
            return {
                "response": self.safety_gate.get_emergency_response(detected_flags),
                "is_emergency": True,
                "detected_flags": detected_flags,
                "is_complete": True,
                "needs_followup": False
            }
        
        conversation_context = user_info.get("conversation_history", [])
        missing_fields = self.followup_agent.identify_missing_fields(conversation_context)
        
        if missing_fields:
            followup_question = self.followup_agent.generate_followup_question(
                missing_fields, 
                "\n".join([msg.get("content", "") for msg in conversation_context])
            )
            logger.info(f"Followup needed for consultation {consultation_id}, missing: {missing_fields}")
            return {
                "response": followup_question,
                "is_emergency": False,
                "is_complete": False,
                "needs_followup": True,
                "missing_fields": missing_fields
            }
        
        rag_context = self.rag_agent.retrieve(message)
        user_info["symptoms"] = message
        risk_report = self.risk_classifier.generate_risk_report(user_info)
        advice = self.advice_generator.generate_advice(user_info, rag_context, risk_report["risk_level"])
        
        response = f"📊 **风险评估：{risk_report['risk_name']}**\n\n"
        response += f"风险等级：{risk_report['risk_level']}\n"
        response += f"评估分数：{risk_report['score']:.1f}\n"
        response += f"风险因素：{', '.join(risk_report['factors'])}\n\n"
        response += f"💡 **健康建议**\n\n{advice}\n\n"
        response += f"\n⚠️ 本建议仅供参考，不能替代专业医生诊断"
        
        logger.info(f"Consultation {consultation_id} completed with risk level {risk_report['risk_level']}")
        
        return {
            "response": response,
            "is_emergency": False,
            "is_complete": True,
            "needs_followup": False,
            "risk_report": risk_report
        }
