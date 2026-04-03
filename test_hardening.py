from core.retry_queue import add_to_retry, get_retryable, mark_attempt, mark_resolved
from core.database import initialize_database, get_connection

def test_hardening():
    initialize_database()

    # Test retry queue
    add_to_retry(1, "Network timeout")
    retries = get_retryable()
    print(f"Retryable: {retries}")
    # Note: last_attempt_at is NOW, so it won't be returned by get_retryable (needs 10 min wait)
    # But we can verify it's in the DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM retry_queue")
    row = cursor.fetchone()
    print(f"Retry row: {dict(row)}")
    assert row['product_id'] == 1

    mark_attempt(1)
    cursor.execute("SELECT attempts FROM retry_queue WHERE product_id=1")
    assert cursor.fetchone()[0] == 1

    mark_resolved(1)
    cursor.execute("SELECT COUNT(*) FROM retry_queue")
    assert cursor.fetchone()[0] == 0
    conn.close()

    # Test duplicate detection
    from core.importer import save_products, check_duplicates
    import pandas as pd

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (raw_name) VALUES ('DUP_TEST')")
    conn.commit()
    conn.close()

    dups = check_duplicates(['DUP_TEST', 'NEW_PROD'])
    print(f"Duplicates found: {dups}")
    assert 'DUP_TEST' in dups

    df = pd.DataFrame({"Name": ["DUP_TEST", "NEW_PROD", ""]})
    saved, empty, duplicate = save_products(df, {"product_name": "Name"})
    print(f"Saved: {saved}, Empty: {empty}, Duplicate: {duplicate}")
    assert saved == 1
    assert empty == 1
    assert duplicate == 1

    print("Hardening test passed!")

if __name__ == "__main__":
    test_hardening()
