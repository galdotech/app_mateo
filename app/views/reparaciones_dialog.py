# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QDialog, QMessageBox, QMainWindow
from PySide6.QtGui import QIcon

from app.resources import icons_rc  # noqa: F401

from app.ui.ui_reparaciones import Ui_ReparacionesDialog
from app.data import db


class ReparacionesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ReparacionesDialog()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon(":/icons/wrench.svg"))
        self._set_button_icon(self.ui.btnGuardar, ":/icons/wrench.svg")
        self._set_button_icon(self.ui.btnCancelar, ":/icons/exit.svg")

        # Totals are recalculated whenever related values change
        for widget in (
            self.ui.doubleSpinBoxManoObra,
            self.ui.doubleSpinBoxCostoPiezas,
            self.ui.doubleSpinBoxDeposito,
        ):
            widget.valueChanged.connect(self._actualizar_totales)

        self.ui.doubleSpinBoxTotal.setReadOnly(True)
        self.ui.doubleSpinBoxSaldo.setReadOnly(True)
        self._actualizar_totales()

        self.ui.btnGuardar.clicked.connect(self._guardar)
        self.ui.btnCancelar.clicked.connect(self.reject)

    def _set_button_icon(self, btn, resource):
        icon = QIcon(resource)
        if not icon.isNull():
            btn.setIcon(icon)

    def _show_status(self, text: str) -> None:
        parent = self.parent()
        if isinstance(parent, QMainWindow):
            parent.statusBar().showMessage(text, 3000)

    def _set_error(self, widget, state: bool) -> None:
        widget.setProperty("error", state)
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def _guardar(self):
        cliente = self.ui.lineEditCliente.text().strip()
        marca = self.ui.lineEditMarca.text().strip()
        modelo = self.ui.lineEditModelo.text().strip()
        diagnostico = self.ui.plainTextDiagnostico.toPlainText().strip()
        acciones = self.ui.plainTextAcciones.toPlainText().strip()
        piezas = self.ui.plainTextPiezas.toPlainText().strip()
        estado = self.ui.comboEstado.currentText()
        prioridad = self.ui.comboPrioridad.currentText()
        mano_obra = self.ui.doubleSpinBoxManoObra.value()
        deposito = self.ui.doubleSpinBoxDeposito.value()
        total = self.ui.doubleSpinBoxTotal.value()
        saldo = self.ui.doubleSpinBoxSaldo.value()
        tecnico = self.ui.lineEditTecnico.text().strip()
        garantia = self.ui.spinBoxGarantia.value()
        pass_bloqueo = self.ui.lineEditPassBloqueo.text().strip()
        respaldo = self.ui.checkBoxRespaldo.isChecked()
        accesorios = self.ui.lineEditAccesorios.text().strip()

        if not cliente or not marca or not modelo:
            self._set_error(self.ui.lineEditCliente, not cliente)
            self._set_error(self.ui.lineEditMarca, not marca)
            self._set_error(self.ui.lineEditModelo, not modelo)
            QMessageBox.warning(self, "Validación", "Cliente, marca y modelo son obligatorios.")
            return
        self._set_error(self.ui.lineEditCliente, False)
        self._set_error(self.ui.lineEditMarca, False)
        self._set_error(self.ui.lineEditModelo, False)
        if deposito > total:
            QMessageBox.warning(self, "Validación", "El depósito no puede superar el total.")
            return

        db.add_repair(
            cliente,
            marca,
            modelo,
            diagnostico,
            acciones,
            piezas,
            mano_obra,
            deposito,
            total,
            saldo,
            estado,
            prioridad,
            tecnico,
            garantia,
            pass_bloqueo,
            respaldo,
            accesorios,
        )
        QMessageBox.information(self, "Reparación", "Reparación guardada correctamente.")
        self._show_status("Reparación guardada")
        self.accept()

    def _actualizar_totales(self):
        mano = self.ui.doubleSpinBoxManoObra.value()
        piezas = self.ui.doubleSpinBoxCostoPiezas.value()
        total = mano + piezas
        self.ui.doubleSpinBoxTotal.setValue(total)
        deposito = self.ui.doubleSpinBoxDeposito.value()
        saldo = max(total - deposito, 0.0)
        self.ui.doubleSpinBoxSaldo.setValue(saldo)
