from typing import TYPE_CHECKING, Callable, override

from PySide6.QtGui import QAction, QEnterEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtCore import QEvent, Qt, Signal

from tagstudio.core.library.alchemy.models import ValueType
from tagstudio.qt.helpers.escape_text import escape_text
from tagstudio.qt.translations import Translations

if TYPE_CHECKING:
    from tagstudio.core.library.alchemy.library import Library

class FieldTypeWidget(QWidget):

    on_remove = Signal()
    on_click = Signal()
    on_edit = Signal()

    field_type: ValueType | None = None

    def __init__(
        self,
        field_type: ValueType | None,
        has_edit: bool,
        has_remove: bool,
        library: "Library | None" = None,
        on_remove_callback: Callable[[], None] | None = None,
        on_click_callback: Callable[[], None] | None = None,
        on_edit_callback: Callable[[], None] | None = None,
    ) -> None:
        super().__init__()
        self.field_type = field_type
        self.lib: Library | None = library
        self.has_edit = has_edit
        self.has_remove = has_remove

        # If on_click_callback:
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setObjectName("root_layout")
        self.root_layout.setContentsMargins(0, 0, 0, 0)

        self.bg_button = QPushButton(self)
        self.bg_button.setFlat(True)

        # Inner layout
        self.inner_layout = QHBoxLayout()
        self.inner_layout.setObjectName("inner_layout")
        self.inner_layout.setContentsMargins(0, 0, 0, 0)

        # Remove button
        self.remove_button = QPushButton(self)
        self.remove_button.setFlat(True)
        self.remove_button.setText("–")
        self.remove_button.setHidden(True)
        self.remove_button.setMinimumSize(22, 22)
        self.remove_button.setMaximumSize(22, 22)
        self.remove_button.clicked.connect(self.on_remove.emit)
        self.remove_button.setHidden(True)

        self.inner_layout.addWidget(self.remove_button)
        self.inner_layout.addStretch(1)

        # Background button
        self.bg_button.setLayout(self.inner_layout)
        self.bg_button.setMinimumSize(44, 22)

        self.bg_button.setMinimumHeight(22)
        self.bg_button.setMaximumHeight(22)

        self.root_layout.addWidget(self.bg_button)

        # NOTE: Do this if you don't want the tag to stretch, like in a search.
        # self.bg_button.setMaximumWidth(self.bg_button.sizeHint().width())

        # Add callbacks
        if on_remove_callback is not None:
            self.on_remove.connect(on_remove_callback)
        if on_click_callback is not None:
            self.on_click.connect(on_click_callback)
        if on_edit_callback is not None:
            self.on_edit.connect(on_edit_callback)

        # Add edit action
        if has_edit:
            edit_action = QAction(self)
            edit_action.setText(Translations["generic.edit"])
            edit_action.triggered.connect(self.on_edit.emit)
            self.bg_button.addAction(edit_action)
        # If on_click_callback:
        self.bg_button.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)

        self.bg_button.clicked.connect(self.on_click.emit)

        self.set_field_type(field_type)

    def set_field_type(self, field_type: ValueType | None) -> None:
        self.field_type = field_type

        if not field_type:
            return

        if self.lib:
            self.bg_button.setText(escape_text(field_type.name))
        else:
            self.bg_button.setText(escape_text(field_type.name))

    def set_has_remove(self, has_remove: bool):
        self.has_remove = has_remove

    @override
    def enterEvent(self, event: QEnterEvent) -> None:
        if self.has_remove:
            self.remove_button.setHidden(False)
        self.update()
        return super().enterEvent(event)

    @override
    def leaveEvent(self, event: QEvent) -> None:
        if self.has_remove:
            self.remove_button.setHidden(True)
        self.update()
        return super().leaveEvent(event)
