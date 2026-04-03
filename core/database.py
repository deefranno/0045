import sqlite3
import os
from utils.logger import logger

DB_PATH = "data/app_database.sqlite"

def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

def initialize_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # products table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_name TEXT NOT NULL,
            sku TEXT,
            brand TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # normalised table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS normalised (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            cleaned_name TEXT,
            brand TEXT,
            product_type TEXT,
            size TEXT,
            pack_quantity INTEGER,
            tokens TEXT,
            search_variants TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        """)

        # candidates table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            image_url TEXT,
            source_url TEXT,
            domain TEXT,
            page_title TEXT,
            alt_text TEXT,
            query_used TEXT,
            tier INTEGER,
            score INTEGER DEFAULT 0,
            explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        """)

        # decisions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            chosen_image_url TEXT,
            confidence INTEGER,
            explanation TEXT,
            reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        """)

        # retry_queue table (for Phase 9)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS retry_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            reason TEXT,
            attempts INTEGER DEFAULT 0,
            last_attempt_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        """)

        conn.commit()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
