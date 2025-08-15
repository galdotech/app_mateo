import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.data import db
from app.services.auth import AuthService


def setup_db(tmp_path):
    db.init_db(str(tmp_path / "auth.db"))


def test_auth_service_and_roles(tmp_path):
    setup_db(tmp_path)
    service = AuthService()
    assert service.login("admin", "admin")
    assert service.has_permission("delete")
    service.logout()
    assert service.current_user is None


def test_password_reset(tmp_path):
    setup_db(tmp_path)
    db.add_usuario("user", "Password9", "recepcionista")
    token = db.create_password_reset("user")
    assert db.reset_password(token, "Another9")
    user = db.get_usuario("user")
    assert user is not None
    _, password_hash, salt, _ = user
    assert db.verify_password("Another9", password_hash, salt)


def test_audit_log(tmp_path):
    setup_db(tmp_path)
    db.add_usuario("tech", "TechPass9", "tecnico")
    db.log_audit("tech", "delete", "clientes", 1)
    logs = db.get_audit_logs("tech")
    assert len(logs) == 1
    assert logs[0][1] == "tech"
