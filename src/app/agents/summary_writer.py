from langchain_core.prompts import ChatPromptTemplate
from app.utils.llm import get_llm_client

class SummaryWriter:
    def __init__(self):
        self.llm = get_llm_client()
    
    def generate_summary(self, consultation_data: dict) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个医疗记录专员，负责将问诊对话整理成结构化的摘要报告。

请根据提供的问诊信息，生成一份专业的问诊摘要，包含：
1. 患者基本信息
2. 主诉
3. 症状描述
4. 风险评估结果
5. 医学建议
6. 后续行动建议

格式要求：
- 使用清晰的标题分隔
- 关键信息用加粗标注
- 语言简洁专业
"""),
            ("human", """
问诊数据：
{consultation_data}

请生成问诊摘要：
""")
        ])
        
        response = self.llm.invoke(prompt.format(
            consultation_data=str(consultation_data)
        ))
        
        return response.content
    
    def generate_followup_reminder(self, consultation_data: dict) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个医疗助手，负责生成后续随访提醒。"),
            ("human", "基于以下问诊信息，生成随访提醒：\n{consultation_data}")
        ])
        
        response = self.llm.invoke(prompt.format(
            consultation_data=str(consultation_data)
        ))
        
        return response.content
