from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO


def mostrar_menu():
    """Muestra las opciones del sistema."""

    print("\n===== ECOTECH =====")
    print("1. Registrar empleado")
    print("2. Listar empleados")
    print("3. Buscar empleado")
    print("4. Actualizar empleado")
    print("5. Eliminar empleado")
    print("0. Salir")


def registrar_empleado():
    """Registra un empleado."""

    nombre = input("Nombre: ").strip()
    correo = input("Correo: ").strip()
    telefono = input("Teléfono: ").strip()

    if not nombre.replace(" ", "").isalpha():
        print("El nombre debe contener solo letras.")
        return
    if not correo or "@" not in correo:
        print("El correo no es válido.")
        return
    if not telefono.isdigit():
        print("El teléfono debe contener solo números.")
        return
    try:
        sueldo = int(input("Sueldo: "))

        empleado = Empleado(
            nombre,
            correo,
            telefono,
            sueldo
        )

        EmpleadoDAO.insertar(empleado)
        print("Empleado registrado correctamente.")

    except ValueError:
        print("El sueldo debe ser un número.")

    except Exception:
        print("No fue posible registrar el empleado.")


def listar_empleados():
    """Muestra todos los empleados."""

    empleados = EmpleadoDAO.listar()

    for empleado in empleados:
        print(
            empleado.id,
            empleado.nombre,
            empleado.correo
        )


def buscar_empleado():
    """Busca un empleado por ID."""

    try:
        id_empleado = int(
            input("Ingrese el ID del empleado a buscar: ")
        )

        empleado = EmpleadoDAO.obtener_por_id(id_empleado)

        if empleado is None:
            print("Empleado no encontrado.")
        else:
            print(
                "Empleado encontrado:",
                empleado.id,
                empleado.nombre,
                empleado.correo
            )

    except ValueError:
        print("El ID debe ser un número.")


def actualizar_empleado():
    """Actualiza un empleado."""

    try:
        id_empleado = int(
            input("Ingrese el ID del empleado a actualizar: ")
        )

        empleado = EmpleadoDAO.obtener_por_id(id_empleado)

        if empleado is None:
            print("Empleado no encontrado.")
            return

        empleado.nombre = input("Nuevo nombre: ").strip()
        empleado.correo = input("Nuevo correo: ").strip()

        actualizado = EmpleadoDAO.actualizar(empleado)

        if actualizado:
            print("Empleado actualizado correctamente.")
        else:
            print("No fue posible actualizar el empleado.")

    except ValueError:
        print("El ID debe ser un número.")


def eliminar_empleado():
    """Elimina un empleado por ID."""

    try:
        id_empleado = int(
            input("Ingrese el ID del empleado a eliminar: ")
        )

        eliminado = EmpleadoDAO.eliminar(id_empleado)

        if eliminado:
            print("Empleado eliminado correctamente.")
        else:
            print("Empleado no encontrado.")

    except ValueError:
        print("El ID debe ser un número.")


def main():
    while True:
        mostrar_menu()

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_empleado()

        elif opcion == "2":
            listar_empleados()

        elif opcion == "3":
            buscar_empleado()

        elif opcion == "4":
            actualizar_empleado()

        elif opcion == "5":
            eliminar_empleado()

        elif opcion == "0":
            print("Cerrando sesión...")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()