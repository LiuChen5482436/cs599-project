from langchain_core.prompts import ChatPromptTemplate
from app.utils.llm import get_llm_client

class AdviceGenerator:
    def __init__(self):
        self.llm = get_llm_client()
    
    def generate_advice(self, user_info: dict, rag_context: list, risk_level: str) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的医疗健康顾问，负责为用户提供综合的就医建议和健康指导。

原则：
1. 不给出确定诊断，只描述可能的情况
2. 不直接开处方药
3. 基于提供的医学知识提供建议
4. 提醒用户最终需咨询专业医生
5. 建议要具体、可操作

请根据以下信息生成全面的建议报告："""),
            ("human", """
用户信息：
- 年龄：{age}
- 症状：{symptoms}
- 病史：{medical_history}
- 用药情况：{medication}

医学知识库参考：
{medical_context}

风险等级：{risk_level}

请生成一份包含以下内容的建议报告：
1. 初步分析
2. 就医建议
3. 注意事项
4. 观察指标（哪些症状出现时需立即就医）
""")
        ])
        
        response = self.llm.invoke(prompt.format(
            age=user_info.get("age", "未提供"),
            symptoms=user_info.get("symptoms", "未提供"),
            medical_history=user_info.get("medical_history", "无"),
            medication=user_info.get("medication", "无"),
            medical_context="\n\n".join(rag_context) if rag_context else "无相关医学知识",
            risk_level=risk_level
        ))
        
        return response.content
