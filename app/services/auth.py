from __future__ import annotations

"""Simple authentication and session management utilities."""

from dataclasses import dataclass
from typing import Optional, Set

from app.data import db

# Role definitions
ADMIN = "admin"
TECNICO = "tecnico"
RECEPCIONISTA = "recepcionista"

# Permissions per role
ROLE_PERMISSIONS: dict[str, Set[str]] = {
    ADMIN: {"view", "edit", "delete", "create"},
    TECNICO: {"view", "edit", "create"},
    RECEPCIONISTA: {"view", "create"},
}


@dataclass
class UserSession:
    id: int
    nombre: str
    rol: str


class AuthService:
    """Manage the authenticated user session and permissions."""

    def __init__(self) -> None:
        self._session: Optional[UserSession] = None

    # Authentication
    def login(self, nombre: str, password: str) -> bool:
        user = db.get_usuario(nombre)
        if user is None:
            return False
        user_id, password_hash, salt, rol = user
        if not db.verify_password(password, password_hash, salt):
            return False
        self._session = UserSession(user_id, nombre, rol)
        return True

    def logout(self) -> None:
        self._session = None

    # Session info
    @property
    def current_user(self) -> Optional[UserSession]:
        return self._session

    # Permissions
    def has_permission(self, perm: str) -> bool:
        if self._session is None:
            return False
        return perm in ROLE_PERMISSIONS.get(self._session.rol, set())

    def require_role(self, roles: Set[str]) -> None:
        if self._session is None or self._session.rol not in roles:
            raise PermissionError("Insufficient permissions")


auth_service = AuthService()

