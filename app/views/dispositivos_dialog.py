# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QDialog,
    QMessageBox,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from app.ui.ui_dispositivos import Ui_DispositivosDialog
from app.data import db
from .filter_proxy import MultiFilterProxyModel


class DispositivosDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DispositivosDialog()
        self.ui.setupUi(self)

        self._updating = False
        self._changed = False

        self.ui.btnAgregar.clicked.connect(self.agregar)
        self.ui.btnEliminar.clicked.connect(self.eliminar)
        self.ui.btnCerrar.clicked.connect(self.cerrar)

        # Model + proxy
        self.model = QStandardItemModel(0, 7, self)
        self.model.setHorizontalHeaderLabels([
            "Cliente",
            "Marca",
            "Modelo",
            "IMEI",
            "N° Serie",
            "Color",
            "Accesorios",
        ])
        self.model.itemChanged.connect(self._item_changed)
        self.proxy = MultiFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.ui.tableDispositivos.setModel(self.proxy)
        self.ui.tableDispositivos.setSortingEnabled(True)

        self._setup_filters()

        self._load_clientes()
        self._load_dispositivos()

    def _load_clientes(self):
        combo = self.ui.comboCliente
        combo.clear()
        for cid, nombre in db.listar_clientes():
            combo.addItem(nombre, cid)

    def _setup_filters(self) -> None:
        layout = QHBoxLayout()
        self.filter_cliente = QLineEdit(self)
        self.filter_marca = QLineEdit(self)
        self.filter_modelo = QLineEdit(self)
        self.filter_imei = QLineEdit(self)
        self.btn_clear = QPushButton("Limpiar filtros", self)

        layout.addWidget(QLabel("Cliente:"))
        layout.addWidget(self.filter_cliente)
        layout.addWidget(QLabel("Marca:"))
        layout.addWidget(self.filter_marca)
        layout.addWidget(QLabel("Modelo:"))
        layout.addWidget(self.filter_modelo)
        layout.addWidget(QLabel("IMEI:"))
        layout.addWidget(self.filter_imei)
        layout.addWidget(self.btn_clear)

        self.ui.verticalLayout.insertLayout(1, layout)

        self.filter_cliente.textChanged.connect(lambda text: self.proxy.setFilterForColumn(0, text))
        self.filter_marca.textChanged.connect(lambda text: self.proxy.setFilterForColumn(1, text))
        self.filter_modelo.textChanged.connect(lambda text: self.proxy.setFilterForColumn(2, text))
        self.filter_imei.textChanged.connect(lambda text: self.proxy.setFilterForColumn(3, text))
        self.btn_clear.clicked.connect(self._clear_filters)

    def _clear_filters(self) -> None:
        self.filter_cliente.clear()
        self.filter_marca.clear()
        self.filter_modelo.clear()
        self.filter_imei.clear()
        self.proxy.clearFilters()

    def _load_dispositivos(self):
        self._updating = True
        self.model.blockSignals(True)
        self.model.setRowCount(0)
        for (
            did,
            cid,
            cname,
            marca,
            modelo,
            imei,
            n_serie,
            color,
            accesorios,
        ) in db.listar_dispositivos_detallado():
            row = [
                QStandardItem(cname),
                QStandardItem(marca or ""),
                QStandardItem(modelo or ""),
                QStandardItem(imei or ""),
                QStandardItem(n_serie or ""),
                QStandardItem(color or ""),
                QStandardItem(accesorios or ""),
            ]
            row[0].setEditable(False)
            row[1].setEditable(False)
            row[1].setData(did, Qt.UserRole)
            self.model.appendRow(row)
        self.ui.tableDispositivos.resizeColumnsToContents()
        self.model.blockSignals(False)
        self._updating = False

    def agregar(self):
        cid = self.ui.comboCliente.currentData()
        marca = self.ui.lineEditMarca.text().strip()
        modelo = self.ui.lineEditModelo.text().strip()
        imei = self.ui.lineEditIMEI.text().strip()
        n_serie = self.ui.lineEditSerie.text().strip()
        color = self.ui.lineEditColor.text().strip()
        accesorios = self.ui.lineEditAccesorios.text().strip()
        if cid is None:
            QMessageBox.warning(self, "Validación", "Seleccione un cliente.")
            return
        if not marca or not modelo:
            QMessageBox.warning(self, "Validación", "Marca y modelo son obligatorios.")
            return
        db.add_device(
            cid,
            marca,
            modelo,
            imei or None,
            n_serie or None,
            color or None,
            accesorios or None,
        )
        self._changed = True
        self.ui.lineEditMarca.clear()
        self.ui.lineEditModelo.clear()
        self.ui.lineEditIMEI.clear()
        self.ui.lineEditSerie.clear()
        self.ui.lineEditColor.clear()
        self.ui.lineEditAccesorios.clear()
        self._load_dispositivos()

    def _item_changed(self, item):
        if self._updating or item.column() not in (2, 3, 4, 5, 6):
            return
        row = item.row()
        marca_item = self.model.item(row, 1)
        did = marca_item.data(Qt.UserRole)
        modelo = self.model.item(row, 2).text().strip()
        imei_item = self.model.item(row, 3)
        imei = imei_item.text().strip() if imei_item else ""
        serie_item = self.model.item(row, 4)
        n_serie = serie_item.text().strip() if serie_item else ""
        color_item = self.model.item(row, 5)
        color = color_item.text().strip() if color_item else ""
        accesorios_item = self.model.item(row, 6)
        accesorios = accesorios_item.text().strip() if accesorios_item else ""
        if not modelo:
            QMessageBox.warning(self, "Validación", "Modelo no puede estar vacío.")
            self._load_dispositivos()
            return
        db.update_device(
            did,
            modelo=modelo,
            imei=imei or None,
            n_serie=n_serie or None,
            color=color or None,
            accesorios=accesorios or None,
        )
        self._changed = True

    def eliminar(self):
        index = self.ui.tableDispositivos.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Eliminar", "Seleccione un dispositivo.")
            return
        source = self.proxy.mapToSource(index)
        marca_item = self.model.item(source.row(), 1)
        did = marca_item.data(Qt.UserRole)
        if QMessageBox.question(self, "Confirmar", "¿Eliminar dispositivo seleccionado?") == QMessageBox.Yes:
            db.delete_device(did)
            self._changed = True
            self._load_dispositivos()

    def cerrar(self):
        if self._changed:
            super().accept()
        else:
            super().reject()

    def reject(self):  # type: ignore[override]
        self.cerrar()
