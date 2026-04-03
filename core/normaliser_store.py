import json
from core.database import get_connection
from core.normaliser import NormalisedProduct
from utils.logger import logger

def save_normalised(product_id: int, result: NormalisedProduct) -> None:
    """
    Writes to the normalised table via core/database.py
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO normalised (
                product_id, cleaned_name, brand, product_type,
                size, pack_quantity, tokens, search_variants
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product_id,
            result.cleaned_name,
            result.brand,
            result.product_type,
            result.size,
            result.pack_quantity,
            ",".join(result.tokens),
            json.dumps(result.search_variants)
        ))
        conn.commit()
    except Exception as e:
        logger.error(f"Error saving normalised result for product_id {product_id}: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
