from dominio.seguridad_datos import SeguridadDatos


class SistemaAutentificacion:
    """Clase que representa el sistema de autentificación."""

    def __init__(
        self,
        id_empleado: int,
        nombre_usuario: str,
        contrasena: str,
        salario: int
    ):
        self.id_empleado = id_empleado
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.salario = salario
        self.seguridad_datos = None

    def iniciar_sesion(self) -> bool:
        return True

    def cerrar_sesion(self) -> None:
        pass

    def validar_credenciales(self) -> bool:
        return True

    def autorizar_acceso(self) -> bool:
        return True

    def asignar_seguridad(
        self,
        seguridad: SeguridadDatos
    ) -> None:
        self.seguridad_datos = seguridad