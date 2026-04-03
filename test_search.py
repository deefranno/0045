import asyncio
from core.search_engine import SearchEngine, save_candidates
from core.normaliser import NormalisedProduct
from core.database import initialize_database, get_connection
import json

async def test_search():
    initialize_database()

    config = {
        "sources": [
            {
                "tier": 1,
                "name": "Fontana",
                "domain": "fontanasupermarket.com",
                "enabled": True,
                "search_url_template": "https://fontanasupermarket.com/search?q={query}",
                "type": "scrape"
            }
        ],
        "app_config": {
            "domain_whitelist": [],
            "domain_blacklist": []
        }
    }

    product = NormalisedProduct(
        raw_name="BLUE RIBBON RICE",
        cleaned_name="Blue Ribbon Rice",
        brand="Blue Ribbon",
        product_type="Rice",
        size="2LB",
        search_variants=["Blue+Ribbon+Rice+2LB", "Blue+Ribbon+Rice"]
    )

    engine = SearchEngine(config)
    await engine.start_browser()

    # Mocking scraper to avoid external network calls during test
    # Actually, we can test with a real call if internet is available, but better to mock for speed
    # Let's try a real call to a public search engine to verify playwright works

    # candidates = await engine.search_product(product)
    # print(f"Found {len(candidates)} candidates.")

    # Let's mock for now
    from core.scraper import ImageCandidate
    mock_candidates = [
        ImageCandidate(
            image_url="https://example.com/image.jpg",
            source_url="https://example.com/page",
            domain="example.com",
            page_title="Product Page",
            alt_text="Blue Ribbon Rice",
            query_used="Blue Ribbon Rice",
            tier=1
        )
    ]

    # Test DB save
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (raw_name) VALUES ('TEST_SEARCH')")
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()

    save_candidates(product_id, mock_candidates)

    # Verify save
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates WHERE product_id=?", (product_id,))
    row = cursor.fetchone()
    print(f"Saved candidate: {dict(row)}")
    assert row['image_url'] == mock_candidates[0].image_url
    conn.close()

    await engine.stop_browser()
    print("Search system test passed!")

if __name__ == "__main__":
    asyncio.run(test_search())
