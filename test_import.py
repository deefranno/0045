from core.importer import parse_csv, validate_mapping, save_products
from core.database import initialize_database, get_connection
import pandas as pd
import os

def test_importer():
    initialize_database()

    # Create dummy CSV
    csv_path = "test_products.csv"
    df = pd.DataFrame({
        "Prod Name": ["BLUE RIBBON RICE", "LASCO CHOC", ""],
        "SKU ID": ["BR001", "LSC001", "MISSING"],
        "Brand": ["Blue Ribbon", "Lasco", "None"]
    })
    df.to_csv(csv_path, index=False)

    # Test parse
    parsed_df, columns = parse_csv(csv_path)
    print(f"Parsed columns: {columns}")
    assert len(parsed_df) == 3

    # Test validate
    mapping = {"product_name": "Prod Name", "sku": "SKU ID", "brand": "Brand"}
    errors = validate_mapping(parsed_df, mapping)
    print(f"Validation errors: {errors}")
    assert not errors

    # Test save
    saved, skipped = save_products(parsed_df, mapping)
    print(f"Saved: {saved}, Skipped: {skipped}")
    assert saved == 2
    assert skipped == 1

    # Verify in DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    print(f"Products in DB: {len(rows)}")
    assert len(rows) == 2

    os.remove(csv_path)
    print("Importer test passed!")

if __name__ == "__main__":
    test_importer()
