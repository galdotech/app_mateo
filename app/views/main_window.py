# -*- coding: utf-8 -*-
from __future__ import annotations

import importlib
import logging
from pathlib import Path
from typing import Optional, Type

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
)
from PySide6.QtCore import QSettings, Qt, QTimer

from app.resources import icons_rc  # noqa: F401
from app.ui.ui_main_window import Ui_MainWindow
from app.data import db, export_service
from .notificaciones import notify_low_stock, notify_pending_repairs

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, settings: QSettings, user_role: str):
        super().__init__()
        self.settings = settings
        self.user_role = user_role
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
        self.ui.actionActualizar.triggered.connect(self.refresh_all)

        # Export actions
        self._export_menu = self.ui.menuArchivo.addMenu("Exportar")
        export_actions = {
            "clientes": self._export_menu.addAction("Clientes"),
            "dispositivos": self._export_menu.addAction("Dispositivos"),
            "inventario": self._export_menu.addAction("Inventario"),
            "reparaciones": self._export_menu.addAction("Reparaciones"),
        }
        for table, action in export_actions.items():
            action.triggered.connect(lambda _=False, t=table: self._export_table(t))

        # Acciones rápidas
        self.ui.btnClientes.clicked.connect(self._open_clientes)
        self.ui.btnDispositivos.clicked.connect(self._open_dispositivos)
        self.ui.btnInventario.clicked.connect(self._open_inventario)
        self.ui.btnNuevaReparacion.clicked.connect(self._open_reparaciones)
        self.ui.btnActualizar.clicked.connect(self.refresh_all)

        # Permisos según rol
        self._apply_role_permissions()

        # Resumen inicial
        self.refresh_all()
        self._setup_notification_timer()

    def _apply_role_permissions(self) -> None:
        if self.user_role != "admin":
            for action in [
                self.ui.actionClientes,
                self.ui.actionDispositivos,
                self.ui.actionInventario,
            ]:
                action.setEnabled(False)
            for btn in [
                self.ui.btnClientes,
                self.ui.btnDispositivos,
                self.ui.btnInventario,
            ]:
                btn.setEnabled(False)

    def _load_dialog_class(self, base: str, class_name: str) -> Optional[Type[QDialog]]:
        """Try to import a dialog class handling plural/singular variations."""
        variants = [base, base.rstrip('s')]
        if not base.endswith('s'):
            variants.append(base + 's')
        variants = list(dict.fromkeys(variants))
        for variant in variants:
            module_name = f'app.views.{variant}_dialog'
            try:
                module = importlib.import_module(module_name)
                return getattr(module, class_name)
            except ImportError:
                continue
            except Exception:
                logger.exception("Error loading %s from %s", class_name, module_name)
                raise
        return None

    def _open_clientes(self):
        dlg_cls = self._load_dialog_class('clientes', 'ClientesDialog')
        if dlg_cls is None:
            self._no_impl('Clientes')
            return
        dlg = dlg_cls(self)
        if dlg.exec() == QDialog.Accepted:
            self.refresh_all()

    def _open_inventario(self):
        dlg_cls = self._load_dialog_class('inventario', 'InventarioDialog')
        if dlg_cls is None:
            self._no_impl('Inventario')
            return
        dlg = dlg_cls(self)
        if dlg.exec() == QDialog.Accepted:
            self.refresh_all()

    def _open_reparaciones(self):
        dlg_cls = self._load_dialog_class('reparaciones', 'ReparacionesDialog')
        if dlg_cls is None:
            self._no_impl('Reparaciones')
            return
        dlg = dlg_cls(self)
        if dlg.exec() == QDialog.Accepted:
            self.refresh_all()

    def _open_dispositivos(self):
        dlg_cls = self._load_dialog_class('dispositivos', 'DispositivosDialog')
        if dlg_cls is None:
            self._no_impl('Dispositivos')
            return
        dlg = dlg_cls(self)
        if dlg.exec() == QDialog.Accepted:
            self.refresh_all()

    def _export_table(self, table: str) -> None:
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Exportar datos",
            "",
            "CSV (*.csv);;Excel (*.xlsx)",
        )
        if not file_path:
            return
        try:
            if selected_filter.startswith("Excel") or file_path.endswith(".xlsx"):
                if not file_path.endswith(".xlsx"):
                    file_path += ".xlsx"
                export_service.export_table_to_excel(table, file_path)
            else:
                if not file_path.endswith(".csv"):
                    file_path += ".csv"
                export_service.export_table_to_csv(table, file_path)
            QMessageBox.information(self, "Exportar", "Datos exportados correctamente")
        except Exception as exc:  # pragma: no cover - GUI feedback
            logger.exception("Error al exportar %s", table)
            QMessageBox.critical(self, "Error", str(exc))

    def refresh_all(self):
        self.refresh_summary()
        self.load_low_stock()
        self.load_recent_repairs()
        self.statusBar().showMessage("Panel actualizado", 2500)

    def refresh_summary(self):
        total_clientes, total_dispositivos, total_productos, total_reparaciones = db.get_counts()
        self._set_label_text(["label_total_clientes", "labelTotalClientes"], total_clientes)
        self._set_label_text(["label_total_dispositivos", "labelTotalDispositivos"], total_dispositivos)
        self._set_label_text(["label_total_productos", "labelTotalProductos"], total_productos)
        self._set_label_text(["label_total_reparaciones", "labelTotalReparaciones"], total_reparaciones)

    def load_low_stock(self):
        data = db.get_low_stock_products()
        table = self.ui.tableLowStock
        table.setRowCount(len(data))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Producto", "Cantidad", "Stock mínimo"])
        for row, (nombre, cantidad, stock_min) in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(nombre))
            item_qty = QTableWidgetItem(str(cantidad))
            item_qty.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            table.setItem(row, 1, item_qty)
            item_min = QTableWidgetItem(str(stock_min))
            item_min.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            table.setItem(row, 2, item_min)
        table.setSelectionBehavior(table.SelectionBehavior.SelectRows)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        table.resizeColumnsToContents()

    def load_recent_repairs(self):
        data = db.get_recent_repairs()
        table = self.ui.tableRecentRepairs
        table.setRowCount(len(data))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Fecha", "Cliente", "Dispositivo", "Estado", "Costo"])
        for row, (fecha, cliente, dispositivo, estado, costo) in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(fecha))
            table.setItem(row, 1, QTableWidgetItem(cliente))
            table.setItem(row, 2, QTableWidgetItem(dispositivo))
            table.setItem(row, 3, QTableWidgetItem(estado))
            item_cost = QTableWidgetItem(f"{costo:.2f}")
            item_cost.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            table.setItem(row, 4, item_cost)
        table.setSelectionBehavior(table.SelectionBehavior.SelectRows)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        table.resizeColumnsToContents()

    def _setup_notification_timer(self) -> None:
        self._last_low_stock = []
        self._last_pending_count = 0
        self._timer = QTimer(self)
        self._timer.setInterval(60000)  # 1 minuto
        self._timer.timeout.connect(self._check_notifications)
        self._timer.start()
        self._check_notifications()

    def _check_notifications(self) -> None:
        low_stock = db.get_low_stock_products()
        if low_stock and low_stock != self._last_low_stock:
            notify_low_stock(self, low_stock)
            self._last_low_stock = low_stock
        pending = db.contar_reparaciones_pendientes()
        if pending and pending != self._last_pending_count:
            notify_pending_repairs(self, pending)
            self._last_pending_count = pending

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
