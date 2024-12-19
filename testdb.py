# test_db_connection.py
from sqlalchemy import create_engine

DATABASE_URL = 'postgresql://user:password@localhost:5432/mydb'

def test_connection():
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        print("Database connection successful!")
        connection.close()
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_connection()