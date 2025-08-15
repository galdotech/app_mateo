# -*- coding: utf-8 -*-
import sqlite3
import os
import hashlib
from typing import Optional, List, Tuple

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "inventario_app.db")
_conn: Optional[sqlite3.Connection] = None


def hash_password(password: str) -> str:
    """Return a sha256 hash for the given password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def _ensure_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH)
        _conn.execute("PRAGMA foreign_keys = ON")
        _create_tables(_conn)
    return _conn


def close_db() -> None:
    """Close the global database connection if it exists."""
    global _conn
    if _conn is not None:
        _conn.close()
        _conn = None

def _create_tables(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    # Tablas mínimas
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS dispositivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            marca TEXT,
            modelo TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER DEFAULT 0,
            stock_min INTEGER DEFAULT 0
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS reparaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dispositivo_id INTEGER NOT NULL,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            descripcion TEXT,
            costo REAL DEFAULT 0,
            estado TEXT DEFAULT 'Pendiente',
            FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id) ON DELETE CASCADE
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
        """
    )
    cur.execute("SELECT COUNT(*) FROM usuarios")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO usuarios (nombre, password, rol) VALUES (?, ?, ?)",
            ("admin", hash_password("admin"), "admin"),
        )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS meta (
            schema_version INTEGER NOT NULL
        )
        """
    )
    cur.execute("SELECT COUNT(*) FROM meta")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO meta(schema_version) VALUES (1)")

    # Índices
    try:
        cur.execute("CREATE INDEX IF NOT EXISTS idx_clientes_nombre ON clientes(nombre)")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("CREATE INDEX IF NOT EXISTS idx_dispositivos_cliente ON dispositivos(cliente_id)")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("CREATE INDEX IF NOT EXISTS idx_inventario_nombre ON inventario(nombre)")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("CREATE INDEX IF NOT EXISTS idx_reparaciones_estado ON reparaciones(estado)")
    except sqlite3.OperationalError:
        pass

    conn.commit()


def _ensure_stock_min_column(conn: sqlite3.Connection) -> None:
    """Ensure the inventario table has a stock_min column."""
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(inventario)")
    columns = [row[1] for row in cur.fetchall()]
    if "stock_min" not in columns:
        try:
            cur.execute(
                "ALTER TABLE inventario ADD COLUMN stock_min INTEGER DEFAULT 0"
            )
            conn.commit()
        except sqlite3.OperationalError:
            pass


def migrate_if_needed(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    # Asegura tabla meta y versión inicial
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS meta (
            schema_version INTEGER NOT NULL
        )
        """
    )
    cur.execute("SELECT COUNT(*) FROM meta")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO meta(schema_version) VALUES (1)")
        conn.commit()

    cur.execute("SELECT schema_version FROM meta")
    version = cur.fetchone()[0]

    if version < 2:
        for column in [
            "telefono TEXT",
            "email TEXT",
            "direccion TEXT",
            "nif TEXT",
            "notas TEXT",
        ]:
            try:
                cur.execute(f"ALTER TABLE clientes ADD COLUMN {column}")
            except sqlite3.OperationalError:
                pass
        cur.execute("UPDATE meta SET schema_version = 2")
        conn.commit()
        version = 2

    if version < 3:
        for column in [
            "imei TEXT",
            "n_serie TEXT",
            "color TEXT",
            "pin TEXT",
            "patron TEXT",
            "accesorios TEXT",
        ]:
            try:
                cur.execute(f"ALTER TABLE dispositivos ADD COLUMN {column}")
            except sqlite3.OperationalError:
                pass
        cur.execute("UPDATE meta SET schema_version = 3")
        conn.commit()
        version = 3

    if version < 4:
        for column in [
            "sku TEXT",
            "categoria TEXT",
            "costo REAL DEFAULT 0",
            "precio REAL DEFAULT 0",
            "stock_min INTEGER DEFAULT 0",
            "ubicacion TEXT",
            "proveedor TEXT",
            "notas TEXT",
        ]:
            try:
                cur.execute(f"ALTER TABLE inventario ADD COLUMN {column}")
            except sqlite3.OperationalError:
                pass
        try:
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_inventario_sku ON inventario(sku)"
            )
        except sqlite3.OperationalError:
            pass
        cur.execute("UPDATE meta SET schema_version = 4")
        conn.commit()
        version = 4

    if version < 5:
        for column in [
            "diagnostico TEXT",
            "acciones TEXT",
            "piezas_usadas TEXT",
            "costo_mano_obra REAL DEFAULT 0",
            "deposito_pagado REAL DEFAULT 0",
            "total REAL DEFAULT 0",
            "saldo REAL DEFAULT 0",
            "prioridad TEXT DEFAULT 'Normal'",
            "tecnico TEXT",
            "garantia_dias INTEGER DEFAULT 0",
            "pass_bloqueo TEXT",
            "respaldo_datos INTEGER DEFAULT 0",
            "accesorios_entregados TEXT",
        ]:
            try:
                cur.execute(f"ALTER TABLE reparaciones ADD COLUMN {column}")
            except sqlite3.OperationalError:
                pass
        cur.execute("UPDATE meta SET schema_version = 5")
        conn.commit()

    if version < 6:
        try:
            cur.execute("ALTER TABLE reparaciones ADD COLUMN fecha TEXT DEFAULT CURRENT_TIMESTAMP")
        except sqlite3.OperationalError:
            pass
        cur.execute("UPDATE meta SET schema_version = 6")
        conn.commit()

    if version < 7:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                rol TEXT NOT NULL
            )
            """,
        )
        cur.execute("SELECT COUNT(*) FROM usuarios")
        if cur.fetchone()[0] == 0:
            cur.execute(
                "INSERT INTO usuarios (nombre, password, rol) VALUES (?, ?, ?)",
                ("admin", hash_password("admin"), "admin"),
            )
        cur.execute("UPDATE meta SET schema_version = 7")
        conn.commit()

# API pública
def init_db(path: str = DB_PATH) -> None:
    global DB_PATH
    DB_PATH = path
    conn = _ensure_conn()
    _ensure_stock_min_column(conn)
    migrate_if_needed(conn)

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


def get_counts() -> Tuple[int, int, int, int]:
    """Return total counts for dashboard."""
    return (
        contar_clientes(),
        contar_dispositivos(),
        contar_productos(),
        contar_reparaciones_pendientes(),
    )


def get_low_stock_products(limit: int = 8) -> List[Tuple[str, int, int]]:
    cur = _ensure_conn().cursor()
    cur.execute(
        "SELECT nombre, cantidad, stock_min FROM inventario WHERE cantidad <= stock_min ORDER BY cantidad ASC, nombre ASC LIMIT ?",
        (limit,),
    )
    return cur.fetchall()


def get_recent_repairs(limit: int = 8) -> List[Tuple[str, str, str, str, float]]:
    cur = _ensure_conn().cursor()
    cur.execute(
        """
        SELECT r.fecha, c.nombre, d.marca || ' ' || d.modelo, r.estado, r.total
        FROM reparaciones r
        JOIN dispositivos d ON r.dispositivo_id = d.id
        JOIN clientes c ON d.cliente_id = c.id
        ORDER BY r.fecha DESC
        LIMIT ?
        """,
        (limit,),
    )
    return cur.fetchall()

def listar_clientes():
    cur = _ensure_conn().cursor()
    cur.execute("SELECT id, nombre FROM clientes ORDER BY id")
    return cur.fetchall()

def listar_clientes_detallado() -> List[Tuple[int, str, Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]]:
    cur = _ensure_conn().cursor()
    cur.execute(
        "SELECT id, nombre, telefono, email, direccion, nif, notas FROM clientes ORDER BY id"
    )
    return cur.fetchall()


def add_cliente(
    nombre: str,
    *,
    telefono: Optional[str] = None,
    email: Optional[str] = None,
    direccion: Optional[str] = None,
    nif: Optional[str] = None,
    notas: Optional[str] = None,
) -> Optional[int]:
    existing_id = find_client_by_name(nombre)
    if existing_id is not None:
        return None
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO clientes (nombre, telefono, email, direccion, nif, notas) VALUES (?, ?, ?, ?, ?, ?)",
        (nombre, telefono, email, direccion, nif, notas),
    )
    conn.commit()
    return cur.lastrowid


def update_cliente(cliente_id: int, **campos) -> bool:
    if not campos:
        return False
    fields = []
    params: List[object] = []
    for key, value in campos.items():
        if key not in {"nombre", "telefono", "email", "direccion", "nif", "notas"}:
            continue
        fields.append(f"{key} = ?")
        params.append(value)
    if not fields:
        return False
    params.append(cliente_id)
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(f"UPDATE clientes SET {', '.join(fields)} WHERE id = ?", params)
    conn.commit()
    return cur.rowcount > 0

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


def add_device(
    cliente_id: int,
    marca: str,
    modelo: str,
    imei: Optional[str] = None,
    n_serie: Optional[str] = None,
    color: Optional[str] = None,
    accesorios: Optional[str] = None,
) -> int:
    did = find_device(cliente_id, marca, modelo, imei)
    if did is not None:
        return did
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO dispositivos (cliente_id, marca, modelo, imei, n_serie, color, accesorios)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (cliente_id, marca, modelo, imei, n_serie, color, accesorios),
    )
    conn.commit()
    return cur.lastrowid


def listar_dispositivos() -> List[Tuple[int, int, str, str, str, Optional[str]]]:
    """Compat helper retaining legacy API."""
    cur = _ensure_conn().cursor()
    cur.execute(
        """
        SELECT d.id, d.cliente_id, c.nombre, d.marca, d.modelo, d.imei
        FROM dispositivos d
        JOIN clientes c ON d.cliente_id = c.id
        ORDER BY d.id
        """,
    )
    return cur.fetchall()


def listar_dispositivos_detallado() -> List[
    Tuple[int, int, str, Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]
]:
    cur = _ensure_conn().cursor()
    cur.execute(
        """
        SELECT d.id, d.cliente_id, c.nombre, d.marca, d.modelo, d.imei, d.n_serie, d.color, d.accesorios
        FROM dispositivos d
        JOIN clientes c ON d.cliente_id = c.id
        ORDER BY d.id
        """,
    )
    return cur.fetchall()




def update_device(device_id: int, **campos) -> bool:
    if not campos:
        return False
    allowed = {"marca", "modelo", "imei", "n_serie", "color", "pin", "patron", "accesorios"}
    fields: List[str] = []
    params: List[object] = []
    for key, value in campos.items():
        if key not in allowed:
            continue
        fields.append(f"{key} = ?")
        params.append(value)
    if not fields:
        return False
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


def add_repair(
    cliente_nombre: str,
    marca: str,
    modelo: str,
    descripcion: str,
    diagnostico: str,
    acciones: str,
    piezas_usadas: str,
    costo_mano_obra: float,
    costo_piezas: float,
    deposito_pagado: float,
    total: float,
    saldo: float,
    estado: str,
    prioridad: str,
    tecnico: str,
    garantia_dias: int,
    pass_bloqueo: str,
    respaldo_datos: bool,
    accesorios_entregados: str,
) -> int:
    """Insert a new repair with extended fields."""
    cid = add_client(cliente_nombre)
    did = add_device(cid, marca, modelo, None, None, None, None)
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO reparaciones (
            dispositivo_id, descripcion, costo, estado, diagnostico, acciones,
            piezas_usadas, costo_mano_obra, deposito_pagado, total, saldo,
            prioridad, tecnico, garantia_dias, pass_bloqueo, respaldo_datos,
            accesorios_entregados
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            did,
            descripcion,
            costo_piezas,
            estado,
            diagnostico,
            acciones,
            piezas_usadas,
            costo_mano_obra,
            deposito_pagado,
            total,
            saldo,
            prioridad,
            tecnico,
            garantia_dias,
            pass_bloqueo,
            int(respaldo_datos),
            accesorios_entregados,
        ),
    )
    conn.commit()
    return cur.lastrowid


def update_repair(repair_id: int, **campos) -> bool:
    if not campos:
        return False
    allowed = {
        "descripcion",
        "diagnostico",
        "acciones",
        "piezas_usadas",
        "costo_mano_obra",
        "deposito_pagado",
        "total",
        "saldo",
        "estado",
        "prioridad",
        "tecnico",
        "garantia_dias",
        "pass_bloqueo",
        "respaldo_datos",
        "accesorios_entregados",
    }
    fields: List[str] = []
    params: List[object] = []
    for key, value in campos.items():
        if key not in allowed:
            continue
        if key == "respaldo_datos":
            value = int(bool(value))
        fields.append(f"{key} = ?")
        params.append(value)
        if key == "total":
            fields.append("costo = ?")
            params.append(value)
    if not fields:
        return False
    params.append(repair_id)
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE reparaciones SET {', '.join(fields)} WHERE id = ?",
        params,
    )
    conn.commit()
    return cur.rowcount > 0


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


def listar_productos_detallado() -> List[
    Tuple[
        int,
        Optional[str],
        str,
        Optional[str],
        int,
        int,
        float,
        float,
        Optional[str],
        Optional[str],
        Optional[str],
    ]
]:
    cur = _ensure_conn().cursor()
    cur.execute(
        """
        SELECT id, sku, nombre, categoria, cantidad, stock_min, costo, precio, ubicacion, proveedor, notas
        FROM inventario
        ORDER BY id
        """
    )
    return cur.fetchall()


def add_product_ext(
    sku: Optional[str],
    nombre: str,
    categoria: Optional[str],
    cantidad: int,
    stock_min: int,
    costo: float,
    precio: float,
    ubicacion: Optional[str],
    proveedor: Optional[str],
    notas: Optional[str],
) -> Optional[int]:
    conn = _ensure_conn()
    cur = conn.cursor()
    if sku:
        cur.execute("SELECT id FROM inventario WHERE sku = ?", (sku,))
        if cur.fetchone():
            return None
    cur.execute(
        """
        INSERT INTO inventario (sku, nombre, categoria, cantidad, stock_min, costo, precio, ubicacion, proveedor, notas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            sku or None,
            nombre,
            categoria or None,
            cantidad,
            stock_min,
            costo,
            precio,
            ubicacion or None,
            proveedor or None,
            notas or None,
        ),
    )
    conn.commit()
    return cur.lastrowid


def update_product_ext(product_id: int, **campos) -> bool:
    if not campos:
        return False
    allowed = {
        "sku",
        "nombre",
        "categoria",
        "cantidad",
        "stock_min",
        "costo",
        "precio",
        "ubicacion",
        "proveedor",
        "notas",
    }
    fields: List[str] = []
    params: List[object] = []
    if "sku" in campos and campos["sku"]:
        cur = _ensure_conn().cursor()
        cur.execute(
            "SELECT id FROM inventario WHERE sku = ? AND id != ?",
            (campos["sku"], product_id),
        )
        if cur.fetchone():
            return False
    for key, value in campos.items():
        if key not in allowed:
            continue
        fields.append(f"{key} = ?")
        params.append(value)
    if not fields:
        return False
    params.append(product_id)
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(f"UPDATE inventario SET {', '.join(fields)} WHERE id = ?", params)
    conn.commit()
    return cur.rowcount > 0


# --- Usuarios ---

def add_usuario(nombre: str, password: str, rol: str) -> int:
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO usuarios (nombre, password, rol) VALUES (?, ?, ?)",
        (nombre, hash_password(password), rol),
    )
    conn.commit()
    return cur.lastrowid


def get_usuario(nombre: str) -> Optional[Tuple[int, str, str]]:
    cur = _ensure_conn().cursor()
    cur.execute(
        "SELECT id, password, rol FROM usuarios WHERE nombre = ?",
        (nombre,),
    )
    row = cur.fetchone()
    return row if row else None
