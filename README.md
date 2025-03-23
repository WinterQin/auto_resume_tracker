# Resume-Tracker 自动简历追踪系统

## 项目简介
Resume-Tracker 是一个智能化的求职进度追踪系统，专为实习季和工作季的求职者设计。系统能够自动读取和分析您邮箱中的求职相关邮件，帮助您实时掌握各个公司的招聘进度。

## 核心功能
- 📧 自动邮件读取：支持连接到您的邮箱并读取指定文件夹中的求职相关邮件
- 🤖 本地邮件总结：使用本地大语言模型对邮件内容进行智能总结，降低token消耗
- 📊 进度智能分析：利用在线大语言模型对求职进度进行深度分析
- ⚙️ 灵活配置：支持自定义邮箱服务器、文件夹、模型参数等配置

## 技术特点
- 采用本地模型进行邮件内容总结，有效降低运营成本
- 使用高性能在线模型进行求职进度分析，确保分析质量
- 模块化设计，便于扩展和维护
- 完善的配置系统，支持个性化定制

## 安装说明
1. 克隆项目到本地：
```bash
git clone [项目地址]
cd resume-tracker
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置文件设置：
- 在 `config/config.py` 中配置您的：
  - 邮箱服务器信息
  - 邮箱账号密码
  - 本地模型参数
  - API密钥等

## 使用方法
1. 基本使用：
```python
from client import RecruitmentClient

# 创建客户端实例
client = RecruitmentClient()

# 读取并分析邮件
emails = client.read_emails(folder='求职邮件', limit=10)
summarized = client.summarize_emails(emails)
progress = client.analyze_progress(summarized)

# 关闭客户端
client.close()
```

2. 查看分析结果：
- 系统会自动分析并展示各个公司的招聘进度
- 提供求职状态的整体概览
- 智能识别重要的进度更新

## 注意事项
- 首次使用前请确保正确配置邮箱信息
- 建议定期备份重要的求职邮件
- 请确保本地模型所需的计算资源充足

## 贡献指南
欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证
本项目采用 MIT 许可证 