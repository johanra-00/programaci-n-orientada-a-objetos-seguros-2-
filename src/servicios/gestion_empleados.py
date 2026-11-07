from persistencia.RegistroTiempoDAO import RegistroTiempoDAO
from dominio.empleado import Empleado
from persistencia.EmpleadoDAO import EmpleadoDAO
from servicios.permisos import exigir_admin


def registrar_empleado(sesion, nombre, correo, departamento):
    exigir_admin(sesion)

    nombre = Empleado.validar_nombre(nombre)
    correo = Empleado.validar_correo(correo)

    empleado = Empleado(
        nombre=nombre,
        correo=correo,
        telefono="",
        sueldo=0,
        departamento=departamento
    )

    return EmpleadoDAO.insertar(empleado)


def listar_todos(sesion):
    exigir_admin(sesion)
    return EmpleadoDAO.listar()


def buscar_empleado(sesion, empleado_id):
    exigir_admin(sesion)

    if type(empleado_id) is not int or empleado_id <= 0:
        raise ValueError("ID de empleado inválido.")

    return EmpleadoDAO.obtener_por_id(empleado_id)


def actualizar_empleado(sesion, empleado_id, nombre, correo):
    exigir_admin(sesion)

    nombre = Empleado.validar_nombre(nombre)
    correo = Empleado.validar_correo(correo)

    empleado = EmpleadoDAO.obtener_por_id(empleado_id)

    if empleado is None:
        raise ValueError("Empleado no encontrado.")

    empleado.nombre = nombre
    empleado.correo = correo

    return EmpleadoDAO.actualizar(empleado)


def eliminar_empleado(sesion, empleado_id):
    exigir_admin(sesion)

    if type(empleado_id) is not int or empleado_id <= 0:
        raise ValueError("ID de empleado inválido.")

    return EmpleadoDAO.eliminar(empleado_id)

def listar_registros_generales(sesion):
    exigir_admin(sesion)
    return RegistroTiempoDAO.listar()