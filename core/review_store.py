from core.database import get_connection
from utils.logger import logger

def get_pending_products(status_filter: str) -> list[dict]:
    """
    Returns products joined with their best candidate and decision.
    status_filter: 'pending_review' | 'accepted' | 'rejected'
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Join products with their normalised name and decision status
        cursor.execute("""
            SELECT
                p.id, p.raw_name, n.cleaned_name, d.status, d.confidence, d.explanation, d.chosen_image_url
            FROM products p
            LEFT JOIN normalised n ON p.id = n.product_id
            JOIN decisions d ON p.id = d.product_id
            WHERE d.status = ?
        """, (status_filter,))

        rows = [dict(row) for row in cursor.fetchall()]

        # For each product, get all candidates
        for row in rows:
            cursor.execute("SELECT * FROM candidates WHERE product_id = ?", (row['id'],))
            row['candidates'] = [dict(c) for c in cursor.fetchall()]

        return rows
    except Exception as e:
        logger.error(f"Error fetching pending products: {e}")
        return []
    finally:
        conn.close()

def save_decision(product_id: int, status: str, chosen_image_url: str | None) -> None:
    """
    Updates the decision status and chosen image URL for a product.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE decisions
            SET status = ?, chosen_image_url = ?, reviewed_at = CURRENT_TIMESTAMP
            WHERE product_id = ?
        """, (status, chosen_image_url, product_id))
        conn.commit()
    except Exception as e:
        logger.error(f"Error saving decision for product_id {product_id}: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
