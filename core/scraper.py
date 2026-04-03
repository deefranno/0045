import asyncio
import httpx
from playwright.async_api import async_playwright
from dataclasses import dataclass
from utils.logger import logger
import time
from urllib.parse import urljoin, urlparse

@dataclass
class ImageCandidate:
    image_url: str
    source_url: str
    domain: str
    page_title: str
    alt_text: str
    query_used: str
    tier: int

# Global state for rate limiting
last_request_time = {} # domain -> float

async def fetch_images_from_page(url: str, query: str, domain: str, tier: int, browser_context=None) -> list[ImageCandidate]:
    """
    Navigates to url, extracts images, filters and returns candidates.
    """
    # Rate limiting: minimum 1.5 seconds between requests to same domain
    now = time.time()
    if domain in last_request_time:
        wait_time = 1.5 - (now - last_request_time[domain])
        if wait_time > 0:
            await asyncio.sleep(wait_time)

    last_request_time[domain] = time.time()

    candidates = []

    try:
        page = await browser_context.new_page()
        await page.goto(url, timeout=15000, wait_until="domcontentloaded")

        # Extract title
        page_title = await page.title()

        # Extract <img> tags
        img_elements = await page.query_selector_all("img")

        for img in img_elements:
            src = await img.get_attribute("src")
            alt = await img.get_attribute("alt") or ""

            if not src:
                continue

            # Make absolute URL
            abs_url = urljoin(url, src)

            # Simple size filtering via attributes
            try:
                width = await img.get_attribute("width")
                height = await img.get_attribute("height")
                if width and height and (int(width) < 100 or int(height) < 100):
                    continue
            except (ValueError, TypeError):
                pass

            # Find closest ancestor <a>
            source_url = url
            try:
                # Use evaluate to find the closest link
                href = await img.evaluate("""(element) => {
                    const anchor = element.closest('a');
                    return anchor ? anchor.href : null;
                }""")
                if href:
                    source_url = href
            except Exception as e:
                logger.debug(f"Could not find ancestor anchor: {e}")

            # Phase 9: Image Validation
            valid, reason = validate_image(abs_url)
            if not valid:
                logger.debug(f"Skipping invalid image {abs_url}: {reason}")
                continue

            candidates.append(ImageCandidate(
                image_url=abs_url,
                source_url=source_url,
                domain=domain,
                page_title=page_title,
                alt_text=alt,
                query_used=query,
                tier=tier
            ))

            if len(candidates) >= 10:
                break

        await page.close()

    except Exception as e:
        logger.error(f"Scraper error for {url}: {e}")

    return candidates

# For Phase 9 image validation
def validate_image(url: str) -> tuple[bool, str]:
    """
    Performs HEAD request, checks Content-Type and dimensions.
    """
    try:
        with httpx.Client(timeout=5) as client:
            resp = client.head(url)
            if resp.status_code != 200:
                return False, f"HTTP {resp.status_code}"

            content_type = resp.headers.get("Content-Type", "")
            if not any(t in content_type for t in ["image/jpeg", "image/png", "image/webp"]):
                return False, f"Invalid Content-Type: {content_type}"

            # Size check via GET (max 2MB)
            resp = client.get(url, follow_redirects=True)
            if len(resp.content) > 2*1024*1024:
                return False, "File too large"

            from PIL import Image
            from io import BytesIO
            img = Image.open(BytesIO(resp.content))
            w, h = img.size
            if w < 200 or h < 200:
                return False, f"Image too small: {w}x{h}"

            return True, ""
    except Exception as e:
        return False, str(e)
