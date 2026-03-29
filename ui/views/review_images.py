"""Review Images – visually approve or reject candidate images per product."""

from ui.views.base_view import BaseView


class ReviewImagesView(BaseView):
    def __init__(self) -> None:
        super().__init__(
            title="Review Images",
            subtitle="Browse candidate images for each product and mark the best match as approved.",
            placeholder_icon="◫",
            placeholder_text="Product image grid, approve/reject controls, and notes will appear here.",
        )
