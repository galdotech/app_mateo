# -*- coding: utf-8 -*-
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Optional, Type

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QMainWindow, QMessageBox, QApplication
from PySide6.QtCore import QSettings

from app.resources import icons_rc  # noqa: F401
from app.ui.ui_main_window import Ui_MainWindow
from app.data import summary_service


class MainWindow(QMainWindow):
    def __init__(self, settings: QSettings):
        super().__init__()
        self.settings = settings
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon(":/icons/app.svg"))

        # Iconos de acciones (si los recursos están disponibles)
        self._set_action_icon(self.ui.actionClientes, ":/icons/users.svg")
        self._set_action_icon(self.ui.actionDispositivos, ":/icons/devices.svg")
        self._set_action_icon(self.ui.actionInventario, ":/icons/box.svg")
        self._set_action_icon(self.ui.actionReparaciones, ":/icons/wrench.svg")
        self._set_action_icon(self.ui.actionSalir, ":/icons/exit.svg")

        # Tema
        self.ui.actionTemaClaro.triggered.connect(lambda: self._change_theme("light"))
        self.ui.actionTemaOscuro.triggered.connect(lambda: self._change_theme("dark"))

        # Conexión de acciones del menú
        self.ui.actionSalir.triggered.connect(self.close)
        self.ui.actionClientes.triggered.connect(self._open_clientes)
        self.ui.actionDispositivos.triggered.connect(self._open_dispositivos)
        self.ui.actionInventario.triggered.connect(self._open_inventario)
        self.ui.actionReparaciones.triggered.connect(self._open_reparaciones)

        # Resumen inicial
        self.refresh_summary()

    def _load_dialog_class(self, base: str, class_name: str) -> Optional[Type[QDialog]]:
        """Try to import a dialog class handling plural/singular variations."""
        for variant in {base, base.rstrip('s'), base + 's'}:
            module_name = f'app.views.{variant}_dialog'
            try:
                module = importlib.import_module(module_name)
                return getattr(module, class_name)
            except Exception:
                continue
        return None

    def _open_clientes(self):
        dlg_cls = self._load_dialog_class('clientes', 'ClientesDialog')
        if dlg_cls is None:
            self._no_impl('Clientes')
            return
        dlg = dlg_cls(self)
        dlg.exec()
        self.refresh_summary()

    def _open_inventario(self):
        dlg_cls = self._load_dialog_class('inventario', 'InventarioDialog')
        if dlg_cls is None:
            self._no_impl('Inventario')
            return
        dlg = dlg_cls(self)
        dlg.exec()
        self.refresh_summary()

    def _open_reparaciones(self):
        dlg_cls = self._load_dialog_class('reparaciones', 'ReparacionesDialog')
        if dlg_cls is None:
            self._no_impl('Reparaciones')
            return
        dlg = dlg_cls(self)
        if dlg.exec():
            self.refresh_summary()

    def _open_dispositivos(self):
        dlg_cls = self._load_dialog_class('dispositivos', 'DispositivosDialog')
        if dlg_cls is None:
            self._no_impl('Dispositivos')
            return
        dlg = dlg_cls(self)
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

    def _set_action_icon(self, action, resource_path):
        """Asigna un icono a una acción si existe."""
        icon = QIcon(resource_path)
        if not icon.isNull():
            action.setIcon(icon)

    def _change_theme(self, name: str) -> None:
        qss_path = Path(__file__).resolve().parent.parent / "resources" / f"theme_{name}.qss"
        app = QApplication.instance()
        if app and qss_path.exists():
            try:
                with open(qss_path, "r", encoding="utf-8") as fh:
                    app.setStyleSheet(fh.read())
                self.settings.setValue("ui/theme", name)
            except Exception:
                pass

    def _no_impl(self, nombre):
        QMessageBox.information(
            self,
            nombre,
            f"El módulo '{nombre}' aún no está implementado en este base.\nUsa Codex/PRs para generarlo y conéctalo aquí.",
        )
