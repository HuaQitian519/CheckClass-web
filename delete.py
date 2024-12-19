from app import create_app, db
from app.models import User

app = create_app()

# 启动 Flask 应用上下文
with app.app_context():
    # 输入要删除的邮箱
    email_to_delete = "202229013042n@cuc.edu.cn"

    # 查询用户
    user = User.query.filter_by(email=email_to_delete).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        print(f"用户 {email_to_delete} 已成功删除！")
    else:
        print(f"未找到邮箱为 {email_to_delete} 的用户。")