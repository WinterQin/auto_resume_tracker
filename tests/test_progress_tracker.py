"""
进度跟踪服务测试
"""
import unittest
from services.progress_tracker import ProgressTracker
from models.deepseek_model import DeepseekModel


class TestProgressTracker(unittest.TestCase):
    """
    测试进度跟踪功能
    """
    
    def setUp(self):
        """
        测试前准备
        """
        self.model = DeepseekModel()
        self.tracker = ProgressTracker(model=self.model)
    
    def test_analyze_progress(self):
        """
        测试进度分析功能
        """
        # 测试邮件列表
        test_emails = [
            {
                'subject': '【美团】笔试通知',
                'content': '邀请您参加笔试，时间：2024-03-25',
                'date': '2024-03-20',
                'from': 'test@meituan.com'
            },
            {
                'subject': '【字节跳动】简历投递成功',
                'content': '感谢投递字节跳动，我们会尽快处理',
                'date': '2024-03-19',
                'from': 'test@bytedance.com'
            },
            {
                'subject': '【阿里巴巴】面试通知',
                'content': '恭喜通过简历筛选，邀请您参加面试',
                'date': '2024-03-21',
                'from': 'test@alibaba.com'
            }
        ]
        
        # 执行进度分析
        result = self.tracker.analyze_progress(test_emails)
        
        # 验证结果格式
        self.assertIsInstance(result, dict)
        self.assertIn('result', result)
        self.assertIsInstance(result['result'], list)
        
        # 验证分析结果
        companies = result['result']
        self.assertEqual(len(companies), 3)
        
        # 验证每个公司的进度信息
        for company in companies:
            self.assertIn('公司', company)
            self.assertIn('最新进度', company)
            self.assertIn('日期', company)
            
            # 验证进度状态是否符合预期
            status = company['最新进度']
            self.assertIn(status, ['已投递', '笔试(测评)中', '面试中', '已录取', '已拒绝'])
    
    def test_analyze_progress_with_multiple_stages(self):
        """
        测试多阶段进度分析
        """
        # 测试同一公司多个阶段的邮件
        test_emails = [
            {
                'subject': '【阿里巴巴】简历投递成功',
                'content': '感谢投递阿里巴巴',
                'date': '2024-03-15',
                'from': 'test@alibaba.com'
            },
            {
                'subject': '【阿里巴巴】笔试通知',
                'content': '邀请参加笔试',
                'date': '2024-03-17',
                'from': 'test@alibaba.com'
            },
            {
                'subject': '【阿里巴巴】面试通知',
                'content': '恭喜通过笔试，邀请面试',
                'date': '2024-03-20',
                'from': 'test@alibaba.com'
            }
        ]
        
        # 执行进度分析
        result = self.tracker.analyze_progress(test_emails)
        
        # 验证结果
        companies = result['result']
        self.assertEqual(len(companies), 1)  # 应该只有一个公司
        
        company = companies[0]
        self.assertEqual(company['公司'], '阿里巴巴')
        self.assertEqual(company['最新进度'], '面试中')  # 应该显示最新的进度
        self.assertEqual(company['日期'], '2024-03-20')  # 应该是最新邮件的日期


if __name__ == '__main__':
    unittest.main()
