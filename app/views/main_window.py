# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QMainWindow, QMessageBox
from app.ui.ui_main_window import Ui_MainWindow
from app.data import db
from app.views.clientes_dialog import ClientesDialog
from app.views.inventario_dialog import InventarioDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Conexión de acciones del menú
        self.ui.actionSalir.triggered.connect(self.close)
        self.ui.actionClientes.triggered.connect(self._open_clientes)
        self.ui.actionDispositivos.triggered.connect(lambda: self._no_impl("Dispositivos"))
        self.ui.actionInventario.triggered.connect(self._open_inventario)
        self.ui.actionReparaciones.triggered.connect(lambda: self._no_impl("Reparaciones"))

        # Resumen inicial
        self._refresh_summary()

    def _open_clientes(self):
        dlg = ClientesDialog(self)
        dlg.exec()
        self._refresh_summary()

    def _open_inventario(self):
        dlg = InventarioDialog(self)
        dlg.exec()
        self._refresh_summary()

    def _refresh_summary(self):
        self.ui.label_total_clientes.setText(str(db.contar_clientes()))
        self.ui.label_total_dispositivos.setText(str(db.contar_dispositivos()))
        self.ui.label_total_productos.setText(str(db.contar_productos()))
        self.ui.label_total_reparaciones.setText(str(db.contar_reparaciones_pendientes()))

    def _no_impl(self, nombre):
        QMessageBox.information(self, nombre, f"El módulo '{nombre}' aún no está implementado en este base.\n"
                                              f"Usa Codex/PRs para generarlo y conéctalo aquí.")
