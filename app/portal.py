from __future__ import annotations

from flask import Flask, jsonify

from app.data import db

app = Flask(__name__)


@app.route("/tickets/<int:ticket_id>")
def ticket_status(ticket_id: int):
    """Return timeline for a ticket for clients to consult progress."""
    timeline = db.get_ticket_timeline(ticket_id)
    return jsonify({"ticket_id": ticket_id, "timeline": timeline})


@app.route("/tickets/<int:ticket_id>/documents")
def ticket_documents(ticket_id: int):
    """Placeholder for document list associated with a ticket."""
    return jsonify({"ticket_id": ticket_id, "documents": []})


if __name__ == "__main__":
    app.run(debug=True)
