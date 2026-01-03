
import structlog
from PySide6.QtCore import Signal

from tagstudio.qt.translations import Translations
from tagstudio.qt.views.panels.search_panel_view import SearchPanelView

logger = structlog.get_logger(__name__)

class SearchPanel[T](SearchPanelView):
    item_chosen = Signal(type[T])

    is_picker: bool = False

    _limit_items: list[tuple[str, int]] = [
        ("25", 25),
        ("50", 50),
        ("100", 100),
        ("250", 250),
        ("500", 500),
        (Translations["tag.all_tags"], -1)
    ]
    _default_limit_index: int = 0

    __current_limit_index: int = _default_limit_index
    __previous_limit_index: int = _default_limit_index

    __search_results: list[T] = []

    def __init__(self) -> None:
        super().__init__()

        # Limit dropdown
        self.limit_combobox.addItems([ label for label, value in self._limit_items ])
        self.limit_combobox.setCurrentIndex(self._default_limit_index)

        self.limit_combobox.currentIndexChanged.connect(self.update_limit)

        # Search field
        self.search_field.textEdited.connect(lambda text: self.update_items(text))
        self.search_field.returnPressed.connect(lambda: self.on_return(self.search_field.text()))

    def update_limit(self, index: int) -> None:
        logger.info("[SearchPanel] Updating limit")
        self.__current_limit_index = index

        # Method was called outside the limit_combobox callback
        if index != self.limit_combobox.currentIndex():
            self.limit_combobox.setCurrentIndex(index)

        if self.__previous_limit_index == self.__current_limit_index:
            return

        self.update_items(self.search_field.text())

    def update_items(self, query: str | None) -> None:
        query_lower = "" if not query else query.lower()
        search_results = self.search(query_lower)

    def search(self, query: str | None) -> list[T]:
        raise NotImplementedError

    def on_return(self, text: str) -> None:
        if not text:
            self.search_field.setFocus()
            self.parentWidget().hide()
            return

        if self.__search_results.__getitem__(0) is None:
            # self.create_and_add_tag(text)
            return

        if self.is_picker:
            self.item_chosen.emit(self.__search_results.__getitem__(0))

        self.search_field.setText("")
        self.update_items("")

