from app import create_app, db
from app.models import User, Course, CourseEvaluation

app = create_app()

with app.app_context():
    # 删除现有数据库并重新创建（仅在开发环境中使用）
    db.drop_all()
    db.create_all()

    # 插入一些测试数据
    admin = User(email="admin@cuc.edu.cn", is_admin=True, verified=True)
    admin.set_password("adminpassword")

    course1 = Course(name="数据库系统", teacher="张老师", approved=True)
    course2 = Course(name="计算机网络", teacher="李老师", approved=True)

    db.session.add(admin)
    db.session.add(course1)
    db.session.add(course2)
    db.session.commit()

    print("数据库初始化完成，已插入初始数据！")