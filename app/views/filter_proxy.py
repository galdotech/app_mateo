from PySide6.QtCore import QSortFilterProxyModel, Qt


class MultiFilterProxyModel(QSortFilterProxyModel):
    """Proxy model allowing case-insensitive contains filtering on multiple columns."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._filters: dict[int, str] = {}
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)

    def setFilterForColumn(self, column: int, pattern: str) -> None:
        self._filters[column] = pattern.lower()
        self.invalidateFilter()

    def clearFilters(self) -> None:
        self._filters.clear()
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent):  # type: ignore[override]
        model = self.sourceModel()
        for column, pattern in self._filters.items():
            if pattern:
                index = model.index(source_row, column, source_parent)
                data = model.data(index, Qt.DisplayRole)
                if data is None or pattern not in str(data).lower():
                    return False
        return True
