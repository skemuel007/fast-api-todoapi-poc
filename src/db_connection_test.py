from sqlalchemy import create_engine, text

from config import DATABASE_URL

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful!")
        print(result.scalar())  # Should print 1
except Exception as e:
    print(f"Database connection failed: {e}")