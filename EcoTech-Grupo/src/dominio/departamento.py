class Departamento:
    """Clase que representa a un departamento."""

    def __init__(
        self,
        nombre: str,
        gerente: str = "",
        ubicacion: str = "",
        id_departamento: int = None
    ):
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.gerente = gerente
        self.ubicacion = ubicacion
        self._empleados = []

    def agregar_empleados(self, empleado) -> bool:
        if empleado not in self._empleados:
            self._empleados.append(empleado)
            return True
        return False

    def mostrardatos(self) -> str:
        return f"Departamento: {self.nombre}"

    def empleados(self) -> tuple:
        return tuple(self._empleados)

    def cant_empleados(self) -> int:
        return len(self._empleados)

    def crear_departamento(self) -> None:
        pass

    def editar_departamento(self) -> None:
        pass

    def borrar_departamento(self) -> None:
        pass