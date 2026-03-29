"""Exports – download approved images and export results as CSV or JSON."""

from ui.views.base_view import BaseView


class ExportsView(BaseView):
    def __init__(self) -> None:
        super().__init__(
            title="Exports",
            subtitle="Download approved images locally and export the full results as CSV or JSON.",
            placeholder_icon="↗",
            placeholder_text="Export options, download progress, and output path settings will appear here.",
        )
