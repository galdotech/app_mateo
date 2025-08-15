# -*- coding: utf-8 -*-
import sqlite3
import os
import hashlib
import hmac
import secrets
import time
from typing import Optional, List, Tuple

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "inventario_app.db")
_conn: Optional[sqlite3.Connection] = None


def hash_password(password: str, salt: bytes | None = None) -> Tuple[str, str]:
    """Return a PBKDF2 hash and salt for the given password."""
    if salt is None:
        salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return hashed.hex(), salt.hex()


def validate_password(password: str) -> None:
    """Validate password against basic security policies."""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    """Verify a password against the stored hash and salt.

    Falls back to legacy sha256 hashes if no salt is stored.
    """
    if not salt:
        return hashlib.sha256(password.encode("utf-8")).hexdigest() == password_hash
    new_hash, _ = hash_password(password, bytes.fromhex(salt))
    return hmac.compare_digest(new_hash, password_hash)

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
        CREATE TABLE IF NOT EXISTS repuestos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            stock INTEGER DEFAULT 0,
            stock_min INTEGER DEFAULT 0,
            proveedor TEXT,
            precio REAL DEFAULT 0
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
            diagnostico TEXT,
            acciones TEXT,
            piezas_usadas TEXT,
            costo REAL DEFAULT 0,
            costo_mano_obra REAL DEFAULT 0,
            deposito_pagado REAL DEFAULT 0,
            total REAL DEFAULT 0,
            saldo REAL DEFAULT 0,
            estado TEXT DEFAULT 'Pendiente',
            prioridad TEXT DEFAULT 'Normal',
            tecnico TEXT,
            garantia_dias INTEGER DEFAULT 0,
            pass_bloqueo TEXT,
            respaldo_datos INTEGER DEFAULT 0,
            accesorios_entregados TEXT,
            tiempo_estimado INTEGER DEFAULT 0,
            FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id) ON DELETE CASCADE
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS reparacion_repuestos (
            reparacion_id INTEGER NOT NULL,
            repuesto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 1,
            PRIMARY KEY (reparacion_id, repuesto_id),
            FOREIGN KEY (reparacion_id) REFERENCES reparaciones(id) ON DELETE CASCADE,
            FOREIGN KEY (repuesto_id) REFERENCES repuestos(id) ON DELETE CASCADE
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            password_hash TEXT,
            salt TEXT,
            rol TEXT NOT NULL
        )
        """
    )
    cur.execute("PRAGMA table_info(usuarios)")
    columns = [row[1] for row in cur.fetchall()]
    if "password_hash" not in columns:
        cur.execute("ALTER TABLE usuarios ADD COLUMN password_hash TEXT")
    if "salt" not in columns:
        cur.execute("ALTER TABLE usuarios ADD COLUMN salt TEXT")
    if "password" in columns:
        cur.execute("SELECT id, nombre, password FROM usuarios")
        for uid, nombre, pwd in cur.fetchall():
            if nombre == "admin" and pwd == hashlib.sha256("admin".encode("utf-8")).hexdigest():
                pwd_hash, salt = hash_password("admin")
            else:
                pwd_hash, salt = pwd, ""
            cur.execute(
                "UPDATE usuarios SET password_hash = ?, salt = ? WHERE id = ?",
                (pwd_hash, salt, uid),
            )
    cur.execute("SELECT COUNT(*) FROM usuarios")
    if cur.fetchone()[0] == 0:
        pwd_hash, salt = hash_password("admin")
        cur.execute(
            "INSERT INTO usuarios (nombre, password_hash, salt, rol) VALUES (?, ?, ?, ?)",
            ("admin", pwd_hash, salt, "admin"),
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

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            dispositivo TEXT NOT NULL,
            descripcion TEXT,
            estado TEXT DEFAULT 'recibido',
            fecha TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ticket_fotos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            ruta TEXT NOT NULL,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ticket_estados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            estado TEXT NOT NULL,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS presupuestos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reparacion_id INTEGER NOT NULL,
            repuestos TEXT,
            mano_obra REAL DEFAULT 0,
            tiempo_estimado INTEGER DEFAULT 0,
            total REAL DEFAULT 0,
            aprobado INTEGER DEFAULT 0,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (reparacion_id) REFERENCES reparaciones(id) ON DELETE CASCADE
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reparacion_id INTEGER NOT NULL,
            cliente_id INTEGER NOT NULL,
            total REAL NOT NULL,
            pagado REAL DEFAULT 0,
            saldo REAL DEFAULT 0,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (reparacion_id) REFERENCES reparaciones(id) ON DELETE CASCADE,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS pagos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            factura_id INTEGER NOT NULL,
            monto REAL NOT NULL,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE
        )
        """
    )

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
    try:
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tickets_cliente ON tickets(cliente)")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tickets_dispositivo ON tickets(dispositivo)")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tickets_estado ON tickets(estado)")
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
                password_hash TEXT,
                salt TEXT,
                rol TEXT NOT NULL
            )
            """,
        )
        cur.execute("SELECT COUNT(*) FROM usuarios")
        if cur.fetchone()[0] == 0:
            pwd_hash, salt = hash_password("admin")
            cur.execute(
                "INSERT INTO usuarios (nombre, password_hash, salt, rol) VALUES (?, ?, ?, ?)",
                ("admin", pwd_hash, salt, "admin"),
            )
        cur.execute("UPDATE meta SET schema_version = 7")
        conn.commit()

    if version < 8:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                dispositivo TEXT NOT NULL,
                descripcion TEXT,
                estado TEXT DEFAULT 'recibido',
                fecha TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ticket_fotos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                ruta TEXT NOT NULL,
                FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ticket_estados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                estado TEXT NOT NULL,
                fecha TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE
            )
            """
        )
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_tickets_cliente ON tickets(cliente)")
        except sqlite3.OperationalError:
            pass
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_tickets_dispositivo ON tickets(dispositivo)")
        except sqlite3.OperationalError:
            pass
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_tickets_estado ON tickets(estado)")
        except sqlite3.OperationalError:
            pass
        cur.execute("UPDATE meta SET schema_version = 8")
        conn.commit()

    if version < 9:
        try:
            cur.execute(
                "ALTER TABLE reparaciones ADD COLUMN tiempo_estimado INTEGER DEFAULT 0"
            )
        except sqlite3.OperationalError:
            pass
        cur.execute("UPDATE meta SET schema_version = 9")
        conn.commit()

    if version < 10:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS presupuestos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reparacion_id INTEGER NOT NULL,
                repuestos TEXT,
                mano_obra REAL DEFAULT 0,
                tiempo_estimado INTEGER DEFAULT 0,
                total REAL DEFAULT 0,
                aprobado INTEGER DEFAULT 0,
                fecha TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (reparacion_id) REFERENCES reparaciones(id) ON DELETE CASCADE
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reparacion_id INTEGER NOT NULL,
                cliente_id INTEGER NOT NULL,
                total REAL NOT NULL,
                pagado REAL DEFAULT 0,
                saldo REAL DEFAULT 0,
                fecha TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (reparacion_id) REFERENCES reparaciones(id) ON DELETE CASCADE,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factura_id INTEGER NOT NULL,
                monto REAL NOT NULL,
                fecha TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE
            )
            """
        )
        cur.execute("UPDATE meta SET schema_version = 10")
        conn.commit()

    if version < 11:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS notificaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destinatario TEXT NOT NULL,
                canal TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                fecha TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cur.execute("UPDATE meta SET schema_version = 11")
        conn.commit()

    if version < 12:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                accion TEXT NOT NULL,
                tabla TEXT,
                registro_id INTEGER,
                fecha TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS password_resets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                token TEXT NOT NULL,
                expira INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
            """
        )
        cur.execute("UPDATE meta SET schema_version = 12")
        conn.commit()

# API pública
def init_db(path: str = DB_PATH) -> None:
    global DB_PATH
    if _conn is not None:
        close_db()
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

def get_low_stock_products(limit: int = 8) -> List[Tuple[str, int, int]]:
    cur = _ensure_conn().cursor()
    cur.execute(
        "SELECT nombre, cantidad, stock_min FROM inventario "
        "WHERE cantidad <= stock_min "
        "ORDER BY cantidad ASC, nombre ASC LIMIT ?",
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


def find_device_by_serial(n_serie: str, exclude_id: int | None = None) -> Optional[int]:
    """Return device id matching the given serial number.

    Optionally exclude a specific device id (useful when updating).
    """
    cur = _ensure_conn().cursor()
    if exclude_id is None:
        cur.execute("SELECT id FROM dispositivos WHERE n_serie = ?", (n_serie,))
    else:
        cur.execute(
            "SELECT id FROM dispositivos WHERE n_serie = ? AND id != ?",
            (n_serie, exclude_id),
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
) -> Optional[int]:
    """Add a new device and return its id.

    If a device with same cliente/marca/modelo/imei exists or the serial number is
    already used, return None.
    """
    did = find_device(cliente_id, marca, modelo, imei)
    if did is not None:
        return did
    if n_serie and find_device_by_serial(n_serie) is not None:
        return None
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


def listar_dispositivos_por_cliente(cliente_id: int) -> List[
    Tuple[int, int, str, Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]
]:
    """Return detailed devices for a specific client."""
    cur = _ensure_conn().cursor()
    cur.execute(
        """
        SELECT d.id, d.cliente_id, c.nombre, d.marca, d.modelo, d.imei, d.n_serie, d.color, d.accesorios
        FROM dispositivos d
        JOIN clientes c ON d.cliente_id = c.id
        WHERE d.cliente_id = ?
        ORDER BY d.id
        """,
        (cliente_id,),
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
        if key == "n_serie" and value:
            # Ensure serial number is unique when updating
            if find_device_by_serial(value, exclude_id=device_id) is not None:
                return False
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
    tiempo_estimado: int,
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
            prioridad, tecnico, tiempo_estimado, garantia_dias, pass_bloqueo,
            respaldo_datos, accesorios_entregados
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            tiempo_estimado,
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
        "tiempo_estimado",
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


def assign_repair(
    repair_id: int,
    tecnico: str,
    prioridad: str = "Normal",
    tiempo_estimado: int = 0,
) -> bool:
    """Assign a repair to a technician with priority and estimated time."""
    return update_repair(
        repair_id,
        tecnico=tecnico,
        prioridad=prioridad,
        tiempo_estimado=tiempo_estimado,
    )


def get_tasks_by_date(fecha: str) -> List[Tuple[int, str, str]]:
    """Return repairs scheduled for a specific date."""
    cur = _ensure_conn().cursor()
    cur.execute(
        "SELECT id, descripcion, tecnico FROM reparaciones WHERE date(fecha) = date(?)",
        (fecha,),
    )
    return cur.fetchall()


def get_workload_metrics() -> List[Tuple[str, int, int]]:
    """Return workload metrics per technician.

    Each tuple contains (technician, pending_repairs, total_estimated_time).
    """
    cur = _ensure_conn().cursor()
    cur.execute(
        """
        SELECT tecnico, COUNT(*), COALESCE(SUM(tiempo_estimado), 0)
        FROM reparaciones
        WHERE estado = 'Pendiente' AND tecnico IS NOT NULL AND tecnico != ''
        GROUP BY tecnico
        ORDER BY tecnico
        """
    )
    return cur.fetchall()


def get_productivity_metrics() -> List[Tuple[str, int, int, float]]:
    """Return productivity metrics per technician.

    Each tuple contains:
        (technician, completed_repairs, pending_repairs, avg_estimated_time)
    """
    cur = _ensure_conn().cursor()
    cur.execute(
        """
        SELECT tecnico,
               SUM(CASE WHEN estado = 'Completada' THEN 1 ELSE 0 END) AS completadas,
               SUM(CASE WHEN estado = 'Pendiente' THEN 1 ELSE 0 END) AS pendientes,
               COALESCE(AVG(tiempo_estimado), 0)
        FROM reparaciones
        WHERE tecnico IS NOT NULL AND tecnico != ''
        GROUP BY tecnico
        ORDER BY tecnico
        """
    )
    return cur.fetchall()


def get_financial_summary() -> List[Tuple[str, float, float, float]]:
    """Return financial summary per month.

    Each tuple contains:
        (period, ingresos, costos, margen)
    """
    cur = _ensure_conn().cursor()
    # Ingresos por mes
    cur.execute(
        """
        SELECT strftime('%Y-%m', fecha) AS periodo, SUM(total)
        FROM facturas
        GROUP BY periodo
        ORDER BY periodo
        """
    )
    ingresos = {period: total or 0.0 for period, total in cur.fetchall()}

    # Costos por mes
    cur.execute(
        """
        SELECT strftime('%Y-%m', fecha) AS periodo,
               SUM(COALESCE(costo, 0) + COALESCE(costo_mano_obra, 0))
        FROM reparaciones
        GROUP BY periodo
        ORDER BY periodo
        """
    )
    costos = {period: total or 0.0 for period, total in cur.fetchall()}

    periods = sorted(set(ingresos) | set(costos))
    summary: List[Tuple[str, float, float, float]] = []
    for period in periods:
        inc = ingresos.get(period, 0.0)
        cost = costos.get(period, 0.0)
        summary.append((period, inc, cost, inc - cost))
    return summary


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


# --- Repuestos ---

def add_repuesto(
    nombre: str,
    stock: int,
    proveedor: Optional[str],
    precio: float,
    stock_min: int = 0,
) -> int:
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO repuestos (nombre, stock, stock_min, proveedor, precio)
        VALUES (?, ?, ?, ?, ?)
        """,
        (nombre, stock, stock_min, proveedor, precio),
    )
    conn.commit()
    return cur.lastrowid


def use_repuesto(repuesto_id: int, cantidad: int = 1) -> bool:
    cur = _ensure_conn().cursor()
    cur.execute("SELECT stock FROM repuestos WHERE id = ?", (repuesto_id,))
    row = cur.fetchone()
    if not row or row[0] < cantidad:
        return False
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE repuestos SET stock = stock - ? WHERE id = ?",
        (cantidad, repuesto_id),
    )
    conn.commit()
    return True


def assign_repuesto_to_repair(
    repair_id: int, repuesto_id: int, cantidad: int = 1
) -> bool:
    if not use_repuesto(repuesto_id, cantidad):
        return False
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO reparacion_repuestos (reparacion_id, repuesto_id, cantidad)
        VALUES (?, ?, ?)
        """,
        (repair_id, repuesto_id, cantidad),
    )
    conn.commit()
    return True


def get_low_stock_repuestos(limit: int = 8) -> List[Tuple[str, int, int]]:
    cur = _ensure_conn().cursor()
    cur.execute(
        "SELECT nombre, stock, stock_min FROM repuestos "
        "WHERE stock <= stock_min ORDER BY stock ASC, nombre ASC LIMIT ?",
        (limit,),
    )
    return cur.fetchall()


# --- Usuarios ---

def add_usuario(nombre: str, password: str, rol: str) -> int:
    validate_password(password)
    if rol not in {"admin", "tecnico", "recepcionista"}:
        raise ValueError("Invalid role")
    conn = _ensure_conn()
    cur = conn.cursor()
    pwd_hash, salt = hash_password(password)
    cur.execute(
        "INSERT INTO usuarios (nombre, password_hash, salt, rol) VALUES (?, ?, ?, ?)",
        (nombre, pwd_hash, salt, rol),
    )
    conn.commit()
    return cur.lastrowid


def get_usuario(nombre: str) -> Optional[Tuple[int, str, str, str]]:
    cur = _ensure_conn().cursor()
    cur.execute(
        "SELECT id, password_hash, salt, rol FROM usuarios WHERE nombre = ?",
        (nombre,),
    )
    row = cur.fetchone()
    return row if row else None


def create_password_reset(nombre: str, ttl_seconds: int = 3600) -> str:
    """Create a password reset token for the given user name."""
    user = get_usuario(nombre)
    if user is None:
        raise ValueError("Usuario no encontrado")
    user_id = user[0]
    token = secrets.token_hex(16)
    expires = int(time.time()) + ttl_seconds
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO password_resets (usuario_id, token, expira) VALUES (?, ?, ?)",
        (user_id, token, expires),
    )
    conn.commit()
    return token


def reset_password(token: str, new_password: str) -> bool:
    """Reset a user's password given a valid token."""
    validate_password(new_password)
    now = int(time.time())
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT usuario_id FROM password_resets WHERE token = ? AND expira > ?",
        (token, now),
    )
    row = cur.fetchone()
    if row is None:
        return False
    user_id = row[0]
    pwd_hash, salt = hash_password(new_password)
    cur.execute(
        "UPDATE usuarios SET password_hash = ?, salt = ? WHERE id = ?",
        (pwd_hash, salt, user_id),
    )
    cur.execute("DELETE FROM password_resets WHERE token = ?", (token,))
    conn.commit()
    return True


def log_audit(usuario: str, accion: str, tabla: str | None, registro_id: int | None) -> int:
    """Store an audit log entry for a critical action."""
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO auditoria (usuario, accion, tabla, registro_id) VALUES (?, ?, ?, ?)",
        (usuario, accion, tabla, registro_id),
    )
    conn.commit()
    return cur.lastrowid


def get_audit_logs(usuario: str | None = None) -> List[Tuple[int, str, str, str | None, int | None, str]]:
    """Return audit log entries optionally filtered by user."""
    cur = _ensure_conn().cursor()
    query = "SELECT id, usuario, accion, tabla, registro_id, fecha FROM auditoria"
    params: List[object] = []
    if usuario:
        query += " WHERE usuario = ?"
        params.append(usuario)
    cur.execute(query, params)
    return cur.fetchall()


# --- Tickets ---

TICKET_STATES = ["recibido", "en reparación", "listo", "entregado"]


def create_ticket(cliente: str, dispositivo: str, descripcion: str, fotos: Optional[List[str]] = None) -> int:
    """Create a new ticket and optional associated photos."""
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tickets (cliente, dispositivo, descripcion) VALUES (?, ?, ?)",
        (cliente, dispositivo, descripcion),
    )
    ticket_id = cur.lastrowid
    if fotos:
        cur.executemany(
            "INSERT INTO ticket_fotos (ticket_id, ruta) VALUES (?, ?)",
            [(ticket_id, ruta) for ruta in fotos],
        )
    # Estado inicial
    cur.execute(
        "INSERT INTO ticket_estados (ticket_id, estado) VALUES (?, ?)",
        (ticket_id, "recibido"),
    )
    conn.commit()
    return ticket_id


def update_ticket_state(ticket_id: int, estado: str) -> None:
    """Update the ticket's current state and record it in the timeline."""
    if estado not in TICKET_STATES:
        raise ValueError("Estado inválido")
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute("UPDATE tickets SET estado = ? WHERE id = ?", (estado, ticket_id))
    cur.execute(
        "INSERT INTO ticket_estados (ticket_id, estado) VALUES (?, ?)",
        (ticket_id, estado),
    )
    conn.commit()


def get_ticket_timeline(ticket_id: int) -> List[Tuple[str, str]]:
    """Return the chronological list of states for a ticket."""
    cur = _ensure_conn().cursor()
    cur.execute(
        "SELECT estado, fecha FROM ticket_estados WHERE ticket_id = ? ORDER BY fecha ASC",
        (ticket_id,),
    )
    return cur.fetchall()


def search_tickets(cliente: str | None = None, dispositivo: str | None = None, estado: str | None = None) -> List[Tuple[int, str, str, str]]:
    """Search tickets by client name, device or state."""
    cur = _ensure_conn().cursor()
    query = "SELECT id, cliente, dispositivo, estado FROM tickets WHERE 1=1"
    params: List[object] = []
    if cliente:
        query += " AND cliente LIKE ?"
        params.append(f"%{cliente}%")
    if dispositivo:
        query += " AND dispositivo LIKE ?"
        params.append(f"%{dispositivo}%")
    if estado:
        query += " AND estado = ?"
        params.append(estado)
    cur.execute(query, params)
    return cur.fetchall()


def add_presupuesto(
    reparacion_id: int,
    repuestos: str,
    mano_obra: float,
    tiempo_estimado: int,
    total: float,
) -> int:
    """Insert a new budget for a repair."""
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO presupuestos (reparacion_id, repuestos, mano_obra, tiempo_estimado, total)
        VALUES (?, ?, ?, ?, ?)
        """,
        (reparacion_id, repuestos, mano_obra, tiempo_estimado, total),
    )
    conn.commit()
    return cur.lastrowid


def aprobar_presupuesto(presupuesto_id: int) -> bool:
    """Mark a budget as approved by the client."""
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE presupuestos SET aprobado = 1 WHERE id = ?",
        (presupuesto_id,),
    )
    conn.commit()
    return cur.rowcount > 0


def crear_factura(reparacion_id: int, cliente_id: int, total: float) -> int:
    """Create an invoice for a repair and client."""
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO facturas (reparacion_id, cliente_id, total, pagado, saldo)
        VALUES (?, ?, ?, 0, ?)
        """,
        (reparacion_id, cliente_id, total, total),
    )
    conn.commit()
    return cur.lastrowid


def registrar_pago(factura_id: int, monto: float) -> int:
    """Register a payment for an invoice and update its balance."""
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pagos (factura_id, monto) VALUES (?, ?)",
        (factura_id, monto),
    )
    cur.execute(
        "UPDATE facturas SET pagado = pagado + ?, saldo = saldo - ? WHERE id = ?",
        (monto, monto, factura_id),
    )
    conn.commit()
    return cur.lastrowid


def obtener_estado_factura(factura_id: int) -> Tuple[float, float, float]:
    """Return total, paid amount and outstanding balance for an invoice."""
    cur = _ensure_conn().cursor()
    cur.execute(
        "SELECT total, pagado, saldo FROM facturas WHERE id = ?",
        (factura_id,),
    )
    row = cur.fetchone()
    if row is None:
        return (0.0, 0.0, 0.0)
    return row  # type: ignore[return-value]


def deuda_cliente(cliente_id: int) -> float:
    """Return the outstanding debt for a client."""
    cur = _ensure_conn().cursor()
    cur.execute(
        "SELECT SUM(saldo) FROM facturas WHERE cliente_id = ?",
        (cliente_id,),
    )
    result = cur.fetchone()[0]
    return float(result) if result is not None else 0.0


def log_notification(destinatario: str, canal: str, mensaje: str) -> None:
    """Store a notification event with timestamp."""
    conn = _ensure_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notificaciones (destinatario, canal, mensaje) VALUES (?, ?, ?)",
        (destinatario, canal, mensaje),
    )
    conn.commit()


def get_notifications(destinatario: str | None = None) -> List[Tuple[int, str, str, str]]:
    """Return logged notifications optionally filtered by recipient."""
    cur = _ensure_conn().cursor()
    query = "SELECT id, destinatario, canal, fecha FROM notificaciones"
    params: List[object] = []
    if destinatario:
        query += " WHERE destinatario = ?"
        params.append(destinatario)
    cur.execute(query, params)
    return cur.fetchall()
