"""
ProductRepository – all product and candidate_image persistence logic.

Raw SQL only — no ORM.  Every method opens and closes its own connection
via DatabaseManager.connection() so callers don't manage transactions.
"""

import logging
from datetime import datetime, timezone

from core.database import DatabaseManager
from core.models import CandidateImage, Product

logger = logging.getLogger(__name__)


def _now() -> str:
    """ISO-8601 timestamp in UTC, used for created_at / updated_at."""
    return datetime.now(timezone.utc).isoformat()


def _row_to_product(row) -> Product:
    return Product(
        id=row["id"],
        original_name=row["original_name"],
        cleaned_name=row["cleaned_name"],
        manual_search_query=row["manual_search_query"],
        approved_image_url=row["approved_image_url"],
        approved_source_url=row["approved_source_url"],
        downloaded_file_path=row["downloaded_file_path"],
        status=row["status"],
        notes=row["notes"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def _row_to_candidate(row) -> CandidateImage:
    return CandidateImage(
        id=row["id"],
        product_id=row["product_id"],
        image_url=row["image_url"],
        source_url=row["source_url"],
        position=row["position"],
        created_at=row["created_at"],
    )


class ProductRepository:
    def __init__(self, db: DatabaseManager) -> None:
        self._db = db

    # ── Aggregate queries (used by Dashboard) ─────────────────────────────

    def get_status_counts(self) -> dict[str, int]:
        """Return {status: count} for every status present in the table."""
        with self._db.connection() as conn:
            rows = conn.execute(
                "SELECT status, COUNT(*) AS cnt FROM products GROUP BY status"
            ).fetchall()
        return {row["status"]: row["cnt"] for row in rows}

    def get_total_count(self) -> int:
        with self._db.connection() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS cnt FROM products"
            ).fetchone()
        return row["cnt"] if row else 0

    def get_all_original_names_lower(self) -> set[str]:
        """Return a set of lowercase-stripped original_names for all products.
        Used by the importer for fast O(1) duplicate detection."""
        with self._db.connection() as conn:
            rows = conn.execute(
                "SELECT original_name FROM products"
            ).fetchall()
        return {row["original_name"].lower().strip() for row in rows}

    # ── Single-row CRUD ───────────────────────────────────────────────────

    def get_all(self) -> list[Product]:
        with self._db.connection() as conn:
            rows = conn.execute(
                "SELECT * FROM products ORDER BY created_at DESC"
            ).fetchall()
        return [_row_to_product(r) for r in rows]

    def get_by_id(self, product_id: int) -> Product | None:
        with self._db.connection() as conn:
            row = conn.execute(
                "SELECT * FROM products WHERE id = ?", (product_id,)
            ).fetchone()
        return _row_to_product(row) if row else None

    def create(self, original_name: str) -> Product:
        """Insert a new product with status='new' and return it."""
        now = _now()
        with self._db.connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO products (original_name, status, created_at, updated_at)
                VALUES (?, 'new', ?, ?)
                """,
                (original_name, now, now),
            )
            product_id = cursor.lastrowid
        logger.debug("Created product id=%s name=%r", product_id, original_name)
        return Product(
            id=product_id,
            original_name=original_name,
            cleaned_name=None,
            manual_search_query=None,
            approved_image_url=None,
            approved_source_url=None,
            downloaded_file_path=None,
            status="new",
            notes=None,
            created_at=now,
            updated_at=now,
        )

    def create_batch(self, names: list[str]) -> int:
        """Insert multiple products in a single transaction.
        Returns the number of rows inserted."""
        now = _now()
        rows = [(name, "new", now, now) for name in names if name.strip()]
        with self._db.connection() as conn:
            conn.executemany(
                """
                INSERT INTO products (original_name, status, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                rows,
            )
        logger.debug("Batch-inserted %d products", len(rows))
        return len(rows)

    def update(self, product: Product) -> None:
        """Persist all mutable fields of a Product back to the database."""
        product.updated_at = _now()
        with self._db.connection() as conn:
            conn.execute(
                """
                UPDATE products SET
                    cleaned_name         = ?,
                    manual_search_query  = ?,
                    approved_image_url   = ?,
                    approved_source_url  = ?,
                    downloaded_file_path = ?,
                    status               = ?,
                    notes                = ?,
                    updated_at           = ?
                WHERE id = ?
                """,
                (
                    product.cleaned_name,
                    product.manual_search_query,
                    product.approved_image_url,
                    product.approved_source_url,
                    product.downloaded_file_path,
                    product.status,
                    product.notes,
                    product.updated_at,
                    product.id,
                ),
            )
        logger.debug("Updated product id=%s status=%s", product.id, product.status)

    def update_status(self, product_id: int, status: str) -> None:
        """Lightweight status-only update — avoids loading the full row."""
        with self._db.connection() as conn:
            conn.execute(
                "UPDATE products SET status = ?, updated_at = ? WHERE id = ?",
                (status, _now(), product_id),
            )

    def delete(self, product_id: int) -> None:
        """Delete a product and all its candidates (CASCADE handles FK)."""
        with self._db.connection() as conn:
            conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        logger.debug("Deleted product id=%s", product_id)

    # ── Candidate images ──────────────────────────────────────────────────

    def get_candidates(self, product_id: int) -> list[CandidateImage]:
        with self._db.connection() as conn:
            rows = conn.execute(
                """
                SELECT * FROM candidate_images
                WHERE product_id = ?
                ORDER BY position ASC
                """,
                (product_id,),
            ).fetchall()
        return [_row_to_candidate(r) for r in rows]

    def add_candidate(
        self,
        product_id: int,
        image_url: str,
        source_url: str | None,
        position: int | None,
    ) -> CandidateImage:
        now = _now()
        with self._db.connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO candidate_images
                    (product_id, image_url, source_url, position, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (product_id, image_url, source_url, position, now),
            )
            candidate_id = cursor.lastrowid
        return CandidateImage(
            id=candidate_id,
            product_id=product_id,
            image_url=image_url,
            source_url=source_url,
            position=position,
            created_at=now,
        )

    def delete_candidates(self, product_id: int) -> None:
        """Clear all candidate images for a product (e.g. before a re-search)."""
        with self._db.connection() as conn:
            conn.execute(
                "DELETE FROM candidate_images WHERE product_id = ?", (product_id,)
            )
