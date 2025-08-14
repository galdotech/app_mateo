# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PySide6.QtCore import Qt

from app.ui.ui_inventario import Ui_InventarioDialog
from app.data import db


class InventarioDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_InventarioDialog()
        self.ui.setupUi(self)

        self._updating = False

        self.ui.btnAgregar.clicked.connect(self.agregar)
        self.ui.btnEliminar.clicked.connect(self.eliminar)
        self.ui.btnCerrar.clicked.connect(self.close)
        self.ui.tableProductos.itemChanged.connect(self._item_changed)

        self._load_products()

    def _load_products(self):
        self._updating = True
        table = self.ui.tableProductos
        table.blockSignals(True)
        table.setRowCount(0)
        for row, (pid, nombre, cantidad) in enumerate(db.get_products()):
            table.insertRow(row)
            name_item = QTableWidgetItem(nombre)
            name_item.setData(Qt.UserRole, pid)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            qty_item = QTableWidgetItem(str(cantidad))
            table.setItem(row, 0, name_item)
            table.setItem(row, 1, qty_item)
        table.resizeColumnsToContents()
        table.blockSignals(False)
        self._updating = False

    def agregar(self):
        nombre = self.ui.lineEditNombre.text().strip()
        cantidad = self.ui.spinCantidad.value()
        if not nombre:
            QMessageBox.warning(self, "Validación", "El nombre no puede estar vacío.")
            return
        if db.add_product(nombre, cantidad) is None:
            QMessageBox.warning(self, "Duplicado", "Ya existe un producto con ese nombre.")
            return
        self.ui.lineEditNombre.clear()
        self.ui.spinCantidad.setValue(0)
        self._load_products()

    def _item_changed(self, item):
        if self._updating or item.column() != 1:
            return
        row = item.row()
        name_item = self.ui.tableProductos.item(row, 0)
        pid = name_item.data(Qt.UserRole)
        try:
            cantidad = int(item.text())
            if cantidad < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Validación", "Cantidad inválida.")
            self._load_products()
            return
        db.update_product(pid, quantity=cantidad)

    def eliminar(self):
        row = self.ui.tableProductos.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Eliminar", "Seleccione un producto.")
            return
        name_item = self.ui.tableProductos.item(row, 0)
        pid = name_item.data(Qt.UserRole)
        if QMessageBox.question(self, "Confirmar", "¿Eliminar producto seleccionado?") == QMessageBox.Yes:
            db.delete_product(pid)
            self._load_products()
