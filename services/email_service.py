"""
邮件服务类
"""
import imaplib
import email
import smtplib
import re
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from typing import List, Dict, Optional
from config.config import EMAIL_CONFIG


class EmailService:
    """
    邮件服务类，处理邮件的读取和发送
    """
    
    def __init__(self):
        self.config = EMAIL_CONFIG
        self.imap = None
        self.smtp = None
        self.current_folder = None
    
    def connect_imap(self) -> None:
        """
        连接IMAP服务器
        """
        self.imap = imaplib.IMAP4_SSL(self.config['IMAP_SERVER'], self.config['IMAP_PORT'])
        self.imap.login(self.config['EMAIL'], self.config['PASSWORD'])
        print("登录成功！")
        self._find_folder()
    
    def _find_folder(self) -> None:
        """
        查找匹配关键词的文件夹
        """
        # 列出所有可用文件夹
        status, folders = self.imap.list()
        
        matched_folders = []
        for folder in folders:
            if self.config['TARGET_FOLDER'] in str(folder):
                # 转换为字符串并处理转义
                str_data = folder.decode('utf-8').replace('\\', '')  # 去除转义反斜杠
                str_data = str_data.split(" ")[-1].split('"')[1]
                matched_folders.append(str_data)
        
        if not matched_folders:
            raise ValueError(f"未找到包含关键词 '{self.config['TARGET_FOLDER']}' 的文件夹")
        
        # 选择第一个匹配的文件夹
        status, count = self.imap.select(matched_folders[0], readonly=True)
        self.current_folder = matched_folders[0]
        print(f"当前文件夹：{matched_folders[0]}，邮件总数：{count[0].decode()}")
    
    def connect_smtp(self) -> None:
        """
        连接SMTP服务器
        """
        self.smtp = smtplib.SMTP(self.config['SMTP_SERVER'], self.config['SMTP_PORT'])
        self.smtp.starttls()
        self.smtp.login(self.config['EMAIL'], self.config['PASSWORD'])
    
    def _get_email_content(self, msg) -> str:
        """
        获取邮件内容，支持纯文本和HTML格式，并提取中文内容
        
        Args:
            msg: 邮件消息对象
            
        Returns:
            str: 处理后的邮件内容
        """
        content = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or 'utf-8'
                        content = payload.decode(charset, errors='replace')
                        break
                    except:
                        continue
                elif part.get_content_type() == "text/html" and not content:
                    try:
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or 'utf-8'
                        html_content = payload.decode(charset, errors='replace')
                        
                        # 使用BeautifulSoup解析HTML
                        soup = BeautifulSoup(html_content, 'html.parser')
                        
                        # 移除script和style标签
                        for script in soup(["script", "style"]):
                            script.decompose()
                        
                        # 提取所有文本
                        text = soup.get_text('\n')
                        
                        # 分割成行并去除空白行
                        lines = [line.strip() for line in text.splitlines() if line.strip()]
                        
                        # 处理每一行，仅保留中文字符和标点
                        chinese_lines = []
                        for line in lines:
                            # 使用正则表达式替换非中文字符和标点
                            cleaned_line = re.sub(r'[^\u4e00-\u9fa5，。！？：；""''（）《》【】、]', '', line)
                            if cleaned_line:
                                chinese_lines.append(cleaned_line)
                        
                        # 合并成最终的文本
                        content = '\n'.join(chinese_lines)
                    except:
                        continue
        else:
            try:
                payload = msg.get_payload(decode=True)
                charset = msg.get_content_charset() or 'utf-8'
                raw_content = payload.decode(charset, errors='replace')
                
                # 对非HTML内容也进行中文提取
                lines = [line.strip() for line in raw_content.splitlines() if line.strip()]
                chinese_lines = []
                for line in lines:
                    cleaned_line = re.sub(r'[^\u4e00-\u9fa5，。！？：；""''（）《》【】、]', '', line)
                    if cleaned_line:
                        chinese_lines.append(cleaned_line)
                content = '\n'.join(chinese_lines)
            except:
                content = "无法解码邮件内容"
        
        # 清理内容
        content = re.sub(r'\n\s*\n', '\n', content)  # 合并多个空行
        return content.strip()
    
    def read_emails(self, limit: Optional[int] = None) -> List[Dict]:
        """
        读取邮件
        
        Args:
            limit: 读取邮件数量限制，如果为None则读取所有邮件
            
        Returns:
            List[Dict]: 邮件列表，每个邮件包含主题、发件人、日期和内容
        """
        if not self.imap:
            self.connect_imap()
        
        # 搜索所有邮件
        _, messages = self.imap.search(None, 'ALL')
        email_ids = messages[0].split()
        
        # 如果指定了限制，只取最新的N封
        if limit:
            email_ids = email_ids[-limit:]
        
        emails = []
        for email_id in email_ids:
            _, msg_data = self.imap.fetch(email_id, '(RFC822)')
            email_body = msg_data[0][1]
            msg = email.message_from_bytes(email_body)
            
            # 解析主题
            subject = decode_header(msg['subject'])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            
            # 解析发件人
            sender = self._parse_sender(msg['from'])
            
            # 解析内容
            content = self._get_email_content(msg)
            
            email_info = {
                'subject': subject,
                'from': sender,
                'date': msg['date'],
                'content': content
            }
            emails.append(email_info)
        
        return emails
    
    def _parse_sender(self, sender: str) -> str:
        """
        解析发件人信息
        
        Args:
            sender: 原始发件人信息
            
        Returns:
            str: 格式化后的发件人信息
        """
        name_parts = []
        email_part = ""
        
        for info, encoding in decode_header(sender):
            if isinstance(info, bytes):
                info = info.decode(encoding if encoding else 'utf-8')
            else:
                info = str(info)
            
            if '@' in info:
                email_part = info.split()[-1]
            else:
                name_parts.append(info.strip('"'))
        
        return f'"{", ".join(name_parts)}" <{email_part}>'
    
    def close(self) -> None:
        """
        关闭连接
        """
        if self.imap:
            self.imap.close()
            self.imap.logout()
        
        if self.smtp:
            self.smtp.quit() 
