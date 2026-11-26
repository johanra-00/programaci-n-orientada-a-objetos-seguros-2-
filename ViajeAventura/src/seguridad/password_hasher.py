import hashlib
import hmac
import secrets
from src.seguridad.input_sanitizer import InputSanitizer


class SecurityValidator:
    _HASH_ALGORITHM = "pbkdf2_sha256"
    _HASH_ITERATIONS = 600_000

    @classmethod
    def validate_email(cls, email: str) -> str:
        return InputSanitizer.sanitize_email(email)

    @staticmethod
    def validate_password_strength(plain_password: str) -> None:
        if not plain_password or len(plain_password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        if any(ch in plain_password for ch in ("\x00", "\n", "\r")):
            raise ValueError("La contraseña contiene caracteres de control no permitidos.")
        if not any(c.isupper() for c in plain_password):
            raise ValueError("La contraseña debe incluir al menos una letra mayúscula.")
        if not any(c.islower() for c in plain_password):
            raise ValueError("La contraseña debe incluir al menos una letra minúscula.")
        if not any(c.isdigit() for c in plain_password):
            raise ValueError("La contraseña debe incluir al menos un número.")

    @staticmethod
    def hash_password(plain_password: str) -> str:
        salt = secrets.token_bytes(16)
        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt,
            SecurityValidator._HASH_ITERATIONS,
        )
        return "$".join((
            SecurityValidator._HASH_ALGORITHM,
            str(SecurityValidator._HASH_ITERATIONS),
            salt.hex(),
            password_hash.hex(),
        ))

    @staticmethod
    def verify_password(plain_password: str, password_hash: str) -> bool:
        if not plain_password or not password_hash:
            return False
        try:
            algorithm, iterations, salt_hex, hash_hex = password_hash.split("$", 3)
            if algorithm != SecurityValidator._HASH_ALGORITHM:
                return False
            iterations = int(iterations)
            if iterations <= 0:
                return False
            salt = bytes.fromhex(salt_hex)
            expected_hash = bytes.fromhex(hash_hex)
            actual_hash = hashlib.pbkdf2_hmac(
                "sha256", plain_password.encode("utf-8"), salt, iterations
            )
            return hmac.compare_digest(actual_hash, expected_hash)
        except (ValueError, TypeError):
            return False