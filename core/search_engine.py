import asyncio
import json
from playwright.async_api import async_playwright
from core.normaliser import NormalisedProduct
from core.source_manager import Source, load_sources, get_tiers
from core.scraper import fetch_images_from_page, ImageCandidate
from core.database import get_connection
from utils.logger import logger

class SearchEngine:
    def __init__(self, config: dict):
        self.config = config
        self.sources = load_sources(config)
        self.browser = None
        self.playwright = None

    async def start_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)

    async def stop_browser(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def search_product(self, product: NormalisedProduct, max_candidates: int = 30) -> list[ImageCandidate]:
        """
        Orchestrates searching across tiers and search variants.
        """
        if not self.browser:
            await self.start_browser()

        all_candidates = []
        image_urls = set()

        # Domain controls
        whitelist = self.config.get("app_config", {}).get("domain_whitelist", [])
        blacklist = self.config.get("app_config", {}).get("domain_blacklist", [])

        tiers = get_tiers(self.sources)
        for tier in tiers:
            tier_sources = [s for s in self.sources if s.tier == tier]

            # Sort whitelist domains first in tier
            tier_sources.sort(key=lambda s: s.domain in whitelist, reverse=True)

            for source in tier_sources:
                if source.domain in blacklist:
                    continue

                for variant in product.search_variants:
                    if len(all_candidates) >= max_candidates:
                        return all_candidates

                    url = source.search_url_template.replace("{query}", variant.replace(" ", "+"))
                    candidates = await fetch_images_from_page(
                        url, variant, source.domain, source.tier, self.browser
                    )

                    for cand in candidates:
                        if cand.image_url not in image_urls:
                            all_candidates.append(cand)
                            image_urls.add(cand.image_url)

                        if len(all_candidates) >= max_candidates:
                            return all_candidates

        return all_candidates

def save_candidates(product_id: int, candidates: list[ImageCandidate]) -> None:
    """
    Writes candidates to the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        for cand in candidates:
            cursor.execute("""
                INSERT INTO candidates (
                    product_id, image_url, source_url, domain, page_title, alt_text, query_used, tier
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product_id,
                cand.image_url,
                cand.source_url,
                cand.domain,
                cand.page_title,
                cand.alt_text,
                cand.query_used,
                cand.tier
            ))
        conn.commit()
    except Exception as e:
        logger.error(f"Error saving candidates for product_id {product_id}: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
