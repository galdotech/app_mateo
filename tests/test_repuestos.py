import os
import sys
import csv
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.data import db, export_service


@pytest.fixture(autouse=True)
def setup_db(tmp_path):
    db_path = tmp_path / "repuestos.db"
    db.init_db(str(db_path))
    yield
    db.close_db()


def _create_basic_repair():
    cid = db.add_client("Juan")
    did = db.add_device(cid, "Marca", "Modelo")
    cur = db._ensure_conn().cursor()
    cur.execute("INSERT INTO reparaciones (dispositivo_id) VALUES (?)", (did,))
    repair_id = cur.lastrowid
    db._ensure_conn().commit()
    return repair_id


def test_assign_repuesto_to_repair_decrements_stock():
    rep_id = db.add_repuesto("Pantalla", 5, "ACME", 10.0, stock_min=1)
    repair_id = _create_basic_repair()
    assert db.assign_repuesto_to_repair(repair_id, rep_id, 3) is True
    cur = db._ensure_conn().cursor()
    cur.execute("SELECT stock FROM repuestos WHERE id = ?", (rep_id,))
    assert cur.fetchone()[0] == 2
    cur.execute(
        "SELECT cantidad FROM reparacion_repuestos WHERE reparacion_id = ? AND repuesto_id = ?",
        (repair_id, rep_id),
    )
    assert cur.fetchone()[0] == 3


def test_get_low_stock_repuestos():
    db.add_repuesto("Bateria", 1, "ACME", 5.0, stock_min=2)
    assert db.get_low_stock_repuestos() == [("Bateria", 1, 2)]


def test_export_import_repuestos_csv(tmp_path):
    db.add_repuesto("A", 2, "Prov", 1.0)
    db.add_repuesto("B", 3, "Prov", 2.0)
    path = tmp_path / "repuestos.csv"
    export_service.export_table_to_csv("repuestos", str(path))
    conn = db._ensure_conn()
    conn.execute("DELETE FROM repuestos")
    conn.commit()
    export_service.import_table_from_csv("repuestos", str(path))
    cur = db._ensure_conn().cursor()
    cur.execute("SELECT nombre, stock FROM repuestos ORDER BY id")
    assert cur.fetchall() == [("A", 2), ("B", 3)]
