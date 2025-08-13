# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from app.ui.ui_clientes import Ui_ClientesDialog
from app.data import db


class ClientesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ClientesDialog()
        self.ui.setupUi(self)

        self.ui.btnAgregar.clicked.connect(self.agregar)
        self.ui.btnEliminar.clicked.connect(self.eliminar)
        self.ui.btnCerrar.clicked.connect(self.close)

        self._load_clientes()

    def _load_clientes(self):
        self.ui.tableClientes.setRowCount(0)
        for row, (cid, nombre) in enumerate(db.listar_clientes()):
            self.ui.tableClientes.insertRow(row)
            self.ui.tableClientes.setItem(row, 0, QTableWidgetItem(str(cid)))
            self.ui.tableClientes.setItem(row, 1, QTableWidgetItem(nombre))
        self.ui.tableClientes.resizeColumnsToContents()

    def agregar(self):
        nombre = self.ui.lineEditNombre.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Validación", "El nombre no puede estar vacío.")
            return
        db.add_cliente(nombre)
        self.ui.lineEditNombre.clear()
        self._load_clientes()

    def eliminar(self):
        row = self.ui.tableClientes.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Eliminar", "Seleccione un cliente.")
            return
        id_item = self.ui.tableClientes.item(row, 0)
        if not id_item:
            return
        cid = int(id_item.text())
        if QMessageBox.question(self, "Confirmar", "¿Eliminar cliente seleccionado?") == QMessageBox.Yes:
            db.delete_cliente(cid)
            self._load_clientes()
