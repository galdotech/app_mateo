import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.data import db


@pytest.fixture(autouse=True)
def setup_db(tmp_path):
    db_path = tmp_path / "tickets.db"
    db.init_db(str(db_path))
    yield
    db.close_db()


def test_create_ticket_with_photos():
    tid = db.create_ticket("Juan", "iPhone", "No enciende", ["a.jpg", "b.jpg"])
    cur = db._ensure_conn().cursor()
    cur.execute("SELECT cliente, dispositivo, estado FROM tickets WHERE id = ?", (tid,))
    assert cur.fetchone() == ("Juan", "iPhone", "recibido")
    cur.execute("SELECT COUNT(*) FROM ticket_fotos WHERE ticket_id = ?", (tid,))
    assert cur.fetchone()[0] == 2
    cur.execute("SELECT estado FROM ticket_estados WHERE ticket_id = ? ORDER BY id", (tid,))
    assert [row[0] for row in cur.fetchall()] == ["recibido"]


def test_update_ticket_state_and_timeline():
    tid = db.create_ticket("Ana", "Samsung", "Pantalla rota")
    db.update_ticket_state(tid, "en reparación")
    db.update_ticket_state(tid, "listo")
    cur = db._ensure_conn().cursor()
    cur.execute("SELECT estado FROM tickets WHERE id = ?", (tid,))
    assert cur.fetchone()[0] == "listo"
    timeline = db.get_ticket_timeline(tid)
    assert [estado for estado, _ in timeline] == ["recibido", "en reparación", "listo"]


def test_search_tickets_by_filters():
    tid1 = db.create_ticket("Juan", "iPhone", "No enciende")
    tid2 = db.create_ticket("Ana", "Samsung", "Pantalla rota")
    db.update_ticket_state(tid2, "en reparación")
    assert {t[0] for t in db.search_tickets(cliente="Juan")} == {tid1}
    assert {t[0] for t in db.search_tickets(estado="en reparación")} == {tid2}
    assert {t[0] for t in db.search_tickets(dispositivo="Samsung")} == {tid2}
