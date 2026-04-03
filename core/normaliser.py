import re
from dataclasses import dataclass, field
from utils.logger import logger

@dataclass
class NormalisedProduct:
    raw_name: str
    cleaned_name: str = ""
    brand: str = ""
    product_type: str = ""
    size: str = ""
    pack_quantity: int = 1
    tokens: list[str] = field(default_factory=list)
    search_variants: list[str] = field(default_factory=list)

def normalise(raw_name: str, config: dict) -> NormalisedProduct:
    """
    Processing Pipeline for product name normalisation.
    """
    if not raw_name:
        return NormalisedProduct(raw_name="")

    try:
        # 1. Uppercase -> lowercase
        name = raw_name.lower()

        # 2. Expand abbreviations
        abbrevs = config.get("abbreviations", {})
        # Sort by length descending to match longest first
        sorted_abbrevs = sorted(abbrevs.keys(), key=len, reverse=True)
        for abbrev in sorted_abbrevs:
            pattern = r'\b' + re.escape(abbrev.lower()) + r'\b'
            name = re.sub(pattern, abbrevs[abbrev].lower(), name)

        # 3. Extract pack pattern: NxSIZE (e.g. 12X2LB, 10X50G)
        pack_quantity = 1
        size = ""
        pack_match = re.search(r'(\d+)\s*x\s*(\d+(?:\.\d+)?\s*(?:lb|g|kg|ml|oz|cl|l))', name)
        if pack_match:
            pack_quantity = int(pack_match.group(1))
            size = pack_match.group(2).strip().upper()
            name = name.replace(pack_match.group(0), "")

        # 4. Extract standalone size: 500G, 900ML, 15OZ, 2LB, etc.
        if not size:
            size_match = re.search(r'(\d+(?:\.\d+)?\s*(?:lb|g|kg|ml|oz|cl|l))\b', name)
            if size_match:
                size = size_match.group(1).strip().upper()
                name = name.replace(size_match.group(0), "")

        # 5. Detect brand
        brands = config.get("brands", [])
        detected_brand = ""
        # Clean name of multiple spaces for brand matching
        name = " ".join(name.split())
        for brand in sorted(brands, key=len, reverse=True):
            if name.startswith(brand.lower()):
                detected_brand = brand
                name = name[len(brand):].strip()
                break

        # 6. Apply synonyms
        synonyms = config.get("synonyms", {})
        tokens = name.split()
        cleaned_tokens = []
        for token in tokens:
            if token.upper() in synonyms:
                cleaned_tokens.append(synonyms[token.upper()].lower())
            else:
                cleaned_tokens.append(token)

        # 7. Reconstruct cleaned_name
        cleaned_name = " ".join(cleaned_tokens)
        if detected_brand:
            cleaned_name = f"{detected_brand} {cleaned_name}".strip()

        # 8. Infer product_type (last meaningful noun)
        # For simplicity, we'll take the last token as product_type if it exists
        product_type = cleaned_tokens[-1] if cleaned_tokens else ""

        # 9. Generate search_variants
        search_variants = []
        b = detected_brand
        pt = product_type
        s = size
        cn = " ".join(cleaned_tokens)

        # brand + product_type + size
        if b and pt and s: search_variants.append(f"{b} {pt} {s}")
        # brand + cleaned_name
        if b and cn: search_variants.append(f"{b} {cn}")
        # product_type + size (no brand)
        if pt and s: search_variants.append(f"{pt} {s}")
        # cleaned_name only
        if cn: search_variants.append(cn)
        # brand + product_type (no size)
        if b and pt: search_variants.append(f"{b} {pt}")

        # Fill up to 5 if needed
        if len(search_variants) < 5 and raw_name:
            search_variants.append(raw_name)

        return NormalisedProduct(
            raw_name=raw_name,
            cleaned_name=cleaned_name,
            brand=detected_brand,
            product_type=product_type,
            size=size,
            pack_quantity=pack_quantity,
            tokens=cleaned_tokens,
            search_variants=list(dict.fromkeys(search_variants)) # deduplicate
        )

    except Exception as e:
        logger.error(f"Normalisation failed for '{raw_name}': {e}")
        return NormalisedProduct(raw_name=raw_name)

def batch_normalise(names: list[str], config: dict) -> list[NormalisedProduct]:
    results = []
    for name in names:
        results.append(normalise(name, config))
    return results
