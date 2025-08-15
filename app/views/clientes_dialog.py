# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QRegularExpressionValidator, QStandardItemModel, QStandardItem, QIcon
from PySide6.QtCore import QRegularExpression, Qt

from app.resources import icons_rc  # noqa: F401

from app.ui.ui_clientes import Ui_ClientesDialog
from app.data import db
from .filter_proxy import MultiFilterProxyModel
from .base_dialog import BaseDialog


class ClientesDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ClientesDialog()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon(":/icons/users.svg"))
        self._set_button_icon(self.ui.btnAgregar, ":/icons/users.svg")
        self._set_button_icon(self.ui.btnGuardar, ":/icons/users.svg")
        self._set_button_icon(self.ui.btnEliminar, ":/icons/exit.svg")
        self._set_button_icon(self.ui.btnCerrar, ":/icons/exit.svg")

        phone_regex = QRegularExpression(r"^[0-9 +]*$")
        email_regex = QRegularExpression(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
        self.ui.lineEditTelefono.setValidator(QRegularExpressionValidator(phone_regex, self))
        self.ui.lineEditEmail.setValidator(QRegularExpressionValidator(email_regex, self))

        self.ui.btnAgregar.clicked.connect(self.agregar)
        self.ui.btnGuardar.clicked.connect(self.guardar_cambios)
        self.ui.btnEliminar.clicked.connect(self.eliminar)
        self.ui.btnCerrar.clicked.connect(self.close)

        # Model + proxy for filtering
        self.model = QStandardItemModel(0, 4, self)
        self.model.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono", "Email"])
        self.proxy = MultiFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.ui.tableClientes.setModel(self.proxy)
        self.ui.tableClientes.setSortingEnabled(True)
        self.ui.tableClientes.selectionModel().selectionChanged.connect(
            lambda *_: self.cargar_seleccion()
        )

        self._build_filters(
            self.ui.verticalLayout,
            [("Nombre", 1), ("Teléfono", 2), ("Email", 3)],
            2,
        )

        self._clientes = {}
        self._load_clientes()


    def _load_clientes(self) -> None:
        self.model.setRowCount(0)
        self._clientes = {}
        for cid, nombre, telefono, email, direccion, nif, notas in db.listar_clientes_detallado():
            self._clientes[cid] = {
                "nombre": nombre or "",
                "telefono": telefono or "",
                "email": email or "",
                "direccion": direccion or "",
                "nif": nif or "",
                "notas": notas or "",
            }
            row = [
                QStandardItem(str(cid)),
                QStandardItem(nombre or ""),
                QStandardItem(telefono or ""),
                QStandardItem(email or ""),
            ]
            self.model.appendRow(row)
        self.ui.tableClientes.resizeColumnsToContents()

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
            self._set_error(self.ui.lineEditNombre, True)
            QMessageBox.warning(self, "Validación", "El nombre no puede estar vacío.")
            return
        self._set_error(self.ui.lineEditNombre, False)
        if email and not self.ui.lineEditEmail.hasAcceptableInput():
            self._set_error(self.ui.lineEditEmail, True)
            QMessageBox.warning(self, "Validación", "Email no válido.")
            return
        self._set_error(self.ui.lineEditEmail, False)
        if telefono and not self.ui.lineEditTelefono.hasAcceptableInput():
            self._set_error(self.ui.lineEditTelefono, True)
            QMessageBox.warning(self, "Validación", "Teléfono no válido.")
            return
        self._set_error(self.ui.lineEditTelefono, False)

        cid = db.add_cliente(
            nombre,
            telefono=telefono or None,
            email=email or None,
            direccion=direccion or None,
            nif=nif or None,
            notas=notas or None,
        )
        if cid is None:
            QMessageBox.warning(self, "Agregar", "El cliente ya existe.")
            return
        self._clear_form()
        self._load_clientes()
        self._show_status("Cliente agregado")

    def cargar_seleccion(self) -> None:
        index = self.ui.tableClientes.currentIndex()
        if not index.isValid():
            return
        source = self.proxy.mapToSource(index)
        cid_item = self.model.item(source.row(), 0)
        if cid_item is None:
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
        index = self.ui.tableClientes.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Guardar", "Seleccione un cliente.")
            return
        cid_item = self.model.item(self.proxy.mapToSource(index).row(), 0)
        if cid_item is None:
            return
        cid = int(cid_item.text())

        nombre = self.ui.lineEditNombre.text().strip()
        telefono = self.ui.lineEditTelefono.text().strip()
        email = self.ui.lineEditEmail.text().strip()
        direccion = self.ui.lineEditDireccion.text().strip()
        nif = self.ui.lineEditNif.text().strip()
        notas = self.ui.plainTextEditNotas.toPlainText().strip()

        if not nombre:
            self._set_error(self.ui.lineEditNombre, True)
            QMessageBox.warning(self, "Validación", "El nombre no puede estar vacío.")
            return
        self._set_error(self.ui.lineEditNombre, False)
        if email and not self.ui.lineEditEmail.hasAcceptableInput():
            self._set_error(self.ui.lineEditEmail, True)
            QMessageBox.warning(self, "Validación", "Email no válido.")
            return
        self._set_error(self.ui.lineEditEmail, False)
        if telefono and not self.ui.lineEditTelefono.hasAcceptableInput():
            self._set_error(self.ui.lineEditTelefono, True)
            QMessageBox.warning(self, "Validación", "Teléfono no válido.")
            return
        self._set_error(self.ui.lineEditTelefono, False)

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
        self._show_status("Cliente actualizado")

    def eliminar(self) -> None:
        index = self.ui.tableClientes.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Eliminar", "Seleccione un cliente.")
            return
        cid_item = self.model.item(self.proxy.mapToSource(index).row(), 0)
        if cid_item is None:
            return
        cid = int(cid_item.text())
        if QMessageBox.question(self, "Confirmar", "¿Eliminar cliente seleccionado?") == QMessageBox.Yes:
            db.delete_cliente(cid)
            self._clear_form()
            self._load_clientes()
            self._show_status("Cliente eliminado")

