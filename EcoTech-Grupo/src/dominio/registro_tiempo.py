class RegistroTiempo:
    """Clase que representa el registro de tiempo."""

    def __init__(
        self,
        fecha_registro: str,
        horas_registradas: float
    ):
        self.fecha_registro = fecha_registro
        self.horas_registradas = horas_registradas

    def registrar_tiempo(self) -> str:
        return "Tiempo registrado"