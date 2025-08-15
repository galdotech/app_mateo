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
from PySide6.QtGui import QKeySequence, QShortcut

from app.services.auth import auth_service


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
        btn_login.setDefault(True)
        btn_cancel = QPushButton("Cancelar", self)
        btns.addWidget(btn_login)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

        btn_login.clicked.connect(self._do_login)
        btn_cancel.clicked.connect(self.reject)

        # Conectar Enter en los campos de texto al login
        self.edit_user.returnPressed.connect(self._do_login)
        self.edit_pass.returnPressed.connect(self._do_login)

        # Cancelar con tecla Escape
        shortcut_cancel = QShortcut(QKeySequence("Escape"), self)
        shortcut_cancel.activated.connect(btn_cancel.click)

        self.user_role: str | None = None

    def _do_login(self) -> None:
        nombre = self.edit_user.text().strip()
        password = self.edit_pass.text()
        if not nombre or not password:
            QMessageBox.warning(self, "Login", "Ingrese usuario y contraseña.")
            return
        if not auth_service.login(nombre, password):
            QMessageBox.warning(self, "Login", "Usuario o contraseña incorrectos.")
            return
        self.user_role = auth_service.current_user.rol if auth_service.current_user else None
        self.accept()
