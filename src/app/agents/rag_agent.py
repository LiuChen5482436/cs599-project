import os
import dashscope
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from app.utils.config import Config
from app.utils.llm import get_llm_client

class RAGAgent:
    def __init__(self):
        self.llm = get_llm_client()
        dashscope.api_key = Config.DASHSCOPE_API_KEY
        self.embeddings = DashScopeEmbeddings(model="text-embedding-v1")
        self.db = self._init_chroma()
        self._ensure_knowledge_base()

    def _init_chroma(self):
        os.makedirs(Config.CHROMA_DB_PATH, exist_ok=True)
        return Chroma(
            persist_directory=Config.CHROMA_DB_PATH,
            embedding_function=self.embeddings
        )

    def _ensure_knowledge_base(self):
        os.makedirs(Config.KNOWLEDGE_BASE_PATH, exist_ok=True)

        docs_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "rag", "medical_docs")
        )
        if os.path.exists(docs_path):
            texts = []
            for filename in os.listdir(docs_path):
                if filename.endswith(".md"):
                    filepath = os.path.join(docs_path, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        texts.append(f.read())

            if texts and self.db._collection.count() == 0:
                text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                chunks = text_splitter.split_text("\n\n".join(texts))
                self.db.add_texts(chunks)

    def retrieve(self, query: str, k: int = 3) -> list[str]:
        results = self.db.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

    def add_document(self, content: str, metadata: dict = None):
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_text(content)
        self.db.add_texts(chunks)

    def generate_response(self, query: str, context: list[str]) -> str:
        prompt = f"""基于以下医学知识，为用户问题提供专业建议：

医学知识：
{chr(10).join(context)}

用户问题：{query}

请提供专业的医疗建议（不作为诊断，仅供参考）：
"""
        response = self.llm.invoke(prompt)
        return response.content
