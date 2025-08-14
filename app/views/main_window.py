# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QMainWindow, QMessageBox
from app.ui.ui_main_window import Ui_MainWindow
from app.data import summary_service
from app.views.clientes_dialog import ClientesDialog
from app.views.inventario_dialog import InventarioDialog
from app.views.reparaciones_dialog import ReparacionesDialog

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
        self.ui.actionReparaciones.triggered.connect(self._open_reparaciones)

        # Resumen inicial
        self.refresh_summary()

    def _open_clientes(self):
        dlg = ClientesDialog(self)
        dlg.exec()
        self.refresh_summary()

    def _open_inventario(self):
        dlg = InventarioDialog(self)
        dlg.exec()
        self.refresh_summary()

    def _open_reparaciones(self):
        dlg = ReparacionesDialog(self)
        if dlg.exec():
            self.refresh_summary()

    def refresh_summary(self):
        total_clientes, total_dispositivos, total_productos, total_reparaciones = summary_service.get_counts()
        self._set_label_text(["label_total_clientes", "labelTotalClientes"], total_clientes)
        self._set_label_text(["label_total_dispositivos", "labelTotalDispositivos"], total_dispositivos)
        self._set_label_text(["label_total_productos", "labelTotalProductos"], total_productos)
        self._set_label_text(["label_total_reparaciones", "labelTotalReparaciones"], total_reparaciones)

    def _set_label_text(self, names, value):
        for name in names:
            label = getattr(self.ui, name, None)
            if label is not None:
                label.setText(str(value))
                break

    def _no_impl(self, nombre):
        QMessageBox.information(self, nombre, f"El módulo '{nombre}' aún no está implementado en este base.\n"
                                              f"Usa Codex/PRs para generarlo y conéctalo aquí.")
