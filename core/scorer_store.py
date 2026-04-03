import json
from core.database import get_connection
from core.scorer import ScoredCandidate
from utils.logger import logger

def save_scores(product_id: int, scored: list[ScoredCandidate]) -> None:
    """
    Updates scores and explanation on existing rows in candidates table.
    Writes best match to decisions table.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        for s in scored:
            cursor.execute("""
                UPDATE candidates
                SET score = ?, explanation = ?
                WHERE product_id = ? AND image_url = ?
            """, (s.score, json.dumps(s.explanation), product_id, s.image_url))

        best = scored[0] if scored else None
        if best:
            status = "auto_accepted" if best.confidence_band == "auto_accept" else "pending_review"
            cursor.execute("""
                INSERT INTO decisions (
                    product_id, status, chosen_image_url, confidence, explanation
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                product_id,
                status,
                best.image_url,
                best.score,
                json.dumps(best.explanation)
            ))

        conn.commit()
    except Exception as e:
        logger.error(f"Error saving scores for product_id {product_id}: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
