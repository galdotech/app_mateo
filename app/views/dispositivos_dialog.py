# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PySide6.QtCore import Qt

from app.ui.ui_dispositivos import Ui_DispositivosDialog
from app.data import db


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
        self.ui.tableDispositivos.itemChanged.connect(self._item_changed)

        self._load_clientes()
        self._load_dispositivos()

    def _load_clientes(self):
        combo = self.ui.comboCliente
        combo.clear()
        for cid, nombre in db.listar_clientes():
            combo.addItem(nombre, cid)

    def _load_dispositivos(self):
        self._updating = True
        table = self.ui.tableDispositivos
        table.blockSignals(True)
        table.setRowCount(0)
        for row, (
            did,
            cid,
            cname,
            marca,
            modelo,
            imei,
            n_serie,
            color,
            accesorios,
        ) in enumerate(db.listar_dispositivos_detallado()):
            table.insertRow(row)
            cliente_item = QTableWidgetItem(cname)
            cliente_item.setFlags(cliente_item.flags() & ~Qt.ItemIsEditable)
            marca_item = QTableWidgetItem(marca or "")
            marca_item.setData(Qt.UserRole, did)
            marca_item.setFlags(marca_item.flags() & ~Qt.ItemIsEditable)
            modelo_item = QTableWidgetItem(modelo or "")
            imei_item = QTableWidgetItem(imei or "")
            serie_item = QTableWidgetItem(n_serie or "")
            color_item = QTableWidgetItem(color or "")
            accesorios_item = QTableWidgetItem(accesorios or "")
            table.setItem(row, 0, cliente_item)
            table.setItem(row, 1, marca_item)
            table.setItem(row, 2, modelo_item)
            table.setItem(row, 3, imei_item)
            table.setItem(row, 4, serie_item)
            table.setItem(row, 5, color_item)
            table.setItem(row, 6, accesorios_item)
        table.resizeColumnsToContents()
        table.blockSignals(False)
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
        marca_item = self.ui.tableDispositivos.item(row, 1)
        did = marca_item.data(Qt.UserRole)
        modelo = self.ui.tableDispositivos.item(row, 2).text().strip()
        imei_item = self.ui.tableDispositivos.item(row, 3)
        imei = imei_item.text().strip() if imei_item else ""
        serie_item = self.ui.tableDispositivos.item(row, 4)
        n_serie = serie_item.text().strip() if serie_item else ""
        color_item = self.ui.tableDispositivos.item(row, 5)
        color = color_item.text().strip() if color_item else ""
        accesorios_item = self.ui.tableDispositivos.item(row, 6)
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
        row = self.ui.tableDispositivos.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Eliminar", "Seleccione un dispositivo.")
            return
        marca_item = self.ui.tableDispositivos.item(row, 1)
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
