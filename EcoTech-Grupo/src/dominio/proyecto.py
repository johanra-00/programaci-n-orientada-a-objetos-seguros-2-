class Proyecto:
    """Clase que representa un proyecto."""

    def __init__(
        self,
        nombre: str,
        descripcion: str,
        cantidad_empleados: int
    ):
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad_empleados = cantidad_empleados

    def asignar_empleado(self) -> bool:
        return True

    def desasignar_empleado(self) -> bool:
        return True

    def crear_proyecto(self) -> bool:
        return True

    def eliminar_proyecto(self) -> bool:
        return True