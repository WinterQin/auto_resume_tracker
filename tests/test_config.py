"""
配置文件测试
"""
import unittest
import os
from config.config import LLM_CONFIG, EMAIL_CONFIG, API_CONFIG


class TestConfig(unittest.TestCase):
    """
    测试配置文件加载
    """
    
    def test_llm_config_structure(self):
        """
        测试大语言模型配置结构
        """
        # 验证Deepseek配置
        self.assertIn('DEEPSEEK', LLM_CONFIG)
        deepseek_config = LLM_CONFIG['DEEPSEEK']
        self.assertIn('API_KEY', deepseek_config)
        self.assertIn('BASE_URL', deepseek_config)
        self.assertIn('MODEL', deepseek_config)
        
        # 验证Ollama配置
        self.assertIn('OLLAMA', LLM_CONFIG)
        ollama_config = LLM_CONFIG['OLLAMA']
        self.assertIn('BASE_URL', ollama_config)
        self.assertIn('MODEL', ollama_config)
    
    def test_llm_config_values(self):
        """
        测试大语言模型配置值
        """
        # 验证Deepseek配置值
        deepseek_config = LLM_CONFIG['DEEPSEEK']
        self.assertIsInstance(deepseek_config['API_KEY'], str)
        self.assertTrue(deepseek_config['API_KEY'])  # 不应为空
        self.assertTrue(deepseek_config['BASE_URL'].startswith('http'))
        self.assertTrue(deepseek_config['MODEL'])
        
        # 验证Ollama配置值
        ollama_config = LLM_CONFIG['OLLAMA']
        self.assertTrue(ollama_config['BASE_URL'].startswith('http'))
        self.assertTrue(ollama_config['MODEL'])

    
    def test_email_config_values(self):
        """
        测试邮件配置值
        """
        # 验证服务器配置
        self.assertTrue(EMAIL_CONFIG['IMAP_SERVER'].endswith('.com'))
        self.assertTrue(EMAIL_CONFIG['SMTP_SERVER'].endswith('.com'))
        
        # 验证端口配置
        self.assertIsInstance(EMAIL_CONFIG['PORT'], int)
        self.assertGreater(EMAIL_CONFIG['PORT'], 0)
        
        # 验证邮箱配置
        self.assertIsInstance(EMAIL_CONFIG['EMAIL'], str)
        self.assertIn('@', EMAIL_CONFIG['EMAIL'])
        self.assertTrue(EMAIL_CONFIG['PASSWORD'])
        
        # 验证过滤配置
        filter_config = EMAIL_CONFIG['FILTER']
        self.assertIsInstance(filter_config['TARGET_FOLDER'], str)
    
    def test_api_config(self):
        """
        测试API配置
        """
        # 验证配置结构
        self.assertIn('HOST', API_CONFIG)
        self.assertIn('PORT', API_CONFIG)
        
        # 验证配置值
        self.assertIsInstance(API_CONFIG['PORT'], int)
        self.assertGreater(API_CONFIG['PORT'], 0)
        self.assertLess(API_CONFIG['PORT'], 65536)  # 有效端口范围
        
        self.assertIsInstance(API_CONFIG['HOST'], str)
        self.assertTrue(API_CONFIG['HOST'])  # 不应为空
    
    def test_config_environment_override(self):
        """
        测试环境变量覆盖配置
        """
        # 测试API密钥环境变量覆盖
        test_api_key = "test_api_key"
        os.environ['DEEPSEEK_API_KEY'] = test_api_key
        
        # 测试邮件过滤配置覆盖
        test_target_word = "test_job"
        os.environ['TARGET_FOLDER'] = test_target_word
        
        # 重新导入配置
        try:
            from importlib import reload
            from config import config
            reload(config)
            
            # 验证API密钥覆盖
            self.assertEqual(config.LLM_CONFIG['DEEPSEEK']['API_KEY'], test_api_key)
            
            # 验证邮件过滤配置覆盖
            self.assertEqual(config.EMAIL_CONFIG['FILTER']['TARGET_FOLDER'], test_target_word)
        finally:
            # 清理环境变量
            del os.environ['DEEPSEEK_API_KEY']
            del os.environ['TARGET_FOLDER']


if __name__ == '__main__':
    unittest.main() 