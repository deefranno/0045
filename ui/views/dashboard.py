"""Dashboard – summary overview of the product image workflow."""

from ui.views.base_view import BaseView


class DashboardView(BaseView):
    def __init__(self) -> None:
        super().__init__(
            title="Dashboard",
            subtitle="Overview of your product image workflow — totals, status counts, and recent activity.",
            placeholder_icon="▦",
            placeholder_text="Summary statistics and workflow progress will appear here.",
        )
