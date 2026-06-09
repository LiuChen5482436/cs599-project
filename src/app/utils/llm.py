from langchain_openai import ChatOpenAI
from app.utils.config import Config

def get_llm_client(model_name: str = "qwen-max", temperature: float = 0.1):
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=Config.DASHSCOPE_API_KEY,
        base_url=Config.DASHSCOPE_API_URL
    )
