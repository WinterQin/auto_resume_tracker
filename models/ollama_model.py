"""
Ollama模型实现
"""
from typing import List
from langchain_ollama import OllamaLLM
from .base_model import BaseModel
from config.config import LLM_CONFIG


class OllamaModel(BaseModel):
    """
    Ollama模型实现类
    """
    
    def __init__(self):
        self.llm = None
        self.config = LLM_CONFIG['OLLAMA']
    
    def initialize(self) -> None:
        """
        初始化Ollama模型
        """
        self.llm = OllamaLLM(
            base_url=self.config['BASE_URL'],
            model=self.config['MODEL'],
            temperature=0.1
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
        if not self.llm:
            self.initialize()
        
        response = self.llm.invoke(prompt)
        return response
    
    def batch_generate(self, prompts: List[str], **kwargs) -> List[str]:
        """
        批量生成回复
        
        Args:
            prompts: 提示词列表
            **kwargs: 其他参数
            
        Returns:
            List[str]: 模型生成的回复列表
        """
        if not self.llm:
            self.initialize()
        
        responses = []
        for prompt in prompts:
            response = self.generate(prompt, **kwargs)
            responses.append(response)
        
        return responses 