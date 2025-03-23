"""
FastAPI接口
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from .services.email_service import EmailService
from .services.email_summarizer import EmailSummarizer
from .services.progress_tracker import ProgressTracker
from .config.config import API_CONFIG


# 定义请求模型
class EmailRequest(BaseModel):
    folder: str = 'INBOX'
    limit: int = 10


# 创建FastAPI应用
app = FastAPI(title="招聘邮件分析API")

# 创建服务实例
email_service = EmailService()
email_summarizer = EmailSummarizer()
progress_tracker = ProgressTracker()


@app.get("/")
async def root():
    """
    根路径，返回API信息
    """
    return {"message": "招聘邮件分析API服务"}


@app.post("/emails/read")
async def read_emails(request: EmailRequest) -> List[Dict]:
    """
    读取邮件
    """
    try:
        emails = email_service.read_emails(request.folder, request.limit)
        return emails
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/emails/summarize")
async def summarize_emails(request: EmailRequest) -> List[Dict]:
    """
    读取并简化邮件
    """
    try:
        emails = email_service.read_emails(request.folder, request.limit)
        summarized = email_summarizer.batch_summarize_emails(emails)
        return summarized
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/progress/analyze")
async def analyze_progress(request: EmailRequest) -> Dict:
    """
    分析招聘进度
    """
    try:
        emails = email_service.read_emails(request.folder, request.limit)
        progress = progress_tracker.analyze_progress(emails)
        return progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_api():
    """
    启动API服务
    """
    import uvicorn
    uvicorn.run(app, host=API_CONFIG['HOST'], port=API_CONFIG['PORT']) 