"""
DatabaseManager – owns the SQLite connection lifecycle and schema.

One DatabaseManager instance is created at startup and passed to
repositories.  Every public method opens a fresh connection, does its
work, and closes it.  This is intentionally simple and safe for a
single-user desktop app; no connection pool is needed.

Database file location:
    <project_root>/data/products.db
    Created automatically on first run.
"""

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

logger = logging.getLogger(__name__)

# ── Schema DDL ────────────────────────────────────────────────────────────────
#
# executescript() is used for the DDL so all statements run in one shot.
# Individual queries use parameterised execute() calls.

_DDL = """
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS products (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    original_name        TEXT    NOT NULL,
    cleaned_name         TEXT,
    manual_search_query  TEXT,
    approved_image_url   TEXT,
    approved_source_url  TEXT,
    downloaded_file_path TEXT,
    status               TEXT    NOT NULL DEFAULT 'new',
    notes                TEXT,
    created_at           TEXT    NOT NULL,
    updated_at           TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS candidate_images (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id  INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    image_url   TEXT    NOT NULL,
    source_url  TEXT,
    position    INTEGER,
    created_at  TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_products_status
    ON products(status);

CREATE INDEX IF NOT EXISTS idx_candidates_product
    ON candidate_images(product_id);
"""


class DatabaseManager:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        # Ensure the data directory exists before any connection is attempted
        db_path.parent.mkdir(parents=True, exist_ok=True)

    # ── Schema init ───────────────────────────────────────────────────────────

    def initialize(self) -> None:
        """Create all tables and indexes if they don't already exist.
        Safe to call every startup — all statements use IF NOT EXISTS."""
        logger.info("Initialising database at %s", self.db_path)
        # executescript() manages its own implicit transaction, so we don't
        # use the context manager here.
        conn = sqlite3.connect(self.db_path)
        try:
            conn.executescript(_DDL)
            conn.commit()
        finally:
            conn.close()
        logger.info("Database ready")

    # ── Connection context manager ─────────────────────────────────────────

    @contextmanager
    def connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Yield a connection with foreign keys enabled and row_factory set.
        Commits on clean exit; rolls back on any exception."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
