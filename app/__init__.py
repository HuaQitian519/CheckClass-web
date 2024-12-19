from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    mail.init_app(app)

    from .admin_routes import admin_bp
    from .user_routes import user_bp
    from .course_routes import course_bp

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp)
    app.register_blueprint(course_bp)

    with app.app_context():
        # 在生产环境下应使用数据库迁移工具进行初始化
        pass

    return app
