import threading
import asyncio
from PySide6.QtCore import QThread, Signal
from core.normaliser import normalise
from core.search_engine import SearchEngine, save_candidates
from core.scorer import score_candidates
from core.scorer_store import save_scores
from core.normaliser_store import save_normalised
from core.database import get_connection
from core.retry_queue import add_to_retry, mark_attempt, mark_resolved
from utils.logger import logger

class SearchWorker(QThread):
    progress = Signal(int)
    status_message = Signal(str)
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, product_ids, config):
        super().__init__()
        self.product_ids = product_ids
        self.config = config
        self.pause_event = threading.Event()
        self.pause_event.set() # Default to not paused
        self.cancel_event = threading.Event()
        self.cancel_event.clear()

    def run(self):
        try:
            asyncio.run(self._run_async())
        except Exception as e:
            logger.error(f"Worker error: {e}")
            self.error.emit(str(e))

    async def _run_async(self):
        engine = SearchEngine(self.config)
        await engine.start_browser()

        results = []
        total = len(self.product_ids)

        for i, p_id in enumerate(self.product_ids):
            # Check for cancel
            if self.cancel_event.is_set():
                break

            # Check for pause
            self.pause_event.wait()

            try:
                mark_attempt(p_id)
                # 1. Fetch product
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT raw_name FROM products WHERE id = ?", (p_id,))
                row = cursor.fetchone()
                conn.close()

                if not row: continue
                raw_name = row['raw_name']

                self.status_message.emit(f"Processing: {raw_name}")

                # 2. Normalise
                norm = normalise(raw_name, self.config)
                save_normalised(p_id, norm)

                # 3. Search
                candidates = await engine.search_product(norm)
                save_candidates(p_id, candidates)

                # 4. Score
                scored = score_candidates(norm, candidates, self.config)
                save_scores(p_id, scored)
                mark_resolved(p_id)
                results.append(p_id)

            except Exception as e:
                logger.error(f"Failed to process product {p_id}: {e}")
                add_to_retry(p_id, str(e))

            # Emit progress
            prog_val = int(((i + 1) / total) * 100)
            self.progress.emit(prog_val)

        await engine.stop_browser()
        self.finished.emit(results)

    def pause(self):
        self.pause_event.clear()

    def resume(self):
        self.pause_event.set()

    def cancel(self):
        self.cancel_event.set()
        self.pause_event.set() # Resume so it can check the cancel event
