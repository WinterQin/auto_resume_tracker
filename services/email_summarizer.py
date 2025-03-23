"""
邮件简化服务类
"""
from models.base_model import BaseModel
from models.ollama_model import OllamaModel


class EmailSummarizer:
    """
    邮件简化服务类，用于简化邮件内容
    """

    def __init__(self, model: BaseModel = None):
        self.model = model if model else OllamaModel()
        self._init_prompt_template()

    def _init_prompt_template(self) -> None:
        """
        初始化提示词模板
        """
        self.prompt_template = """你是一个邮件内容精简助手。请帮我将招聘相关邮件内容精简，遵循以下规则：

1. 只保留以下关键信息：
   - 招聘流程的当前阶段（如：简历筛选、笔试通知、面试通知等）
   - 必要的时间信息（如截止时间、考试时间等）
   - 关键的后续步骤说明

2. 去除以下内容：
   - 冗长的注意事项说明
   - 重复的提醒内容
   - 公司介绍和宣传内容
   - 系统操作指导
   - 技术支持信息
   - 邮件免责声明

3. 输出格式要求：
   将内容压缩至1-2句话，使用简洁的语言概括主要信息。
   格式：[公司名称] - [当前阶段] - [关键时间信息]（如有）- [必要的后续步骤]

请按照上述规则精简以下邮件内容：
{email_content}"""

    def summarize_email(self, email_content: str) -> str:
        """
        简化单个邮件内容
        
        Args:
            email_content: 原始邮件内容
            
        Returns:
            str: 简化后的邮件内容
        """
        prompt = self.prompt_template.format(email_content=email_content)
        return self.model.generate(prompt)

