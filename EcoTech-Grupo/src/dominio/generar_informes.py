class GenerarInforme:
    """Clase que representa la generación de informes."""

    def __init__(
        self,
        informe: str,
        tipo_archivo: str
    ):
        self.informe = informe
        self.tipo_archivo = tipo_archivo

    def generar_informe(self) -> str:
        return self.informe