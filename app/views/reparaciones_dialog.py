# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QDialog, QMessageBox

from app.ui.ui_reparaciones import Ui_ReparacionesDialog
from app.data import db


class ReparacionesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ReparacionesDialog()
        self.ui.setupUi(self)

        self.ui.btnGuardar.clicked.connect(self._guardar)
        self.ui.btnCancelar.clicked.connect(self.reject)

    def _guardar(self):
        cliente = self.ui.lineEditCliente.text().strip()
        marca = self.ui.lineEditMarca.text().strip()
        modelo = self.ui.lineEditModelo.text().strip()
        descripcion = self.ui.plainTextDescripcion.toPlainText().strip()
        estado = self.ui.comboEstado.currentText()
        costo_text = self.ui.inputCosto.text().strip()

        if not cliente or not marca or not modelo:
            QMessageBox.warning(self, "Validación", "Cliente, marca y modelo son obligatorios.")
            return
        try:
            costo = float(costo_text) if costo_text else 0.0
            if costo < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Validación", "Costo inválido.")
            return

        db.add_repair(cliente, marca, modelo, descripcion, costo, estado)
        QMessageBox.information(self, "Reparación", "Reparación guardada correctamente.")
        self.accept()
