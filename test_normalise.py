from core.normaliser import normalise, NormalisedProduct
from core.normaliser_store import save_normalised
from core.database import initialize_database, get_connection
import json

def test_normaliser():
    initialize_database()

    config = {
        "abbreviations": {"P/BOIL": "parboiled", "PWDR": "powder"},
        "brands": ["Blue Ribbon", "Lasco", "Grace"],
        "synonyms": {"CHOC": "chocolate", "COCK": "cock-flavoured"}
    }

    test_cases = [
        "BLUE RIBBON P/BOIL RICE 12X2LB",
        "LASCO CHOC PWDR 500G",
        "GRACE COCK SOUP MIX 10X50G"
    ]

    results = []
    for raw in test_cases:
        res = normalise(raw, config)
        print(f"Raw: {raw} -> Cleaned: {res.cleaned_name}, Brand: {res.brand}, Size: {res.size}, Qty: {res.pack_quantity}, Variants: {res.search_variants}")
        results.append(res)

    # Verify first case
    assert results[0].brand == "Blue Ribbon"
    assert results[0].size == "2LB"
    assert results[0].pack_quantity == 12

    # Test save
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (raw_name) VALUES ('TEST')")
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()

    save_normalised(product_id, results[0])

    # Verify save
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM normalised WHERE product_id=?", (product_id,))
    row = cursor.fetchone()
    print(f"Saved row: {dict(row)}")
    assert row['cleaned_name'] == results[0].cleaned_name
    conn.close()

    print("Normaliser test passed!")

if __name__ == "__main__":
    test_normaliser()
