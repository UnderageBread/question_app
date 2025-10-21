import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import os


class EmailSender:
    
    def __init__(self, sender_email, password):
        self.sender_email = sender_email
        self.password = password
        self.smtp_server = "smtp.qq.com"
        self.smtp_port = 465
    
def send_email(self, receiver_email, subject, content, attachments=None):
    try:
        message = MIMEMultipart()
        message['From'] = self.sender_email  # 改这里，不要用Header包装
        
        if isinstance(receiver_email, list):
            message['To'] = ','.join(receiver_email)
        else:
            message['To'] = receiver_email
            receiver_email = [receiver_email]
        
        message['Subject'] = Header(subject, 'utf-8')
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        attachment = MIMEApplication(f.read())
                        attachment.add_header(
                            'Content-Disposition', 
                            'attachment', 
                            filename=('utf-8', '', os.path.basename(file_path))
                        )
                        message.attach(attachment)
                else:
                    print(f"附件文件不存在: {file_path}")
        
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())
        
        print(f"邮件发送成功！收件人: {', '.join(receiver_email)}")
        return True
        
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")
        return False
