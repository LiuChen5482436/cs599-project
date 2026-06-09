from langchain_core.prompts import ChatPromptTemplate
from app.utils.llm import get_llm_client

class FollowupAgent:
    def __init__(self):
        self.llm = get_llm_client()
        self.required_fields = ["症状", "部位", "持续时间", "严重程度", "伴随症状"]
        self.field_keywords = {
            "症状": ["症状", "痛", "疼", "咳", "发热", "发烧", "腹泻", "呕吐", "头晕", "不舒服"],
            "部位": ["部位", "头", "胸", "腹", "胃", "喉", "咽", "腰", "背", "腿", "手", "眼"],
            "持续时间": ["持续", "时间", "天", "小时", "分钟", "周", "月", "昨天", "今天", "刚才"],
            "严重程度": ["严重", "轻微", "剧烈", "明显", "一点", "很", "非常", "难忍"],
            "伴随症状": ["伴随", "同时", "还", "并且", "恶心", "乏力", "咳痰", "流鼻涕", "胸闷"],
        }
    
    def generate_followup_question(self, missing_fields: list[str], conversation_context: str = "") -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个友好的医疗问诊助手，负责在用户描述不完整时追问缺失的关键信息。
请针对以下缺失的字段生成一个自然、友好的追问问题：
- 使用温和的语气
- 一次只问1-2个最重要的问题
- 问题要具体且易于回答"""),
            ("human", """缺失字段：{missing_fields}

对话历史：
{context}

请生成追问问题：""")
        ])
        
        response = self.llm.invoke(prompt.format(
            missing_fields=", ".join(missing_fields),
            context=conversation_context or "暂无历史对话"
        ))
        
        return response.content
    
    def identify_missing_fields(self, conversation_history: list) -> list[str]:
        missing = []
        
        full_text = "\n".join([
            msg.get("content", "") for msg in conversation_history
        ])
        
        for field in self.required_fields:
            keywords = self.field_keywords.get(field, [field])
            if not any(keyword in full_text for keyword in keywords):
                missing.append(field)
        
        return missing
