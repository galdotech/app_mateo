import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.data import db
from app.services.payment import PaymentService, PaymentGateway


class DummyGateway(PaymentGateway):
    def __init__(self):
        super().__init__("http://dummy", "key")
        self.charges = []

    def charge(self, invoice_id: int, amount: float):  # type: ignore[override]
        self.charges.append((invoice_id, amount))
        return {"status": "succeeded"}


def _create_invoice() -> int:
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
    cliente_id = db.listar_clientes()[0][0]
    return db.crear_factura(repair_id, cliente_id, 15.0)


def test_payment_service(tmp_path):
    db.init_db(str(tmp_path / "test.db"))
    factura_id = _create_invoice()

    service = PaymentService(DummyGateway())
    result = service.process_payment(factura_id, 15.0)

    assert result["status"] == "succeeded"
    total, pagado, saldo = db.obtener_estado_factura(factura_id)
    assert total == 15.0
    assert pagado == 15.0
    assert saldo == 0.0
    db.close_db()
