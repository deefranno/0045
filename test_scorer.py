from core.scorer import score_candidates, ScoredCandidate
from core.normaliser import NormalisedProduct
from core.scraper import ImageCandidate
from core.scorer_store import save_scores
from core.database import initialize_database, get_connection
import json

def test_scorer():
    initialize_database()

    product = NormalisedProduct(
        raw_name="BLUE RIBBON RICE",
        cleaned_name="Blue Ribbon Rice",
        brand="Blue Ribbon",
        product_type="Rice",
        size="2LB"
    )

    candidates = [
        ImageCandidate(
            image_url="https://example.com/best.jpg",
            source_url="https://example.com/p1",
            domain="example.com",
            page_title="Blue Ribbon Rice 2LB",
            alt_text="Blue Ribbon Rice",
            query_used="Blue Ribbon Rice",
            tier=1
        ),
        ImageCandidate(
            image_url="https://other.com/bad.jpg",
            source_url="https://other.com/p2",
            domain="other.com",
            page_title="Bad Product",
            alt_text="None",
            query_used="Blue Ribbon Rice",
            tier=1
        )
    ]

    config = {"app_config": {"trusted_domains": ["example.com"], "domain_blacklist": []}}

    scored = score_candidates(product, candidates, config)
    print(f"Scored {len(scored)} candidates.")
    for s in scored:
        print(f"Score: {s.score}, Band: {s.confidence_band}, Explanation: {s.explanation}")

    # With original weights: 30 (Fuzzy) + 15 (Brand) + 10 (Size) + 10 (Type) + 10 (Trusted) = 75
    # Wait, 75 < 85. So it will be in 'review' band.
    # To get auto_accept (85), we need more factors.
    assert scored[0].score >= 60
    assert scored[1].score < 60

    # Test DB save
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (raw_name) VALUES ('TEST_SCORER')")
    product_id = cursor.lastrowid
    # Pre-insert candidates to update them
    for cand in candidates:
        cursor.execute("INSERT INTO candidates (product_id, image_url) VALUES (?, ?)", (product_id, cand.image_url))
    conn.commit()
    conn.close()

    save_scores(product_id, scored)

    # Verify save
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM decisions WHERE product_id=?", (product_id,))
    row = cursor.fetchone()
    print(f"Decision: {dict(row)}")
    assert row['status'] == "pending_review"
    conn.close()

    print("Scorer test passed!")

if __name__ == "__main__":
    test_scorer()
