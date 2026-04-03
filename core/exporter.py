import pandas as pd
from core.database import get_connection
from utils.logger import logger
import os

def build_export_dataframe(status_filter: str) -> pd.DataFrame:
    """
    Queries products JOIN normalised JOIN decisions.
    status_filter: "accepted" | "all" | "no_match"
    """
    conn = get_connection()

    query = """
        SELECT
            p.raw_name AS original_product_name,
            n.cleaned_name AS cleaned_product_name,
            p.sku,
            p.brand,
            n.size,
            d.chosen_image_url AS image_url,
            c.source_url,
            c.domain,
            d.confidence,
            d.status
        FROM products p
        LEFT JOIN normalised n ON p.id = n.product_id
        LEFT JOIN decisions d ON p.id = d.product_id
        LEFT JOIN candidates c ON p.id = c.product_id AND d.chosen_image_url = c.image_url
        WHERE d.status != 'rejected' OR d.status IS NULL
    """

    if status_filter == "accepted":
        query += " AND d.status = 'accepted'"
    elif status_filter == "no_match":
        query += " AND d.status = 'no_match'"

    try:
        df = pd.read_sql_query(query, conn)
        df.fillna("", inplace=True)
        return df
    except Exception as e:
        logger.error(f"Error building export dataframe: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def export_to_csv(df: pd.DataFrame, filepath: str) -> tuple[bool, str]:
    """
    Writes CSV with UTF-8 BOM encoding for WooCommerce compatibility.
    """
    try:
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        return True, ""
    except Exception as e:
        logger.error(f"Failed to export CSV: {e}")
        return False, str(e)
