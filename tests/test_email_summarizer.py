"""
邮件简化服务测试
"""
import unittest
from services.email_summarizer import EmailSummarizer
from models.ollama_model import OllamaModel


class TestEmailSummarizer(unittest.TestCase):
    """
    测试邮件简化功能
    """
    
    def setUp(self):
        """
        测试前准备
        """
        self.model = OllamaModel()
        self.summarizer = EmailSummarizer(model=self.model)
    
    def test_summarize_email(self):
        """
        测试单个邮件简化
        """
        # 测试邮件内容
        test_email = """
""\n""""\n""\n""\n校招在线测评通知候选人邮件模板\n""\n""\n""\n""\n""\n""""\n""""""\n""\n""""""\n""""""\n""\n""""""\n""""""""\n""\n""\n""""""""\n""\n""\n""""""""\n""""""\n""""""\n""""""\n""""""\n""\n""\n秦文涛：\n""""""\n""""""""\n""""""\n""""""\n""\n""""\n您好！\n欢迎参加蚂蚁集团届转正实习笔试测评，请在面试前完成。\n""测评入口：\n""，与您的信息绑定，请勿转发给他人。\n""测评时长：分钟左右\n""测评截止日期：请在2025-03-25之前完成\n""""""\n""""""""\n""""""\n""""""\n""\n""""\n""【特别说明】\n""\n本次测评为素质类测评，是简历评估时重要参考维度之一，请亲务必在失效前按照个人真实情况完成作答。\n""【注意事项】\n请在没有外界干扰的环境下进行答题，关闭下载工具和等通讯软件，确保网络连接畅通，网速应在以上。\n如遇突发情况，如断网、长时间接听电话、电脑死机、断电等，请关闭浏览器或计算机。当可以作答时，再次使用您的通行证和邮箱重新登录，即可继续作答。\n答题过程中，如有无法登录、无法按照合适版本的浏览器等操作性问题，请联系校招官网页面右侧的蚂小招。\n本次考试系统自动限制跳出页面，如同学跳出次数超出限制次数，则无法继续作答，请务必关闭其他任何页面及聊天工具，始终保持在作答页面。\n""""""\n""""""""\n""""""\n""""""\n""\n""""\n声明\n本邮件含有保密信息，仅限于收件人所用。禁止任何人未经发件人许可以任何形式（包括但不限于部分地泄露、复制或散发）不当地使用本邮件中的信息。如果您错收了本邮件，请您立即电话或邮件通知发件人并删除本邮件，谢谢！\n""""""\n""""""""\n""""""\n""""""\n""\n""此邮件由系统自动发出，请勿直接回复，谢谢！\n""""\n""\n""蚂蚁集团校园招聘组\n""""\n""""""'


        """
        
        # 执行简化
        result = self.summarizer.summarize_email(test_email)
        
        # 验证结果
        self.assertIsInstance(result, str)
        self.assertIn('蚂蚁', result)
        self.assertIn('笔试', result)
        self.assertIn('2025-03-25', result)



if __name__ == '__main__':
    unittest.main() 