import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.data import db, summary_service


@pytest.fixture(autouse=True)
def setup_db(tmp_path):
    path = tmp_path / "test.db"
    db.init_db(str(path))
    yield
    db.close_db()


def test_transfer_repuesto_between_sucursales():
    s1 = db.add_sucursal("Centro")
    s2 = db.add_sucursal("Norte")
    db.add_repuesto("Pantalla", 5, "ACME", 10.0, sucursal_id=s1)
    assert db.transfer_repuesto("Pantalla", s1, s2, 3) is True
    cur = db._ensure_conn().cursor()
    cur.execute("SELECT stock FROM repuestos WHERE nombre = 'Pantalla' AND sucursal_id = ?", (s1,))
    assert cur.fetchone()[0] == 2
    cur.execute("SELECT stock FROM repuestos WHERE nombre = 'Pantalla' AND sucursal_id = ?", (s2,))
    assert cur.fetchone()[0] == 3


def test_summary_filtered_by_sucursal():
    s1 = db.add_sucursal("Centro")
    s2 = db.add_sucursal("Norte")
    db.add_product("Prod", 10, sucursal_id=s1)
    db.add_product("Prod", 5, sucursal_id=s2)
    cid = db.add_client("Juan")
    did = db.add_device(cid, "M", "X")
    conn = db._ensure_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO reparaciones (dispositivo_id, estado, sucursal_id) VALUES (?, 'Pendiente', ?)", (did, s1))
    cur.execute("INSERT INTO reparaciones (dispositivo_id, estado, sucursal_id) VALUES (?, 'Pendiente', ?)", (did, s2))
    conn.commit()
    c1 = summary_service.get_counts(sucursal_id=s1)
    c2 = summary_service.get_counts(sucursal_id=s2)
    assert c1[2:] == (1, 1)
    assert c2[2:] == (1, 1)


def test_config_scope():
    s1 = db.add_sucursal("Centro")
    db.set_config("moneda", "USD")
    db.set_config("moneda", "EUR", s1)
    assert db.get_config("moneda", s1) == "EUR"
    assert db.get_config("moneda") == "USD"
    # Unknown branch falls back to global
    assert db.get_config("moneda", 9999) == "USD"
