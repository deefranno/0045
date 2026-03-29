"""Settings – configure application preferences and storage paths."""

from ui.views.base_view import BaseView


class SettingsView(BaseView):
    def __init__(self) -> None:
        super().__init__(
            title="Settings",
            subtitle="Configure output directories, search engine preferences, and application behaviour.",
            placeholder_icon="⚙",
            placeholder_text="Application settings and configuration options will appear here.",
        )
