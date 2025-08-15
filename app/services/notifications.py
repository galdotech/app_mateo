from __future__ import annotations

import smtplib
from email.message import EmailMessage
from typing import Any, Dict

import requests

from .templates import render_template
from app.data import db


class NotificationService:
    """Send messages through various channels and record them."""

    def __init__(self, sms_url: str | None = None, sms_token: str | None = None):
        self.sms_url = sms_url
        self.sms_token = sms_token

    def send_sms(self, to: str, template: str, context: Dict[str, Any]) -> None:
        message = render_template(template, context)
        if self.sms_url and self.sms_token:
            requests.post(
                self.sms_url,
                json={"to": to, "message": message},
                headers={"Authorization": f"Bearer {self.sms_token}"},
                timeout=10,
            )
        db.log_notification(to, "sms", message)

    def send_email(
        self,
        to: str,
        subject_template: str,
        body_template: str,
        context: Dict[str, Any],
        smtp_server: str = "localhost",
        smtp_port: int = 25,
    ) -> None:
        subject = render_template(subject_template, context)
        body = render_template(body_template, context)
        msg = EmailMessage()
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.send_message(msg)
        db.log_notification(to, "email", body)

    def send_whatsapp(self, to: str, template: str, context: Dict[str, Any]) -> None:
        message = render_template(template, context)
        if self.sms_url and self.sms_token:
            requests.post(
                self.sms_url,
                json={"to": to, "message": message, "channel": "whatsapp"},
                headers={"Authorization": f"Bearer {self.sms_token}"},
                timeout=10,
            )
        db.log_notification(to, "whatsapp", message)
