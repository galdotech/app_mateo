"""Summary service for dashboard counts."""
from __future__ import annotations

from app.data import db


def get_counts() -> tuple[int, int, int, int]:
    """Return counts of clients, devices, products and pending repairs.

    Returns:
        tuple: (total_clientes, total_dispositivos, total_productos, total_reparaciones_pendientes)
        If an error occurs when retrieving a count, the affected value will be ``0``.
    """
    counts = []
    funcs = (
        db.contar_clientes,
        db.contar_dispositivos,
        db.contar_productos,
        db.contar_reparaciones_pendientes,
    )
    for func in funcs:
        try:
            counts.append(func())
        except Exception:
            counts.append(0)
    return tuple(counts)  # type: ignore[return-value]
