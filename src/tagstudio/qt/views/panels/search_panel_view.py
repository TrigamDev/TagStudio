from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel, QComboBox, QLineEdit, QScrollArea, QFrame

from tagstudio.core.library.alchemy.library import Library
from tagstudio.qt.translations import Translations
from tagstudio.qt.views.panel_modal import PanelModal, PanelWidget


class SearchPanel(PanelWidget):

    def __init__(self, library: Library) -> None:
        super().__init__()

        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(6, 0, 6, 0)

        # Limit container
        self.limit_container = QWidget()
        self.root_layout.addWidget(self.limit_container)

        self.limit_layout = QHBoxLayout(self.limit_container)
        self.limit_layout.setContentsMargins(0, 0, 0, 0)
        self.limit_layout.setSpacing(12)
        self.limit_layout.addStretch(1)

        self.limit_title = QLabel(Translations["tag.view_limit"])
        self.limit_layout.addWidget(self.limit_title)

        # Limit dropdown
        self.limit_combobox = QComboBox()
        self.limit_combobox.setEditable(False)
        self.limit_combobox.addItems([str(x) for x in TagSearchPanel._limit_items])
        self.limit_combobox.setCurrentIndex(TagSearchPanel._default_limit_idx)
        self.limit_combobox.currentIndexChanged.connect(self.update_limit)
        self.previous_limit: int = (
            TagSearchPanel.tag_limit if isinstance(TagSearchPanel.tag_limit, int) else -1
        )
        self.limit_layout.addWidget(self.limit_combobox)
        self.limit_layout.addStretch(1)

        # Search field
        self.search_field = QLineEdit()
        self.search_field.setObjectName("search_field")
        self.search_field.setMinimumSize(QSize(0, 32))
        self.search_field.setPlaceholderText(Translations["home.search_tags"])
        self.search_field.textEdited.connect(lambda text: self.g(text))
        self.search_field.returnPressed.connect(lambda: self.on_return(self.search_field.text()))

        self.root_layout.addWidget(self.search_field)

        # Scroll area
        self.scroll_contents = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_contents)
        self.scroll_layout.setContentsMargins(6, 0, 6, 0)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShadow(QFrame.Shadow.Plain)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setWidget(self.scroll_contents)

        self.root_layout.addWidget(self.scroll_area)

    def search(self, query: str | None) -> None:
        raise NotImplementedError
