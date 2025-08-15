import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.data import db


def test_presupuesto_factura_pago(tmp_path):
    db.init_db(str(tmp_path / "test.db"))

    repair_id = db.add_repair(
        cliente_nombre="Juan",
        marca="X",
        modelo="Y",
        descripcion="desc",
        diagnostico="diag",
        acciones="acc",
        piezas_usadas="",
        costo_mano_obra=10.0,
        costo_piezas=5.0,
        deposito_pagado=0.0,
        total=15.0,
        saldo=15.0,
        estado="Pendiente",
        prioridad="Normal",
        tecnico="tech",
        tiempo_estimado=2,
        garantia_dias=0,
        pass_bloqueo="",
        respaldo_datos=False,
        accesorios_entregados="",
    )

    presupuesto_id = db.add_presupuesto(repair_id, "pieza1:1", 10.0, 2, 15.0)
    assert db.aprobar_presupuesto(presupuesto_id) is True

    cliente_id = db.listar_clientes()[0][0]
    factura_id = db.crear_factura(repair_id, cliente_id, 15.0)
    db.registrar_pago(factura_id, 5.0)

    total, pagado, saldo = db.obtener_estado_factura(factura_id)
    assert total == 15.0
    assert pagado == 5.0
    assert saldo == 10.0

    assert db.deuda_cliente(cliente_id) == 10.0

    db.close_db()

