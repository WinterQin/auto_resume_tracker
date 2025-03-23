"""
本地调用接口
"""
from typing import List, Dict, Optional
from .services.email_service import EmailService
from .services.email_summarizer import EmailSummarizer
from .services.progress_tracker import ProgressTracker


class RecruitmentClient:
    """
    招聘邮件分析客户端
    """
    
    def __init__(self):
        self.email_service = EmailService()
        self.email_summarizer = EmailSummarizer()
        self.progress_tracker = ProgressTracker()
    
    def read_emails(self, folder: str = 'INBOX', limit: int = 10) -> List[Dict]:
        """
        读取邮件
        
        Args:
            folder: 邮件文件夹
            limit: 读取邮件数量限制
            
        Returns:
            List[Dict]: 邮件列表
        """
        return self.email_service.read_emails(folder, limit)
    
    def summarize_emails(self, emails: Optional[List[Dict]] = None, 
                        folder: str = 'INBOX', limit: int = 10) -> List[Dict]:
        """
        简化邮件内容
        
        Args:
            emails: 邮件列表，如果为None则会先读取邮件
            folder: 邮件文件夹
            limit: 读取邮件数量限制
            
        Returns:
            List[Dict]: 简化后的邮件列表
        """
        if emails is None:
            emails = self.read_emails(folder, limit)
        return self.email_summarizer.batch_summarize_emails(emails)
    
    def analyze_progress(self, emails: Optional[List[Dict]] = None,
                        folder: str = 'INBOX', limit: int = 10) -> Dict:
        """
        分析招聘进度
        
        Args:
            emails: 邮件列表，如果为None则会先读取邮件
            folder: 邮件文件夹
            limit: 读取邮件数量限制
            
        Returns:
            Dict: 分析结果
        """
        if emails is None:
            emails = self.read_emails(folder, limit)
        return self.progress_tracker.analyze_progress(emails)
    
    def close(self) -> None:
        """
        关闭连接
        """
        self.email_service.close()


# 使用示例
if __name__ == "__main__":
    client = RecruitmentClient()
    
    try:
        # 读取邮件
        print("读取邮件...")
        emails = client.read_emails(limit=5)
        print(f"读取到 {len(emails)} 封邮件\n")
        
        # 简化邮件
        print("简化邮件内容...")
        summarized = client.summarize_emails(emails)
        for email in summarized:
            print(f"主题: {email['subject']}")
            print(f"简化内容: {email['content']}\n")
        
        # 分析进度
        print("分析招聘进度...")
        progress = client.analyze_progress(emails)
        print("进度分析结果:")
        print(progress)
        
    finally:
        client.close() 