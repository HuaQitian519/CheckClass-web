from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object('config.Config')  # 加载配置

mail = Mail(app)

with app.app_context():
    msg = Message(subject="测试邮件",
                  recipients=["huaqitian@vip.qq.com"],  # 收件人邮箱
                  body="这是一封测试邮件，测试邮件发送功能。")
    try:
        mail.send(msg)
        print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送失败: {e}")