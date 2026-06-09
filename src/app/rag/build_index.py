import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from langchain_chroma import Chroma
from langchain_text_splitters import MarkdownTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from app.utils.config import Config
import dashscope

def build_index():
    print("初始化嵌入模型...")
    dashscope.api_key = Config.DASHSCOPE_API_KEY
    embeddings = DashScopeEmbeddings(model="text-embedding-v1")

    print(f"初始化Chroma数据库，路径: {Config.CHROMA_DB_PATH}")
    os.makedirs(Config.CHROMA_DB_PATH, exist_ok=True)
    db = Chroma(persist_directory=Config.CHROMA_DB_PATH, embedding_function=embeddings)

    docs_path = os.path.join(os.path.dirname(__file__), "medical_docs")

    if not os.path.exists(docs_path):
        print(f"医学文档目录不存在: {docs_path}")
        return

    print(f"读取医学文档...")
    texts = []
    for filename in os.listdir(docs_path):
        if filename.endswith(".md"):
            filepath = os.path.join(docs_path, filename)
            print(f"  - 读取 {filename}")
            with open(filepath, "r", encoding="utf-8") as f:
                texts.append(f.read())

    if not texts:
        print("未找到任何医学文档")
        return

    print(f"分割文本为 {len(texts)} 个文档...")
    text_splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text("\n\n".join(texts))
    print(f"生成了 {len(chunks)} 个文本块")

    existing_count = db._collection.count()
    if existing_count > 0:
        print(f"数据库已包含 {existing_count} 个文档，是否重新构建？(y/n)")
        response = input()
        if response.lower() != 'y':
            print("跳过索引构建")
            return
        print("清空现有索引...")
        db.delete_collection()
        db = Chroma(persist_directory=Config.CHROMA_DB_PATH, embedding_function=embeddings)

    print("添加文档到向量数据库...")
    db.add_texts(chunks)
    print(f"索引构建完成！共 {db._collection.count()} 个文档")

if __name__ == "__main__":
    build_index()
