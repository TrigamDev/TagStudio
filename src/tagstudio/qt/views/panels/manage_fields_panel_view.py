
import structlog

from tagstudio.qt.translations import Translations
from tagstudio.qt.views.panels.search_panel_view import SearchPanelView

logger = structlog.get_logger(__name__)


class ManageFieldsPanelView(SearchPanelView):

    def __init__(self):
        super().__init__()

        self.limit_title.setText(Translations["field.view_limit"])
        self.search_field.setPlaceholderText(Translations["home.search_fields"])

    # def update_fields(self, query: str | None = None):
    #     """Update the field list given a search query."""
    #     logger.info("[ManageFieldsPanel] Updating Fields")
    #
    #     # Get results for the search query
    #     query_lower = "" if not query else query.lower()
    #     field_results: set[ValueType] = self.lib.search_fields(name=query)
    #
    #     # Sort and prioritize the results
    #     results = list(field_results)
    #     results.sort(key=lambda field: field.name.lower())
    #     priority_results: set[ValueType] = set()
    #
    #     if query and query.strip():
    #         for tag in results:
    #             if tag.name.lower().startswith(query_lower):
    #                 priority_results.add(tag)
    #
    #     all_results: list[ValueType] = sorted(
    #         list(priority_results), key=lambda field: len(field.name)
    #     ) + [
    #         r for r in results if r not in priority_results
    #     ]
    #
    #     if all_results:
    #         self.first_field_key = None
    #         self.first_field_key = all_results[0].key if len(all_results) > 0 else all_results[0].key
    #
    #     else:
    #         self.first_field_key = None
    #
    #     # Update every tag widget with the new search result data
    #     #norm_previous = self.previous_limit if self.previous_limit > 0 else len(self.lib.tags)
    #     #norm_limit = tag_limit if tag_limit > 0 else len(self.lib.tags)
    #     #range_limit = max(norm_previous, norm_limit)
    #     for i in range(0, len(all_results)):
    #     #    tag = None
    #     #    with contextlib.suppress(IndexError):
    #     #        tag = all_results[i]
    #         self.set_field_widget(field=all_results[i], index=i)
    #     #self.previous_limit = tag_limit
    #
    #     # Add back the "Create & Add" button
    #     #if query and query.strip():
    #     #    cb: QPushButton = self.build_create_button(query)
    #     #    cb.setText(Translations.format("tag.create_add", query=query))
    #     #    with catch_warnings(record=True):
    #     #        cb.clicked.disconnect()
    #     #    cb.clicked.connect(lambda: self.create_and_add_tag(query or ""))
    #     #    self.scroll_layout.addWidget(cb)
    #     #    self.create_button_in_layout = True
    #
    # def set_field_widget(self, field: ValueType | None, index: int):
    #     """Set the tag of a tag widget at a specific index."""
    #     # Create any new tag widgets needed up to the given index
    #     if self.scroll_layout.count() <= index:
    #         while self.scroll_layout.count() <= index:
    #             field_type_widget = FieldTypeWidget(field_type=field, has_edit=True, has_remove=True, library=self.lib)
    #             field_type_widget.setHidden(True)
    #             self.scroll_layout.addWidget(field_type_widget)
    #
    #     # Assign the tag to the widget at the given index.
    #     field_type_widget: FieldTypeWidget = self.scroll_layout.itemAt(index).widget()  # pyright: ignore[reportAssignmentType]
    #     assert isinstance(field_type_widget, FieldTypeWidget)
    #     field_type_widget.set_field_type(field)
    #
    #     # Set tag widget viability and potentially return early
    #     field_type_widget.setHidden(bool(not field))
    #     if not field:
    #         return
    #
    #     # Configure any other aspects of the tag widget
    #     has_remove_button = False
    #     field_type_widget.has_remove = has_remove_button
    #
    #     with catch_warnings(record=True):
    #         field_type_widget.on_edit.disconnect()
    #         field_type_widget.on_remove.disconnect()
    #         field_type_widget.bg_button.clicked.disconnect()
    #
    #     field_key = field.key
    #     field_type_widget.on_edit.connect(lambda field: self.edit_field(field))
    #     field_type_widget.on_remove.connect(lambda field: self.delete_field(field))
    #     field_type_widget.bg_button.clicked.connect(lambda: self.field_chosen.emit(field.key))
    #
    # def showEvent(self, event: QShowEvent) -> None:  # noqa N802
    #     self.update_fields()
    #     self.scroll_area.verticalScrollBar().setValue(0)
    #     self.search_field.setText("")
    #     self.search_field.setFocus()
    #     return super().showEvent(event)