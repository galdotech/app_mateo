import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.data import db


def _create_repair_and_invoice():
    repair_id = db.add_repair(
        cliente_nombre="Ana",
        marca="A",
        modelo="B",
        descripcion="desc",
        diagnostico="diag",
        acciones="acc",
        piezas_usadas="",
        costo_mano_obra=5.0,
        costo_piezas=5.0,
        deposito_pagado=0.0,
        total=10.0,
        saldo=10.0,
        estado="Pendiente",
        prioridad="Normal",
        tecnico="tech",
        tiempo_estimado=1,
        garantia_dias=0,
        pass_bloqueo="",
        respaldo_datos=False,
        accesorios_entregados="",
    )
    cliente_id = db.listar_clientes()[0][0]
    factura_id = db.crear_factura(repair_id, cliente_id, 10.0)
    return repair_id, factura_id


def test_warranty_and_returns(tmp_path):
    db.init_db(str(tmp_path / "test.db"))
    reparacion_id, factura_id = _create_repair_and_invoice()

    gid = db.registrar_garantia(reparacion_id, "fallo pantalla")
    did = db.registrar_devolucion(factura_id, "defecto")

    garantias = db.listar_garantias()
    devoluciones = db.listar_devoluciones()

    assert gid == garantias[0][0]
    assert did == devoluciones[0][0]
    assert garantias[0][2] == "fallo pantalla"
    assert devoluciones[0][2] == "defecto"
    db.close_db()
