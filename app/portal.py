from __future__ import annotations

from flask import Flask, jsonify, request

from app.data import db
from app.services.payment import PaymentGateway, PaymentService
from app.services.warranty import WarrantyService
from app.services.returns import ReturnService

app = Flask(__name__)

gateway = PaymentGateway("https://api.example.com", "test")
payment_service = PaymentService(gateway)
warranty_service = WarrantyService()
return_service = ReturnService()


@app.route("/tickets/<int:ticket_id>")
def ticket_status(ticket_id: int):
    """Return timeline for a ticket for clients to consult progress."""
    timeline = db.get_ticket_timeline(ticket_id)
    return jsonify({"ticket_id": ticket_id, "timeline": timeline})


@app.route("/tickets/<int:ticket_id>/documents")
def ticket_documents(ticket_id: int):
    """Placeholder for document list associated with a ticket."""
    return jsonify({"ticket_id": ticket_id, "documents": []})


@app.post("/api/payments")
def api_payments():
    data = request.get_json() or {}
    factura_id = data.get("factura_id")
    monto = data.get("monto")
    result = payment_service.process_payment(factura_id, monto)
    return jsonify(result)


@app.post("/api/warranties")
def api_warranties():
    data = request.get_json() or {}
    reparacion_id = data.get("reparacion_id")
    descripcion = data.get("descripcion", "")
    wid = warranty_service.register(reparacion_id, descripcion)
    return jsonify({"garantia_id": wid})


@app.get("/api/warranties")
def list_warranties():
    return jsonify({"garantias": warranty_service.list()})


@app.post("/api/returns")
def api_returns():
    data = request.get_json() or {}
    factura_id = data.get("factura_id")
    motivo = data.get("motivo", "")
    rid = return_service.register(factura_id, motivo)
    return jsonify({"devolucion_id": rid})


@app.get("/api/returns")
def list_returns():
    return jsonify({"devoluciones": return_service.list()})


if __name__ == "__main__":
    app.run(debug=True)
