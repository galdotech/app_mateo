from __future__ import annotations

from typing import List, Tuple

from app.data import db


class ReturnService:
    """Service to register and query product returns."""

    def register(self, factura_id: int, motivo: str) -> int:
        return db.registrar_devolucion(factura_id, motivo)

    def list(self) -> List[Tuple[int, int, str, str, str]]:
        return db.listar_devoluciones()
