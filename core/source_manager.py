from dataclasses import dataclass
from utils.logger import logger

@dataclass
class Source:
    tier: int
    name: str
    domain: str
    enabled: bool
    search_url_template: str
    type: str

def load_sources(config: dict) -> list[Source]:
    """
    Parses sources.json, returns only enabled sources sorted by tier.
    """
    sources_data = config.get("sources", [])
    sources = []

    for s in sources_data:
        if s.get("enabled", True):
            sources.append(Source(
                tier=int(s.get("tier", 99)),
                name=s.get("name", "Unknown"),
                domain=s.get("domain", ""),
                enabled=True,
                search_url_template=s.get("search_url_template", ""),
                type=s.get("type", "scrape")
            ))

    return sorted(sources, key=lambda x: x.tier)

def get_tiers(sources: list[Source]) -> list[int]:
    """
    Returns distinct tier numbers present in enabled sources.
    """
    return sorted(list(set(s.tier for s in sources)))
