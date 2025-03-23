# """
# 配置文件，存储所有的配置信息
# 支持通过环境变量覆盖配置
# """
# import os

# # 大语言模型配置
# LLM_CONFIG = {
#     # Deepseek配置
#     # 用于分析招聘进度，需要能力较强的大语言模型
#     'DEEPSEEK': {
#         'API_KEY': os.getenv('DEEPSEEK_API_KEY', 'sk-5范德萨给633d223b92fd'),
#         'BASE_URL': os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com'),
#         'MODEL': os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
#     },
#     # Ollama配置
#     # 用于总结邮件，需要本地的模型，减少在线模型的token，减少成本
#     'OLLAMA': {
#         'BASE_URL': os.getenv('OLLAMA_BASE_URL', 'http://your-ollama-server:11434'),
#         'MODEL': os.getenv('OLLAMA_MODEL', 'qwen2.5')
#     }
# }

# # 邮件配置
# EMAIL_CONFIG = {
#     # 服务器配置
#     # 目前只支持qq邮箱
#     'IMAP_SERVER': os.getenv('EMAIL_IMAP_SERVER', 'imap.qq.com'), # 邮箱服务器地址
#     'SMTP_SERVER': os.getenv('EMAIL_SMTP_SERVER', 'smtp.qq.com'), # 邮箱服务器地址
#     'IMAP_PORT': int(os.getenv('EMAIL_IMAP_PORT', '993')), # 邮箱服务器端口
#     'SMTP_PORT': int(os.getenv('EMAIL_SMTP_PORT', '587')), # 邮箱服务器端口
    
#     # 账号配置
#     'EMAIL': os.getenv('EMAIL_ADDRESS', 'your-email@example.com'), # 邮箱地址
#     'PASSWORD': os.getenv('EMAIL_PASSWORD', 'your-email-password'),  # 邮箱授权码
#     'TARGET_FOLDER': os.getenv('TARGET_FOLDER', 'your-target-folder') # 存放招聘信息邮件的邮箱文件夹

# }


# # API配置
# API_CONFIG = {
#     'HOST': os.getenv('API_HOST', '0.0.0.0'),
#     'PORT': int(os.getenv('API_PORT', '8000'))
# } 