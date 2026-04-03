from core.database import initialize_database, get_connection
from utils.logger import setup_logging
import os

if __name__ == "__main__":
    logger = setup_logging()
    logger.info("Running DB init test script...")
    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Tables found: {tables}")
    conn.close()
