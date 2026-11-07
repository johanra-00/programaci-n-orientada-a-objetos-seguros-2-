
from getpass import getpass

from entradas import pedir_dato
from dominio.usuario import Usuario

from servicios.autenticacion import registrar_usuario, autenticar
from servicios.indicadores import mostrar_indicador, mostrar_historial

from servicios.gestion_empleados import (
    listar_todos,
    listar_registros_generales
)

from servicios.mi_cuenta import (
    mi_ficha,
    mis_registros,
    actualizar_mis_datos
)


def solicitar_registro(sesion):
    try:
        empleado_id = pedir_dato("ID del empleado: ", int)

        nombre = pedir_dato(
            "Nuevo usuario: ",
            Usuario.normalizar_usuario
        )

        clave = pedir_dato(
            "Contraseña: ",
            Usuario.validar_clave,
            getpass
        )

        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden.")
            return None

        usuario_id = registrar_usuario(
            empleado_id, nombre, clave, sesion
        )

    except (TypeError, ValueError, PermissionError) as error:
        print(error)
        return None

    print(f"Cuenta creada correctamente. ID: {usuario_id}")
    return usuario_id


def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")

    try:
        usuario = autenticar(nombre, clave)

    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None

    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print(
            f"Sesión iniciada correctamente. "
            f"Rol: {usuario['rol']}"
        )

    return usuario


def mostrar_perfil(usuario_actual):
    try:
        empleado = mi_ficha(usuario_actual)

        print("\n--- MI FICHA ---")
        print(f"ID: {empleado.id}")
        print(f"Nombre: {empleado.nombre}")
        print(f"Correo: {empleado.correo}")
        print(f"Departamento: {empleado.departamento}")
        print(f"Teléfono: {empleado.telefono}")
        print(f"Sueldo: {empleado.sueldo}")

    except (ValueError, PermissionError) as error:
        print(error)


def consultar_mis_registros(usuario_actual):
    try:
        registros = mis_registros(usuario_actual)

        print("\n--- MIS REGISTROS DE TIEMPO ---")

        if not registros:
            print("No tienes registros de tiempo.")
            return

        for registro in registros:
            print(registro.__dict__)

    except (ValueError, PermissionError) as error:
        print(error)


def modificar_mis_datos(usuario_actual):
    try:
        nombre = input("Nuevo nombre: ")
        correo = input("Nuevo correo: ")

        resultado = actualizar_mis_datos(
            usuario_actual,
            nombre,
            correo
        )

        if resultado:
            print("Tus datos fueron actualizados.")
        else:
            print("No se pudieron actualizar tus datos.")

    except (ValueError, TypeError, PermissionError) as error:
        print(error)


def consultar_empleados(usuario_actual):
    try:
        empleados = listar_todos(usuario_actual)

        print("\n--- LISTA DE EMPLEADOS ---")

        if not empleados:
            print("No hay empleados registrados.")
            return

        for empleado in empleados:
            print(empleado.__dict__)

    except (ValueError, PermissionError) as error:
        print(error)


def consultar_registros_generales(usuario_actual):
    try:
        registros = listar_registros_generales(usuario_actual)

        print("\n--- REGISTROS LABORALES GENERALES ---")

        if not registros:
            print("No existen registros laborales.")
            return

        for registro in registros:
            print(registro.__dict__)

    except (ValueError, PermissionError) as error:
        print(error)


def consultar_indicador(usuario_actual):
    if usuario_actual is not None:
        mostrar_indicador()


def consultar_historial(usuario_actual):
    if usuario_actual is not None:
        mostrar_historial()


def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"

    while True:

        if usuario_actual["rol"] == "admin":
            print("\n--- MENÚ ADMINISTRADOR ---")
            print("1. Registrar cuenta de empleado")
            print("2. Listar empleados")
            print("3. Consultar indicador")
            print("4. Ver historial de indicadores")
            print("5. Consultar registros laborales generales")
            print("9. Cerrar sesión")
            print("0. Salir")

        else:
            print("\n--- MENÚ EMPLEADO ---")
            print("1. Ver mi ficha")
            print("2. Consultar mis registros")
            print("3. Modificar mis datos")
            print("4. Consultar indicador")
            print("5. Ver historial de indicadores")
            print("9. Cerrar sesión")
            print("0. Salir")

        opcion = input("Opción: ").strip()

        if opcion in ("0", "9"):
            return opcion

        if usuario_actual["rol"] == "admin":

            if opcion == "1":
                solicitar_registro(usuario_actual)

            elif opcion == "2":
                consultar_empleados(usuario_actual)

            elif opcion == "3":
                consultar_indicador(usuario_actual)

            elif opcion == "4":
                consultar_historial(usuario_actual)

            elif opcion == "5":
                consultar_registros_generales(usuario_actual)

            else:
                print("Opción no válida.")

        else:

            if opcion == "1":
                mostrar_perfil(usuario_actual)

            elif opcion == "2":
                consultar_mis_registros(usuario_actual)

            elif opcion == "3":
                modificar_mis_datos(usuario_actual)

            elif opcion == "4":
                consultar_indicador(usuario_actual)

            elif opcion == "5":
                consultar_historial(usuario_actual)

            else:
                print("Opción no válida.")
