# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QDialog,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QMainWindow,
)
from PySide6.QtGui import QIcon


class BaseDialog(QDialog):
    """Diálogo base con utilidades comunes."""

    def _set_button_icon(self, btn: QPushButton, resource: str) -> None:
        icon = QIcon(resource)
        if not icon.isNull():
            btn.setIcon(icon)

    def _show_status(self, text: str) -> None:
        parent = self.parent()
        if isinstance(parent, QMainWindow):
            parent.statusBar().showMessage(text, 3000)

    def _set_error(self, widget: QLineEdit, state: bool) -> None:
        widget.setProperty("error", state)
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def _build_filters(self, layout, specs, insert_index: int) -> None:
        """Create a row of filter widgets.

        Args:
            layout: Layout where the filter row will be inserted.
            specs: Iterable of (label, column) pairs.
            insert_index: Position to insert the filter row.
        """
        self._filter_widgets: list[QLineEdit] = []
        row = QHBoxLayout()
        for label, column in specs:
            edit = QLineEdit(self)
            row.addWidget(QLabel(f"{label}:"))
            row.addWidget(edit)
            edit.textChanged.connect(lambda text, col=column: self.proxy.setFilterForColumn(col, text))
            self._filter_widgets.append(edit)
        btn_clear = QPushButton("Limpiar filtros", self)
        row.addWidget(btn_clear)
        btn_clear.clicked.connect(self._clear_filters)
        layout.insertLayout(insert_index, row)

    def _clear_filters(self) -> None:
        for edit in getattr(self, "_filter_widgets", []):
            edit.clear()
        self.proxy.clearFilters()
