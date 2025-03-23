"""
Deepseek模型实现
"""
from typing import List
from openai import OpenAI
from .base_model import BaseModel
from config.config import LLM_CONFIG


class DeepseekModel(BaseModel):
    """
    Deepseek模型实现类
    """
    
    def __init__(self):
        self.client = None
        self.config = LLM_CONFIG['DEEPSEEK']
        self.initialize()
    
    def initialize(self) -> None:
        """
        初始化Deepseek模型
        """
        self.client = OpenAI(
            api_key=self.config['API_KEY'],
            base_url=self.config['BASE_URL']
        )
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        生成回复
        
        Args:
            prompt: 提示词
            **kwargs: 其他参数
            
        Returns:
            str: 模型生成的回复
        """
        if not self.client:
            self.initialize()
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.chat.completions.create(
            model=self.config['MODEL'],
            messages=messages,
            temperature=0.1,
            max_tokens=1024
        )
        
        return response.choices[0].message.content

    def batch_generate(self, prompts: List[str], **kwargs) -> List[str]:
        """
        批量生成回复

        Args:
            prompts: 提示词列表
            **kwargs: 其他参数

        Returns:
            List[str]: 模型生成的回复列表
        """
        pass 
