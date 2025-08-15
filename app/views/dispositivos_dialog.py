# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtCore import Qt

from app.resources import icons_rc  # noqa: F401

from app.ui.ui_dispositivos import Ui_DispositivosDialog
from app.data import db
from .filter_proxy import MultiFilterProxyModel
from .base_dialog import BaseDialog


class DispositivosDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DispositivosDialog()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon(":/icons/devices.svg"))
        self._set_button_icon(self.ui.btnAgregar, ":/icons/devices.svg")
        self._set_button_icon(self.ui.btnEliminar, ":/icons/exit.svg")
        self._set_button_icon(self.ui.btnCerrar, ":/icons/exit.svg")

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

        self._build_filters(
            self.ui.verticalLayout,
            [("Cliente", 0), ("Marca", 1), ("Modelo", 2), ("IMEI", 3)],
            1,
        )

        self._load_clientes()
        self._load_dispositivos()

    def _load_clientes(self):
        combo = self.ui.comboCliente
        combo.clear()
        for cid, nombre in db.listar_clientes():
            combo.addItem(nombre, cid)

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
            self._set_error(self.ui.lineEditMarca, not marca)
            self._set_error(self.ui.lineEditModelo, not modelo)
            QMessageBox.warning(self, "Validación", "Marca y modelo son obligatorios.")
            return
        self._set_error(self.ui.lineEditMarca, False)
        self._set_error(self.ui.lineEditModelo, False)
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
        self._show_status("Dispositivo agregado")

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
        self._show_status("Dispositivo actualizado")

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
            self._show_status("Dispositivo eliminado")

    def cerrar(self):
        if self._changed:
            super().accept()
        else:
            super().reject()

    def reject(self):  # type: ignore[override]
        self.cerrar()
