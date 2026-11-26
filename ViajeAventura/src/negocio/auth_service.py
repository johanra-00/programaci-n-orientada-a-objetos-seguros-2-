import os
import sqlite3
from src.negocio.models import UserAccount
from src.persistencia.user_dao import UserDAO
from src.seguridad.input_sanitizer import InputSanitizer


def _is_integrity_error(exc: Exception) -> bool:
    return isinstance(exc, sqlite3.IntegrityError) or type(exc).__name__ == "IntegrityError"


class AuthService:
    DEFAULT_ADMIN_EMAIL = "gerencia@viajesaventura.cl"
    DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD")

    def __init__(self, user_dao: UserDAO) -> None:
        self.user_dao = user_dao

    def register_user(
        self, email: str, plain_password: str, role: str = "CLIENT"
    ) -> UserAccount:
        user = UserAccount.register(email=email, plain_password=plain_password, role=role)
        user.validate_credentials()
        try:
            return self.user_dao.create(user)
        except Exception as exc:
            if not _is_integrity_error(exc):
                raise
            raise ValueError("El correo electrónico ya está registrado.") from exc

    def login(self, email: str, plain_password: str) -> UserAccount:
        cleaned_email = InputSanitizer.sanitize_email(email)
        if not plain_password:
            raise ValueError("Debe ingresar su contraseña.")
        user = self.user_dao.get_by_email(cleaned_email)
        if not user or not user.authenticate(plain_password):
            raise ValueError("Credenciales incorrectas.")
        return user

    def ensure_default_admin(self) -> None:
        if not self.user_dao.get_by_email(self.DEFAULT_ADMIN_EMAIL):
            if not self.DEFAULT_ADMIN_PASSWORD:
                raise RuntimeError("Configure la variable de entorno DEFAULT_ADMIN_PASSWORD.")
            admin = UserAccount.register(
                email=self.DEFAULT_ADMIN_EMAIL,
                plain_password=self.DEFAULT_ADMIN_PASSWORD,
                role="ADMIN",
            )
            self.user_dao.create(admin)