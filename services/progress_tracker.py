"""
进度更新服务类
"""
import json
from typing import List, Dict
from models.base_model import BaseModel
from models.deepseek_model import DeepseekModel


class ProgressTracker:
    """
    进度更新服务类，用于分析和跟踪招聘进度
    """
    
    def __init__(self, model: BaseModel = None):
        self.model = model if model else DeepseekModel()
        self._init_prompt_template()
    
    def _init_prompt_template(self) -> None:
        """
        初始化提示词模板
        """
        self.prompt_template = """你是一个专业的招聘进度分析助手。请根据以下规则分析邮件信息并输出结果：

任务：分析求职者的各公司投递进度

分析规则：
1. 将邮件按公司分类，并判断每个公司的最新进度
2. 进度状态分类：
   - 已投递：包含"投递成功"、"已收到"、"感谢投递"等关键词
   - 笔试(测评)中：包含"笔试"、"测评"、"考试"等关键词
   - 面试中：包含"面试"、"AI面试"等关键词
   - 已录取：包含"offer"、"录用"等关键词
   - 已拒绝：包含"面试反馈"、"很遗憾"等关键词

3. 进度判断原则：
   - 以最新的邮件状态为准（参考邮件日期）
   - 如果同一公司有多封邮件，选择代表最深入阶段的状态
   - 面试反馈问卷通常意味着已被拒绝

注意事项：
1. 同一公司的不同部门视为不同公司（如阿里云和阿里巴巴）
2. 进度状态必须为以上5种之一
3. 需要考虑邮件时序，确保返回最新进度

请以固定的JSON格式返回分析结果，格式如下：
{
    "result": [
        {
            "公司": "公司名称1",
            "最新进度": "当前进度状态",
            "日期": "最新状态对应的日期"
        },
        {
            "公司": "公司名称2",
            "最新进度": "当前进度状态",
            "日期": "最新状态对应的日期"
        }
        // ... 其他公司
    ]
}

注意：
1. 返回格式必须是包含companies数组的对象
2. 数组中每个元素都必须包含"公司"、"最新进度"、"日期"三个字段
3. 按照日期从新到旧排序"""
    
    def analyze_progress(self, email_list: List[Dict]) -> Dict:
        """
        分析招聘进度
        
        Args:
            email_list: 邮件列表
            
        Returns:
            Dict: 分析结果，包含各公司的最新进度
        """
        # 构建邮件数据字符串
        simplified_emails = []
        for email in email_list:
            simplified_email = (
                f"主题: {email['subject']}\n"
                f"日期: {email['date']}\n"
                f"内容: {email['content']}\n"
            )
            simplified_emails.append(simplified_email)

        email_data_str = "\n".join(simplified_emails)

        try:
            # 构建完整的提示词
            messages = [
                {"role": "system", "content": self.prompt_template},
                {"role": "user", "content": f"邮件列表：\n{email_data_str}\n\n请分析以上邮件并返回JSON格式的进度状态。"}
            ]

            # 调用API
            response = self.model.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.1,
                max_tokens=2048
            )

            # 提取返回的内容
            response_text = response.choices[0].message.content

            # 解析JSON
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                result = {"error": "无法解析返回的JSON数据"}

        except Exception as e:
            result = {"error": f"发生错误: {str(e)}"}

        return result