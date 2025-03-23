"""
基础模型抽象类
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseModel(ABC):
    """
    大语言模型的基础抽象类
    """
    
    @abstractmethod
    def initialize(self) -> None:
        """
        初始化模型
        """
        pass
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        生成回复
        
        Args:
            prompt: 提示词
            **kwargs: 其他参数
            
        Returns:
            str: 模型生成的回复
        """
        pass
    
    @abstractmethod
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