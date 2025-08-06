"""
Database Setup Instructions for PostgreSQL

1. Install PostgreSQL:
   - Download from: https://www.postgresql.org/download/
   - Or use Docker: docker run --name postgres-db -e POSTGRES_PASSWORD=admin -p 5432:5432 -d postgres

2. Create Database:
   - Connect to PostgreSQL as superuser
   - Create database: CREATE DATABASE task_management;
   - Create user (optional): CREATE USER postgres WITH PASSWORD 'admin';
   - Grant privileges: GRANT ALL PRIVILEGES ON DATABASE task_management TO postgres;

3. Update .env file:
   - Make sure DATABASE_URL is set correctly
   - Current setting: postgresql://postgres:admin@localhost:5432/task_management

4. Install dependencies:
   - pip install -r requirements.txt

5. Run migrations:
   - python run_migrations.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine
from app.models import Base

def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print("📋 Tables created:")
        for table in Base.metadata.tables.keys():
            print(f"   - {table}")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        print("Make sure PostgreSQL is running and the database exists.")
        return False
    return True

def test_connection():
    """Test database connection"""
    try:
        from app.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Setting up PostgreSQL database...")
    
    if test_connection():
        if create_tables():
            print("🎉 Database setup completed!")
        else:
            print("⚠️  Table creation failed")
    else:
        print("⚠️  Database connection failed")
        print("Please check your PostgreSQL installation and .env configuration")
