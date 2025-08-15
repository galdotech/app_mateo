import os
import sqlite3
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.data import db


def test_init_db_switches_connection(tmp_path):
    path1 = tmp_path / "first.db"
    path2 = tmp_path / "second.db"

    db.init_db(str(path1))
    conn1 = db._ensure_conn()

    db.init_db(str(path2))
    conn2 = db._ensure_conn()

    assert db.DB_PATH == str(path2)
    assert conn1 is not conn2
    db_path = conn2.execute("PRAGMA database_list").fetchone()[2]
    assert db_path == str(path2)

    with pytest.raises(sqlite3.ProgrammingError):
        conn1.execute("SELECT 1")

    db.close_db()
