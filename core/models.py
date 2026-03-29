"""
Data model classes for Product Image Finder.
Plain dataclasses — no ORM, no magic.
"""

from dataclasses import dataclass

# All valid status values in workflow order.
# Used for validation and UI labelling across the app.
PRODUCT_STATUSES: list[str] = [
    "new",
    "cleaned",
    "searched",
    "found",
    "approved",
    "rejected",
    "downloaded",
    "exported",
    "error",
]

# Statuses that count as "terminal positive" (work is done)
APPROVED_STATUSES: frozenset[str] = frozenset({"approved", "downloaded", "exported"})

# Statuses that count as "still in progress / pending action"
PENDING_STATUSES: frozenset[str] = frozenset({"new", "cleaned", "searched", "found"})


@dataclass
class Product:
    id: int | None
    original_name: str
    cleaned_name: str | None
    manual_search_query: str | None
    approved_image_url: str | None
    approved_source_url: str | None
    downloaded_file_path: str | None
    status: str
    notes: str | None
    created_at: str
    updated_at: str


@dataclass
class CandidateImage:
    id: int | None
    product_id: int
    image_url: str
    source_url: str | None
    position: int | None
    created_at: str
