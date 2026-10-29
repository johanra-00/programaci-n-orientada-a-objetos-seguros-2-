from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO
from dominio.departamento import Departamento
from persistencia.departamento_dao import DepartamentoDAO
from dominio.registro_tiempo import RegistroTiempo
from persistencia.registro_de_tiempoDAO import RegistroTiempoDAO


def mostrar_menu():
    print("\n===== ECOTECH =====")
    print("1. Gestionar empleados")
    print("2. Gestionar departamentos")
    print("3. Gestionar proyectos")
    print("4. Gestionar registros de tiempo")
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


def menu_empleados():
    while True:
        print("\n===== EMPLEADOS =====")
        print("1. Registrar empleado")
        print("2. Listar empleados")
        print("3. Buscar empleado")
        print("4. Actualizar empleado")
        print("5. Eliminar empleado")
        print("0. Volver")

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
            break
        else:
            print("Opción no válida.")


def menu_departamentos():
    while True:
        print("\n===== DEPARTAMENTOS =====")
        print("1. Ingresar departamento")
        print("2. Listar departamentos")
        print("3. Buscar departamento")
        print("4. Actualizar departamento")
        print("5. Borrar departamento")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                nombre = input("Nombre del departamento: ").strip()

                if not nombre:
                    print("El nombre no puede estar vacío.")
                    continue

                departamento = Departamento(nombre)
                DepartamentoDAO.insertar(departamento)
                print("Departamento registrado correctamente.")

            elif opcion == "2":
                departamentos = DepartamentoDAO.listar()

                if not departamentos:
                    print("No hay departamentos registrados.")

                for departamento in departamentos:
                    print(departamento[0], departamento[1])

            elif opcion == "3":
                id_departamento = int(input("ID del departamento: "))
                departamento = DepartamentoDAO.buscar(id_departamento)

                if departamento:
                    print(departamento[0], departamento[1])
                else:
                    print("Departamento no encontrado.")

            elif opcion == "4":
                id_departamento = int(input("ID del departamento: "))
                departamento = DepartamentoDAO.buscar(id_departamento)

                if departamento:
                    nombre = input("Nuevo nombre: ").strip()

                    if not nombre:
                        print("El nombre no puede estar vacío.")
                        continue

                    actualizado = DepartamentoDAO.actualizar(
                        id_departamento, nombre
                    )
                    print(
                        "Departamento actualizado."
                        if actualizado else "No se pudo actualizar."
                    )
                else:
                    print("Departamento no encontrado.")

            elif opcion == "5":
                id_departamento = int(input("ID del departamento: "))
                eliminado = DepartamentoDAO.eliminar(id_departamento)

                print(
                    "Departamento eliminado."
                    if eliminado else "Departamento no encontrado."
                )

            elif opcion == "0":
                break

            else:
                print("Opción no válida.")

        except ValueError:
            print("Ingrese un ID numérico válido.")

        except Exception as error:
            print("Ocurrió un error:", error)


def menu_proyectos():
    while True:
        print("\n===== PROYECTOS =====")
        print("1. Ingresar proyecto")
        print("2. Listar proyectos")
        print("3. Buscar proyecto")
        print("4. Actualizar proyecto")
        print("5. Borrar proyecto")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                nombre = input("Nombre del proyecto: ").strip()
                descripcion = input("Descripción: ").strip()

                proyecto = Proyecto(nombre, descripcion, 0)
                ProyectoDAO.insertar(proyecto)
                print("Proyecto registrado. ID:", proyecto.id)

            elif opcion == "2":
                proyectos = ProyectoDAO.listar()

                if not proyectos:
                    print("No hay proyectos registrados.")

                for p in proyectos:
                    print(p.id, p.nombre, p.descripcion)

            elif opcion == "3":
                id_proyecto = int(input("ID del proyecto: "))
                p = ProyectoDAO.buscar(id_proyecto)

                if p:
                    print(p.id, p.nombre, p.descripcion)
                else:
                    print("Proyecto no encontrado.")

            elif opcion == "4":
                id_proyecto = int(input("ID del proyecto: "))
                p = ProyectoDAO.buscar(id_proyecto)

                if p:
                    p.nombre = input("Nuevo nombre: ").strip()
                    p.descripcion = input("Nueva descripción: ").strip()

                    if ProyectoDAO.actualizar(p):
                        print("Proyecto actualizado.")
                    else:
                        print("No se pudo actualizar.")
                else:
                    print("Proyecto no encontrado.")

            elif opcion == "5":
                id_proyecto = int(input("ID del proyecto: "))
                eliminado = ProyectoDAO.eliminar(id_proyecto)

                if eliminado:
                    print("Proyecto eliminado.")
                else:
                    print("Proyecto no encontrado.")

            elif opcion == "0":
                break

            else:
                print("Opción no válida.")

        except ValueError:
            print("El ID debe ser un número.")

        except Exception as error:
            print("Error:", error)

def menu_registros_tiempo():
    while True:
        print("\n===== REGISTROS DE TIEMPO =====")
        print("1. Registrar tiempo")
        print("2. Listar registros")
        print("3. Buscar registro")
        print("4. Actualizar registro")
        print("5. Eliminar registro")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                fecha = input("Fecha (AAAA-MM-DD): ").strip()
                horas = float(input("Horas registradas: "))

                if not fecha or horas <= 0:
                    print("La fecha y las horas deben ser válidas.")
                    continue

                registro = RegistroTiempo(fecha, horas)
                RegistroTiempoDAO.insertar(registro)
                print("Registro guardado. ID:", registro.id)

            elif opcion == "2":
                registros = RegistroTiempoDAO.listar()

                if not registros:
                    print("No hay registros de tiempo.")

                for r in registros:
                    print(r.id, r.fecha_registro, r.horas_registradas)

            elif opcion == "3":
                id_registro = int(input("ID del registro: "))
                r = RegistroTiempoDAO.buscar(id_registro)

                if r:
                    print(r.id, r.fecha_registro, r.horas_registradas)
                else:
                    print("Registro no encontrado.")

            elif opcion == "4":
                id_registro = int(input("ID del registro: "))
                r = RegistroTiempoDAO.buscar(id_registro)

                if r:
                    fecha = input("Nueva fecha (AAAA-MM-DD): ").strip()
                    horas = float(input("Nuevas horas: "))

                    if not fecha or horas <= 0:
                        print("La fecha y las horas deben ser válidas.")
                        continue

                    r.fecha_registro = fecha
                    r.horas_registradas = horas

                    if RegistroTiempoDAO.actualizar(r):
                        print("Registro actualizado.")
                    else:
                        print("No se pudo actualizar.")
                else:
                    print("Registro no encontrado.")

            elif opcion == "5":
                id_registro = int(input("ID del registro: "))
                eliminado = RegistroTiempoDAO.eliminar(id_registro)

                if eliminado:
                    print("Registro eliminado.")
                else:
                    print("Registro no encontrado.")

            elif opcion == "0":
                break

            else:
                print("Opción no válida.")

        except ValueError:
            print("Ingrese un ID numérico y horas válidas.")
        except Exception as error:
            print("Error:", error)

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_empleados()

        elif opcion == "2":
            menu_departamentos()

        elif opcion == "3":
            menu_proyectos()

        elif opcion == "4":
            menu_registros_tiempo()

        elif opcion == "0":
            print("Cerrando sesión...")
            break

        else:
            print("Opción no válida.")

from menu_usuario import solicitar_login, menu_privado

def main():
    while True:
        usuario_actual = solicitar_login()
        if usuario_actual is None:
            if input("Enter para reintentar o 0 para salir: ") == "0":
                return
            continue
        opcion = menu_privado(usuario_actual)
        usuario_actual = None # Terminar el acceso de esta sesión.
        if opcion == "0":
            return
        print("Sesión cerrada. Ingrese nuevamente.")

if __name__ == "__main__":
    main()