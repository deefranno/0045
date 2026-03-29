"""Import Products – load a TXT or CSV product list and preview cleaned names."""

from ui.views.base_view import BaseView


class ImportProductsView(BaseView):
    def __init__(self) -> None:
        super().__init__(
            title="Import Products",
            subtitle="Load a .txt or .csv file containing product names. Names will be cleaned and queued for image search.",
            placeholder_icon="⊕",
            placeholder_text="File import, name preview, and cleaning options will appear here.",
        )
