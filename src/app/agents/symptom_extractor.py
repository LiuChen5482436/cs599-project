from langchain_core.prompts import ChatPromptTemplate
from app.agents.safety_gate import SafetyGate
from app.utils.llm import get_llm_client

class SymptomExtractor:
    def __init__(self):
        self.llm = get_llm_client()
        self.safety_gate = SafetyGate()
        self.required_fields = ["症状", "部位", "持续时间", "严重程度", "伴随症状"]
    
    def extract_symptoms(self, user_input: str) -> dict:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个医疗症状提取专家，负责从用户描述中提取结构化的症状信息。
请提取以下信息：
1. 主要症状
2. 症状部位
3. 症状持续时间
4. 症状严重程度
5. 伴随症状
6. 可能的诱因

请以JSON格式输出。"""),
            ("human", "用户输入：{user_input}")
        ])
        
        response = self.llm.invoke(prompt.format(user_input=user_input))
        return {"extracted": response.content, "raw_input": user_input}
    
    def analyze_info_completeness(self, conversation_history: list) -> dict:
        analysis = {field: False for field in self.required_fields}
        full_text = "\n".join([msg.get("content", "") for msg in conversation_history])
        
        for field in self.required_fields:
            if field in full_text:
                analysis[field] = True
        
        return analysis
    
    def is_info_complete(self, conversation_history: list) -> bool:
        info_status = self.analyze_info_completeness(conversation_history)
        return all(info_status.values())
