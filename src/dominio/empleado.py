from dominio.registro_tiempo import RegistroTiempo
from dominio.proyecto import Proyecto
from dominio.sistema_autentificacion import SistemaAutentificacion
from dominio.generar_informes import GenerarInforme


class Empleado:
    """Clase que representa a un empleado."""

    def __init__(
        self,
        nombre: str,
        correo: str,
        telefono: str,
        sueldo: int,
        id=None,
        departamento=None,
        fecha_contrato=None
    ):
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.sueldo = sueldo
        self.id = id
        self.departamento = departamento
        self.fecha_contrato = fecha_contrato

        self.registros_tiempo = []
        self.proyectos = []
        self.sistema_autentificacion = None
        self.informes = []

    def mostrardatos(self) -> str:
        return (
            f"Nombre: {self.nombre}, "
            f"Correo: {self.correo}, "
            f"Teléfono: {self.telefono}, "
            f"ID: {self.id}"
        )

    def registrar_tiempo(self, registro: RegistroTiempo) -> bool:
        if registro not in self.registros_tiempo:
            self.registros_tiempo.append(registro)
            return True
        return False

    def asignar_proyecto(self, proyecto: Proyecto) -> bool:
        if proyecto not in self.proyectos:
            self.proyectos.append(proyecto)
            return True
        return False

    def asignar_autentificacion(
        self,
        sistema: SistemaAutentificacion
    ) -> None:
        self.sistema_autentificacion = sistema

    def agregar_informe(self, informe: GenerarInforme) -> None:
        self.informes.append(informe)