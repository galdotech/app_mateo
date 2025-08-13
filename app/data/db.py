# -*- coding: utf-8 -*-
import sqlite3
import os
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "inventario_app.db")
_conn: Optional[sqlite3.Connection] = None

def _ensure_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH)
        _conn.execute("PRAGMA foreign_keys = ON")
        _create_tables(_conn)
    return _conn

def _create_tables(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    # Tablas mínimas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dispositivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            marca TEXT,
            modelo TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER DEFAULT 0
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reparaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dispositivo_id INTEGER NOT NULL,
            descripcion TEXT,
            estado TEXT DEFAULT 'Pendiente',
            FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id) ON DELETE CASCADE
        )
    """)
    conn.commit()

# API pública
def init_db(path: str = DB_PATH) -> None:
    global DB_PATH
    DB_PATH = path
    _ensure_conn()

def contar_clientes() -> int:
    cur = _ensure_conn().cursor()
    cur.execute("SELECT COUNT(*) FROM clientes")
    return cur.fetchone()[0]

def contar_dispositivos() -> int:
    cur = _ensure_conn().cursor()
    cur.execute("SELECT COUNT(*) FROM dispositivos")
    return cur.fetchone()[0]

def contar_productos() -> int:
    cur = _ensure_conn().cursor()
    cur.execute("SELECT COUNT(*) FROM inventario")
    return cur.fetchone()[0]

def contar_reparaciones_pendientes() -> int:
    cur = _ensure_conn().cursor()
    cur.execute("SELECT COUNT(*) FROM reparaciones WHERE estado = 'Pendiente'")
    return cur.fetchone()[0]
