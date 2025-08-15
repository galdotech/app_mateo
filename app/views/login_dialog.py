# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QMessageBox,
)

from app.data import db


class LoginDialog(QDialog):
    """Simple login dialog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Inicio de sesión")
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Usuario:"))
        self.edit_user = QLineEdit(self)
        layout.addWidget(self.edit_user)

        layout.addWidget(QLabel("Contraseña:"))
        self.edit_pass = QLineEdit(self)
        self.edit_pass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.edit_pass)

        btns = QHBoxLayout()
        btn_login = QPushButton("Entrar", self)
        btn_cancel = QPushButton("Cancelar", self)
        btns.addWidget(btn_login)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

        btn_login.clicked.connect(self._do_login)
        btn_cancel.clicked.connect(self.reject)

        self.user_role: str | None = None

    def _do_login(self) -> None:
        nombre = self.edit_user.text().strip()
        password = self.edit_pass.text()
        if not nombre or not password:
            QMessageBox.warning(self, "Login", "Ingrese usuario y contraseña.")
            return
        user = db.get_usuario(nombre)
        if user is None:
            QMessageBox.warning(self, "Login", "Usuario no encontrado.")
            return
        _, password_hash, rol = user
        if db.hash_password(password) != password_hash:
            QMessageBox.warning(self, "Login", "Contraseña incorrecta.")
            return
        self.user_role = rol
        self.accept()
