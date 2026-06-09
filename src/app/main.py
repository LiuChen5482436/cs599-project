from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, triage, summary, feedback
from app.database.session import init_db
from app.utils.logger import setup_logger
import uvicorn

logger = setup_logger(__name__)

app = FastAPI(
    title="医疗智能体API",
    description="基于LLM的医疗问诊智能体系统",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(triage.router)
app.include_router(summary.router)
app.include_router(feedback.router)

@app.on_event("startup")
async def startup_event():
    logger.info("初始化数据库...")
    init_db()
    logger.info("医疗智能体API启动成功")

@app.get("/")
async def root():
    return {
        "message": "医疗智能体API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
