from application.pms.database import engine, Base
from sqlalchemy import text

# Add new columns to existing users table
with engine.begin() as connection:
    connection.execute(text("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255)
    """))

    connection.execute(text("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS role VARCHAR(20)
        NOT NULL DEFAULT 'student'
    """))

    # Add new columns to existing tasks table
    connection.execute(text("""
        ALTER TABLE tasks
        ADD COLUMN IF NOT EXISTS teacher_id INTEGER
        REFERENCES users(id)
    """))

    connection.execute(text("""
        ALTER TABLE tasks
        ADD COLUMN IF NOT EXISTS work_notes TEXT
    """))

# Create the new auth_sessions table
Base.metadata.create_all(bind=engine)

print("Database migration completed successfully!")


