# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon

from app.resources import icons_rc  # noqa: F401

from app.ui.ui_reparaciones import Ui_ReparacionesDialog
from app.data import db
from .base_dialog import BaseDialog


class ReparacionesDialog(BaseDialog):
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
        costo_piezas = self.ui.doubleSpinBoxCostoPiezas.value()
        deposito = self.ui.doubleSpinBoxDeposito.value()
        total = self.ui.doubleSpinBoxTotal.value()
        saldo = self.ui.doubleSpinBoxSaldo.value()
        tecnico = self.ui.lineEditTecnico.text().strip()
        tiempo_widget = getattr(self.ui, "spinBoxTiempoEstimado", None)
        if tiempo_widget is not None:
            tiempo_estimado = tiempo_widget.value()
        else:
            tiempo_estimado = 0
        garantia = self.ui.spinBoxGarantia.value()
        pass_bloqueo = self.ui.lineEditPassBloqueo.text().strip()
        respaldo = self.ui.checkBoxRespaldo.isChecked()
        accesorios = self.ui.lineEditAccesorios.text().strip()

        descripcion_widget = getattr(self.ui, "plainTextDescripcion", None)
        if descripcion_widget is not None:
            descripcion = descripcion_widget.toPlainText().strip()
        else:
            descripcion = diagnostico

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
            descripcion,
            diagnostico,
            acciones,
            piezas,
            mano_obra,
            costo_piezas,
            deposito,
            total,
            saldo,
            estado,
            prioridad,
            tecnico,
            tiempo_estimado,
            garantia,
            pass_bloqueo,
            respaldo,
            accesorios,
        )
        if tecnico:
            from .notificaciones import notify_new_assignment

            notify_new_assignment(self, tecnico, descripcion)
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
