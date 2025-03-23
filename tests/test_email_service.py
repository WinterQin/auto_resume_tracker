"""
邮件服务测试
"""
import unittest
from services.email_service import EmailService


class TestEmailService(unittest.TestCase):
    """
    测试邮件服务功能
    """
    
    def setUp(self):
        """
        测试前准备
        """
        self.email_service = EmailService()
    
    def tearDown(self):
        """
        测试后清理
        """
        self.email_service.close()
    
    def test_read_emails(self):
        """
        测试读取邮件功能
        """
        # 测试读取最新的5封邮件
        emails = self.email_service.read_emails(limit=5)
        
        # 验证返回结果
        self.assertIsInstance(emails, list)
        self.assertLessEqual(len(emails), 5)
        
        # 验证邮件格式
        if emails:
            email = emails[0]
            print(email)
            self.assertIn('subject', email)
            self.assertIn('from', email)
            self.assertIn('date', email)
            self.assertIn('content', email)



if __name__ == '__main__':
    unittest.main() 