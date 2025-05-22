import psycopg2
from psycopg2.extras import RealDictCursor
import os
import logging

logger = logging.getLogger(__name__)


DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "project_db"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "dima1205"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "cursor_factory": RealDictCursor
}

def get_connection():

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info("Database connection established")
        return conn
    except psycopg2.OperationalError as e:
        error_msg = str(e)
        logger.error(f"Failed to connect to database: {error_msg}")
        
        if "password authentication failed" in error_msg:
            raise Exception(f"Ошибка аутентификации: проверьте пароль для пользователя {DB_CONFIG['user']}")
        elif "database" in error_msg and "does not exist" in error_msg:
            raise Exception(f"База данных {DB_CONFIG['dbname']} не существует. Создайте её командой: CREATE DATABASE {DB_CONFIG['dbname']};")
        elif "could not connect to server" in error_msg:
            raise Exception("PostgreSQL сервер не запущен или недоступен на localhost:5432")
        elif "role" in error_msg and "does not exist" in error_msg:
            raise Exception(f"Пользователь {DB_CONFIG['user']} не существует. Создайте его командой: CREATE USER {DB_CONFIG['user']} WITH PASSWORD 'пароль';")
        else:
            raise Exception(f"Database connection failed: {error_msg}")
    except Exception as e:
        logger.error(f"Unexpected error connecting to database: {e}")
        raise

def test_connection():

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version()")
            db_version = cursor.fetchone()
            logger.info(f"Connected to: {db_version['version']}")
            return True
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False
