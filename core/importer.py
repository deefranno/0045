import pandas as pd
import sqlite3
import os
from datetime import datetime
from utils.logger import logger
from core.database import get_connection

def parse_csv(filepath: str) -> tuple[pd.DataFrame, list[str]]:
    """
    Reads CSV using pandas. Handles encoding issues and malformed files.
    Returns (dataframe, list_of_column_names)
    """
    try:
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(filepath, encoding='latin-1')

        return df, df.columns.tolist()
    except Exception as e:
        logger.error(f"Failed to parse CSV {filepath}: {e}")
        return pd.DataFrame(), []

def check_duplicates(raw_names: list[str]) -> list[str]:
    """
    Queries products table for existing raw_name values.
    Returns list of names that already exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check in batches of 500 to avoid SQL limit
        duplicates = []
        for i in range(0, len(raw_names), 500):
            batch = raw_names[i:i+500]
            placeholders = ",".join(["?"] * len(batch))
            cursor.execute(f"SELECT raw_name FROM products WHERE raw_name IN ({placeholders})", batch)
            duplicates.extend([row[0] for row in cursor.fetchall()])

        return list(set(duplicates))
    except Exception as e:
        logger.error(f"Error checking duplicates: {e}")
        return []
    finally:
        conn.close()

def validate_mapping(df: pd.DataFrame, mapping: dict) -> list[str]:
    """
    mapping is e.g. {"product_name": "Col A", "sku": "Col B"}
    Returns a list of validation error strings (empty = valid)
    """
    errors = []

    if "product_name" not in mapping or not mapping["product_name"] or mapping["product_name"] == "-- ignore --":
        errors.append("Product Name mapping is required.")

    for key, col in mapping.items():
        if col and col != "-- ignore --" and col not in df.columns:
            errors.append(f"Mapped column '{col}' for '{key}' does not exist in CSV.")

    return errors

def save_products(df: pd.DataFrame, mapping: dict) -> tuple[int, int, int]:
    """
    Inserts rows into the products SQLite table.
    Returns (rows_saved, rows_skipped_empty, rows_skipped_duplicate)
    """
    rows_saved = 0
    rows_skipped_empty = 0
    rows_skipped_duplicate = 0

    conn = get_connection()
    cursor = conn.cursor()

    # Extract column names from mapping
    product_name_col = mapping.get("product_name")
    sku_col = mapping.get("sku")
    brand_col = mapping.get("brand")

    try:
        # Pre-check duplicates
        all_raw_names = []
        for _, row in df.iterrows():
            rv = row.get(product_name_col)
            if not pd.isna(rv): all_raw_names.append(str(rv).strip())

        existing_names = set(check_duplicates(all_raw_names))

        for _, row in df.iterrows():
            raw_val = row.get(product_name_col)
            if pd.isna(raw_val):
                raw_name = ""
            else:
                raw_name = str(raw_val).strip()

            if not raw_name or raw_name.lower() == "nan":
                rows_skipped_empty += 1
                continue

            if raw_name in existing_names:
                rows_skipped_duplicate += 1
                continue

            sku = str(row.get(sku_col, "")).strip() if sku_col and sku_col != "-- ignore --" else None
            brand = str(row.get(brand_col, "")).strip() if brand_col and brand_col != "-- ignore --" else None

            cursor.execute(
                "INSERT INTO products (raw_name, sku, brand) VALUES (?, ?, ?)",
                (raw_name, sku, brand)
            )
            rows_saved += 1
            existing_names.add(raw_name) # Avoid duplicates within the same batch

        conn.commit()
        logger.info(f"Imported {rows_saved}, empty {rows_skipped_empty}, duplicates {rows_skipped_duplicate}.")
    except Exception as e:
        logger.error(f"Database error during import: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

    return rows_saved, rows_skipped_empty, rows_skipped_duplicate
