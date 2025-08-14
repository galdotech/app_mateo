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
from PySide6.QtGui import QRegularExpressionValidator, QStandardItemModel, QStandardItem, QIcon
from PySide6.QtCore import QRegularExpression, Qt

from app.resources import icons_rc  # noqa: F401

from app.ui.ui_clientes import Ui_ClientesDialog
from app.data import db
from .filter_proxy import MultiFilterProxyModel


class ClientesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ClientesDialog()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon(":/icons/users.svg"))
        self._set_button_icon(self.ui.btnAgregar, ":/icons/users.svg")
        self._set_button_icon(self.ui.btnGuardar, ":/icons/users.svg")
        self._set_button_icon(self.ui.btnEliminar, ":/icons/exit.svg")
        self._set_button_icon(self.ui.btnCerrar, ":/icons/exit.svg")

        phone_regex = QRegularExpression(r"^$|[0-9 +]+$")
        email_regex = QRegularExpression(r"^$|[^@\s]+@[^@\s]+\.[^@\s]+$")
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

        self._setup_filters()

        self._clientes = {}
        self._load_clientes()

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

    def _setup_filters(self) -> None:
        layout = QHBoxLayout()
        self.filter_name = QLineEdit(self)
        self.filter_phone = QLineEdit(self)
        self.filter_email = QLineEdit(self)
        self.btn_clear = QPushButton("Limpiar filtros", self)

        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.filter_name)
        layout.addWidget(QLabel("Teléfono:"))
        layout.addWidget(self.filter_phone)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.filter_email)
        layout.addWidget(self.btn_clear)

        self.ui.verticalLayout.insertLayout(2, layout)

        self.filter_name.textChanged.connect(lambda text: self.proxy.setFilterForColumn(1, text))
        self.filter_phone.textChanged.connect(lambda text: self.proxy.setFilterForColumn(2, text))
        self.filter_email.textChanged.connect(lambda text: self.proxy.setFilterForColumn(3, text))
        self.btn_clear.clicked.connect(self._clear_filters)

    def _clear_filters(self) -> None:
        self.filter_name.clear()
        self.filter_phone.clear()
        self.filter_email.clear()
        self.proxy.clearFilters()

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

