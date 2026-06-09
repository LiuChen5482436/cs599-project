import os
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
import dashscope
from app.utils.config import Config

class MedicalRetriever:
    def __init__(self):
        dashscope.api_key = Config.DASHSCOPE_API_KEY
        self.embeddings = DashScopeEmbeddings(model="text-embedding-v1")
        self.db = Chroma(
            persist_directory=Config.CHROMA_DB_PATH,
            embedding_function=self.embeddings
        )

    def retrieve(self, query: str, k: int = 3) -> list[dict]:
        results = self.db.similarity_search_with_relevance_scores(query, k=k)
        return [
            {"content": doc.page_content, "score": score}
            for doc, score in results
        ]

    def retrieve_by_category(self, query: str, category: str, k: int = 2) -> list[dict]:
        all_results = self.retrieve(query, k=k*2)
        return [r for r in all_results if category.lower() in r["content"].lower()][:k]

    def get_related_topics(self, query: str, k: int = 3) -> list[str]:
        results = self.retrieve(query, k=k)
        topics = []
        for r in results:
            lines = r["content"].split("\n")
            for line in lines:
                if line.startswith("#"):
                    topics.append(line.strip())
        return topics

def get_retriever() -> MedicalRetriever:
    return MedicalRetriever()
