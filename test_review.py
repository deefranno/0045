from core.database import initialize_database, get_connection
from core.review_store import get_pending_products, save_decision
import json

def test_review_store():
    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (raw_name) VALUES ('TEST_REVIEW')")
    product_id = cursor.lastrowid
    cursor.execute("INSERT INTO normalised (product_id, cleaned_name) VALUES (?, ?)", (product_id, "Cleaned Product"))
    cursor.execute("INSERT INTO decisions (product_id, status, confidence, explanation) VALUES (?, ?, ?, ?)", (product_id, "pending_review", 75, '["test"]'))
    cursor.execute("INSERT INTO candidates (product_id, image_url, domain) VALUES (?, ?, ?)", (product_id, "https://example.com/img.jpg", "example.com"))
    conn.commit()
    conn.close()

    # Test fetch
    products = get_pending_products("pending_review")
    print(f"Fetched {len(products)} products.")
    assert len(products) == 1
    assert products[0]['id'] == product_id
    assert len(products[0]['candidates']) == 1

    # Test save decision
    save_decision(product_id, "accepted", "https://example.com/chosen.jpg")

    # Verify save
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, chosen_image_url FROM decisions WHERE product_id=?", (product_id,))
    row = cursor.fetchone()
    print(f"Updated decision: {dict(row)}")
    assert row['status'] == "accepted"
    assert row['chosen_image_url'] == "https://example.com/chosen.jpg"
    conn.close()

    print("Review store test passed!")

if __name__ == "__main__":
    test_review_store()
