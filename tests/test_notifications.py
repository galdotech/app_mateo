import os
import sys
from unittest import mock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.data import db
from app.services import templates, notifications


def test_render_template_uses_context():
    result = templates.render_template(
        "ticket_update", {"name": "Ana", "ticket_id": 1, "status": "listo"}
    )
    assert "Ana" in result
    assert "1" in result


def test_log_notification_records_entry(tmp_path):
    db.init_db(str(tmp_path / "test.db"))
    db.log_notification("user", "sms", "hola")
    cur = db._ensure_conn().cursor()
    cur.execute(
        "SELECT destinatario, canal, mensaje FROM notificaciones"
    )
    assert cur.fetchone() == ("user", "sms", "hola")
    db.close_db()


def test_notification_service_sms(monkeypatch, tmp_path):
    db.init_db(str(tmp_path / "test.db"))

    sent: dict[str, object] = {}

    def fake_post(url, json, headers=None, timeout=10):
        sent.update({"url": url, "json": json, "headers": headers})
        class Resp:
            status_code = 200
        return Resp()

    monkeypatch.setattr(notifications.requests, "post", fake_post)

    service = notifications.NotificationService(
        sms_url="http://api.example", sms_token="tkn"
    )
    service.send_sms(
        "123", "ticket_update", {"name": "Ana", "ticket_id": 5, "status": "proceso"}
    )

    cur = db._ensure_conn().cursor()
    cur.execute("SELECT canal, mensaje FROM notificaciones")
    canal, mensaje = cur.fetchone()
    assert canal == "sms"
    assert "Ana" in mensaje
    assert sent["json"]["to"] == "123"
    db.close_db()
