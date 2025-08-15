# -*- coding: utf-8 -*-
from typing import List, Tuple

from PySide6.QtWidgets import QMessageBox, QWidget


def notify_low_stock(parent: QWidget, products: List[Tuple[str, int, int]]) -> None:
    """Show a warning for products with low stock."""
    if not products:
        return
    lines = [f"{nombre}: {cantidad} (mín {stock_min})" for nombre, cantidad, stock_min in products]
    QMessageBox.warning(
        parent,
        "Stock bajo",
        "Los siguientes productos están por debajo del stock mínimo:\n" + "\n".join(lines),
    )


def notify_pending_repairs(parent: QWidget, count: int) -> None:
    """Show info about pending repairs."""
    if count <= 0:
        return
    QMessageBox.information(
        parent,
        "Reparaciones pendientes",
        f"Hay {count} reparaciones pendientes.",
    )
