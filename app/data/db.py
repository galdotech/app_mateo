# -*- coding: utf-8 -*-
import sqlite3
import os
from typing import Optional, List, Tuple

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
            imei TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        )
    """)
    # Ensure column 'imei' exists
    cur.execute("PRAGMA table_info(dispositivos)")
    cols = [row[1] for row in cur.fetchall()]
    if "imei" not in cols:
        cur.execute("ALTER TABLE dispositivos ADD COLUMN imei TEXT")
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
            costo REAL DEFAULT 0,
            estado TEXT DEFAULT 'Pendiente',
            FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id) ON DELETE CASCADE
        )
    """)
    # Ensure column 'costo' exists
    cur.execute("PRAGMA table_info(reparaciones)")
    cols = [row[1] for row in cur.fetchall()]
    if "costo" not in cols:
        cur.execute("ALTER TABLE reparaciones ADD COLUMN costo REAL DEFAULT 0")
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

def listar_clientes():
    cur = _ensure_conn().cursor()
    cur.execute("SELECT id, nombre FROM clientes ORDER BY id")
    return cur.fetchall()

def add_cliente(nombre: str) -> int:
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO clientes (nombre) VALUES (?)", (nombre,))
    conn.commit()
    return cur.lastrowid

def delete_cliente(cliente_id: int) -> bool:
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    return cur.rowcount > 0


# --- Dispositivos y Reparaciones ---

def find_client_by_name(nombre: str) -> Optional[int]:
    cur = _ensure_conn().cursor()
    cur.execute("SELECT id FROM clientes WHERE nombre = ?", (nombre,))
    row = cur.fetchone()
    return row[0] if row else None


def add_client(nombre: str) -> int:
    cid = find_client_by_name(nombre)
    if cid is not None:
        return cid
    return add_cliente(nombre)


def find_device(cliente_id: int, marca: str, modelo: str, imei: Optional[str] = None) -> Optional[int]:
    cur = _ensure_conn().cursor()
    cur.execute(
        """
        SELECT id FROM dispositivos
        WHERE cliente_id = ? AND marca = ? AND modelo = ? AND (imei = ? OR (imei IS NULL AND ? IS NULL))
        """,
        (cliente_id, marca, modelo, imei, imei),
    )
    row = cur.fetchone()
    return row[0] if row else None


def add_device(cliente_id: int, marca: str, modelo: str, imei: Optional[str]) -> int:
    did = find_device(cliente_id, marca, modelo, imei)
    if did is not None:
        return did
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO dispositivos (cliente_id, marca, modelo, imei) VALUES (?, ?, ?, ?)",
        (cliente_id, marca, modelo, imei),
    )
    conn.commit()
    return cur.lastrowid


def listar_dispositivos() -> List[Tuple[int, int, str, str, str, Optional[str]]]:
    cur = _ensure_conn().cursor()
    cur.execute(
        """
        SELECT d.id, d.cliente_id, c.nombre, d.marca, d.modelo, d.imei
        FROM dispositivos d
        JOIN clientes c ON d.cliente_id = c.id
        ORDER BY d.id
        """
    )
    return cur.fetchall()


def update_device(device_id: int, *, marca: Optional[str] = None, modelo: Optional[str] = None, imei: Optional[str] = None) -> bool:
    if marca is None and modelo is None and imei is None:
        return False
    fields = []
    params: List[object] = []
    if marca is not None:
        fields.append("marca = ?")
        params.append(marca)
    if modelo is not None:
        fields.append("modelo = ?")
        params.append(modelo)
    if imei is not None:
        fields.append("imei = ?")
        params.append(imei)
    params.append(device_id)
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(f"UPDATE dispositivos SET {', '.join(fields)} WHERE id = ?", params)
    conn.commit()
    return cur.rowcount > 0


def delete_device(device_id: int) -> bool:
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM dispositivos WHERE id = ?", (device_id,))
    conn.commit()
    return cur.rowcount > 0


def add_repair(cliente_nombre: str, marca: str, modelo: str, descripcion: str, costo: float, estado: str) -> int:
    cid = add_client(cliente_nombre)
    did = add_device(cid, marca, modelo, None)
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reparaciones (dispositivo_id, descripcion, costo, estado) VALUES (?, ?, ?, ?)",
        (did, descripcion, costo, estado),
    )
    conn.commit()
    return cur.lastrowid


# --- Inventario ---

def get_products() -> List[Tuple[int, str, int]]:
    cur = _ensure_conn().cursor()
    cur.execute("SELECT id, nombre, cantidad FROM inventario ORDER BY id")
    return cur.fetchall()


def find_product_by_name(nombre: str) -> Optional[int]:
    cur = _ensure_conn().cursor()
    cur.execute("SELECT id FROM inventario WHERE nombre = ?", (nombre,))
    row = cur.fetchone()
    return row[0] if row else None


def add_product(nombre: str, cantidad: int) -> Optional[int]:
    if find_product_by_name(nombre) is not None:
        return None
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO inventario (nombre, cantidad) VALUES (?, ?)",
        (nombre, cantidad),
    )
    conn.commit()
    return cur.lastrowid


def update_product(product_id: int, *, name: Optional[str] = None, quantity: Optional[int] = None) -> bool:
    if name is None and quantity is None:
        return False
    fields = []
    params = []
    if name is not None:
        fields.append("nombre = ?")
        params.append(name)
    if quantity is not None:
        fields.append("cantidad = ?")
        params.append(quantity)
    params.append(product_id)
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(f"UPDATE inventario SET {', '.join(fields)} WHERE id = ?", params)
    conn.commit()
    return cur.rowcount > 0


def delete_product(product_id: int) -> bool:
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM inventario WHERE id = ?", (product_id,))
    conn.commit()
    return cur.rowcount > 0
