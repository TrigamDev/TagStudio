from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from tagstudio.qt.views.panel_modal import PanelWidget


class SearchPanelView(PanelWidget):

    def __init__(self) -> None:
        super().__init__()

        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(6, 0, 6, 0)
        self.setMinimumSize(300, 400)

        # Limit container
        self.limit_container = QWidget()
        self.root_layout.addWidget(self.limit_container)

        self.limit_layout = QHBoxLayout(self.limit_container)
        self.limit_layout.setContentsMargins(0, 0, 0, 0)
        self.limit_layout.setSpacing(12)
        self.limit_layout.addStretch(1)

        self.limit_title = QLabel()
        self.limit_layout.addWidget(self.limit_title)

        # Limit dropdown
        self.limit_combobox = QComboBox()
        self.limit_combobox.setEditable(False)
        self.limit_layout.addWidget(self.limit_combobox)
        self.limit_layout.addStretch(1)

        # Search field
        self.search_field = QLineEdit()
        self.search_field.setObjectName("search_field")
        self.search_field.setMinimumSize(QSize(0, 32))

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
