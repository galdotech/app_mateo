from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from app.data import db


@dataclass
class PaymentGateway:
    """Simple HTTP-based payment gateway client."""

    base_url: str
    api_key: str

    def charge(self, invoice_id: int, amount: float) -> dict[str, Any]:
        """Charge an invoice through the remote gateway.

        Raises ``HTTPError`` if the request fails.
        """
        response = requests.post(
            f"{self.base_url.rstrip('/')}/charge",
            json={"invoice_id": invoice_id, "amount": amount},
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()


class PaymentService:
    """Process payments using a payment gateway and record them in the DB."""

    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def process_payment(self, factura_id: int, amount: float) -> dict[str, Any]:
        """Charge the amount and record the payment if successful."""
        data = self.gateway.charge(factura_id, amount)
        if data.get("status") != "succeeded":
            raise RuntimeError("Payment failed")
        db.registrar_pago(factura_id, amount)
        return data
