from dataclasses import dataclass
from rapidfuzz import fuzz
import re
from core.normaliser import NormalisedProduct
from core.scraper import ImageCandidate
from utils.logger import logger

@dataclass
class ScoredCandidate:
    image_url: str
    source_url: str
    domain: str
    page_title: str
    alt_text: str
    score: int
    confidence_band: str
    explanation: list[str]

def score_candidates(product: NormalisedProduct, candidates: list[ImageCandidate], config: dict) -> list[ScoredCandidate]:
    """
    Applies the scoring rubric to candidates and returns them sorted by score descending.
    """
    scored = []

    trusted_domains = config.get("app_config", {}).get("trusted_domains", [])
    domain_blacklist = config.get("app_config", {}).get("domain_blacklist", [])

    for cand in candidates:
        score = 0
        explanation = []

        try:
            # Fuzzy name match (RapidFuzz token_sort_ratio)
            ratio = fuzz.token_sort_ratio(product.cleaned_name.lower(), cand.page_title.lower())
            if ratio >= 90:
                score += 30
                explanation.append(f"Fuzzy name match >= 90% ({ratio}%)")
            elif ratio >= 70:
                score += 20
                explanation.append(f"Fuzzy name match 70-89% ({ratio}%)")
            elif ratio >= 50:
                score += 10
                explanation.append(f"Fuzzy name match 50-69% ({ratio}%)")

            # Brand match (exact, case-insensitive)
            if product.brand and (product.brand.lower() in cand.page_title.lower() or product.brand.lower() in cand.alt_text.lower()):
                score += 15
                explanation.append("Brand match")

            # Size match (same unit and value)
            if product.size and (product.size.upper() in cand.page_title.upper() or product.size.upper() in cand.alt_text.upper()):
                score += 10
                explanation.append("Size match")

            # Product type match
            if product.product_type and (product.product_type.lower() in cand.page_title.lower() or product.product_type.lower() in cand.alt_text.lower()):
                score += 10
                explanation.append("Product type match")

            # Phase 6 additions: Wrong brand/size detection
            # For simplicity, we check if any other known brand/size is mentioned that isn't the product's
            # Actually, the requirement says "Wrong brand detected in alt_text or page_title"
            # We'll check if a different brand from config is present
            other_brands = config.get("brands", [])
            for b in other_brands:
                if b.lower() != product.brand.lower() and b.lower() in cand.page_title.lower():
                    score -= 20
                    explanation.append(f"Wrong brand detected: {b}")
                    break

            # Wrong size (This is tricky, but let's look for a different size pattern)
            if product.size:
                # Look for patterns like \d+(LB|G|KG|ML|OZ)
                size_patterns = re.findall(r'(\d+(?:\.\d+)?\s*(?:LB|G|KG|ML|OZ|CL|L))', cand.page_title.upper())
                for s in size_patterns:
                    if s != product.size.upper():
                        score -= 15
                        explanation.append(f"Wrong size detected: {s}")
                        break

            # Trusted domain
            if cand.domain in trusted_domains:
                score += 10
                explanation.append("Trusted domain")

            # Domain blacklist
            if cand.domain in domain_blacklist:
                score -= 10
                explanation.append("Blacklisted domain")

            # Irrelevant keywords
            irrelevant_keywords = ["logo", "icon", "banner", "avatar", "sprite"]
            if any(k in cand.image_url.lower() for k in irrelevant_keywords):
                score -= 10
                explanation.append("Irrelevant keyword in image_url")

            # Cap and floor
            score = max(0, min(100, score))

            # Confidence Band
            if score >= 85: band = "auto_accept"
            elif score >= 60: band = "review"
            else: band = "reject"

            scored.append(ScoredCandidate(
                image_url=cand.image_url,
                source_url=cand.source_url,
                domain=cand.domain,
                page_title=cand.page_title,
                alt_text=cand.alt_text,
                score=score,
                confidence_band=band,
                explanation=explanation
            ))

        except Exception as e:
            logger.error(f"Scoring error for candidate {cand.image_url}: {e}")
            scored.append(ScoredCandidate(
                image_url=cand.image_url,
                source_url=cand.source_url,
                domain=cand.domain,
                page_title=cand.page_title,
                alt_text=cand.alt_text,
                score=0,
                confidence_band="reject",
                explanation=["scoring_error"]
            ))

    return sorted(scored, key=lambda x: x.score, reverse=True)

def get_best_match(scored: list[ScoredCandidate]) -> ScoredCandidate | None:
    return scored[0] if scored else None
