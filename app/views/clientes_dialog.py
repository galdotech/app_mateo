# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

from app.ui.ui_clientes import Ui_ClientesDialog
from app.data import db


class ClientesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ClientesDialog()
        self.ui.setupUi(self)

        phone_regex = QRegularExpression(r"^$|[0-9 +]+$")
        email_regex = QRegularExpression(r"^$|[^@\s]+@[^@\s]+\.[^@\s]+$")
        self.ui.lineEditTelefono.setValidator(QRegularExpressionValidator(phone_regex, self))
        self.ui.lineEditEmail.setValidator(QRegularExpressionValidator(email_regex, self))

        self.ui.btnAgregar.clicked.connect(self.agregar)
        self.ui.btnGuardar.clicked.connect(self.guardar_cambios)
        self.ui.btnEliminar.clicked.connect(self.eliminar)
        self.ui.btnCerrar.clicked.connect(self.close)
        self.ui.tableClientes.itemSelectionChanged.connect(self.cargar_seleccion)

        self._clientes = {}
        self._load_clientes()

    def _load_clientes(self) -> None:
        table = self.ui.tableClientes
        table.setRowCount(0)
        self._clientes = {}
        for row, (cid, nombre, telefono, email, direccion, nif, notas) in enumerate(
            db.listar_clientes_detallado()
        ):
            self._clientes[cid] = {
                "nombre": nombre or "",
                "telefono": telefono or "",
                "email": email or "",
                "direccion": direccion or "",
                "nif": nif or "",
                "notas": notas or "",
            }
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(str(cid)))
            table.setItem(row, 1, QTableWidgetItem(nombre or ""))
            table.setItem(row, 2, QTableWidgetItem(telefono or ""))
            table.setItem(row, 3, QTableWidgetItem(email or ""))
        table.resizeColumnsToContents()

    def _clear_form(self) -> None:
        self.ui.lineEditNombre.clear()
        self.ui.lineEditTelefono.clear()
        self.ui.lineEditEmail.clear()
        self.ui.lineEditDireccion.clear()
        self.ui.lineEditNif.clear()
        self.ui.plainTextEditNotas.clear()
        self.ui.tableClientes.clearSelection()

    def agregar(self) -> None:
        nombre = self.ui.lineEditNombre.text().strip()
        telefono = self.ui.lineEditTelefono.text().strip()
        email = self.ui.lineEditEmail.text().strip()
        direccion = self.ui.lineEditDireccion.text().strip()
        nif = self.ui.lineEditNif.text().strip()
        notas = self.ui.plainTextEditNotas.toPlainText().strip()

        if not nombre:
            QMessageBox.warning(self, "Validación", "El nombre no puede estar vacío.")
            return
        if email and not self.ui.lineEditEmail.hasAcceptableInput():
            QMessageBox.warning(self, "Validación", "Email no válido.")
            return
        if telefono and not self.ui.lineEditTelefono.hasAcceptableInput():
            QMessageBox.warning(self, "Validación", "Teléfono no válido.")
            return

        db.add_cliente(
            nombre,
            telefono=telefono or None,
            email=email or None,
            direccion=direccion or None,
            nif=nif or None,
            notas=notas or None,
        )
        self._clear_form()
        self._load_clientes()

    def cargar_seleccion(self) -> None:
        row = self.ui.tableClientes.currentRow()
        if row < 0:
            return
        cid_item = self.ui.tableClientes.item(row, 0)
        if not cid_item:
            return
        cid = int(cid_item.text())
        cliente = self._clientes.get(cid)
        if not cliente:
            return
        self.ui.lineEditNombre.setText(cliente["nombre"])
        self.ui.lineEditTelefono.setText(cliente["telefono"])
        self.ui.lineEditEmail.setText(cliente["email"])
        self.ui.lineEditDireccion.setText(cliente["direccion"])
        self.ui.lineEditNif.setText(cliente["nif"])
        self.ui.plainTextEditNotas.setPlainText(cliente["notas"])

    def guardar_cambios(self) -> None:
        row = self.ui.tableClientes.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Guardar", "Seleccione un cliente.")
            return
        cid_item = self.ui.tableClientes.item(row, 0)
        if not cid_item:
            return
        cid = int(cid_item.text())

        nombre = self.ui.lineEditNombre.text().strip()
        telefono = self.ui.lineEditTelefono.text().strip()
        email = self.ui.lineEditEmail.text().strip()
        direccion = self.ui.lineEditDireccion.text().strip()
        nif = self.ui.lineEditNif.text().strip()
        notas = self.ui.plainTextEditNotas.toPlainText().strip()

        if not nombre:
            QMessageBox.warning(self, "Validación", "El nombre no puede estar vacío.")
            return
        if email and not self.ui.lineEditEmail.hasAcceptableInput():
            QMessageBox.warning(self, "Validación", "Email no válido.")
            return
        if telefono and not self.ui.lineEditTelefono.hasAcceptableInput():
            QMessageBox.warning(self, "Validación", "Teléfono no válido.")
            return

        db.update_cliente(
            cid,
            nombre=nombre,
            telefono=telefono or None,
            email=email or None,
            direccion=direccion or None,
            nif=nif or None,
            notas=notas or None,
        )
        self._clear_form()
        self._load_clientes()

    def eliminar(self) -> None:
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
            self._clear_form()
            self._load_clientes()

