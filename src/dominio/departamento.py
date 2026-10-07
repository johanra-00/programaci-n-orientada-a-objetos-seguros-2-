# src/dominio/departamento.py
from dominio.empleado import Empleado

class Departamento:
    """Clase que representa a un departamento"""

    def __init__(self, nombre:str):
        self.nombre = nombre,
        self._empleados: list[Empleado] = []

    def  agregar_empleados(self, empleado: Empleado) -> bool:
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