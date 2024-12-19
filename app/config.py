import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'devsecretkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://hainanwall_user:yourpassword@localhost:5432/hainanwall'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = '465'
    MAIL_USE_TLS = False  # TLS 设置为 False
    MAIL_USE_SSL = True  # SSL 设置为 True
    MAIL_USERNAME = '2224339882@qq.com'
    MAIL_PASSWORD = 'bqehqikvcpamebga'
    MAIL_DEFAULT_SENDER = ('Course Review', '2224339882@qq.com')
