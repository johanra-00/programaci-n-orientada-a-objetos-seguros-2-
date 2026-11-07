
from dominio.empleado import Empleado
from persistencia.EmpleadoDAO import EmpleadoDAO
from persistencia.RegistroTiempoDAO import RegistroTiempoDAO
from servicios.permisos import exigir_sesion


def mis_registros(sesion):
    exigir_sesion(sesion)

    return RegistroTiempoDAO.listar_por_empleado(
        sesion["empleado_id"]
    )


def actualizar_mis_datos(sesion, nombre, correo):
    exigir_sesion(sesion)

    nombre = Empleado.validar_nombre(nombre)
    correo = Empleado.validar_correo(correo)

    empleado = EmpleadoDAO.obtener_por_id(
        sesion["empleado_id"]
    )

    if empleado is None:
        raise ValueError("No se encontró el empleado.")

    empleado.nombre = nombre
    empleado.correo = correo

    return EmpleadoDAO.actualizar(empleado)
def mi_ficha(sesion):
    exigir_sesion(sesion)

    empleado = EmpleadoDAO.obtener_por_id(
        sesion["empleado_id"]
    )

    if empleado is None:
        raise ValueError("No se encontró el empleado.")

    return empleado