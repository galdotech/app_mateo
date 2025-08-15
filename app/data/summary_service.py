"""Summary service for dashboard counts."""
from __future__ import annotations

from typing import cast, List, Tuple

from app.data import db


def get_counts(sucursal_id: int | None = None) -> tuple[int, int, int, int]:
    """Return counts of clients, devices, products and pending repairs.

    Returns:
        tuple: (total_clientes, total_dispositivos, total_productos, total_reparaciones_pendientes)
        If an error occurs when retrieving a count, the affected value will be ``0``.
    """
    counts: list[int] = []
    funcs = (
        db.contar_clientes,
        db.contar_dispositivos,
        db.contar_productos,
        db.contar_reparaciones_pendientes,
    )
    for func in funcs:
        try:
            import inspect
            if "sucursal_id" in inspect.signature(func).parameters:
                counts.append(func(sucursal_id))
            else:
                counts.append(func())
        except Exception:
            counts.append(0)

    return cast(tuple[int, int, int, int], tuple(counts))


def get_workload_metrics(sucursal_id: int | None = None) -> List[Tuple[str, int, int]]:
    """Return workload metrics per technician."""
    try:
        return db.get_workload_metrics(sucursal_id)
    except Exception:
        return []


def get_productivity_metrics(sucursal_id: int | None = None) -> List[Tuple[str, int, int, float]]:
    """Return productivity metrics per technician."""
    try:
        return db.get_productivity_metrics(sucursal_id)
    except Exception:
        return []


def get_financial_summary(sucursal_id: int | None = None) -> List[Tuple[str, float, float, float]]:
    """Return monthly financial summary."""
    try:
        return db.get_financial_summary(sucursal_id)
    except Exception:
        return []
