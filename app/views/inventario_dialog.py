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

    def _clear_inputs(self) -> None:
        self.ui.lineEditSKU.clear()
        self.ui.lineEditNombre.clear()
        self.ui.comboCategoria.setCurrentText("")
        self.ui.spinCantidad.setValue(0)
        self.ui.spinStockMin.setValue(0)
        self.ui.doubleCosto.setValue(0.0)
        self.ui.doublePrecio.setValue(0.0)
        self.ui.lineUbicacion.clear()
        self.ui.lineProveedor.clear()

    def _load_products(self) -> None:
        self._updating = True
        table = self.ui.tableProductos
        table.blockSignals(True)
        table.setRowCount(0)
        for row, (
            pid,
            sku,
            nombre,
            categoria,
            cantidad,
            stock_min,
            costo,
            precio,
            ubicacion,
            proveedor,
            _notas,
        ) in enumerate(db.listar_productos_detallado()):
            table.insertRow(row)
            sku_item = QTableWidgetItem(sku or "")
            sku_item.setData(Qt.UserRole, pid)
            sku_item.setFlags(sku_item.flags() & ~Qt.ItemIsEditable)
            name_item = QTableWidgetItem(nombre)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            cat_item = QTableWidgetItem(categoria or "")
            cat_item.setFlags(cat_item.flags() & ~Qt.ItemIsEditable)
            qty_item = QTableWidgetItem(str(cantidad))
            stock_item = QTableWidgetItem(str(stock_min))
            costo_item = QTableWidgetItem(f"{costo:.2f}")
            precio_item = QTableWidgetItem(f"{precio:.2f}")
            precio_item.setToolTip(f"Margen: {precio - costo:.2f}")
            ubic_item = QTableWidgetItem(ubicacion or "")
            prov_item = QTableWidgetItem(proveedor or "")
            table.setItem(row, 0, sku_item)
            table.setItem(row, 1, name_item)
            table.setItem(row, 2, cat_item)
            table.setItem(row, 3, qty_item)
            table.setItem(row, 4, stock_item)
            table.setItem(row, 5, costo_item)
            table.setItem(row, 6, precio_item)
            table.setItem(row, 7, ubic_item)
            table.setItem(row, 8, prov_item)
        table.resizeColumnsToContents()
        table.blockSignals(False)
        self._updating = False

    def agregar(self) -> None:
        sku = self.ui.lineEditSKU.text().strip() or None
        nombre = self.ui.lineEditNombre.text().strip()
        categoria = self.ui.comboCategoria.currentText().strip() or None
        cantidad = self.ui.spinCantidad.value()
        stock_min = self.ui.spinStockMin.value()
        costo = self.ui.doubleCosto.value()
        precio = self.ui.doublePrecio.value()
        ubicacion = self.ui.lineUbicacion.text().strip() or None
        proveedor = self.ui.lineProveedor.text().strip() or None

        if not nombre:
            QMessageBox.warning(self, "Validación", "El nombre no puede estar vacío.")
            return
        if costo < 0 or precio < 0:
            QMessageBox.warning(self, "Validación", "Costo y precio deben ser >= 0.")
            return
        pid = db.add_product_ext(
            sku,
            nombre,
            categoria,
            cantidad,
            stock_min,
            costo,
            precio,
            ubicacion,
            proveedor,
            None,
        )
        if pid is None:
            QMessageBox.warning(self, "Duplicado", "Ya existe un producto con ese SKU.")
            return
        self._clear_inputs()
        self._load_products()

    def _item_changed(self, item) -> None:
        if self._updating:
            return
        row = item.row()
        pid_item = self.ui.tableProductos.item(row, 0)
        if not pid_item:
            return
        pid = pid_item.data(Qt.UserRole)
        col = item.column()
        try:
            if col == 3:
                val = int(item.text())
                if val < 0:
                    raise ValueError
                db.update_product_ext(pid, cantidad=val)
            elif col == 4:
                val = int(item.text())
                if val < 0:
                    raise ValueError
                db.update_product_ext(pid, stock_min=val)
            elif col == 5:
                val = float(item.text())
                if val < 0:
                    raise ValueError
                db.update_product_ext(pid, costo=val)
            elif col == 6:
                val = float(item.text())
                if val < 0:
                    raise ValueError
                db.update_product_ext(pid, precio=val)
            elif col == 7:
                db.update_product_ext(pid, ubicacion=item.text().strip() or None)
            elif col == 8:
                db.update_product_ext(pid, proveedor=item.text().strip() or None)
            else:
                return
        except ValueError:
            QMessageBox.warning(self, "Validación", "Valor inválido.")
            self._load_products()
            return
        if col in (5, 6):
            costo = float(self.ui.tableProductos.item(row, 5).text())
            precio = float(self.ui.tableProductos.item(row, 6).text())
            self.ui.tableProductos.item(row, 6).setToolTip(f"Margen: {precio - costo:.2f}")

    def eliminar(self) -> None:
        row = self.ui.tableProductos.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Eliminar", "Seleccione un producto.")
            return
        id_item = self.ui.tableProductos.item(row, 0)
        if not id_item:
            return
        pid = id_item.data(Qt.UserRole)
        if (
            QMessageBox.question(
                self, "Confirmar", "¿Eliminar producto seleccionado?"
            )
            == QMessageBox.Yes
        ):
            db.delete_product(pid)
            self._load_products()
