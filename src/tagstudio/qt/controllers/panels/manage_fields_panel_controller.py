import typing

from tagstudio.core.library.alchemy.models import ValueType
from tagstudio.qt.controllers.panels.search_panel_controller import SearchPanel
from tagstudio.qt.views.panels.manage_fields_panel_view import ManageFieldsPanelView

if typing.TYPE_CHECKING:
    from tagstudio.core.library.alchemy.library import Library


class ManageFieldsPanel(SearchPanel[ValueType], ManageFieldsPanelView):

    def __init__(self, lib: "Library"):
        super().__init__()
        self.lib = lib

    def search(self, query: str | None) -> list[ValueType]:
        search_set: set[ValueType] = self.lib.search_fields(query)
        results = list(search_set)
        results.sort(key=lambda field: field.name.lower())
        return results
