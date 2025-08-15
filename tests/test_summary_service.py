import os
import sys
from types import SimpleNamespace

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.data import summary_service


def test_get_counts_returns_db_values(monkeypatch):
    fake_db = SimpleNamespace(
        contar_clientes=lambda: 1,
        contar_dispositivos=lambda: 2,
        contar_productos=lambda: 3,
        contar_reparaciones_pendientes=lambda: 4,
    )
    monkeypatch.setattr(summary_service, "db", fake_db)

    assert summary_service.get_counts() == (1, 2, 3, 4)


def test_get_counts_handles_exceptions(monkeypatch):
    def raise_exc():
        raise RuntimeError("boom")

    fake_db = SimpleNamespace(
        contar_clientes=raise_exc,
        contar_dispositivos=lambda: 2,
        contar_productos=raise_exc,
        contar_reparaciones_pendientes=lambda: 4,
    )
    monkeypatch.setattr(summary_service, "db", fake_db)

    assert summary_service.get_counts() == (0, 2, 0, 4)
