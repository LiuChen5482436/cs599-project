import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
    DASHSCOPE_API_URL = os.getenv("DASHSCOPE_API_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    DASHSCOPE_EMBEDDING_URL = "https://dashscope.aliyuncs.com/api/text/embedding"
    
    CHROMA_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/chroma_db"))
    KNOWLEDGE_BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/knowledge_base"))
    
    RED_FLAG_SYMPTOMS = [
        "胸痛", "胸闷", "呼吸困难", "心跳加速",
        "头晕", "晕厥", "意识模糊", "剧烈头痛",
        "呕血", "黑便", "持续呕吐",
        "高热", "抽搐", "肢体麻木", "言语不清",
        "严重创伤", "大量出血", "窒息"
    ]
    
    SPECIAL_POPULATIONS = {
        "儿童": {"age_range": (0, 12), "multiplier": 1.5},
        "孕妇": {"multiplier": 1.5},
        "老年人": {"age_range": (65, float('inf')), "multiplier": 1.3},
        "免疫低下者": {"multiplier": 1.4}
    }
    
    RISK_LEVELS = {
        "A": {"name": "急诊", "description": "需立即就医"},
        "B": {"name": "尽快就医", "description": "24小时内就诊"},
        "C": {"name": "门诊", "description": "1-3天内就诊"},
        "D": {"name": "居家观察", "description": "可居家护理"}
    }
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../logs/medical_agent.log"))
