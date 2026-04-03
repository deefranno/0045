import asyncio
from core.database import initialize_database, get_connection
from core.config_loader import load_all_configs
from core.importer import parse_csv, save_products
from core.worker import SearchWorker
from core.exporter import build_export_dataframe, export_to_csv
import os
import pandas as pd
from utils.logger import setup_logging

async def test_e2e():
    setup_logging()
    initialize_database()
    config = load_all_configs()

    # 1. Import
    csv_path = "sample_products.csv"
    df, cols = parse_csv(csv_path)
    mapping = {"product_name": "product_name", "sku": "sku", "brand": "brand"}
    saved, empty, duplicate = save_products(df, mapping)
    print(f"Imported: {saved}")

    # 2. Process (Partial)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM products LIMIT 3")
    p_ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    print(f"Processing product IDs: {p_ids}")
    worker = SearchWorker(p_ids, config)

    # Run worker logic manually (async)
    await worker._run_async()
    print("Worker finished processing.")

    # 3. Export
    export_df = build_export_dataframe("all")
    print(f"Export rows: {len(export_df)}")
    success, err = export_to_csv(export_df, "e2e_export.csv")
    print(f"Export success: {success}")

    assert os.path.exists("e2e_export.csv")
    os.remove("e2e_export.csv")
    print("E2E test passed!")

if __name__ == "__main__":
    asyncio.run(test_e2e())
