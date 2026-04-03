from core.database import initialize_database, get_connection
from core.exporter import build_export_dataframe, export_to_csv
import pandas as pd
import os

def test_exporter():
    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (raw_name, sku, brand) VALUES ('EX_PROD', 'SKU-01', 'Test Brand')")
    product_id = cursor.lastrowid
    cursor.execute("INSERT INTO normalised (product_id, cleaned_name, size) VALUES (?, ?, ?)", (product_id, "Cleaned Product", "500G"))
    cursor.execute("INSERT INTO decisions (product_id, status, chosen_image_url, confidence) VALUES (?, ?, ?, ?)", (product_id, "accepted", "http://img.com/a.jpg", 90))
    cursor.execute("INSERT INTO candidates (product_id, image_url, source_url, domain) VALUES (?, ?, ?, ?)", (product_id, "http://img.com/a.jpg", "http://source.com/p", "source.com"))
    conn.commit()
    conn.close()

    # Test build DF
    df = build_export_dataframe("accepted")
    print(f"Export DF columns: {df.columns.tolist()}")
    print(f"Export DF rows: {len(df)}")
    assert len(df) == 1
    assert df.iloc[0]['original_product_name'] == 'EX_PROD'
    assert df.iloc[0]['image_url'] == 'http://img.com/a.jpg'

    # Test export CSV
    csv_path = "test_export.csv"
    success, error = export_to_csv(df, csv_path)
    print(f"Export success: {success}, error: {error}")
    assert success

    # Check encoding
    with open(csv_path, 'rb') as f:
        content = f.read(3)
        print(f"BOM check: {content}")
        assert content == b'\xef\xbb\xbf'

    os.remove(csv_path)
    print("Exporter test passed!")

if __name__ == "__main__":
    test_exporter()
