"""Search Queue – manage and run image searches for queued products."""

from ui.views.base_view import BaseView


class SearchQueueView(BaseView):
    def __init__(self) -> None:
        super().__init__(
            title="Search Queue",
            subtitle="Products pending image search. Run searches individually or in batch via Playwright.",
            placeholder_icon="⊙",
            placeholder_text="The search queue, run controls, and per-product progress will appear here.",
        )
