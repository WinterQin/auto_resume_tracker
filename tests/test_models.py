"""
模型测试
"""
import unittest
from models.ollama_model import OllamaModel
from models.deepseek_model import DeepseekModel


class TestModels(unittest.TestCase):
    """
    测试大语言模型功能
    """
    
    def setUp(self):
        """
        测试前准备
        """
        self.ollama = OllamaModel()
        self.deepseek = DeepseekModel()
    
    def test_ollama_connection(self):
        """
        测试Ollama模型连接
        """
        try:
            self.ollama.initialize()
            self.assertIsNotNone(self.ollama.llm)
        except Exception as e:
            self.fail(f"Ollama模型初始化失败: {str(e)}")
    
    def test_deepseek_connection(self):
        """
        测试Deepseek模型连接
        """
        try:
            self.deepseek.initialize()
            self.assertIsNotNone(self.deepseek.client)
        except Exception as e:
            self.fail(f"Deepseek模型初始化失败: {str(e)}")
    
    def test_ollama_generation(self):
        """
        测试Ollama模型生成功能
        """
        test_prompt = "你好，这是一个测试。请回复：测试成功。"
        try:
            response = self.ollama.generate(test_prompt)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
        except Exception as e:
            self.fail(f"Ollama模型生成失败: {str(e)}")
    
    def test_deepseek_generation(self):
        """
        测试Deepseek模型生成功能
        """
        test_prompt = "你好，这是一个测试。请回复：测试成功。"
        try:
            response = self.deepseek.generate(test_prompt)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
        except Exception as e:
            self.fail(f"Deepseek模型生成失败: {str(e)}")
    
    def test_ollama_batch_generation(self):
        """
        测试Ollama模型批量生成功能
        """
        test_prompts = [
            "这是第一个测试",
            "这是第二个测试"
        ]
        try:
            responses = self.ollama.batch_generate(test_prompts)
            self.assertIsInstance(responses, list)
            self.assertEqual(len(responses), len(test_prompts))
            for response in responses:
                self.assertIsInstance(response, str)
                self.assertGreater(len(response), 0)
        except Exception as e:
            self.fail(f"Ollama模型批量生成失败: {str(e)}")
    
    def test_deepseek_batch_generation(self):
        """
        测试Deepseek模型批量生成功能
        """
        test_prompts = [
            "这是第一个测试",
            "这是第二个测试"
        ]
        try:
            responses = self.deepseek.batch_generate(test_prompts)
            self.assertIsInstance(responses, list)
            self.assertEqual(len(responses), len(test_prompts))
            for response in responses:
                self.assertIsInstance(response, str)
                self.assertGreater(len(response), 0)
        except Exception as e:
            self.fail(f"Deepseek模型批量生成失败: {str(e)}")


if __name__ == '__main__':
    unittest.main() 