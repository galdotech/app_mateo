"""Dialog displaying productivity indicators and financial charts."""
from __future__ import annotations

import tempfile
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QFileDialog,
)

from app.data import summary_service
from app.services import report_service


class DashboardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Panel de productividad")
        layout = QVBoxLayout(self)

        self.table = QTableWidget(self)
        layout.addWidget(self.table)

        self.chart_label = QLabel(self)
        self.chart_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.chart_label)

        btn_layout = QHBoxLayout()
        self.btn_pdf = QPushButton("Exportar PDF")
        self.btn_excel = QPushButton("Exportar Excel")
        btn_layout.addWidget(self.btn_pdf)
        btn_layout.addWidget(self.btn_excel)
        layout.addLayout(btn_layout)

        self.btn_pdf.clicked.connect(self._export_pdf)
        self.btn_excel.clicked.connect(self._export_excel)

        self.refresh()

    def refresh(self) -> None:
        data = summary_service.get_productivity_metrics()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Técnico",
            "Completadas",
            "Pendientes",
            "Tiempo prom. (h)",
        ])
        for row, (tec, comp, pend, avg) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(tec))
            self.table.setItem(row, 1, QTableWidgetItem(str(comp)))
            self.table.setItem(row, 2, QTableWidgetItem(str(pend)))
            self.table.setItem(row, 3, QTableWidgetItem(f"{avg:.1f}"))
        self.table.resizeColumnsToContents()

        fin_data = summary_service.get_financial_summary()
        if fin_data:
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            tmp.close()
            report_service.create_financial_chart(fin_data, tmp.name)
            self.chart_label.setPixmap(QPixmap(tmp.name))
            self._last_chart = tmp.name
        else:
            self.chart_label.setText("Sin datos financieros")
            self._last_chart = None

    def _export_pdf(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", "reporte.pdf", "PDF (*.pdf)")
        if path:
            data = summary_service.get_financial_summary()
            report_service.export_report_to_pdf(data, path)

    def _export_excel(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Guardar Excel", "reporte.xlsx", "Excel (*.xlsx)")
        if path:
            data = summary_service.get_financial_summary()
            report_service.export_report_to_excel(data, path)
