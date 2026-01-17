from sqlalchemy import text
from app.database import engine
from app.config import get_settings

settings = get_settings()

print(f"Testing connection to: {settings.database_url}")

try:
    # Try to connect
    with engine.connect() as connection:
        print("✅ Database connection successful!")
        result = connection.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"PostgreSQL version: {version}")
except Exception as e:
    print(f"❌ Connection failed: {e}")