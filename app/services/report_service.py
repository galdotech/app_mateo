"""Service functions for generating and exporting reports."""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterable, List, Tuple
import threading

from openpyxl import Workbook

try:  # pragma: no cover - optional dependency checked at runtime
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except Exception:  # pragma: no cover
    canvas = None  # type: ignore

import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend for tests
import matplotlib.pyplot as plt

from app.data import summary_service

FinancialRow = Tuple[str, float, float, float]


def create_financial_chart(data: Iterable[FinancialRow], filepath: str) -> None:
    """Generate a line chart of ingresos, costos and margen."""
    periods = [row[0] for row in data]
    incomes = [row[1] for row in data]
    costs = [row[2] for row in data]
    margins = [row[3] for row in data]

    plt.figure()
    plt.plot(periods, incomes, label="Ingresos")
    plt.plot(periods, costs, label="Costos")
    plt.plot(periods, margins, label="Margen")
    plt.legend()
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()


def export_report_to_excel(data: Iterable[FinancialRow], filepath: str) -> None:
    """Export financial summary to an Excel file."""
    wb = Workbook()
    ws = wb.active
    ws.append(["Periodo", "Ingresos", "Costos", "Margen"])
    for row in data:
        ws.append(list(row))
    wb.save(filepath)


def export_report_to_pdf(data: Iterable[FinancialRow], filepath: str) -> None:
    """Export financial summary to a simple PDF file."""
    if canvas is None:  # pragma: no cover - depends on optional lib
        raise RuntimeError("reportlab is required for PDF export")
    c = canvas.Canvas(filepath, pagesize=letter)
    text = c.beginText(40, 750)
    text.textLine("Reporte financiero")
    for period, ingreso, costo, margen in data:
        text.textLine(f"{period}: {ingreso:.2f} / {costo:.2f} / {margen:.2f}")
    c.drawText(text)
    c.showPage()
    c.save()


def generate_full_report(output_dir: str) -> List[FinancialRow]:
    """Generate financial summary and export to PDF and Excel."""
    data = summary_service.get_financial_summary()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    export_report_to_excel(data, str(out / "reporte.xlsx"))
    try:  # PDF is optional
        export_report_to_pdf(data, str(out / "reporte.pdf"))
    except Exception:
        pass
    chart_path = out / "reporte.png"
    create_financial_chart(data, str(chart_path))
    return data


def schedule_periodic_report(
    interval_seconds: int,
    output_dir: str,
    *,
    task: Callable[[str], List[FinancialRow]] = generate_full_report,
) -> "_RepeatingTimer":
    """Schedule periodic generation of financial reports."""

    class _RepeatingTimer:
        def __init__(self) -> None:
            self._stopped = False
            self._timer: threading.Timer | None = None

        def _run(self) -> None:
            if self._stopped:
                return
            task(output_dir)
            self._timer = threading.Timer(interval_seconds, self._run)
            self._timer.daemon = True
            self._timer.start()

        def start(self) -> "_RepeatingTimer":
            self._timer = threading.Timer(interval_seconds, self._run)
            self._timer.daemon = True
            self._timer.start()
            return self

        def cancel(self) -> None:
            self._stopped = True
            if self._timer:
                self._timer.cancel()

    return _RepeatingTimer().start()
