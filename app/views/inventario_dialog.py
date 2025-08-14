# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QDialog,
    QMessageBox,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QMainWindow,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtCore import Qt

from app.resources import icons_rc  # noqa: F401

from app.ui.ui_inventario import Ui_InventarioDialog
from app.data import db
from .filter_proxy import MultiFilterProxyModel


class InventarioDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_InventarioDialog()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon(":/icons/box.svg"))
        self._set_button_icon(self.ui.btnAgregar, ":/icons/box.svg")
        self._set_button_icon(self.ui.btnEliminar, ":/icons/exit.svg")
        self._set_button_icon(self.ui.btnCerrar, ":/icons/exit.svg")

        self._updating = False

        self.ui.btnAgregar.clicked.connect(self.agregar)
        self.ui.btnEliminar.clicked.connect(self.eliminar)
        self.ui.btnCerrar.clicked.connect(self.close)

        # Model + proxy
        self.model = QStandardItemModel(0, 9, self)
        self.model.setHorizontalHeaderLabels(
            [
                "SKU",
                "Nombre",
                "Categoría",
                "Cantidad",
                "Stock mín",
                "Costo",
                "Precio",
                "Ubicación",
                "Proveedor",
            ]
        )
        self.model.itemChanged.connect(self._item_changed)
        self.proxy = MultiFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.ui.tableProductos.setModel(self.proxy)
        self.ui.tableProductos.setSortingEnabled(True)

        self._setup_filters()

        self._load_products()

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

    def _setup_filters(self) -> None:
        layout = QHBoxLayout()
        self.filter_nombre = QLineEdit(self)
        self.filter_sku = QLineEdit(self)
        self.filter_categoria = QLineEdit(self)
        self.filter_proveedor = QLineEdit(self)
        self.btn_clear = QPushButton("Limpiar filtros", self)

        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.filter_nombre)
        layout.addWidget(QLabel("SKU:"))
        layout.addWidget(self.filter_sku)
        layout.addWidget(QLabel("Categoría:"))
        layout.addWidget(self.filter_categoria)
        layout.addWidget(QLabel("Proveedor:"))
        layout.addWidget(self.filter_proveedor)
        layout.addWidget(self.btn_clear)

        self.ui.verticalLayout.insertLayout(1, layout)

        self.filter_nombre.textChanged.connect(lambda text: self.proxy.setFilterForColumn(1, text))
        self.filter_sku.textChanged.connect(lambda text: self.proxy.setFilterForColumn(0, text))
        self.filter_categoria.textChanged.connect(lambda text: self.proxy.setFilterForColumn(2, text))
        self.filter_proveedor.textChanged.connect(lambda text: self.proxy.setFilterForColumn(8, text))
        self.btn_clear.clicked.connect(self._clear_filters)

    def _clear_filters(self) -> None:
        self.filter_nombre.clear()
        self.filter_sku.clear()
        self.filter_categoria.clear()
        self.filter_proveedor.clear()
        self.proxy.clearFilters()

    def _load_products(self) -> None:
        self._updating = True
        self.model.blockSignals(True)
        self.model.setRowCount(0)
        for (
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
        ) in db.listar_productos_detallado():
            row = [
                QStandardItem(sku or ""),
                QStandardItem(nombre),
                QStandardItem(categoria or ""),
                QStandardItem(str(cantidad)),
                QStandardItem(str(stock_min)),
                QStandardItem(f"{costo:.2f}"),
                QStandardItem(f"{precio:.2f}"),
                QStandardItem(ubicacion or ""),
                QStandardItem(proveedor or ""),
            ]
            row[0].setEditable(False)
            row[0].setData(pid, Qt.UserRole)
            row[1].setEditable(False)
            row[2].setEditable(False)
            row[6].setToolTip(f"Margen: {precio - costo:.2f}")
            self.model.appendRow(row)
        self.ui.tableProductos.resizeColumnsToContents()
        self.model.blockSignals(False)
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
            self._set_error(self.ui.lineEditNombre, True)
            QMessageBox.warning(self, "Validación", "El nombre no puede estar vacío.")
            return
        self._set_error(self.ui.lineEditNombre, False)
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
        self._show_status("Producto agregado")

    def _item_changed(self, item) -> None:
        if self._updating:
            return
        row = item.row()
        pid_item = self.model.item(row, 0)
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
            costo = float(self.model.item(row, 5).text())
            precio = float(self.model.item(row, 6).text())
            self.model.item(row, 6).setToolTip(f"Margen: {precio - costo:.2f}")
        self._show_status("Producto actualizado")

    def eliminar(self) -> None:
        index = self.ui.tableProductos.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Eliminar", "Seleccione un producto.")
            return
        source = self.proxy.mapToSource(index)
        id_item = self.model.item(source.row(), 0)
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
            self._show_status("Producto eliminado")
