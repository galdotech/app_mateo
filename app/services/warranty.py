from __future__ import annotations

from typing import List, Tuple

from app.data import db


class WarrantyService:
    """Service to register and query warranty claims."""

    def register(self, reparacion_id: int, descripcion: str) -> int:
        return db.registrar_garantia(reparacion_id, descripcion)

    def list(self) -> List[Tuple[int, int, str, str, str]]:
        return db.listar_garantias()
