"""
Configuration file for database connection
Supports both Supabase (PostgreSQL) and SQLite
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_DB_NAME = os.getenv('SUPABASE_DB_NAME', 'postgres')
SUPABASE_DB_USER = os.getenv('SUPABASE_DB_USER', 'postgres')
SUPABASE_DB_PASSWORD = os.getenv('SUPABASE_DB_PASSWORD', '')
SUPABASE_DB_HOST = os.getenv('SUPABASE_DB_HOST', '')
SUPABASE_DB_PORT = os.getenv('SUPABASE_DB_PORT', '5432')

# Use Supabase if credentials are provided, otherwise use SQLite
USE_SUPABASE = bool(SUPABASE_URL or (SUPABASE_DB_HOST and SUPABASE_DB_PASSWORD))

def get_database_uri():
    """Get database URI based on configuration"""
    if USE_SUPABASE:
        # Construct Supabase PostgreSQL connection string
        if SUPABASE_URL:
            # If using Supabase connection pooler URL
            return SUPABASE_URL
        else:
            # Construct from individual components
            return f"postgresql://{SUPABASE_DB_USER}:{SUPABASE_DB_PASSWORD}@{SUPABASE_DB_HOST}:{SUPABASE_DB_PORT}/{SUPABASE_DB_NAME}"
    else:
        # Fallback to SQLite
        basedir = os.path.abspath(os.path.dirname(__file__))
        return f'sqlite:///{os.path.join(basedir, "file_agent.db")}'


