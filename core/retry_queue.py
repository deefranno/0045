from core.database import get_connection
from utils.logger import logger
from datetime import datetime, timedelta

def add_to_retry(product_id, reason):
    """
    Inserts row into retry_queue table, max attempts = 3.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, attempts FROM retry_queue WHERE product_id = ?", (product_id,))
        row = cursor.fetchone()

        if row:
            if row['attempts'] < 3:
                cursor.execute("UPDATE retry_queue SET reason = ?, last_attempt_at = CURRENT_TIMESTAMP WHERE product_id = ?", (reason, product_id))
        else:
            cursor.execute("INSERT INTO retry_queue (product_id, reason, attempts, last_attempt_at) VALUES (?, ?, 0, CURRENT_TIMESTAMP)", (product_id, reason))

        conn.commit()
    except Exception as e:
        logger.error(f"Error adding to retry queue for product_id {product_id}: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_retryable() -> list[int]:
    """
    Returns product_ids where attempts < 3 and last_attempt_at < now - 10 minutes.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # For simplicity in SQL, let's just get anything that needs retry
        # and handle time logic if needed, but 10 minutes wait is specified
        cursor.execute("""
            SELECT product_id FROM retry_queue
            WHERE attempts < 3
            AND (last_attempt_at IS NULL OR last_attempt_at < datetime('now', '-10 minutes'))
        """)
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error fetching retryable products: {e}")
        return []
    finally:
        conn.close()

def mark_attempt(product_id):
    """
    Increments attempts, updates last_attempt_at.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE retry_queue SET attempts = attempts + 1, last_attempt_at = CURRENT_TIMESTAMP WHERE product_id = ?", (product_id,))
        conn.commit()
    except Exception as e:
        logger.error(f"Error marking attempt for product_id {product_id}: {e}")
        conn.rollback()
    finally:
        conn.close()

def mark_resolved(product_id):
    """
    Deletes row from retry_queue.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM retry_queue WHERE product_id = ?", (product_id,))
        conn.commit()
    except Exception as e:
        logger.error(f"Error marking resolved for product_id {product_id}: {e}")
        conn.rollback()
    finally:
        conn.close()
