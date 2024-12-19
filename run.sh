#!/usr/bin/env bash
# 等待数据库服务启动
sleep 5

# 数据库迁移
alembic upgrade head

# 使用gunicorn启动应用
exec gunicorn -b 0.0.0.0:8000 app.wsgi:app -w 4 --threads 2