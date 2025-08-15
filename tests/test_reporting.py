import os
import sys
import time
from datetime import datetime

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.data import db, summary_service
from app.services import report_service


def setup_sample_db(tmp_path):
    db.init_db(str(tmp_path / "test.db"))
    # Completed repair for tech1
    r1 = db.add_repair(
        cliente_nombre="Juan",
        marca="Marca",
        modelo="Modelo",
        descripcion="",
        diagnostico="",
        acciones="",
        piezas_usadas="",
        costo_mano_obra=20.0,
        costo_piezas=30.0,
        deposito_pagado=0.0,
        total=100.0,
        saldo=0.0,
        estado="Completada",
        prioridad="Normal",
        tecnico="tech1",
        tiempo_estimado=2,
        garantia_dias=0,
        pass_bloqueo="",
        respaldo_datos=False,
        accesorios_entregados="",
    )
    # Pending repair for tech1
    db.add_repair(
        cliente_nombre="Juan",
        marca="Marca",
        modelo="Modelo",
        descripcion="",
        diagnostico="",
        acciones="",
        piezas_usadas="",
        costo_mano_obra=5.0,
        costo_piezas=10.0,
        deposito_pagado=0.0,
        total=0.0,
        saldo=0.0,
        estado="Pendiente",
        prioridad="Normal",
        tecnico="tech1",
        tiempo_estimado=1,
        garantia_dias=0,
        pass_bloqueo="",
        respaldo_datos=False,
        accesorios_entregados="",
    )
    # Pending repair for tech2
    db.add_repair(
        cliente_nombre="Juan",
        marca="Marca",
        modelo="Modelo",
        descripcion="",
        diagnostico="",
        acciones="",
        piezas_usadas="",
        costo_mano_obra=0.0,
        costo_piezas=0.0,
        deposito_pagado=0.0,
        total=0.0,
        saldo=0.0,
        estado="Pendiente",
        prioridad="Normal",
        tecnico="tech2",
        tiempo_estimado=3,
        garantia_dias=0,
        pass_bloqueo="",
        respaldo_datos=False,
        accesorios_entregados="",
    )
    cid = db.listar_clientes()[0][0]
    factura_id = db.crear_factura(r1, cid, 100.0)
    return factura_id


def test_productivity_and_financial_summary(tmp_path):
    setup_sample_db(tmp_path)
    prod = summary_service.get_productivity_metrics()
    prod_dict = {row[0]: row[1:] for row in prod}
    assert prod_dict["tech1"] == (1, 1, pytest.approx(1.5))
    assert prod_dict["tech2"] == (0, 1, pytest.approx(3.0))

    period = datetime.now().strftime("%Y-%m")
    fin = summary_service.get_financial_summary()
    assert fin == [(period, 100.0, 65.0, 35.0)]


def test_report_service_exports(tmp_path):
    setup_sample_db(tmp_path)
    data = summary_service.get_financial_summary()
    chart_path = tmp_path / "chart.png"
    report_service.create_financial_chart(data, str(chart_path))
    assert chart_path.exists() and chart_path.stat().st_size > 0

    excel_path = tmp_path / "report.xlsx"
    report_service.export_report_to_excel(data, str(excel_path))
    assert excel_path.exists() and excel_path.stat().st_size > 0

    pdf_path = tmp_path / "report.pdf"
    report_service.export_report_to_pdf(data, str(pdf_path))
    assert pdf_path.exists() and pdf_path.stat().st_size > 0


def test_schedule_periodic_report(tmp_path):
    out_dir = tmp_path / "sched"
    setup_sample_db(tmp_path)
    timer = report_service.schedule_periodic_report(0.1, str(out_dir))
    time.sleep(0.25)
    timer.cancel()
    # Expect at least one file created
    assert any(out_dir.iterdir())
