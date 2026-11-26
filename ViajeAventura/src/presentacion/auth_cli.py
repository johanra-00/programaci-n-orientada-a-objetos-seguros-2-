from getpass import getpass
from typing import Optional
from src.negocio.auth_service import AuthService
from src.negocio.models import UserAccount
from src.seguridad.input_sanitizer import InputSanitizer


class AuthCLI:
    def __init__(self, auth_service: AuthService) -> None:
        self.auth_service = auth_service

    def prompt_access(self) -> Optional[UserAccount]:
        while True:
            print("\n=== VIAJES AVENTURA - ACCESO AL SISTEMA ===")
            print("1. Iniciar sesión")
            print("2. Registrarse como cliente")
            print("0. Salir")

            option = input("Seleccione una opción: ").strip()

            try:
                if option == "1":
                    return self._handle_login()
                elif option == "2":
                    return self._handle_register()
                elif option == "0":
                    return None
                else:
                    print("Opción inválida. Intente nuevamente.")
            except ValueError as err:
                print(f"[Error de validación] {err}")
            except Exception as err:
                print(f"[Error inesperado] {err}")

    def _handle_login(self) -> UserAccount:
        raw_email = input("Correo electrónico: ")
        clean_email = InputSanitizer.sanitize_email(raw_email)
        password = getpass("Contraseña: ")
        user = self.auth_service.login(clean_email, password)
        print(f"Bienvenido/a, {user.email} ({user.role}).")
        return user

    def _handle_register(self) -> UserAccount:
        raw_email = input("Correo electrónico: ")
        clean_email = InputSanitizer.sanitize_email(raw_email)
        password = getpass("Contraseña (mín. 8 caracteres, mayúscula, minúscula y número): ")
        user = self.auth_service.register_user(clean_email, password, role="CLIENT")
        print(f"Cuenta creada exitosamente para {user.email}.")
        return user
