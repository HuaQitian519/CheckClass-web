FROM python:3.11-slim

WORKDIR /app

# 安装必要的依赖以编译psycopg2-binary (若有需要)
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x run.sh

EXPOSE 8000
CMD ["./run.sh"]